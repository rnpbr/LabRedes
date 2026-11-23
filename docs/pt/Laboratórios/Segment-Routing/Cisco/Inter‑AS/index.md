# Inter-AS - transporte SR-MPLS entre domínios

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/inter-as">`labs/cisco/sr-mpls/inter-as`</a>.

!!! info "Pré-requisitos"
    [fundamentos de SR-MPLS](../../index.md).

## :material-bookmark: **O problema**

Segment Routing não elimina MPLS nem BGP. Ele muda **onde** o estado de caminho é
mantido e **como** as instruções de encaminhamento são expressas. Dentro de um
domínio isso é resolvido pelo IGP: o OSPF anuncia o Prefix-SID, todo nó calcula
o SPF e a LFIB fica programada sem protocolo de distribuição de label.

Fora do domínio, não. Dois ASes não trocam LSAs. O Prefix-SID de um PE do AS
1916 simplesmente não existe na base de dados OSPF do AS 65001, e nenhum nó do
lado de cá sabe construir um LSP até ele.

BGP labeled-unicast é a costura. Ele associa um prefixo a um label e o carrega
entre domínios que não compartilham IGP - estendendo o alcance MPLS sem criar
uma adjacência IGP interdomínio e sem LDP ou RSVP-TE.

## Planos separados

| Plano | Protocolos/objetos | Função |
|---|---|---|
| Descoberta intradomínio | OSPFv2 área 0 | topologia e melhor caminho |
| Transporte intradomínio | Prefix-SIDs OSPF + LFIB | LSP SR-MPLS até o ASBR/PE |
| Transporte interdomínio | iBGP/eBGP IPv4 labeled-unicast | label para a loopback remota |
| Proteção local | TI-LFA | repair path pré-instalado |
| Engenharia explícita | SR Policy + PeerNode SID | caminho alternativo e peer de saída |
| Serviço | sessão PE-PE (VPNv4, ou IPv4 unicast no lab) | troca dos prefixos de cliente |

Essa separação importa na hora de ler as saídas. Adjacência OSPF `FULL` não prova
label forwarding. Rota BGP-LU válida não prova que uma sessão de serviço multihop
atravessa uma imagem control-plane-only. SR Policy operacional não prova que
houve tráfego. Cada camada tem sua própria evidência.

## BGP-LU, RFC 8277

O BGP anuncia o prefixo com um label MPLS anexado à NLRI (SAFI 4). Para
encaminhar por essa rota, o nó impõe o label recebido **e** cria um túnel até o
next hop do anúncio. As duas coisas são necessárias - é aí que nasce a recursão.

A implementação precisa alocar um label local para os prefixos que origina ou
repassa nessa família. Sem isso, não há label a anunciar.

Alocação e encaminhamento não são a mesma prova. Se o ASBR aprende o mesmo
`/32` por iBGP-LU e por um IGP com SR, o IGP pode ser o dono da rota global e
do Prefix-SID instalado enquanto o BGP aloca outro binding apenas para seu
próprio caminho. Um label presente no UPDATE, mas ausente da LFIB do ASBR que o
anunciou, cria um buraco negro.

Uma forma explícita de costurar os planos é importar no BGP somente as
loopbacks locais já rotuladas pelo IGP. A policy de redistribuição deve ser
restrita aos `/32` autorizados e pode exigir `route-has-label`. Assim, o ASBR
anuncia por BGP-LU um Prefix-SID que já possui ação válida na LFIB, sem mudar a
preferência administrativa entre OSPF e iBGP.

## Recursão de transporte

O ponto que mais se perde de vista: **uma rota BGP-LU não é encaminhável
sozinha.** Ela traz um label e um next hop, mas esse next hop tipicamente é uma
loopback remota, não um vizinho diretamente conectado. Ele precisa ser resolvido
pelo transporte do domínio local.

```text
BGP-LU  →  prefixo remoto + label + next hop (loopback do ASBR local)
                                        ↓ recursa
OSPF/SR →  Node-SID do ASBR local
                                        ↓
CEF     →  impõe a pilha { Node-SID , label BGP }
```

O label de baixo sobrevive a todo o domínio local; o de cima é consumido salto a
salto pelo SPF e some no penúltimo (PHP). Quando o pacote chega ao ASBR, só resta
o label BGP - e é ele que a fronteira troca.

O label global identifica a instrução; a LFIB de cada nó decide a operação local
(`push`, `swap`, `pop`). PHP pode fazer um label desaparecer um salto antes do
nó-alvo, e isso **não** significa que o segmento deixou de ser cumprido.

