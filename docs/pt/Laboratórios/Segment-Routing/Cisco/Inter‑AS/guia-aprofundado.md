# Guia aprofundado: da configuração ao fio

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/inter-as/bgp-lu">`labs/cisco/sr-mpls/inter-as/bgp-lu`</a>.

!!! info "Sobre este documento"
    Documento de apoio ao [lab `bgp-lu`](bgp-lu.md). Conceitos da categoria no
    documento [Inter-AS](index.md).

Este documento explica o laboratório como uma cadeia completa:

```text
configuração
    ↓
protocolo anuncia estado
    ↓
RIB, LIB, LFIB e CEF são programados
    ↓
o pacote recebe uma pilha MPLS
    ↓
cada roteador executa a instrução do label no topo
```

O foco não é reapresentar OSPF, MPLS ou SR-MPLS. O foco é responder às
perguntas que normalmente ficam entre a configuração e o pacote:

- quem aloca cada label;
- para quem esse label tem significado;
- o que exatamente viaja em um UPDATE BGP-LU;
- por que aparecem `Local Label` e `Received Label` diferentes;
- como o CEF combina um Node-SID SR com um label BGP;
- qual entrada da LFIB faz `swap`, `pop` ou `push` em cada salto;
- o que realmente estaria no fio;
- como BGP-EPE e uma SR Policy atravessam a fronteira entre os ASes;
- quais fatos foram observados e quais são comportamento esperado;
- como o serviço final é encaminhado e como a SR Policy aparece no traceroute.

!!! info "Sobre este documento"
    **Formato para celular:** as seções são curtas, os diagramas principais são
    texto, as tabelas evitam muitas colunas e as saídas longas ficam recolhidas em
    blocos expansíveis.

---

## Sumário

