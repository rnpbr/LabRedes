# Validação do lab flex-algo-anycast

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/multidominio/flex-algo-anycast">`labs/cisco/sr-mpls/multidominio/flex-algo-anycast`</a>.

!!! info "Sobre este documento"
    Documento de apoio ao [lab `flex-algo-anycast`](flex-algo-anycast.md): o que as
    execuções de referência efetivamente confirmaram, e o que elas não autorizam
    concluir.

## Três níveis independentes

1. **estático:** coerência entre topologia, configs e documentação;
2. **plano de controle:** estado observado no IOS XR;
3. **data plane:** encaminhamento de pacotes.

Uma verificação em um nível não é promovida automaticamente ao seguinte.

## Ambiente das execuções de referência

| Item | Valor |
|---|---|
| Data | 21 de outubro de 2026 |
| Host | Linux 6.12 (Debian 13), 12 CPUs, 125 GiB RAM |
| Docker | 28.5.1 |
| Containerlab | 0.79.0 |
| Imagem | XRd Control Plane 7.10.2 (`ios-xr/xrd-control-plane:7.10.2`) |
| Roteadores | 10 XRd Control Plane |

Foram três execuções:

1. **Lab original**, ainda no layout anterior à reorganização do repositório
   (`flex-algo-anycast.clab.yml`, gerência dinâmica em `172.20.20.0/24`, sem
   bloco base). Todos os comandos do roteiro original foram executados.
2. **Formato atual sem a ACL de gerência.** Revelou a tempestade descrita
   abaixo.
3. **Formato atual, arquivos deste diretório.** Destroy, deploy limpo e todos os
   comandos do roteiro, na ordem, com o pior caso da ponte de gerência forçado
   antes do estágio 3 e de cada ensaio. É a execução que vale para os arquivos
   versionados.

## Conferência estática

Verificado por script, antes do deploy:

- 17 enlaces e 10 nós no `.clab.yml`;
- os 17 enlaces da tabela do roteiro batem com o `.clab.yml` e com os `.cfg`:
  interfaces, prefixo `/31`, processo OSPF do domínio, custo e afinidade;
- custo, afinidade `red` e processo OSPF **iguais nos dois lados** de cada
  enlace;
- as 14 linhas da tabela de SIDs batem com os `.cfg`: interface, prefixo,
  router-id, processo e índices dos algoritmos 0 e 128; label = `16000 + índice`;
- endereços de gerência do roteiro iguais aos do `.clab.yml`;
- todo link relativo e âncora dos markdowns do repositório resolve, e toda
  imagem citada existe em `images/`.

## Plano de controle e data plane

| Verificação | Estado |
|---|---|
| Deploy dos 10 contêineres | aprovado; policy `up` 180 s após o fim do deploy |
| `show configuration failed startup` | aprovado, nenhuma linha rejeitada nos 10 nós |
| Adjacências OSPF nos três processos | aprovado, contagens do roteiro |
| Isolamento entre domínios | aprovado, sem rota default e sem vazamento |
| Divergência SPF default × Algo 128 | aprovado nos três domínios |
| Anycast AB e BC, contribuidores e LFIB | aprovado |
| N-flag desligada no anycast | aprovado, Extended Prefix `Flags : 0x0` |
| Afinidade `red` sinalizada | aprovado, admin group `0x00000400` |
| SR Policy color 128 | aprovado, `Operational: up`, lista `(valid)` |
| Ping e traceroute com origem na gerência | aprovado, 100% e cinco saltos |
| `ping mpls` e `traceroute sr-mpls` | aprovado |
| Ensaio 1, falha benigna | aprovado, troca para `dbr-ab2` em um dead interval |
| Ensaio 2, risco do anycast | aprovado, buraco negro com policy `up` |
| Restauração dos dois ensaios | aprovado em 40 s |
| Ponte de gerência no pior caso | aprovado com a ACL; reprovado sem ela |

### Resultados observados

