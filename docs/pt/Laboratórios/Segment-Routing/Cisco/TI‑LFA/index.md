# TI-LFA — conceitos

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/ti-lfa">`labs/cisco/sr-mpls/ti-lfa`</a>.

!!! info "Pré-requisitos"
    [fundamentos de SR-MPLS](../../index.md).

## :material-bookmark: **O que é**

TI-LFA é o fast reroute do Segment Routing, padronizado na RFC 9855.

Quando um link ou nó cai, o roteador do lado da falha (o PLR, Point of Local Repair) já tem um caminho de backup pronto na FIB. Ele comuta em menos de 50ms, sem esperar o IGP reconvergir.

Isso existe porque reconvergência não é instantânea. Cada roteador recalcula SPF no próprio tempo, e nessa janela o tráfego cai se não houver backup pronto.

## De LFA a TI-LFA

- **LFA** (RFC 5286): usa um vizinho como backup, desde que o caminho dele até o destino não volte pelo PLR. Simples, mas em muitas topologias nenhum vizinho serve.
- **Remote LFA** (RFC 7490): estende o LFA com um túnel LDP até um nó mais distante. Cobre mais casos, mas exige LDP.
- **TI-LFA** (RFC 9855): usa uma pilha de labels SR para alcançar o nó de reparo. Não precisa de LDP nem de o nó ser vizinho. Cobertura garantida em qualquer rede duplamente conectada.

O backup do TI-LFA é sempre o **caminho pós-convergência**, ou seja, o caminho que a rede vai usar depois de convergir. Isso evita ter que escolher entre vários backups possíveis na mão.

## P-space, Q-space e PQ-node

A pergunta central: como o PLR leva o tráfego até um nó que já sabe chegar ao destino sem cruzar a falha?

- **P-space**: nós que o PLR alcança pelo caminho mais curto sem usar o recurso que falhou.
- **P-space estendido**: o P-space do PLR mais o P-space de cada vizinho que sobrou. Serve para alcançar nós que estão a dois ou mais saltos.
- **Q-space**: nós que alcançam o destino pelo caminho mais curto sem usar o recurso que falhou.

Um nó que está nos dois conjuntos é um **PQ-node**. O PLR só precisa levar o tráfego até ele.

Quando existe mais de um PQ-node válido, a escolha fica a cargo da
implementação. Na prática, a seleção deve ser confirmada no estado de
encaminhamento da plataforma, não deduzida apenas pela topologia.

## Zero, single e double-segment

O nome do cenário vem de quantos labels o PLR empilha **além** do label do destino:

| Cenário | Situação | Labels extras | Pilha |
|---|---|:-:|---|
| Zero-segment | PQ-node é vizinho direto do PLR | 0 | `{dest}` |
| Single-segment | PQ-node está no P-space estendido | 1 | `{PQ, dest}` |
| Double-segment | P-space e Q-space não se cruzam | 2 | `{P-node, adj-SID, dest}` |

No double-segment, o Adj-SID força a passagem por um enlace específico, ignorando o custo IGP dele. É o que costura o P-space ao Q-space quando o caminho mais curto não faz essa ponte.

Casos com mais de dois segmentos existem, mas são raros. A RFC 9855 mediu redes reais: para proteção de link e de SRLG, 1 segmento cobre mais de 99% dos prefixos; para proteção de nó, 2 segmentos cobrem 99%. Por isso a trilha de labs para no double-segment.

## :material-file-document-multiple: **Laboratórios desta trilha**

Execute os labs nesta ordem. Cada um assume o anterior.

| Lab | O que mostra | Nós |
|---|---|---:|
| [zero-segment](00-zero-segment.md) | PQ-node vizinho direto do PLR, nenhum label extra | 4 |
| [single-segment](01-single-segment.md) | PQ-node no P-space estendido, um label extra | 6 |
| [double-segment](02-double-segment.md) | P-space e Q-space disjuntos, Adj-SID como ponte | 6 |

## :material-book-open-variant: **Referências**

- RFC 9855 - *Topology Independent Fast Reroute Using Segment Routing*: https://datatracker.ietf.org/doc/html/rfc9855
- RFC 5286 - *IP Fast Reroute: Loop-Free Alternates*: https://datatracker.ietf.org/doc/html/rfc5286
- RFC 7490 - *Remote Loop-Free Alternate (LFA) Fast Reroute*: https://datatracker.ietf.org/doc/html/rfc7490
- RFC 8402 - *Segment Routing Architecture*: https://datatracker.ietf.org/doc/html/rfc8402
