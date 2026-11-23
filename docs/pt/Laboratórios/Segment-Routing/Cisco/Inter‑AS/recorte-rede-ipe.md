# Recorte PoP-PB ↔ backbone Rede Ipê

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/inter-as/bgp-lu">`labs/cisco/sr-mpls/inter-as/bgp-lu`</a>.

!!! info "Sobre este documento"
    Documento de apoio ao [lab `bgp-lu`](bgp-lu.md): de onde veio a topologia,
    o que é evidência pública e o que é invenção didática.

## A abstração administrativa

O laboratório separa dois domínios:

![Topologia lógica: o PoP-PB em AS 65001, com ramo primário de custo 10 e alternativo de custo 20, ligado por eBGP labeled-unicast ao recorte PB-RN/BA-CE do backbone em AS 1916](images/bgp-lu/topology-bgp-lu.svg#only-light)
![Topologia lógica: o PoP-PB em AS 65001, com ramo primário de custo 10 e alternativo de custo 20, ligado por eBGP labeled-unicast ao recorte PB-RN/BA-CE do backbone em AS 1916](images/bgp-lu/topology-bgp-lu-escuro.svg#only-dark)

Essa fronteira é uma **abstração arquitetural**, não a afirmação de que exista
em produção uma sessão eBGP `AS65001 ↔ AS1916` com esses equipamentos. As fontes
públicas permitem sustentar que PoPs/redes regionais entregam conectividade ao
backbone, mas não publicam a topologia interna, os ASNs locais, os protocolos ou
o ponto exato de demarcação do PoP-PB.

A [Política de Uso da Rede Ipê](https://www.pop-mg.rnp.br/_media/conectividade/politica-uso-rede-ipe_0.pdf)
distingue o tráfego trocado entre redes regionais/PoPs e o backbone. Páginas
institucionais de PoPs descrevem o PoP como ponto de conexão de instituições ao
backbone, por exemplo o [PoP-GO](https://www.pop-go.rnp.br/). A página da
[Metro-CG/PoP-PB](https://pop-pb.rnp.br/metro-cg/) documenta uma rede
metropolitana atendida pelo PoP-PB. Essas evidências justificam a separação de
papéis; não justificam copiar uma arquitetura interna.

## O que vem do Panorama

No lado do backbone, o lab usa um único losango do
[Panorama de Tráfego da Rede Ipê](https://redeipe.rnp.br/panorama), consultado
em **29 de julho de 2026**:

```text
             RN
           /    \
      100G/      \100G
         PB      CE
       40G\      /100G
           \    /
             BA
```

| Enlace público | Capacidade exibida | Enlace lógico no AS 1916 | Custo OSPF do lab |
|---|---:|---|---:|
| PB-RN | 100G | `asbr-ipe-pb`-`p-ipe-rn` | 10 |
| RN-CE | 100G | `p-ipe-rn`-`pe-ipe-ce` | 10 |
| PB-BA | 40G | `asbr-ipe-pb`-`p-ipe-ba` | 20 |
| BA-CE | 100G | `p-ipe-ba`-`pe-ipe-ce` | 20 |

O ramo PB-RN-CE é primário apenas por decisão pedagógica: seu gargalo nominal é
100G, contra 40G no ramo via BA. Capacidade isolada não revela métrica IGP,
latência, utilização, política, SRLG ou preferência operacional da RNP.

O Panorama é uma página viva. Se os quatro enlaces ou suas capacidades mudarem,
a escolha de qual ramo é primário perde a justificativa registrada aqui - mas o
lab continua válido, porque o que ele demonstra não depende da capacidade
nominal. Ao revisar o lab, reconsulte a página e atualize a tabela acima junto
com a data.

## O que é assumido no PoP

O losango `pe-pop-pb`-`p-pop-a`/`p-pop-b`-`asbr-pop-pb` preserva a mesma
oportunidade de SPF, TI-LFA e engenharia explícita do lado público. Ele
representa redundância **interna ao domínio administrativo do PoP**, sem
associação com roteadores, fibras, cidades ou caminhos reais.

| Objeto do lab | Interpretação permitida |
|---|---|
| `instituicao-pb` | uma instituição usuária abstrata |
| `pe-pop-pb` | borda de serviço do domínio do PoP |
| `p-pop-a`, `p-pop-b` | dois caminhos internos abstratos |
| `asbr-pop-pb` | borda administrativa do PoP |
| `asbr-pop-pb`-`asbr-ipe-pb` | ponto lógico de entrega ao backbone |

O enlace entre os ASBRs não corresponde a uma aresta do Panorama. Ele foi
desenhado como demarcação de controle para o exercício inter-AS.

## ASNs e endereços

- `65001` é ASN privado (RFC 6996) e identifica somente o PoP didático.
- `1916` é o ASN público da RNP e identifica o papel do backbone no lab isolado.
- Usar `1916` não torna os roteadores, políticas ou sessões uma reprodução da
  Rede Ipê.
- `192.0.2.0/24`, `198.51.100.0/24` e `203.0.113.0/24` são blocos de
  documentação da RFC 5737.
- `10.0.0.0/24` é espaço privado usado apenas para loopbacks.

Nenhum endereço operacional da RNP é reproduzido.

## Limites da analogia

| Elemento | Evidência pública | Somente no laboratório |
|---|---|---|
| existência dos PoPs PB, RN, BA e CE | Panorama | um contêiner XRd por vértice |
| quatro enlaces e capacidades | Panorama | custos OSPF 10/20 |
| papel de entrega PoP/rede regional ↔ backbone | páginas institucionais | fronteira eBGP e seus ASBRs |
| AS 1916 da RNP | documentação pública | IGP, SR-MPLS, TI-LFA, LU e EPE |
| redes metropolitanas ligadas a PoPs | página Metro-CG | `instituicao-pb` e sua sub-rede |

O recorte não é inventário, diagrama físico, desenho de produção nem recomendação
de implantação. Não modela outros enlaces dos PoPs, fabricante, interfaces,
SRLG, PTTs, conexões internacionais, telemetria ou políticas reais. As
capacidades são anotações narrativas e **não** configuram shaping no
Containerlab.

## Referências

- RNP, [Panorama de Tráfego da Rede Ipê](https://redeipe.rnp.br/panorama).
- RNP, [Portal Rede Ipê](https://redeipe.rnp.br/).
- RNP, [Rede Ipê: Política de Uso](https://www.pop-mg.rnp.br/_media/conectividade/politica-uso-rede-ipe_0.pdf).
- PoP-PB/RNP, [Projeto Metro-CG](https://pop-pb.rnp.br/metro-cg/).
- PoP-GO/RNP, [Ponto de conexão ao backbone](https://www.pop-go.rnp.br/).
- RNP, documento público que descreve a Rede Ipê como
  [Sistema Autônomo AS 1916](https://plataforma.rnp.br/arquivos/documents/Termo%20Tecnico%20-%20SD-WAN%20v1.pdf).