### `next-hop-self` não é detalhe de estilo

Na direção ASBR → PE, o ASBR precisa reescrever o next hop para a própria
loopback. Se não reescrever, o PE recebe como next hop um endereço da fronteira
inter-AS, que não está no seu IGP. A rota LU chega, é aceita, aparece na tabela -
e nunca resolve. É a falha mais comum e a mais silenciosa deste desenho.

### Labels dinâmicos

Labels da faixa dinâmica não devem ser fixados em documentação. Correlacione as
saídas **da mesma execução**: BGP contra CEF contra LFIB. Igualdade numérica
entre labels de contextos diferentes nunca deve ser inferida pelo valor - quem
define a semântica de um label é o roteador que o recebe.

Um label da SRGB reaproveitado no anúncio BGP-LU não é dinâmico só porque foi
transportado pelo BGP. Se `16008` é o Prefix-SID derivado de SRGB mais índice e
o ASBR importa essa rota OSPF/SR, a presença de `16008` na NLRI representa a
continuidade deliberada desse binding.

## "Option C": formulação precisa

Na literatura de L3VPN inter-AS, a Opção C inclui três coisas:

- troca de reachability rotulada entre ASBRs;
- sessão de serviço entre PEs, normalmente MP-BGP VPNv4/vpnv6;
- ASBRs que não precisam manter as rotas VPN dos clientes.

Um lab que faz só a primeira e a terceira implementa o **substrato de transporte
inspirado na Opção C**, não uma L3VPN Option C. Sem AF VPNv4/vpnv6, VRF, RD, RT
ou label VPN, o termo não deve ser usado como sinônimo genérico de "BGP-LU
inter-AS". A ressalva é o que mantém a expressão útil.

O que separa as duas camadas é um filtro: um prefix-set que admite nas sessões
labeled-unicast apenas as loopbacks dos PEs. Redes de cliente nunca recebem
label. Mesmo em ambiente fechado, separar os filtros evita que um prefixo de
cliente escape acidentalmente pelo LU.

## BGP-EPE e PeerNode SID

Egress Peer Engineering (RFC 9087) dá ao ASBR de saída um SID por peer BGP. O
PeerNode SID significa **"encaminhe ao peer BGP X"** - não "alcance o Node-SID
IGP de X". O peer pode estar inteiramente fora do IGP; o label é uma instrução
local do ASBR de saída, alocada da SRLB.

Isso é o que permite uma segment list atravessar uma fronteira administrativa:
um Node-SID entrega o pacote ao ASBR, o PeerNode SID o joga para o outro lado, e
os SIDs seguintes já são interpretados pelo IGP do domínio remoto. A lista é
válida porque cada label só precisa ser compreendido pelo nó em que ele se torna
o topo da pilha.

Configurar EPE localmente não é a solução centralizada completa da RFC 9087:
essa envolve controlador, exportação BGP-LS da topologia de peering (RFC 9086) e
programação remota da policy. O objeto de data plane, porém, é o mesmo - o BGP
Peering SID.

## TI-LFA em topologias simples

TI-LFA calcula, no Point of Local Repair, uma lista de reparo que evita o recurso
protegido e segue um caminho pós-convergência. Em um grafo simples - um losango,
por exemplo - o vizinho do outro ramo já satisfaz a condição de LFA clássico, e
a implementação pode reportar o repair path como `Local-LFA` mesmo com TI-LFA
habilitado. Não há contradição: o caso simples não precisa de uma pilha remota.

Habilitar TI-LFA prova a **instalação do reparo no CEF**, não um SLA de 50 ms.
Tempo de detecção, BFD, programação de hardware e carga determinam a perda real.
Para ver uma repair list com múltiplos segmentos é preciso uma topologia em que
nenhum LFA local atenda — ver os [conceitos de TI-LFA](../TI‑LFA/index.md).

## :material-alert: **Antes de transportar o desenho**

Isto é material de laboratório, não um baseline de produção:

- substitua `route-policy PASS` por políticas de import/export explícitas;
- valide AS paths, comunidades, limites de prefixo e origem;
- autentique sessões e o acesso de gestão; não reutilize as credenciais do lab;
- valide TTL security ou multihop, CoPP e limites de prefixos;
- modele SRLGs e proteção de nó quando o requisito exceder proteção de enlace;
- verifique MSD, MTU e comportamento de PHP/explicit-null - uma policy aceita
  em ambiente virtual não prova que um ASIC alvo imponha a mesma profundidade
  de pilha;