1. [A resposta curta](#1-a-resposta-curta)
2. [Escopo e limites](#2-escopo-e-limites)
3. [Topologia e papéis](#3-topologia-e-papeis)
4. [O modelo mental dos labels](#4-o-modelo-mental-dos-labels)
5. [RIB, LIB, LFIB e CEF](#5-rib-lib-lfib-e-cef)
6. [Como o SR intradomínio nasce](#6-como-o-sr-intradominio-nasce)
7. [Como o BGP-LU funciona no controle](#7-como-o-bgp-lu-funciona-no-controle)
8. [A propagação LU deste lab](#8-a-propagacao-lu-deste-lab)
9. [A LFIB e o pacote no caminho normal](#9-a-lfib-e-o-pacote-no-caminho-normal)
10. [O que existe no fio](#10-o-que-existe-no-fio)
11. [A sobreposição de serviço](#11-a-sobreposicao-de-servico)
12. [SR Policy, cor, BSID e BGP-EPE](#12-sr-policy-cor-bsid-e-bgp-epe)
13. [TI-LFA neste losango](#13-ti-lfa-neste-losango)
14. [Leitura da configuração](#14-leitura-da-configuracao)
15. [Execução por estágios](#15-execucao-por-estagios)
16. [Como provar cada camada](#16-como-provar-cada-camada)
17. [Como capturar o controle no fio](#17-como-capturar-o-controle-no-fio)
18. [Troubleshooting orientado por dependências](#18-troubleshooting-orientado-por-dependencias)
19. [Experimentos úteis](#19-experimentos-uteis)
20. [Checklist final e referências](#20-checklist-final-e-referencias)

---

## 1. A resposta curta

### O roteador não traduz um label SR em um label BGP

Essa é a ideia mais importante do laboratório.

Há dois contratos independentes:

1. **OSPF/SR:** “para alcançar o ASBR `10.0.0.4`, use o Prefix-SID 16004”.
2. **BGP-LU:** “quando chegar ao ASBR `10.0.0.4`, apresente o label que ele
   anunciou para `10.0.0.8/32`”.

O PE de ingresso faz recursão entre esses contratos e empilha os dois:

```text
topo → 16004   transporte SR até o next hop BGP
        16008  label LU entendido por esse next hop
base → IPv4    pacote destinado a 10.0.0.8
```

Na execução registrada, o CEF de `pe-pop-pb` mostrou exatamente:

```text
via 10.0.0.4/32
next hop 10.0.0.4/32 via 16004/0/21
next hop 192.0.2.1 Gi0/0/0/1 labels imposed {16004 16008}
```

O primeiro 16004 não vira 16008. Ele é removido quando termina o transporte até
o ASBR. Só então 16008 sobe ao topo e passa a selecionar uma entrada diferente da
LFIB.

### A regra de ouro do label MPLS

!!! note "Observação"
    Um label só tem significado no roteador que o recebe como label de topo.

Por consequência:

- o label que um roteador **anuncia** é o label que ele se compromete a
  receber;
- o label que um roteador **recebe via BGP** é o label que ele deve enviar ao
  vizinho;
- números iguais em roteadores diferentes não identificam necessariamente o
  mesmo objeto;
- números diferentes podem representar a mesma FEC em saltos consecutivos;
- a faixa `24xxx` não identifica o protocolo: neste lab ela contém Adj-SIDs,
  labels BGP e um Binding SID.

### O caminho de controle e o caminho de dados

```text
CONTROLE

pe-ipe-ce
  anuncia 10.0.0.8/32 + label
      ↓ iBGP-LU
asbr-ipe-pb
  muda next hop, cria novo binding
      ↓ eBGP-LU
asbr-pop-pb
  usa next-hop-self, cria novo binding
      ↓ iBGP-LU
pe-pop-pb
  recebe next hop 10.0.0.4 + label 16008


DADOS

pe-pop-pb
  impõe {SID até 10.0.0.4, label LU}
      ↓
AS 65001 remove o SID
      ↓
asbr-pop-pb troca o label LU
      ↓
asbr-ipe-pb cria transporte SR até 10.0.0.8
      ↓
AS 1916 remove o transporte e entrega ao PE
```

---

## 2. Escopo e limites

### O que o lab implementa

- dois domínios OSPF área 0 independentes;
- SR-MPLS intradomínio com Prefix-SIDs;
- uma fronteira eBGP IPv4 labeled-unicast;
- iBGP-LU entre cada PE e seu ASBR;
- recursão do next hop BGP sobre o transporte SR;
- TI-LFA nas interfaces de core;
- BGP-EPE com PeerNode SID;
- uma SR Policy explícita inter-AS;
- uma sessão eBGP IPv4 unicast multihop entre os PEs;
- duas redes globais de documentação como serviço didático.

### O que ele não implementa

- VPNv4 ou VPNv6;
- VRF, RD ou RT;
- label VPN por serviço;
- LDP ou RSVP-TE;
- controlador, PCEP ou BGP-LS;
- BFD;
- medição de convergência;
- data plane suportado na imagem usada.

Portanto, isto não é uma L3VPN inter-AS Option C completa. O lab implementa o
**padrão de transporte** no qual os ASBRs trocam reachability rotulada para as
loopbacks dos PEs, mas substitui a camada VPN por eBGP IPv4 unicast global.

### O limite mais importante da plataforma

A topologia usa `xrd-control-plane:7.10.2`. A execução de referência provou:

- OSPF;
- programação SR na RIB/CEF/LFIB;
- três sessões BGP-LU;
- labels e recursão BGP-LU;
- backup Local-LFA;
- EPE;
- SR Policy operacional;
- sessão de serviço estabelecida;
- encaminhamento cliente–cliente nos dois sentidos;
- pilha da policy observada em traceroute.

Ela provou o encaminhamento deste lab, mas não mede capacidade, latência de
hardware nem convergência de produção. Esses resultados exigem uma plataforma
de forwarding representativa e instrumentação própria.

O que a execução de referência efetivamente observou, e a separação dos
níveis de prova, estão em [`validacao.md`](validacao.md). As saídas
integrais daquela execução não são versionadas: cada execução produz seus
próprios labels dinâmicos, e uma captura antiga versionada vira fonte de
confusão.

Ao longo do guia, leia as afirmações com esta legenda:

- **capturado:** foi observado na execução de referência e está registrado
  em [`validacao.md`](validacao.md);
- **derivado:** é a ação exigida para ligar dois estados capturados, segundo o
  comportamento do protocolo;
- **esperado no fio:** é o resultado em um data plane MPLS funcional, mas não
  foi observado em pcap nesta imagem.

---

## 3. Topologia e papéis

### Vista lógica

```text
instituicao-pb
198.51.100.10
       |
       | 198.51.100.0/24
       |
  pe-pop-pb (10.0.0.1, SID 16001)
       | \
    10 |  \ 20
       |   \
  p-pop-a  p-pop-b
  SID 16002 SID 16003
       |   /
    10 |  / 20
       | /
 asbr-pop-pb (10.0.0.4, SID 16004)
       |
       | eBGP-LU 65001 ↔ 1916
       | 192.0.2.8/31
       |
 asbr-ipe-pb (10.0.0.5, SID 16005)
       | \
    10 |  \ 20
       |   \
 p-ipe-rn  p-ipe-ba
 SID 16006 SID 16007
       |   /
    10 |  / 20
       | /
  pe-ipe-ce (10.0.0.8, SID 16008)
       |
       | 203.0.113.0/24
       |
   servico-ce
  203.0.113.10
```

O ramo superior de cada losango é o caminho SPF primário. O inferior é mais
caro e serve como alternativo e como caminho explícito da policy.

### Domínio PoP-PB — AS 65001

- `pe-pop-pb`
  - PE de ingresso;
  - recebe o tráfego de `instituicao-pb`;
  - headend da SR Policy;
  - peer iBGP-LU de `asbr-pop-pb`;
  - peer eBGP multihop de serviço de `pe-ipe-ce`.

- `p-pop-a`
  - P do caminho primário;
  - custo 10 em cada enlace;
  - penúltimo salto SR até `asbr-pop-pb`.

- `p-pop-b`
  - P do caminho alternativo;
  - custo 20 em cada enlace;
  - caminho de reparo e primeiro waypoint da SR Policy.

- `asbr-pop-pb`
  - ASBR do AS 65001;
  - costura iBGP-LU e eBGP-LU;
  - muda o next hop em direção ao PE;
  - aloca o PeerNode SID 15100 para `asbr-ipe-pb`.

### Domínio backbone — AS 1916

- `asbr-ipe-pb`
  - ASBR do AS 1916;
  - recebe LU de `pe-ipe-ce` e anuncia ao outro AS;
  - inicia o transporte SR do segundo domínio.

- `p-ipe-rn`
  - P do caminho primário;
  - custo 10 por enlace;
  - penúltimo salto para `pe-ipe-ce`.

- `p-ipe-ba`
  - P do caminho alternativo;
  - custo 20 por enlace;
  - waypoint do segundo domínio na SR Policy.

- `pe-ipe-ce`
  - PE remoto;
  - origina `10.0.0.8/32` no transporte LU;
  - origina `203.0.113.0/24` na sobreposição de serviço.

### Endereços que importam para a costura

| Objeto | Endereço |
|---|---|
| PE local | `10.0.0.1/32` |
| ASBR do PoP | `10.0.0.4/32` |
| enlace inter-AS | `192.0.2.8/31` |
| ASBR do backbone | `10.0.0.5/32` |
| PE remoto | `10.0.0.8/32` |
| cliente local | `198.51.100.0/24` |
| cliente remoto | `203.0.113.0/24` |

O enlace entre `192.0.2.8` e `192.0.2.9` não participa de OSPF. Cada IGP termina
no próprio ASBR.

---

## 4. O modelo mental dos labels

### 4.1 Label não é endereço global

Um endereço IP identifica um destino de forma relativamente estável. Um label
MPLS é uma chave curta para uma ação local:

```text
label recebido no topo
       ↓
lookup na LFIB local
       ↓
{próximo salto, interface, nova pilha, tratamento}
```

O mesmo número pode ter outra ação no próximo roteador. O roteador atual só pode
usar como label de saída um valor que o downstream esteja preparado para
interpretar.

### 4.2 Três famílias de label no lab

#### Prefix-SIDs na SRGB

Todos os nós configuram:

```text
segment-routing global-block 16000 23999
```

Os Prefix-SIDs são índices. Como há uma única faixa contígua:

```text
label = base da SRGB + índice
```

Exemplos:

```text
índice 4 → 16000 + 4 = 16004
índice 8 → 16000 + 8 = 16008
```

“Global” quer dizer que o SID tem semântica conhecida no domínio SR que recebeu
o anúncio IGP. Não quer dizer que OSPF inundou o SID para o outro AS.

A distinção entre SRGB/SRLB e o cálculo do label a partir do índice seguem as
seções 2.3 e 2.4 da
[RFC 8660](https://www.rfc-editor.org/rfc/rfc8660.html).

O lab usa a mesma SRGB nos dois domínios. Isso simplifica a lista explícita, mas
não une as LSDBs nem cria alcance inter-AS.

#### SIDs locais na SRLB

Todos os nós reservam:

```text
segment-routing local-block 15000 15999
```

O PeerNode SID de índice 100 resulta em:

```text
15000 + 100 = 15100
```

Esse 15100 só é uma instrução EPE no ASBR que o programou. No
`asbr-pop-pb`, significa “retire este label e envie ao peer `192.0.2.9`”.

#### Labels observados, indexados e dinâmicos

O IOS XR aloca labels fora da SRGB/SRLB para vários clientes do plano MPLS:

- Adj-SIDs SR;
- bindings BGP-LU;
- Binding SIDs de SR Policy;
- outros clientes internos da plataforma.

Por isso, nunca interprete um label apenas pelo número. Pergunte:

```text
em qual roteador?
qual comando mostrou o label?
qual é o campo ou owner?
ele é label de entrada ou de saída?
```

Na captura de referência:

- `16008` é o Prefix-SID indexado do PE remoto, importado da rota OSPF/SR para
  o BGP-LU e preservado ao longo da cadeia; não é uma alocação dinâmica que
  coincidiu com o SID;
- `24005` é o Binding SID dinâmico da policy no `pe-pop-pb`;
- `24005` também aparece como label EPE de adjacência no `asbr-pop-pb`, em
  outro roteador e contexto;
- `24000` a `24003` no `asbr-pop-pb` são Adj-SIDs SR.

Não existe conflito porque o contexto local e a direção são diferentes. A
SRGB ocupa `16000-23999`; os labels dinâmicos desta execução começam em
`24000`.

### 4.3 O contrato downstream

Considere dois roteadores, A e B:

```text
B anuncia a A: prefixo P, label 900
```

Isso significa:

```text
A → B: envie label 900 no topo para selecionar P em B
```

Em A, 900 é um **label recebido** e potencial **label de saída**.

Em B, 900 é um **label local** e **label de entrada**.

Se B readvertir P para C com next hop B e label 800, B programa:

```text
entrada 800 → troca por 900 → envia a A
```

No sentido C → A:

- C envia 800 a B;
- B consulta sua LFIB para 800;
- B troca 800 por 900;
- A recebe o valor que havia anunciado.

Essa é a mecânica central do BGP-LU.

### 4.4 Implicit-null e PHP

Um downstream pode anunciar implicit-null para pedir ao upstream que retire o
label antes de enviar. O valor reservado não precisa aparecer no fio; ele é uma
instrução de programação.

Se houver uma pilha:

```text
{16004, label-LU, IPv4}
```

e o penúltimo salto executar PHP em 16004, somente o topo desaparece:

```text
{label-LU, IPv4}
```

O label LU fica exposto para o ASBR. PHP não encerra o pacote MPLS inteiro
quando ainda há outro label abaixo.

---

## 5. RIB, LIB, LFIB e CEF

Os nomes se sobrepõem em conversas informais. Para este lab, use esta separação.

### RIB

A Routing Information Base responde:

```text
qual protocolo conhece o prefixo?
qual é o melhor caminho?
qual distância, métrica e next hop?
```

Comandos úteis:

```text
show route 10.0.0.4/32 detail
show bgp ipv4 labeled-unicast 10.0.0.8/32
```

A tabela BGP e a RIB IPv4 não são a LFIB. Uma rota pode estar válida no BGP e
ainda falhar na resolução do next hop.

### LIB ou label table

A label table responde:

```text
quais labels locais foram reservados?
qual cliente os possui?
qual FEC está associada?
```

Comando:

```text
show mpls label table
```

Ela ajuda a distinguir SR Prefix, SR Adj, BGP e SR Policy. Alocação não prova
que exista uma ação de forwarding utilizável.

### LFIB

A Label Forwarding Information Base responde:

```text
se este label chegar no topo, o que o roteador fará?
```

Comando:

```text
show mpls forwarding
```

Uma entrada típica contém:

```text
local/incoming label
outgoing label ou Pop
FEC/owner
interface de saída
next hop
backup, quando houver
```

### CEF/FIB IPv4

O CEF responde à pergunta do ingresso:

```text
se chegar um pacote IP para este prefixo, como ele sai?
```

É aqui que a recursão fica visível:

```text
rota BGP-LU para 10.0.0.8
    ↓ next hop 10.0.0.4 + label LU
rota OSPF/SR para 10.0.0.4
    ↓ next hop 192.0.2.1 + SID 16004
resultado
    ↓ {16004, label LU}
```

Comando:

```text
show cef 10.0.0.8/32 detail
```

### Um prefixo, dois pontos de entrada

Para `10.0.0.8/32`, o `pe-pop-pb` pode ter:

1. uma entrada CEF para um pacote **IP** destinado a `10.0.0.8`;
2. uma entrada LFIB para um pacote **MPLS** que chegue com o label local BGP.

O primeiro caso impõe labels. O segundo encaminha um label já recebido. Não são
a mesma direção nem a mesma operação.

---

## 6. Como o SR intradomínio nasce

### 6.1 Configuração do Prefix-SID

Em `pe-pop-pb`:

```text
router ospf 1
 router-id 10.0.0.1
 segment-routing mpls
 area 0
  segment-routing mpls
  interface Loopback0
   passive enable
   prefix-sid index 1
```

Há três fatos independentes:

- a loopback existe na RIB conectada;
- OSPF anuncia `10.0.0.1/32`;
- a extensão SR de OSPF associa o índice 1 ao prefixo.

Os outros roteadores recebem o índice e usam a SRGB local para calcular 16001.

### 6.2 Por que todos têm entrada para o Node-SID

Cada roteador do domínio calcula o SPF para a loopback e programa a ação local
para o SID:

```text
roteador de trânsito:
  entrada 16004 → swap para o label esperado pelo próximo salto

penúltimo salto:
  entrada 16004 → pop → entrega ao dono do SID

dono do SID:
  entrada 16004 → termina o segmento e continua com a próxima instrução
```

Como todos usam a mesma SRGB, um trânsito frequentemente mostra 16004 → 16004.
Ainda é um swap lógico: o label de entrada pertence à LFIB atual; o de saída é o
valor que o próximo salto entende.

Se os roteadores anunciassem SRGBs diferentes, um mesmo índice poderia resultar
em valores de saída diferentes em cada salto.

### 6.3 Caminho SR até o ASBR do PoP

O caminho primário é:

```text
pe-pop-pb → p-pop-a → asbr-pop-pb
```

O `show route` capturado mostra:

```text
10.0.0.4/32
Known via OSPF, metric 21, labeled SR
primary: 192.0.2.1 via Gi0/0/0/1, label 16004
backup:  192.0.2.3 via Gi0/0/0/2, label 16004
Local Label: 16004
```

A métrica 21 corresponde aos dois enlaces de custo 10 mais o custo do prefixo
stub. O dado operacional mais importante é o next hop primário.

No caminho normal, o modelo da LFIB é:

```text
pe-pop-pb
  pacote IP para 10.0.0.4 → push 16004 → p-pop-a

p-pop-a
  topo 16004 → pop por PHP → asbr-pop-pb

asbr-pop-pb
  recebe o pacote destinado a si sem esse label de transporte
```

### 6.4 O que a LFIB capturada já ensina

No `asbr-pop-pb`:

```text
16001  16001  SR Pfx (idx 1)  Gi0/0/0/0  192.0.2.4
16002  Pop    SR Pfx (idx 2)  Gi0/0/0/0  192.0.2.4
16003  Pop    SR Pfx (idx 3)  Gi0/0/0/1  192.0.2.6
```

Interpretação:

- para o PE `10.0.0.1`, o ASBR envia 16001 ao próximo salto `p-pop-a`;
- para o próprio `p-pop-a`, o ASBR é penúltimo e executa `Pop`;
- para o próprio `p-pop-b`, o ASBR também é penúltimo e executa `Pop`.

As linhas adicionais com `(!)` são caminhos de backup programados. Elas não são
ECMP do caminho primário.

---

## 7. Como o BGP-LU funciona no controle

### 7.1 O que é anunciado

BGP labeled-unicast usa MP-BGP:

```text
AFI  = 1  (IPv4)
SAFI = 4  (labeled-unicast)
```

Um anúncio vincula três objetos:

```text
prefixo + label ou pilha de labels + next hop
```

O significado rigoroso é:

!!! note "Observação"
    No nó identificado pelo next hop, esse label está vinculado ao prefixo.

O next hop faz parte do contrato. Um label sem o next hop que o alocou não é
informação suficiente.

Essa associação entre prefixo, label e nó identificado pelo next hop, bem como
a troca de label quando o speaker se torna o novo next hop, é definida pela
[RFC 8277](https://www.rfc-editor.org/rfc/rfc8277.html).

### 7.2 O label está dentro do UPDATE, não no cabeçalho MPLS

O BGP OPEN negocia Multiprotocol BGP. Depois, um UPDATE transporta um atributo
`MP_REACH_NLRI` com:

- AFI;
- SAFI;
- endereço de next hop;
- NLRI rotulada.

Para um único label e prefixo `/32`, a NLRI contém conceitualmente:

```text
Length = 24 bits de label + 32 bits de prefixo = 56
Label  = 20 bits de valor + bits reservados/S
Prefix = quatro octetos IPv4
```

O label codificado na NLRI BGP ocupa três octetos e não tem TTL MPLS. Ele é
informação de controle.

O UPDATE em si viaja como BGP sobre TCP porta 179. Ele não precisa chegar com
aquele label como cabeçalho de dados. Mesmo que a sessão iBGP seja transportada
sobre um LSP, esse encapsulamento é outra camada e não muda a NLRI.

### 7.3 O que acontece quando o next hop não muda

Se um speaker propaga a rota LU sem mudar o next hop, deve preservar o binding
de label associado a esse next hop.

Em uma rede com route reflector, por exemplo, o RR pode refletir reachability
sem se inserir no data plane. O next hop e o label continuam apontando para o
nó que entende o binding.

### 7.4 O que acontece quando o next hop muda

Se um speaker muda o next hop para si, o label antigo não pode simplesmente
continuar sendo anunciado como se pertencesse ao novo next hop.

O speaker normalmente:

1. recebe `prefixo P, label L1, next hop N1`;
2. seleciona a rota;
3. aloca um label local L2;
4. anuncia `prefixo P, label L2, next hop S1`;
5. programa sua LFIB:

```text
entrada L2
  → substitui L2 por L1
  → cria um túnel até N1
```

Se N1 for diretamente conectado, o “túnel” pode ser apenas a adjacência L2.
Se N1 for uma loopback distante, o túnel pode ser o transporte SR, adicionando
um Node-SID acima de L1.

Esse comportamento costura o ASBR do PoP ao PE local. No ASBR do backbone, a
continuidade final usa diretamente o Prefix-SID já instalado pelo OSPF/SR.

### 7.5 Origem local no IOS XR do lab

No PE remoto:

```text
router bgp 1916
 address-family ipv4 unicast
  network 10.0.0.8/32
  network 203.0.113.0/24
  allocate-label all
```

O `network` só origina o prefixo se houver uma rota correspondente na RIB. A
loopback conectada satisfaz essa condição para `10.0.0.8/32`.

`allocate-label all` permite ao BGP alocar bindings locais. A route-policy de
saída da sessão LU determina o que realmente pode ser anunciado.

### 7.6 Importação da rota OSPF/SR no ASBR

O anúncio do PE por iBGP-LU e a rota OSPF/SR descrevem o mesmo `/32`, mas não
têm o mesmo efeito no encaminhamento do ASBR. O OSPF vence a seleção da RIB
global e instala o Prefix-SID; apenas alocar outro label no BGP não garante uma
segunda entrada LFIB para a mesma FEC.

Cada ASBR importa somente a loopback rotulada de seu PE local:

```text
prefix-set LOCAL_PE_LOOPBACK
 10.0.0.8/32
end-set

route-policy OSPF_TO_BGP_LU
 if destination in LOCAL_PE_LOOPBACK and route-has-label then
  pass
 else
  drop
 endif
end-policy

router bgp 1916
 address-family ipv4 unicast
  redistribute ospf 1 match internal route-policy OSPF_TO_BGP_LU
```

No AS 65001, a policy equivalente contém `10.0.0.1/32`. O filtro local evita
realimentação caso a loopback remota venha a aparecer no OSPF no futuro;
`route-has-label` impede exportar uma rota IP que perdeu seu binding SR.

Dentro do BGP do ASBR, a rota redistribuída localmente vence a cópia recebida
por iBGP. Seu label é o Prefix-SID já programado (`16001` ou `16008`), portanto
o label anunciado ao peer eBGP também é uma chave de entrada válida na LFIB do
ASBR anunciante.

### 7.7 O filtro LU

```text
prefix-set LU_LOOPBACKS
 10.0.0.1/32,
 10.0.0.8/32
end-set
```

Somente as loopbacks dos PEs atravessam a malha LU.

As redes `198.51.100.0/24` e `203.0.113.0/24` pertencem à sobreposição de
serviço. Elas não devem adquirir bindings LU nem aparecer nos ASBRs.

A captura confirmou:

```text
show bgp ipv4 labeled-unicast 203.0.113.0/24
% Network not in table
```

Isso é parte da separação de papéis, não apenas higiene de configuração.

---

## 8. A propagação LU deste lab

Esta seção acompanha `10.0.0.8/32` do PE remoto ao PE local.

### 8.1 Nomes simbólicos

Para entender a cadeia sem confundir papéis locais, use símbolos:

- `S-CE`: Prefix-SID de `pe-ipe-ce`, `16008`;
- `L-IPE`: binding que `asbr-ipe-pb` entrega a `asbr-pop-pb`;
- `L-POP`: binding que `asbr-pop-pb` entrega a `pe-pop-pb`;
- `L-ING`: label local que o próprio `pe-pop-pb` associa à rota.

Na execução registrada:

```text
S-CE  = 16008
L-POP = 16008
L-IPE = 16008
L-ING = 16008
```

A igualdade não é acidental. `asbr-ipe-pb` importa a rota OSPF/SR rotulada e
anuncia seu Prefix-SID por BGP-LU. Os papéis continuam distintos porque cada
label é interpretado na LFIB do roteador que o recebe.

### 8.2 Passo 1 — OSPF/SR e iBGP anunciam a loopback

`pe-ipe-ce` anuncia `10.0.0.8/32` no OSPF com Prefix-SID `16008`. O ASBR instala:

```text
10.0.0.8/32
  → via p-ipe-rn
  → local label 16008
```

O PE também origina o `/32` no BGP e o envia por iBGP-LU, normalmente com
implicit-null para a própria loopback. Essa cópia continua visível no BGP do
ASBR, mas não é a rota usada para originar o anúncio inter-AS depois da
redistribuição.

### 8.3 Passo 2 — `asbr-ipe-pb` importa a rota OSPF/SR

`OSPF_TO_BGP_LU` admite somente `10.0.0.8/32` e exige que a rota tenha label.
O BGP cria uma rota local redistribuída, que vence a cópia recebida por iBGP e
preserva o binding instalado:

```text
prefixo:     10.0.0.8/32
origem:      OSPF interno redistribuído
local label: S-CE = 16008
```

Ao anunciar a rota para o AS 65001, o eBGP muda o next hop para o endereço da
fronteira do próprio ASBR:

```text
NLRI:     10.0.0.8/32
next hop: 192.0.2.9
label:    L-IPE = 16008
AS path:  1916
```

Esse anúncio é seguro porque `16008` já possui ação na LFIB do ASBR: encaminhar
o Prefix-SID pelo domínio SR até `pe-ipe-ce`.

### 8.4 Passo 3 — `asbr-pop-pb` aprende por eBGP

O ASBR do PoP recebe:

```text
10.0.0.8/32
next hop 192.0.2.9
received label L-IPE
AS path 1916
```

O next hop é diretamente conectado no enlace inter-AS.

Ao anunciar para `pe-pop-pb`, a configuração usa:

```text
neighbor 10.0.0.1
 address-family ipv4 labeled-unicast
  next-hop-self
```

O anúncio iBGP passa a ser:

```text
NLRI:     10.0.0.8/32
next hop: 10.0.0.4
label:    L-POP
AS path:  1916
```

O ASBR programa:

```text
entrada L-POP
  → swap para L-IPE
  → envia ao next hop 192.0.2.9
```

A LFIB capturada mostra:

```text
16008  16008  SR Pfx (idx 8)  next hop 10.0.0.5
```

Leia a linha por direção:

```text
16008 da esquerda = L-POP, binding local do ASBR
16008 da direita  = L-IPE, label enviado ao next hop
```

### 8.5 Passo 4 — `pe-pop-pb` aprende por iBGP

O BGP capturado mostra:

```text
BGP routing table entry for 10.0.0.8/32
Local Label: 16008
AS path: 1916
next hop: 10.0.0.4, metric 21
Received Label 16008
valid, internal, best, labeled-unicast
Label-Index: 8
```

Interpretação:

- `16008` recebido é `L-POP`, o valor que o PE impõe ao enviar ao ASBR;
- o `Local Label` 16008 é `L-ING`, um binding local no PE;
- a igualdade acompanha o binding SR importado na origem, mas não torna os
  objetos globais;
- o next hop BGP `10.0.0.4` ainda precisa de resolução.

### 8.6 Passo 5 — recursão no CEF

O PE consulta a rota para `10.0.0.4/32`:

```text
OSPF/SR
next hop 192.0.2.1
label 16004
metric 21
```

Depois combina os dois resultados:

```text
BGP-LU fornece: L-POP = 16008
OSPF/SR fornece: SID para next hop = 16004

CEF instala: {16004, 16008}
```

Essa é a “tradução” aparente. Na realidade é **recursão e composição de pilha**.

### 8.7 Por que `next-hop-self` é decisivo

Sem `next-hop-self`, o PE do PoP poderia receber `192.0.2.9` como next hop. Esse
endereço pertence ao enlace inter-AS e não está no OSPF do AS 65001.

Com `next-hop-self`, o PE só precisa conhecer `10.0.0.4`, que é uma loopback
intradomínio com transporte SR.

O ASBR se compromete a receber `L-POP`, fazer o swap e continuar a cadeia.

---

## 9. A LFIB e o pacote no caminho normal

### 9.1 Estado lógico necessário

Para enviar um pacote IP a `10.0.0.8`, a cadeia precisa destas ações:

#### `pe-pop-pb`

Entrada: pacote IPv4.

Lookup:

```text
10.0.0.8/32 → BGP-LU via 10.0.0.4, received label L-POP
10.0.0.4/32 → OSPF/SR via p-pop-a, SID 16004
```

Ação:

```text
push {16004, L-POP}
send p-pop-a
```

#### `p-pop-a`

Entrada:

```text
topo 16004
abaixo L-POP
```

Ação esperada por PHP:

```text
pop 16004
send asbr-pop-pb
```

Saída:

```text
topo L-POP
```

#### `asbr-pop-pb`

Entrada:

```text
topo L-POP
```

LFIB:

```text
L-POP → swap L-IPE → 192.0.2.9
```

Saída:

```text
topo L-IPE
```

#### `asbr-ipe-pb`

Entrada:

```text
topo L-IPE
```

Ação definida pela LFIB do Prefix-SID importado para o BGP-LU:

```text
L-IPE = 16008
encaminhar pelo caminho SR até 10.0.0.8
```

Saída:

```text
{16008, IPv4}
```

#### `p-ipe-rn`

É o penúltimo salto do Node-SID 16008.

Ação esperada:

```text
pop 16008
send pe-ipe-ce
```

Depois do PHP, o pacote sai como IPv4 para o PE.

#### `pe-ipe-ce`

O PE entrega o pacote ao processamento IP da própria loopback.

### 9.2 Pilha por enlace

Use esta tabela como modelo, não como pcap da imagem Control Plane:

| Enlace | Pilha, topo primeiro |
|---|---|
| PE local → P primário | `{16004, L-POP, IPv4}` |
| P primário → ASBR local | `{L-POP, IPv4}` |
| ASBR local → ASBR remoto | `{L-IPE, IPv4}` |
| ASBR remoto → P primário | `{16008, IPv4}` |
| P primário → PE remoto | `IPv4` após PHP |

Na execução registrada, substitua:

```text
L-POP = 16008
L-IPE = 16008
```

Logo, o início observado pelo CEF foi:

```text
PE local → P primário: {16004, 16008}
```

O pop nas LFIBs de `p-pop-a` e `p-ipe-rn` não foi capturado diretamente no
artefato versionado. É comportamento esperado pela programação SR/PHP, não uma
captura de pacote.

### 9.3 Por que o P não conhece o BGP-LU

`p-pop-a` não precisa de sessão BGP nem da rota `10.0.0.8/32`.

Enquanto 16004 está no topo, ele só executa a FEC SR:

```text
“alcance asbr-pop-pb pelo SPF”
```

O label LU está escondido abaixo. Ele só vira topo no ASBR. Essa separação evita
colocar rotas inter-AS nos Ps.

### 9.4 Caminho reverso

A mesma lógica vale para `10.0.0.1/32`, em sentido inverso:

```text
pe-pop-pb origina LU
  → asbr-pop-pb muda next hop na fronteira
  → asbr-ipe-pb usa next-hop-self para pe-ipe-ce
  → pe-ipe-ce recursa sobre SID 16005 até seu ASBR
```

A captura em `pe-ipe-ce` mostrou:

```text
10.0.0.1/32
next hop 10.0.0.5
Received Label 16001
Local Label 16001
AS path 65001
```

Novamente, igualdade numérica não elimina a distinção entre label local e
label recebido.

---

## 10. O que existe no fio

### 10.1 O quadro de dados MPLS

Em Ethernet, um pacote MPLS unicast normalmente usa EtherType `0x8847`.

Cada entrada da pilha tem 32 bits:

```text
+--------------------+-----+-+--------+
| label: 20 bits     | TC  |S| TTL    |
+--------------------+-----+-+--------+
                      3     1   8 bits
```

- **Label:** chave da LFIB;
- **TC:** classe de tráfego/ECN conforme a política;
- **S:** 1 somente no último label da pilha;
- **TTL:** TTL MPLS daquele nível.

Para `{16004, 16008, IPv4}`:

```text
16004: S=0, porque há outro label abaixo
16008: S=1, porque é o último label antes do IPv4
```

O valor exato de TC/TTL depende do modo de propagação e da plataforma. O lab não
os configurou nem capturou; não os deduza da pilha CEF.

O formato de 32 bits, o bit de fundo da pilha e as operações de lookup são
definidos pela [RFC 3032](https://www.rfc-editor.org/rfc/rfc3032.html).

### 10.2 Lookup somente no topo

Um LSR não procura todos os labels simultaneamente.

Em `p-pop-a`:

```text
topo = 16004 → consulta LFIB de 16004
16008 permanece opaco abaixo
```

Em `asbr-pop-pb`, após PHP:

```text
topo = 16008 → consulta LFIB de 16008
```

É assim que uma pilha funciona como uma sequência de instruções.

### 10.3 O UPDATE BGP-LU no fio

O pacote de controle é diferente:

```text
Ethernet/IP
  TCP porta 179
    cabeçalho BGP
      UPDATE
        path attributes
          MP_REACH_NLRI
            AFI 1
            SAFI 4
            next hop
            label + prefixo
```

Não há um shim MPLS de dados “16008” automaticamente na frente desse UPDATE só
porque ele anuncia 16008. O valor é um campo da NLRI.

### 10.4 O que mudaria em uma captura real

No controle, você veria UPDATEs diferentes em cada sessão:

```text
PE remoto → ASBR remoto:
  next hop 10.0.0.8, implicit-null ou label local
  (cópia iBGP, não selecionada para o anúncio inter-AS)

OSPF/SR → BGP no ASBR remoto:
  prefixo 10.0.0.8/32, local label 16008

ASBR remoto → ASBR local:
  next hop 192.0.2.9, label L-IPE = 16008, AS path 1916

ASBR local → PE local:
  next hop 10.0.0.4, label L-POP, AS path 1916
```

No data plane, veria a pilha mudar por enlace como na seção anterior.

Na imagem deste repositório, capture e confie no primeiro conjunto. Para provar
o segundo, use uma imagem/plataforma com data plane suportado.

---

## 11. A sobreposição de serviço

### 11.1 Sessão PE–PE

Os PEs configuram eBGP IPv4 unicast multihop entre as loopbacks:

```text
pe-pop-pb, AS 65001, source 10.0.0.1
        ↕ eBGP multihop
pe-ipe-ce, AS 1916, source 10.0.0.8
```

Ela deveria anunciar:

```text
198.51.100.0/24 → lado do PoP
203.0.113.0/24  → lado CE
```

### 11.2 Dependência circular aparente

A sessão de serviço precisa alcançar as loopbacks dos PEs. Esse alcance vem do
BGP-LU:

```text
LU transporta reachability rotulada das loopbacks
        ↓
TCP/179 multihop entre as loopbacks pode formar
        ↓
IPv4 unicast troca os prefixos de cliente
```

Não é uma circularidade real. O transporte LU é estabelecido primeiro e não
depende da sessão de serviço.

### 11.3 O pacote de serviço pretendido

Sem VPN, o fluxo conceitual para `203.0.113.10` seria:

```text
instituicao-pb envia IPv4 ao gateway 198.51.100.1
  ↓
pe-pop-pb encontra 203.0.113.0/24 via BGP, next hop 10.0.0.8
  ↓
o next hop remoto recursa sobre o transporte inter-AS
  ↓
pe-ipe-ce recebe IPv4
  ↓
rota conectada 203.0.113.0/24 entrega ao servico-ce
```

Não há label VPN no fundo da pilha. No egress, a rota global IPv4 decide a
interface de cliente.

### 11.4 O que ocorreu na execução

```text
neighbor 10.0.0.8, AF IPv4 unicast: Established, 1 prefixo recebido
203.0.113.0/24: best path com color 100 e BSID 24005
ping nos dois sentidos: 0% de perda
traceroute: destino alcançado com extensões ICMP MPLS
```

O traceroute mostrou a lista explícita ativa e sua redução salto a salto. Assim,
a execução correlaciona policy operacional, rota elegível e tráfego efetivamente
dirigido, em vez de inferir steering apenas de `Operational: up`.

### 11.5 Por que isso não é Option C completa

Em Option C completa, normalmente:

- ASBRs trocam rotas rotuladas para reachability dos PEs;
- PEs estabelecem MP-BGP para VPNv4/vpnv6;
- a rota VPN carrega RD, RT e label de VPN;
- o pacote tem transporte e label de serviço.

Aqui:

- a camada LU existe;
- a sessão PE–PE é IPv4 unicast global;
- não existem AF VPN, VRF, RD, RT ou label VPN.

Use a expressão “substrato de transporte inspirado na Option C”.

---

## 12. SR Policy, cor, BSID e BGP-EPE

### 12.1 Identidade da policy

A policy é identificada por:

```text
headend = pe-pop-pb
color   = 100
endpoint= 10.0.0.8
```

No contexto do headend, color + endpoint selecionam o objeto.

Essa identidade e as condições de per-destination steering estão na
[RFC 9256](https://www.rfc-editor.org/rfc/rfc9256.html).

### 12.2 Candidate path e lista explícita

```text
segment-list INTERAS-BACKUP
 16003
 16004
 15100
 16007
 16008
```

Sem a policy, o SPF usaria os ramos `p-pop-a` e `p-ipe-rn`. A lista força:

```text
pe-pop-pb
  → p-pop-b
  → asbr-pop-pb
  → peer asbr-ipe-pb
  → p-ipe-ba
  → pe-ipe-ce
```

### 12.3 Semântica de cada segmento

#### 16003

Node-SID de `p-pop-b` no AS 65001.

Enquanto estiver ativo:

```text
siga o SPF do domínio do PoP até p-pop-b
```

Como é vizinho direto do headend, a plataforma pode aplicar otimização/PHP na
pilha física. A lista lógica continua contendo o segmento.

#### 16004

Node-SID de `asbr-pop-pb` no AS 65001.

Depois de alcançar `p-pop-b`, esse label conduz diretamente ao ASBR pelo ramo
alternativo.

#### 15100

PeerNode SID local no `asbr-pop-pb`:

```text
15100 → Pop → Gi0/0/0/2 → 192.0.2.9
```

Ele não significa “Node-SID de `asbr-ipe-pb`”. Significa “use este peer BGP como
saída”.

Quando 15100 é retirado, 16007 fica no topo. O pacote já chegou ao nó exato que
entende 15100, e o próximo nó pertence ao domínio que entende 16007.

#### 16007

Node-SID de `p-ipe-ba` no AS 1916. O `asbr-ipe-pb` consulta a LFIB do segundo
domínio e envia pelo ramo alternativo.

#### 16008

Node-SID de `pe-ipe-ce`, destino final da policy.

### 12.4 Por que uma lista pode cruzar domínios

Os labels não precisam ser compreendidos por todos os roteadores ao mesmo
tempo. Precisam ser válidos quando chegam ao topo.

```text
AS 65001 entende 16003 e 16004
asbr-pop-pb entende localmente 15100
15100 entrega ao AS 1916
AS 1916 entende 16007 e 16008
```

O segmento de transição é o PeerNode SID.

Se 16007 subisse ao topo ainda no `asbr-pop-pb`, sua semântica seria ambígua ou
incorreta. A ordem evita isso.

### 12.5 LFIB do EPE

A captura mostra:

```text
15100  Pop  SRLB (idx 100)  Gi0/0/0/2  192.0.2.9
```

O `Pop` remove somente 15100. Qualquer label abaixo permanece.

Na pilha completa:

```text
antes: {15100, 16007, 16008, IPv4}
depois:{16007, 16008, IPv4}
```

O frame cruza o enlace inter-AS ainda como MPLS, agora com uma instrução válida
no domínio receptor.

PeerNode, PeerAdj e PeerSet são BGP Peering Segments. O comportamento de
PeerNode usado aqui segue a
[RFC 9087](https://www.rfc-editor.org/rfc/rfc9087.html), mas o lab não implementa
a distribuição BGP-LS/controlador descrita na solução centralizada completa.

### 12.6 Binding SID

A policy operacional recebeu dinamicamente:

```text
Binding SID: 24005
```

No `pe-pop-pb`, esse BSID significa:

```text
encaminhe pela instância local da policy color 100 / endpoint 10.0.0.8
```

A LFIB do BSID expande ou referencia a lista ativa. Isso permite que outras
rotas ou policies apontem para um único label em vez de repetir os cinco
segmentos.

Esse 24005 não é o label LU 16008 recebido do `asbr-pop-pb`. O BSID é
interpretado localmente no PE; o label LU recebido pertence à recursão da
loopback remota.

### 12.7 Cor e steering BGP

A route-policy de entrada faz:

```text
set extcommunity color 100
```

Para per-destination steering, o headend precisa simultaneamente de:

1. uma rota BGP com next hop N;
2. Color Extended Community C autorizada;
3. uma policy válida `(color C, endpoint N)`.

Quando as três condições existem, a rota pode resolver pelo BSID/policy em vez
do caminho IGP comum ao next hop.

Na execução de referência, as três condições foram satisfeitas: a sessão de
serviço ficou `Established`, `203.0.113.0/24` foi recebida com cor 100 e a rota
foi associada ao BSID 24005. Portanto:

```text
policy operacional = provado
capacidade de BGP steering = habilitada
rota efetivamente dirigida = provado
pacotes na policy = provado pelo traceroute MPLS
```

O traceroute mostrou `{16004, 15100, 16007, 16008}` após o PHP do primeiro SID
da lista explícita, seguido pela redução esperada da pilha até o PE remoto.

### 12.8 Pilha lógica da policy

No headend, antes de otimizações de PHP:

```text
topo → 16003
        16004
        15100
        16007
base →  16008
        IPv4
```

Cada segmento concluído expõe o próximo. A pilha física observada em cada
enlace pode ser menor por PHP e otimizações locais.

O `Maximum SID Depth: 10` mostrado pelo XR aceita os cinco segmentos. Em
hardware real, confirme MSD, MTU e capacidade de imposição da plataforma.

---

## 13. TI-LFA neste losango

### 13.1 Objeto protegido

No `pe-pop-pb`, a rota protegida de referência é `10.0.0.4/32`:

```text
primário: via 192.0.2.1, p-pop-a, metric 21
backup:   via 192.0.2.3, p-pop-b, metric 41
```

O PE é o PLR para uma falha diretamente conectada no ramo primário.

### 13.2 Estado pré-instalado

O CEF capturado mostra os dois estados:

```text
via 192.0.2.1 ... protected
  local label 16004 labels imposed {16004}

via 192.0.2.3 ... backup (Local-LFA)
  local label 16004 labels imposed {16004}
```

O backup já está programado antes da falha. Detectar a falha não precisa esperar
um novo SPF para começar o desvio local.

### 13.3 Por que aparece Local-LFA com TI-LFA habilitado

O vizinho `p-pop-b` já satisfaz a condição de loop-free alternate e tem caminho
direto ao ASBR:

```text
pe-pop-pb → p-pop-b → asbr-pop-pb
```

Não é necessária uma repair list com vários SIDs. O caso simples é representado
como Local-LFA mesmo com TI-LFA habilitado.

TI-LFA não promete que toda topologia produzirá uma pilha de reparo visível. Ele
permite usar segmentos quando o LFA local não basta.

O cálculo de P-space, Q-space e Repair List da solução completa é definido pela
[RFC 9855](https://www.rfc-editor.org/rfc/rfc9855.html). Neste losango, o LFA
local evita a necessidade de uma lista mais longa.

### 13.4 Sequência durante uma falha

```text
1. interface/enlace falha
2. PLR detecta a falha
3. CEF seleciona o backup pré-instalado
4. pacote com FEC 16004 sai por p-pop-b
5. OSPF inunda a mudança
6. roteadores executam novo SPF
7. RIB/FIB convergem para o caminho pós-falha
```

Os passos 2 e 3 são reparo local. Os passos 5 a 7 são convergência global.

### 13.5 O que não foi medido

- tempo de detecção;
- perda de pacotes;
- microloops durante convergência;
- proteção de nó ou SRLG;
- SLA de 50 ms.

Não há BFD e a imagem não possui data plane suportado. O lab prova a presença do
backup no CEF.

---

## 14. Leitura da configuração

Esta seção traduz os blocos principais para seus efeitos.

### 14.1 SRGB e SRLB

```text
segment-routing global-block 16000 23999
segment-routing local-block 15000 15999
```

- reserva a SRGB para SIDs globais por índice;
- reserva a SRLB para SIDs locais;
- não habilita sozinho anúncios SR no OSPF;
- não cria uma sessão ou protocolo de distribuição separado.

### 14.2 OSPF SR

```text
router ospf 1
 segment-routing mpls
 area 0
  segment-routing mpls
```

Habilita as extensões SR no processo/área. Em seguida:

```text
interface Loopback0
 passive enable
 prefix-sid index N
```

associa o Prefix-SID ao prefixo anunciado da loopback sem tentar formar
adjacência nela.

### 14.3 Interfaces do core

```text
network point-to-point
cost 10|20
fast-reroute per-prefix
fast-reroute per-prefix ti-lfa enable
```

- elimina eleição de DR/BDR no enlace de dois nós;
- define preferência do ramo;
- solicita backup por prefixo;
- habilita cálculo TI-LFA.

### 14.4 Originação e labels BGP

```text
address-family ipv4 unicast
 network 10.0.0.X/32
 allocate-label all
```

- injeta a rota local elegível no BGP;
- permite que o processo mantenha um binding MPLS;
- não ignora as route-policies da AF LU.

Nos ASBRs, a origem inter-AS vem da rota OSPF/SR instalada:

```text
prefix-set LOCAL_PE_LOOPBACK
 10.0.0.X/32
end-set

route-policy OSPF_TO_BGP_LU
 if destination in LOCAL_PE_LOOPBACK and route-has-label then
  pass
 else
  drop
 endif
end-policy

address-family ipv4 unicast
 redistribute ospf 1 match internal route-policy OSPF_TO_BGP_LU
 allocate-label all
```

- importa somente a loopback do PE local;
- exige que a rota OSPF tenha binding MPLS;
- faz o anúncio LU usar o Prefix-SID que já possui LFIB no ASBR.

### 14.5 AF labeled-unicast

```text
address-family ipv4 labeled-unicast
 route-policy LU_ONLY in
 route-policy LU_ONLY out
```

Ativa AFI 1/SAFI 4 na sessão e controla import/export.

No iBGP do ASBR para o PE:

```text
next-hop-self
```

cria o ponto de recursão intradomínio e exige um binding local correspondente.

### 14.6 Fronteira MPLS

Nos ASBRs:

```text
! asbr-pop-pb
router static
 address-family ipv4 unicast
  192.0.2.9/32 GigabitEthernet0/0/0/2

mpls static
 interface GigabitEthernet0/0/0/2
```

Esse bloco habilita o contexto de encaminhamento MPLS na interface de fronteira
usada pela LFIB. Ele não fixa o valor dos labels LU. Neste lab, os bindings das
loopbacks exportadas são os Prefix-SIDs importados do OSPF/SR; outros bindings
BGP e o Binding SID da SR Policy podem continuar dinâmicos. No `asbr-ipe-pb`,
a rota simétrica é `192.0.2.8/32 GigabitEthernet0/0/0/2`.

A rota host é necessária no IOS XR para que o label recebido na fronteira
Inter-AS seja vinculado a um FEC `/32`. Sem esse binding, o controle BGP-LU
pode subir normalmente sem que o data plane encaminhe os pacotes rotulados.
A exigência é documentada pela Cisco em
[Configure Inter-AS Option C MPLS VPN With Cisco IOS and Cisco IOS-XR](https://www.cisco.com/c/en/us/support/docs/multiprotocol-label-switching-mpls/mpls/200523-Configuration-and-Verification-of-Layer.html).

### 14.7 EPE

```text
neighbor 192.0.2.9
 egress-engineering
 peer-node-sid index 100
```

- associa o objeto EPE ao peer;
- transforma o índice 100 da SRLB em 15100;
- programa uma ação local para a adjacência do peer;
- não anuncia esse SID pelo OSPF ao outro domínio;
- não cria BGP-LS ou controlador.

### 14.8 Policy explícita

```text
segment-routing
 traffic-eng
  segment-list INTERAS-BACKUP
  policy INTERAS-COLOR-100
   color 100 end-point ipv4 10.0.0.8
```

O candidate path é configurado localmente. A preferência 100 seleciona a lista
entre os candidate paths disponíveis; ela não é a Color Extended Community.

### 14.9 Credenciais e uso de lab

As credenciais `clab/clab@123` são locais e aparecem nos startup-configs. Não as
reaproveite em outro ambiente.

---

## 15. Execução por estágios

### Preparação

```bash
mkdir -p ~/labs/inter-as
cp -r labs/cisco/sr-mpls/inter-as/bgp-lu ~/labs/inter-as/
cd ~/labs/inter-as/bgp-lu
```

`configs/` é o estado final, com tudo ligado. Para percorrer um estágio de
cada vez, copie `configs/` para um diretório de trabalho e retire dos `.cfg`
os blocos que ainda não entraram - a lista do que entra em cada estágio está
no [roteiro principal](bgp-lu.md#progressao-em-seis-estagios). Depois:

```bash
sudo clab deploy -t lab.clab.yml --reconfigure
```

`--reconfigure` reaplica os `.cfg` em vez de reusar a config gravada pela
execução anterior - é o que torna a progressão por estágios repetível.

O Containerlab pode mostrar contêiner `running` antes de o IOS XR estar pronto.
Use estado protocolar como gate, não um sleep fixo.

### Estágio 1 — underlay OSPF

Estado introduzido:

- interfaces e /31s;
- loopbacks;
- dois processos OSPF isolados;
- custos 10/20;
- clientes e rotas default.

Prove:

```text
show ospf neighbor
show route 10.0.0.4/32 detail
show route 10.0.0.8/32 detail
```

Resultado correto:

- `pe-pop-pb` conhece 10.0.0.1–4, mas não 10.0.0.5–8;
- `asbr-ipe-pb` conhece o segundo domínio;
- nenhum IGP cruza o enlace inter-AS.

### Estágio 2 — SR-MPLS

Estado introduzido:

- SRGB/SRLB;
- extensões SR no OSPF;
- Prefix-SID nas loopbacks.

Prove em sequência:

```text
show ospf database opaque-area self-originate
show route 10.0.0.4/32 detail
show mpls label table 0 label 16004 detail
show mpls forwarding
show cef 10.0.0.4/32 detail
```

Não basta encontrar 16004 na label table. Confirme a ação de forwarding e a
pilha imposta para tráfego IP.

### Estágio 3 — BGP-LU

Estado introduzido:

- iBGP-LU PE–ASBR em cada domínio;
- eBGP-LU entre os ASBRs;
- `next-hop-self` em direção aos PEs;
- filtro das loopbacks;
- redistribuição OSPF→BGP filtrada para o Prefix-SID do PE local em cada ASBR;
- continuidade LFIB entre o binding LU e o transporte SR.

Gate completo:

```text
show bgp ipv4 labeled-unicast summary
show bgp ipv4 labeled-unicast 10.0.0.8/32
show cef 10.0.0.8/32 detail
show mpls forwarding
```

Não avance apenas porque a sessão está Established. O lab já observou a sessão
estabelecida antes de label/best path/CEF estabilizarem.

### Estágio 4 — serviço IPv4 multihop

Estado pretendido:

- eBGP IPv4 unicast entre os PEs;
- anúncio de uma rede de cliente em cada sentido;
- filtro de exportação que impede as loopbacks de vazarem na AF unicast;
- ainda sem steering por color.

No estágio 4, o renderer aplica `route-policy PASS in`; a policy `COLOR_100` só
é definida e referenciada no estágio 6. Na saída, cada PE aplica
`PE_UNICAST_EXPORT_ONLY`: `pe-pop-pb` exporta apenas `198.51.100.0/24` e
`pe-ipe-ce` apenas `203.0.113.0/24`. A checagem estática rejeita snapshots que
referenciem uma route-policy ainda não definida.

Na execução final de referência, a sessão ficou `Established`, trocou um prefixo
em cada sentido e encaminhou tráfego entre os clientes.

### Estágio 5 — TI-LFA

Estado introduzido:

- FRR por prefixo;
- cálculo TI-LFA em interfaces do core.

Prove:

```text
show route 10.0.0.4/32 detail
show cef 10.0.0.4/32 detail
```

Procure `protected` no primário e `backup (Local-LFA)` no alternativo.

### Estágio 6 — EPE e SR Policy

Estado introduzido:

- PeerNode SID 15100;
- lista de cinco segmentos;
- policy color 100 / endpoint 10.0.0.8;
- Color Extended Community na rota recebida.

Prove separadamente:

```text
show bgp egress-engineering
show mpls forwarding labels 15100 detail
show segment-routing traffic-eng policy color 100
show bgp ipv4 unicast 203.0.113.0/24
show cef 203.0.113.0/24 detail
```

Os três primeiros podem passar enquanto os dois últimos falham por ausência da
sessão de serviço. Registre os resultados sem misturá-los.

### Estado final direto

```bash
sudo clab deploy -t lab.clab.yml
```

Encerramento:

```bash
sudo clab destroy -t lab.clab.yml --cleanup
```

---

## 16. Como provar cada camada

### Cadeia mínima de evidência para SR

```text
1. OSPF anuncia prefixo + SID
2. RIB instala rota labeled SR
3. label table mostra owner
4. LFIB mostra ação para label de entrada
5. CEF mostra label imposto para pacote IP
```

Comandos:

```text
show ospf database opaque-area
show route 10.0.0.4/32 detail
show mpls label table 0 label 16004 detail
show mpls forwarding labels 16004 detail
show cef 10.0.0.4/32 detail
```

### Cadeia mínima de evidência para BGP-LU

```text
1. sessão AF LU está Established
2. rota OSPF/SR do PE local tem Prefix-SID no ASBR de origem
3. rota OSPF redistribuída é o best path BGP no ASBR de origem
4. label anunciado pelo ASBR existe em sua LFIB
5. rota remota está valid/best/labeled-unicast
6. next hop BGP resolve no IGP/SR
7. CEF impõe {transporte, label recebido}
8. prefixos de cliente estão ausentes da LU
```

Comandos no PE local:

```text
show bgp ipv4 labeled-unicast summary
show bgp ipv4 labeled-unicast 10.0.0.8/32
show route 10.0.0.4/32 detail
show cef 10.0.0.8/32 detail
show bgp ipv4 labeled-unicast 203.0.113.0/24
```

Comandos no ASBR:

```text
show bgp ipv4 labeled-unicast 10.0.0.8/32
show route 10.0.0.8/32 detail
show mpls forwarding labels 16008 detail
```

### Folha de correlação da mesma execução

Preencha sem copiar valores antigos:

```text
prefixo remoto:              10.0.0.8/32
next hop visto no PE:        __________________
Received Label no PE:        __________________  = L-POP
Local Label no PE:           __________________  = L-ING
SID até o next hop:          __________________
pilha no CEF:                __________________
label local no ASBR do PoP:  __________________  deve casar com L-POP
label de saída no ASBR:      __________________  = L-IPE
next hop de fronteira:       __________________
Prefix-SID no ASBR remoto:   __________________  deve casar com L-IPE
```

As relações devem casar. Labels dinâmicos podem mudar; os Prefix-SIDs
continuam derivados da SRGB e dos índices configurados.

### Como ler os campos capturados

```text
Local Label: 16008
```

Binding que o roteador local instalou para a rota. Não é automaticamente o
label imposto em direção ao peer.

```text
Received Label 16008
```

Binding que o next hop anunciou e que deve ser usado na saída.

```text
next hop 10.0.0.4/32 via 16004/0/21
```

Recursão do next hop sobre rota SR com SID 16004, algoritmo 0, métrica 21.

```text
labels imposed {16004 16008}
```

Resultado final para pacote IP: topo à esquerda.

### Evidência para EPE e policy

Não pare em `Operational: up`.

```text
EPE object → mostra peer e label 15100
LFIB 15100 → mostra Pop e interface correta
SR Policy → mostra candidate path ativo e lista válida
BGP route → mostra color e next hop elegíveis
CEF da rota → mostra steering real pela policy
contadores/pcap → mostram tráfego, se houver data plane
```

Neste lab, os seis itens foram positivamente demonstrados. O traceroute exibiu
a pilha da lista explícita e alcançou o cliente remoto.

??? example "Saídas-chave da execução de referência"

    ```text
    pe-pop-pb# show bgp ipv4 labeled-unicast 10.0.0.8/32
    Local Label: 16008
    1916
      10.0.0.4 (metric 21) from 10.0.0.4
        Received Label 16008
        valid, internal, best, labeled-unicast

    pe-pop-pb# show cef 10.0.0.8/32 detail
    via 10.0.0.4/32, recursive
     next hop 10.0.0.4/32 via 16004/0/21
     local label 16008
     next hop 192.0.2.1 Gi0/0/0/1 labels imposed {16004 16008}

    asbr-pop-pb# show mpls forwarding
    15100 Pop   SRLB (idx 100) Gi0/0/0/2 192.0.2.9
    16008 16008 SR Pfx (idx 8)             10.0.0.5

    pe-pop-pb# show segment-routing traffic-eng policy color 100
    Admin: up  Operational: up
    SID[0]: 16003
    SID[1]: 16004
    SID[2]: 15100
    SID[3]: 16007
    SID[4]: 16008
    Binding SID: 24005

    instituicao-pb# traceroute -e 203.0.113.10
    192.0.2.3  <MPLS:L=16004/L=15100/L=16007/L=16008>
    192.0.2.7  <MPLS:L=15100/L=16007/L=16008>
    192.0.2.9  <MPLS:L=16007/L=16008>
    192.0.2.13 <MPLS:L=16008>
    203.0.113.10
    ```

---

## 17. Como capturar o controle no fio

### 17.1 Comece antes das sessões

BGP envia a tabela quando a sessão sobe. Para observar os UPDATEs LU, inicie a
captura antes de subir o estágio 3 ou o estado final.

Em um terminal:

```bash
sudo tcpdump -ni any \
  'tcp port 179 and (host 192.0.2.8 or host 192.0.2.9)' \
  -w /tmp/ipe-ebgp-lu.pcap
```

Em outro, suba (ou reaplique) o lab para forçar o estabelecimento das
sessões enquanto a captura corre:

```bash
sudo clab deploy -t lab.clab.yml --reconfigure
```

O uso de `any` é simples, mas pode registrar o mesmo pacote em mais de um ponto
do host. Para uma captura limpa, descubra a veth específica do enlace com:

```bash
ip -br link | rg 'asbr|ipe|clab'
```

e substitua `any` pelo nome exato.

### 17.2 O que abrir no Wireshark

Use o display filter:

```text
tcp.port == 179
```

Expanda:

```text
Border Gateway Protocol
  UPDATE Message
    Path attributes
      MP_REACH_NLRI
```

Confirme:

- AFI IPv4;
- SAFI Labeled Unicast;
- next hop `192.0.2.8` ou `192.0.2.9`, conforme direção;
- prefixo `10.0.0.1/32` ou `10.0.0.8/32`;
- label anunciado;
- AS_PATH.

### 17.3 Correlacione pcap e CLI

Para um UPDATE recebido por `asbr-pop-pb` de `asbr-ipe-pb`:

```text
label no MP_REACH_NLRI
        = Received Label na rota BGP do asbr-pop-pb
        = Outgoing Label na LFIB que atende o binding local anunciado ao PE
```

Depois confira o anúncio do `asbr-pop-pb` ao PE. O novo label no UPDATE deve
aparecer como:

```text
Received Label no pe-pop-pb
        = Local Label de entrada no asbr-pop-pb
```

Essa correlação prova a cadeia sem precisar adivinhar alocação interna.

### 17.4 Captura MPLS de dados

Em uma plataforma com data plane, capture numa interface de enlace e use:

```bash
sudo tcpdump -eni INTERFACE mpls
```

Ou grave para análise:

```bash
sudo tcpdump -ni INTERFACE 'ether proto 0x8847' -w /tmp/ipe-mpls.pcap
```

No Wireshark:

```text
mpls
```

Repita em cada enlace e compare o topo:

```text
16004 → L-POP → L-IPE (= 16008) → 16008 → IPv4
```

Não espere essa prova na imagem XRd Control Plane usada pelo repositório.

### 17.5 Captura e segurança

Uma pcap pode conter:

- endereços de gestão;
- ASNs;
- atributos BGP;
- tráfego de outros labs se `any` for usado;
- credenciais de protocolos sem criptografia, se existirem.

Restrinja o filtro e revise o arquivo antes de publicá-lo.

---

## 18. Troubleshooting orientado por dependências

### Sintoma: vizinho LU não estabelece

Verifique de baixo para cima:

```text
interface up/up?
rota até o endereço do peer?
source address correto?
TCP/179 alcançável?
remote-as correto?
AF labeled-unicast ativada nos dois lados?
route-policy anexada?
```

Comandos:

```text
show interfaces brief
show route ENDERECO-DO-PEER
show bgp ipv4 labeled-unicast summary
show bgp neighbors ENDERECO detail
```

### Sintoma: sessão Established, zero prefixos

Verifique:

- rota de origem existe na RIB;
- no PE, `network` coincide exatamente;
- no ASBR de origem, `OSPF_TO_BGP_LU` admite a loopback local rotulada;
- label foi alocado;
- `LU_ONLY` permite o `/32`;
- o vizinho ativou a AF correta;
- aguarde best path e label, não apenas keepalives.

### Sintoma: rota LU existe, mas não é best

Leia os motivos no detalhe BGP:

```text
valid?
label presente?
next hop alcançável?
AS path rejeitado?
policy descartou?
```

Uma sessão operacional não torna next hop recursivamente alcançável.

### Sintoma: `Received Label` existe, mas CEF não mostra pilha

Siga o next hop:

```text
show route NEXT-HOP/32 detail
show cef NEXT-HOP/32 detail
show mpls forwarding labels SID detail
```

Se o next hop não tiver transporte, o label BGP isolado não resolve a rota.

Nos ASBRs, confirme também a rota host para o peer da fronteira:

```text
show route 192.0.2.9/32 detail   ! asbr-pop-pb
show route 192.0.2.8/32 detail   ! asbr-ipe-pb
```

Uma sessão BGP-LU `Established` sem essa rota `/32` não prova encaminhamento
MPLS na fronteira.

### Sintoma: o CEF mostra `{16004, 16008}`, mas o tráfego falha

O CEF do ingresso é apenas o primeiro elo. Verifique:

```text
LFIB de 16004 nos Ps
LFIB de L-POP no ASBR local
MPLS habilitado na fronteira
LFIB de L-IPE = 16008 no ASBR remoto
Prefix-SID 16008 até o PE no segundo domínio
MTU/MPLS no data plane
disposição final no PE remoto
```

Na execução de referência o tráfego funcionou. Se outra execução falhar,
confirme também que a sessão de serviço já saiu de `Active`, que a rota remota
foi instalada e que os clientes mantêm as rotas default.

### Sintoma: números de label mudaram

Isso é esperado para labels dinâmicos, como Adj-SIDs e Binding SIDs. Os
Prefix-SIDs `16001` e `16008` são derivados da configuração e não devem mudar
entre boots enquanto a SRGB e os índices permanecerem iguais. Refaça a folha
de correlação da mesma execução.

Não altere configs para forçar números observados apenas para coincidir com o
texto.

### Sintoma: `24005` aparece em dois lugares

Classifique cada ocorrência:

```text
roteador local
owner/FEC
entrada ou saída
vizinho que o anunciou
```

No lab, o BSID 24005 no PE e o label EPE 24005 no ASBR não são o mesmo objeto.

### Sintoma: TI-LFA aparece como Local-LFA

É o resultado esperado deste grafo. Confirme que:

- o primário está marcado `protected`;
- o alternativo está marcado `backup`;
- o próximo salto alternativo evita o recurso protegido.

Não exija uma repair list de vários SIDs em uma topologia que não precisa dela.

### Sintoma: policy está up, mas o prefixo não usa a policy

Confira as três condições de steering:

```text
rota BGP presente?
color anexada e autorizada?
next hop da rota igual ao endpoint da policy?
```

No estado capturado, a primeira condição falha para `203.0.113.0/24`.

### Sintoma: estágio 4 rejeita `COLOR_100`

O snapshot gerado referencia a policy antes de sua definição, como explicado na
seção 15. Isso é diferente da limitação de data plane. Primeiro resolva/registre
o erro de configuração; depois avalie o estado da sessão.

---

## 19. Experimentos úteis

Faça os ensaios em uma cópia do lab e registre o estado antes/depois.

### 19.1 Provar PHP

Objetivo:

```text
mostrar 16004 no primeiro enlace e L-POP no enlace seguinte
```

Procedimento em plataforma com data plane:

1. capture simultaneamente PE–P e P–ASBR;
2. gere tráfego para `10.0.0.8`;
3. confirme `{16004, L-POP}` na primeira captura;
4. confirme `{L-POP}` na segunda.

### 19.2 Provar a costura LU

Capture:

- BGP-LU nas três sessões;
- LFIB dos dois ASBRs;
- MPLS nos enlaces dos dois domínios.

Monte a cadeia:

```text
UPDATE label → Received Label → Outgoing Label → label no pcap seguinte
```

### 19.3 Observar churn de labels

1. capture a folha de correlação;
2. reinicie o lab de forma controlada;
3. espere estabilização completa;
4. preencha uma nova folha;
5. compare relações, não números.

O esperado é que a lógica permaneça e alguns labels dinâmicos mudem.

### 19.4 Falha do ramo primário

No `pe-pop-pb`, depois de registrar o estado:

```text
configure
interface GigabitEthernet0/0/0/1
 shutdown
commit
```

Observe:

```text
show route 10.0.0.4/32 detail
show cef 10.0.0.4/32 detail
```

Restaure:

```text
configure
interface GigabitEthernet0/0/0/1
 no shutdown
commit
```

Na imagem CP, isso prova mudança de controle, não perda/convergência de pacotes.

### 19.5 Comparar SPF e SR Policy

Estado comum:

```text
AS 65001 via p-pop-a
AS 1916 via p-ipe-rn
```

Policy:

```text
AS 65001 via p-pop-b
AS 1916 via p-ipe-ba
fronteira selecionada pelo PeerNode SID
```

Confirme primeiro a lista e depois, em data plane compatível, o caminho efetivo.

### 19.6 Demonstrar que o P não precisa de BGP

No P:

```text
show bgp ipv4 labeled-unicast 10.0.0.8/32
show mpls forwarding labels 16004 detail
```

O primeiro pode não ter a rota; o segundo contém a instrução necessária para
transportar o pacote até o ASBR.

### 19.7 Validar o filtro negativo

Em cada nó BGP-LU:

```text
show bgp ipv4 labeled-unicast 198.51.100.0/24
show bgp ipv4 labeled-unicast 203.0.113.0/24
```

Ambas devem estar ausentes. Uma rota de cliente na LU seria falha de separação,
mesmo que o forwarding parecesse funcionar.

---

## 20. Checklist final e referências

### Checklist de compreensão

Você entendeu a mecânica quando consegue responder sem olhar os números antigos:

- Quem escolhe o label que aparece como `Received Label` no PE?
- Em qual roteador esse label será uma chave de entrada da LFIB?
- Por que o PE precisa de 16004 além do label LU?
- Qual label fica no topo após o PHP em `p-pop-a`?
- Por que o ASBR aloca outro binding quando usa `next-hop-self`?
- Por que 24005 pode aparecer como BSID no PE e label EPE no ASBR sem conflito?
- Quem entende 15100?
- Por que 16007 só pode ficar ativo depois de atravessar o peer?
- O que `Operational: up` da policy não prova?
- Por que Local-LFA não contradiz TI-LFA?

### Respostas resumidas

1. O vizinho BGP downstream escolhe/anuncia o binding que quer receber.
2. No próprio vizinho que o anunciou.
3. Para tunelar o pacote até o next hop BGP que entende o label LU.
4. O label LU `L-POP`.
5. Porque o novo next hop precisa anunciar um label vinculado a si e programar
   a continuidade para o binding antigo.
6. São contextos locais/direções diferentes.
7. Apenas o `asbr-pop-pb` no sentido configurado.
8. Porque sua semântica pertence ao AS 1916.
9. Isoladamente, não prova rota dirigida, pacote encaminhado ou tráfego no
   caminho; por isso a validação também correlaciona BGP e traceroute.
10. O losango possui um LFA local suficiente; TI-LFA não precisa criar uma lista
    maior.

### Arquivos do próprio lab

- [Roteiro do lab, com a progressão por estágios](bgp-lu.md)
- [Conceitos de Inter-AS](index.md)
- [Recorte da Rede Ipê](recorte-rede-ipe.md)
- [Validação](validacao.md)
- [Base SR-MPLS no IOS-XR](../02-base-sr-mpls.md)
- [Configuração final do PE local](https://github.com/rnpbr/LabRedes-segmentrouting/blob/main/labs/cisco/sr-mpls/inter-as/bgp-lu/configs/pe-pop-pb.cfg)
- [Configuração final do ASBR local](https://github.com/rnpbr/LabRedes-segmentrouting/blob/main/labs/cisco/sr-mpls/inter-as/bgp-lu/configs/asbr-pop-pb.cfg)
- [Configuração final do ASBR remoto](https://github.com/rnpbr/LabRedes-segmentrouting/blob/main/labs/cisco/sr-mpls/inter-as/bgp-lu/configs/asbr-ipe-pb.cfg)
- [Configuração final do PE remoto](https://github.com/rnpbr/LabRedes-segmentrouting/blob/main/labs/cisco/sr-mpls/inter-as/bgp-lu/configs/pe-ipe-ce.cfg)

### Referências primárias

- [RFC 3032 — MPLS Label Stack Encoding](https://www.rfc-editor.org/rfc/rfc3032.html)
- [RFC 8277 — Using BGP to Bind MPLS Labels to Address Prefixes](https://www.rfc-editor.org/rfc/rfc8277.html)
- [RFC 8660 — Segment Routing with the MPLS Data Plane](https://www.rfc-editor.org/rfc/rfc8660.html)
- [RFC 8665 — OSPF Extensions for Segment Routing](https://www.rfc-editor.org/rfc/rfc8665.html)
- [RFC 9087 — Segment Routing Centralized BGP Egress Peer Engineering](https://www.rfc-editor.org/rfc/rfc9087.html)
- [RFC 9256 — Segment Routing Policy Architecture](https://www.rfc-editor.org/rfc/rfc9256.html)
- [RFC 9855 — Topology Independent Fast Reroute Using Segment Routing](https://www.rfc-editor.org/rfc/rfc9855.html)
- [Referências comentadas](index.md#referencias)

### A frase para guardar

!!! note "Observação"
    SR leva o pacote até quem entende o binding BGP; BGP-LU troca esse binding em
    cada fronteira de next hop; a LFIB executa uma instrução por vez, sempre pelo
    label que chegou ao topo.
