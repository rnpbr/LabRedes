# Base SR-MPLS no IOS-XR

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/00-base">`labs/cisco/sr-mpls/00-base`</a>.

Convenções, topologia de referência e configuração mínima usadas pelos
laboratórios Cisco. Para a arquitetura e a terminologia, leia primeiro os
[fundamentos de SR-MPLS](../index.md).

Ambiente: [preparação do ambiente](01-preparacao-do-ambiente.md). Índice de labs:
[laboratórios Cisco](index.md).

Imagem usada: `ios-xr/xrd-control-plane:7.10.2`.

## :material-format-list-checks: **Convenções do projeto**

| Item | Valor |
|---|---|
| SRGB | `16000-23999` em todos os nós |
| SRLB | `15000-15999`, só onde há binding-SID manual |
| Adj-SIDs | faixa dinâmica acima do SRGB, a partir de `24000` |
| IGP | OSPFv2, área única `0` |
| Label do node-SID | `16000 + prefix-SID index` |
| Interfaces de core | `network point-to-point` |
| Loopback0 no OSPF | `passive enable` |
| Custo IGP | declarado nos dois lados de cada enlace |
| Kind containerlab | `cisco_xrd` |

O custo precisa estar nos dois lados porque o OSPF usa o custo da interface de saída. Declarar em um lado só gera caminho assimétrico e quebra a análise de P-space e Q-space dos labs de TI-LFA.

## :material-ip-network-outline: **Endereçamento**

O projeto usa três esquemas:

| | Referência, SR-TE e Inter-AS | Labs de TI-LFA | Multidomínio |
|---|---|---|---|
| Loopbacks | `10.0.0.0/24`, host = ID do nó | `10.0.1.248` a `10.0.1.254` | `10.<domínio>.255.<nó>/32` |
| Enlaces | `192.0.2.0/24`, `/31` | `10.10.<a><b>.0/30` | `10.<domínio>.0.0/16`, `/31` |
| Onde aparece | topologia desta página, `explicit-policy`, `bgp-lu` | os labs de TI-LFA | `flex-algo-anycast` |

O lab `bgp-lu` acrescenta `198.51.100.0/24` e `203.0.113.0/24` para as redes de cliente. Os três blocos - com o `192.0.2.0/24` - são reservados pela RFC 5737.

O `192.0.2.0/24` é reservado pela RFC 5737 para documentação: serve em lab, não em produção. Os labs de TI-LFA usam `10.10.<origem><destino>.0/30` porque assim dá para ler o enlace direto na saída de um `traceroute`, sem consultar tabela. O lab `flex-algo-anycast` usa um bloco `10.<domínio>.0.0/16` por domínio OSPF pelo mesmo motivo: o domínio de cada endereço fica legível no `traceroute`.

**Os PoPs têm identidade fixa nos labs de TI-LFA.** Os labs reusam os mesmos nós com os mesmos SIDs, então o label `16007` é BA em qualquer um deles:

| PoP | Loopback0 | SID index | Label |
|---|---|---:|---:|
| SP | `10.0.1.254/32` | 1 | `16001` |
| DF | `10.0.1.253/32` | 2 | `16002` |
| RJ | `10.0.1.252/32` | 3 | `16003` |
| ES | `10.0.1.251/32` | 4 | `16004` |
| MG | `10.0.1.250/32` | 5 | `16005` |
| PR | `10.0.1.249/32` | 6 | `16006` |
| BA | `10.0.1.248/32` | 7 | `16007` |

Cada lab sobe só os PoPs que precisa. A rede de gerência muda por lab (`172.20.20.0/24` no SR-TE, `172.20.21` a `172.20.25` nos de TI-LFA, `172.20.26.0/24` no Inter-AS, `172.20.27.0/24` no multidomínio), então dá para rodar mais de um ao mesmo tempo.

## :material-lan: **Topologia de referência**

Cinco nós, para ilustrar os conceitos. Não tem deploy próprio.

```text
              p1
            / | \
         pe1  p3  pe2
            \ | /
              p2
```

`p3` não tem enlace direto com `pe1` nem com `pe2`.

- `pe1` até `pe2` via `p1` ou `p2`: mesmo custo, ECMP.
- `pe1` até `pe2` via `p3`: mais longo. Serve para forçar um caminho não mais curto em SR-TE.