- use telemetria e OAM MPLS compatíveis com a plataforma;
- ensaie falhas em ambiente representativo antes de qualquer mudança real.

## :material-book-alphabet: **Glossário**

**BGP-LU.** BGP labeled-unicast, SAFI 4. Prefixo IPv4/IPv6 com label MPLS
anexado à NLRI. RFC 8277.

**PeerNode SID.** SID de EPE que identifica um peer BGP específico do ASBR de
saída. Local ao ASBR, alocado da SRLB.

**Recursão de transporte.** Resolução do next hop de uma rota BGP-LU pela rota
SR do domínio local, resultando numa pilha de labels.

**Seamless MPLS.** Arquitetura que usa BGP-LU para estender um LSP fim a fim
através de múltiplos domínios IGP, sem LDP interdomínio.

Termos gerais de SR — Prefix-SID, Node-SID, Adj-SID, SRGB, SRLB e segment list —
estão nos [fundamentos de SR-MPLS](../../index.md).

## :material-file-document-multiple: **Laboratórios desta trilha**

| Página | Para que serve |
|---|---|
| [bgp-lu](bgp-lu.md) | BGP-LU entre domínios SR, recursão de next hop, TI-LFA e EPE (8 roteadores + 2 clientes) |
| [guia-aprofundado](guia-aprofundado.md) | Da configuração ao fio: RIB/LIB/LFIB/CEF e pilhas salto a salto |
| [recorte-rede-ipe](recorte-rede-ipe.md) | Evidência do mapa, método de seleção e limites da analogia |
| [validacao](validacao.md) | O que a execução de referência confirmou, e o que não |

## :material-book-open-variant: **Referências**

### Segment Routing e MPLS

- RFC 8402 - *Segment Routing Architecture*: <https://www.rfc-editor.org/rfc/rfc8402.html>
- RFC 8660 - *Segment Routing with the MPLS Data Plane*: <https://www.rfc-editor.org/rfc/rfc8660.html>
- RFC 8665 - *OSPF Extensions for Segment Routing*: <https://www.rfc-editor.org/rfc/rfc8665.html>
- RFC 9256 - *Segment Routing Policy Architecture*: <https://www.rfc-editor.org/rfc/rfc9256.html>
- RFC 3031 - *Multiprotocol Label Switching Architecture*: <https://www.rfc-editor.org/rfc/rfc3031.html>
- RFC 3032 - *MPLS Label Stack Encoding*: <https://www.rfc-editor.org/rfc/rfc3032.html>

### BGP labeled-unicast, inter-AS e EPE

- RFC 8277 - *Using BGP to Bind MPLS Labels to Address Prefixes*: <https://www.rfc-editor.org/rfc/rfc8277.html>
- RFC 4364 - *BGP/MPLS IP Virtual Private Networks*: <https://www.rfc-editor.org/rfc/rfc4364.html>.
  A seção 10 dá o contexto das opções inter-AS; o lab desta categoria não
  configura a camada VPN descrita na RFC.
- RFC 9087 - *Segment Routing Centralized BGP Egress Peer Engineering*: <https://www.rfc-editor.org/rfc/rfc9087.html>
- RFC 9086 - *BGP-LS Extensions for SR BGP EPE*: <https://www.rfc-editor.org/rfc/rfc9086.html>

### Fast reroute

- RFC 9855 - *Topology Independent Fast Reroute Using Segment Routing*: <https://www.rfc-editor.org/rfc/rfc9855.html>

### Endereçamento de documentação

- RFC 5737 - *IPv4 Address Blocks Reserved for Documentation*: <https://www.rfc-editor.org/rfc/rfc5737.html>
- RFC 3021 - *Using 31-Bit Prefixes on IPv4 Point-to-Point Links*: <https://www.rfc-editor.org/rfc/rfc3021.html>
- RFC 6996 - *Autonomous System (AS) Reservation for Private Use*: <https://www.rfc-editor.org/rfc/rfc6996.html>

### Leitura crítica

As RFCs definem arquitetura e comportamento interoperável. A documentação Cisco
define a superfície de configuração de uma família/versão de IOS XR. As saídas
capturadas em uma execução definem o que aquela imagem efetivamente realizou.
Nenhuma das três deve ser usada isoladamente para deduzir o comportamento de
outra plataforma.