- `pe1` não tinha `0.0.0.0/0` nem prefixos fora do OSPF 100; `show route
  summary` listou 8 rotas OSPF 100, 1 estática e as conectadas.
- Para `10.1.255.12/32` (`dbr-ab2`), o SPF default saiu por `10.1.0.3`
  (`p2`, enlace `red`), métrica 16; o Algo 128 saiu por `10.1.0.1` (`p1`),
  métrica 31, label `17112`.
- Para o anycast AB, o SPF default escolheu `dbr-ab2` via `p2`, métrica 16; o
  Algo 128 escolheu `dbr-ab1` via `p1`, métrica 21, com `dbr-ab2` como segundo
  contribuidor, métrica 31.
- Em `dbr-ab1`, o anycast BC pelo SPF default foi `dbr-bc2` pelo enlace `red`,
  métrica 6; pelo Algo 128, `dbr-bc1`, métrica 21, saída `Pop`. `dbr-bc2`
  apareceu com métrica 41.
- Em `dbr-bc1`, `pe9` pelo SPF default foi via `dbr-bc2` (`10.3.0.11`),
  métrica 16; pelo Algo 128, via `p3`, métrica 21, saída `17309`.
- Em `dbr-ab1`, o Extended Prefix TLV de `10.1.255.11/32` trouxe
  `Flags : 0x40` e o de `10.255.12.12/32`, `Flags : 0x0`. Os flags dos SID
  sub-TLVs foram `0x0` em ambos.
- A policy ficou com Binding SID dinâmico `24003`; o valor muda entre execuções
  e não deve ser fixado na documentação.
- O traceroute IP e o `traceroute sr-mpls` mostraram exatamente as saídas do
  roteiro: `p1`, `dbr-ab1`, `dbr-bc1`, `p3`, `pe9`, com PHP em `p1`, `dbr-ab1`
  e `p3`.
- No ensaio 1, 5 s depois do `shutdown`, `p1` ainda mantinha `dbr-ab1` em
  `FULL` e com a interface `up/up`; `pe1` seguia usando `dbr-ab1` e o
  traceroute respondia em `p1` e parava no segundo salto. Em 45 s, `dbr-ab2` passou a `Inuse`,
  métrica 31, e o traceroute chegou a `pe9` em sete saltos, via `p1`, `p2`,
  `dbr-ab2`, `dbr-bc2`, `p4` e `p3`.
- Na execução 1, o mesmo estado de falha mostrou o traceroute IP passando por
  `dbr-bc1` e o SR-MPLS por `p4`: os dois caminhos Algo 128 de `dbr-bc2` até
  `pe9` custam 25.
- No ensaio 2, `dbr-ab1` manteve `p1` em `FULL`, ficou sem vizinhos OSPF 200 e
  sem entrada para `17230` (`Flags: NoContr, NoLbl, NoSID`); `pe1` continuou
  com `dbr-ab1` como contribuidor de `17120`; a policy seguiu
  `Operational: up` e `(valid)`; o traceroute parou em
  `N 2 10.1.0.7 MRU 0 [No Label]` e o ping caiu a 0%.
- Sem `mpls oam`, `ping mpls` e `traceroute sr-mpls` respondem
  `% MPLS Embedded Management Subsystem is not running.`

## Tempestade na rede de gerência

A execução 2 encontrou um defeito que o roteiro original não tratava.

Sintoma: alguns minutos depois das primeiras provas com origem
`172.20.27.11`, os dez nós passaram de cerca de 15% para mais de 100% de CPU,
a carga do host foi a 28 em 12 CPUs, as adjacências OSPF de `pe1` foram
refeitas, a policy oscilou entre `DOWN` e `UP` e os traceroutes pararam de
responder.

Causa, confirmada por captura na ponte de gerência:

1. `pe1` não transmite pela gerência - suas requisições saem pela policy.
   300 s depois do último quadro de `pe1`, a ponte apaga o MAC dele da tabela
   de encaminhamento.
