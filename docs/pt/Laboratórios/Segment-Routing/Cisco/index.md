# Cisco IOS-XR

## :material-bookmark: **Introdução**

Implementações de Segment Routing executadas em **Containerlab** com **Cisco XRd** (`ios-xr/xrd-control-plane:7.10.2`). Os cenários usam a temática da **Rede Ipê** e cada um é autocontido: topologia, configurações completas dos nós e roteiro de verificação.

Antes de começar, leia os [fundamentos de SR-MPLS](../index.md#fundamentos-de-sr-mpls).

!!! info "Repositório"
    Todos os laboratórios desta página vêm do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**, no diretório `labs/cisco/`.

---

## :material-tools: **Preparação**

1. Instale Docker, Containerlab e a imagem XRd conforme a [preparação do ambiente](01-preparacao-do-ambiente.md).
2. Consulte a [base SR-MPLS no IOS-XR](02-base-sr-mpls.md): convenções de SRGB, endereçamento e configuração mínima reusadas em todos os labs.

!!! info "Recursos"
    Os labs usam de quatro a dez roteadores, com consumo aproximado de 1,5 a 2,2 GB de RAM por nó XRd. O `bgp-lu` pede cerca de 12 GB de RAM e oito CPUs; o `flex-algo-anycast` é o maior, com cerca de 22 GB de RAM medidos.

---

## :material-flask: **Laboratórios**

### TI-LFA

Leia primeiro os [conceitos de TI-LFA](TI‑LFA/index.md). Os labs formam uma sequência e cada um assume o anterior.

| Lab | O que mostra | Nós |
|---|---|---:|
| [zero-segment](TI‑LFA/00-zero-segment.md) | PQ-node vizinho direto do PLR, nenhum label extra | 4 |
| [single-segment](TI‑LFA/01-single-segment.md) | PQ-node no P-space estendido, um label extra | 6 |
| [double-segment](TI‑LFA/02-double-segment.md) | P-space e Q-space disjuntos, Adj-SID como ponte | 6 |

### SR-TE

Conceitos: [SR-TE e SR Policy](SR‑TE/index.md).

| Lab | O que mostra | Nós |
|---|---|---:|
| [explicit-policy](SR‑TE/explicit-policy.md) | Segment list estática forçando um caminho de menor latência | 5 |

### Inter-AS

Conceitos: [transporte Inter-AS](Inter‑AS/index.md).

| Lab | O que mostra | Nós |
|---|---|---:|
| [bgp-lu](Inter‑AS/bgp-lu.md) | BGP-LU entre domínios SR, recursão de next hop, TI-LFA e EPE | 8 + 2 |

Os dois nós adicionais do `bgp-lu` são clientes Alpine. Material de apoio do lab: [guia aprofundado](Inter‑AS/guia-aprofundado.md), [recorte da Rede Ipê](Inter‑AS/recorte-rede-ipe.md) e [validação](Inter‑AS/validacao.md).

### Multidomínio

Conceitos: [multidomínio, Flex-Algo e SID anycast](Multidomínio/index.md).

| Lab | O que mostra | Nós |
|---|---|---:|
| [flex-algo-anycast](Multidomínio/flex-algo-anycast.md) | Três domínios OSPF sem redistribuição, Flex-Algo 128 e SIDs anycast de borda numa SR Policy explícita, e o buraco negro do anycast | 10 |

Material de apoio: [validação](Multidomínio/validacao.md).

### Referência

- [Lab Cisco XRd SR-MPLS de 5 nós](03-referencia-lab-5-nos.md): material de origem, traduzido para o português e preservado como referência histórica.

---

## :material-laptop: **Executar um cenário**

Cada lab do repositório contém todos os arquivos necessários:

```text
<lab>/
├── README.md
├── lab.clab.yml
├── configs/
└── images/
```

Exemplo:

```bash
git clone https://github.com/rnpbr/LabRedes-segmentrouting.git
cd LabRedes-segmentrouting/labs/cisco/sr-mpls/ti-lfa/00-zero-segment
sudo clab deploy -t lab.clab.yml
```

Para encerrar:

```bash
sudo clab destroy -t lab.clab.yml --cleanup
```

O [roadmap](../index.md#roadmap) apresenta os cenários concluídos e planejados.