| Nó | Loopback0 | SID index | Label |
|---|---|---:|---:|
| pe1 | `10.0.0.1/32` | 1 | `16001` |
| p1 | `10.0.0.2/32` | 2 | `16002` |
| p2 | `10.0.0.3/32` | 3 | `16003` |
| p3 | `10.0.0.4/32` | 4 | `16004` |
| pe2 | `10.0.0.5/32` | 5 | `16005` |

| Enlace | Lado A | A | Lado B | B |
|---|---|---|---|---|
| pe1-p1 | pe1 Gi0/0/0/0 | `192.0.2.0/31` | p1 Gi0/0/0/0 | `192.0.2.1/31` |
| pe1-p2 | pe1 Gi0/0/0/1 | `192.0.2.2/31` | p2 Gi0/0/0/0 | `192.0.2.3/31` |
| p1-pe2 | p1 Gi0/0/0/1 | `192.0.2.4/31` | pe2 Gi0/0/0/0 | `192.0.2.5/31` |
| p2-pe2 | p2 Gi0/0/0/1 | `192.0.2.6/31` | pe2 Gi0/0/0/1 | `192.0.2.7/31` |
| p1-p3 | p1 Gi0/0/0/2 | `192.0.2.8/31` | p3 Gi0/0/0/0 | `192.0.2.9/31` |
| p3-p2 | p3 Gi0/0/0/1 | `192.0.2.10/31` | p2 Gi0/0/0/2 | `192.0.2.11/31` |

O material original em inglês desta topologia está em
[Lab Cisco XRd SR-MPLS de 5 nós](03-referencia-lab-5-nos.md).

## :material-file-cog: **Configuração mínima**

Três blocos, reusados em todo lab. Trocar `<ID>` e `<X>` pelos valores da topologia real.

**SR global**, igual em todo nó. As duas formas abaixo são equivalentes no IOS-XR:

```text
segment-routing
 global-block 16000 23999
!
```

```text
segment-routing global-block 16000 23999
```

**Loopback0 e SR no OSPF:**

```text
interface Loopback0
 ipv4 address 10.0.0.<ID> 255.255.255.255
!
router ospf 1
 router-id 10.0.0.<ID>
 segment-routing mpls
 segment-routing forwarding mpls
 area 0
  interface Loopback0
   passive enable
   prefix-sid index <ID>
```

**Interface de core**, repetir por enlace:

```text
interface GigabitEthernet0/0/0/<X>
 description <enlace>
 ipv4 address 192.0.2.<a> 255.255.255.254
 no shutdown
!
router ospf 1
 area 0
  interface GigabitEthernet0/0/0/<X>
   network point-to-point
   cost 10
```

Os blocos acima são só os trechos de SR, para leitura. Os `configs/*.cfg` dos
labs são startup-configs completos, com o bloco base do Containerlab junto. Ver
o [setup Cisco](01-preparacao-do-ambiente.md).

## :material-check-decagram: **Verificação**

A partir de qualquer nó.

| Comando | O que confirmar |
|---|---|
| `show ospf neighbor` | `FULL` em toda interface de core |
| `show ospf segment-routing prefix-sid-map active-policy` | cada loopback com seu SID index |
| `show route 10.0.0.5/32 detail` | rota SR com o label de saída imposto |
| `show mpls forwarding` | uma entrada por label `16001` a `16005` |
| `show cef 10.0.0.5/32` | duas entradas de mesmo custo, se houver ECMP |
| `ping` e `traceroute` | responde, com o label visível nos saltos do meio |

`ping mpls` e `traceroute mpls` só retornam algo útil com `mpls oam` configurado, como no lab `flex-algo-anycast`. Sem ele, use `traceroute` e `show cef`.

## :material-book-open-variant: **Referências**

- RFC 5737 - *IPv4 Address Blocks Reserved for Documentation*: https://datatracker.ietf.org/doc/html/rfc5737
- Cisco IOS-XR 7.10.x - *Segment Routing Configuration Guide*: https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/710x/configuration/guide/b-segment-routing-cg-cisco8000-710x.html
- Containerlab - *Cisco XRd*: https://containerlab.dev/manual/kinds/xrd/