2. A partir daí, cada resposta destinada a `172.20.27.11` é inundada para
   todas as portas da ponte.
3. O XRd mantém a interface de gerência em modo promíscuo e roteia quadros
   endereçados a outros MACs. Cada um dos outros nove nós reencaminha a cópia
   recebida para `pe1`, que é inundada de novo.
4. Com fan-out de nove a cada passagem, o TTL não extingue o tráfego: a
   captura mostrou um único MPLS Echo Reply de `10.1.0.1` para `172.20.27.11`
   circulando a cerca de 225 mil pacotes por segundo em cada nó.

Reprodução determinística: remover o MAC de `pe1` da ponte com
`bridge fdb del` e executar um único `traceroute sr-mpls` com origem na
gerência. Qualquer quadro transmitido por `pe1` na gerência - um `ping` para
o gateway, por exemplo - devolve o MAC à tabela e encerra a tempestade.

Duas correções foram testadas:

- **ACL de saída na `MgmtEth`:** não teve efeito; a tempestade continuou.
- **ACL de entrada `MGMT-NO-TRANSIT`:** aceita o endereço do próprio nó,
  descarta o resto de `172.20.27.0/24` e libera o restante. A tempestade
  parou imediatamente, com o MAC de `pe1` ainda fora da ponte, e todas as
  provas do roteiro passaram em duas rodadas seguidas no pior caso. SSH e ping
  do host para os nós continuaram funcionando.

A ACL de entrada está nos `.cfg` atuais. Na execução 3, o pior caso foi forçado
três vezes e o contador da linha `deny` registrou as cópias descartadas, sem
nenhum tráfego residual na gerência ao fim.

A execução 1 não manifestou o problema porque suas provas couberam na janela
de 300 s após o último ARP de `pe1`. O defeito estava presente no lab original.

## Correções no roteiro original

A execução 1 confirmou o comportamento do lab, mas o roteiro original tinha
imprecisões, todas corrigidas no [`README.md`](flex-algo-anycast.md) atual:

| Roteiro original | Observado |
|---|---|
| Endereço de gerência de `pe1` fixo em `172.20.20.11` | Atribuído dinamicamente; na execução foi `172.20.20.8`. Agora fixado no `.clab.yml` |
| `n-flag-clear` aparece como "SID flags `0x0`" | A N-flag está no Extended Prefix TLV (`0x0` contra `0x40` de uma loopback de nó); os flags do SID sub-TLV são `0x0` nos dois casos |
| Filtro `\| begin 10.255.12.12` | Começa na linha do prefixo e esconde a linha de flags do Extended Prefix TLV |
| Algo 128 em `dbr-ab1` "usando label `17230`" | Saída `Pop`: `dbr-bc1` é o próprio anunciante, há PHP |
| Referências a `base.md` e `MANUAL_ROUTER_CONFIGS.md` | Nenhum dos dois existe; a base agora é [`00-base`](../02-base-sr-mpls.md) |
| Diagrama ASCII | Não mostrava os enlaces `dbr-ab1`-`dbr-ab2`, os dois `dbr-bc1`-`dbr-bc2`, nem qual diagonal é `red` |
| Ensaio benigno | Não mencionava a janela de perda até o dead interval nem o ECMP no domínio C |
| Ensaio maligno | Não registrava que a policy segue `up` nem que o ping cai a 0% |
| Ping com origem na gerência | Funcionava, mas sem proteção contra a tempestade descrita acima |

## O que estas execuções não autorizam concluir

- **Tempo de convergência.** Os ensaios usaram esperas fixas de 40-45 s, sem
  BFD nem medição de perda. Provam o estado final, não a duração da
  transição.
- **Comportamento de outra plataforma.** PHP, validação de segment list e a
  aceitação de quadros com outro MAC na gerência foram observados no XRd
  Control Plane 7.10.2.
- **Que a ACL protege qualquer uso da gerência.** Ela foi validada para o
  padrão deste lab: endereço de gerência de um nó usado como origem de
  tráfego do lab.
