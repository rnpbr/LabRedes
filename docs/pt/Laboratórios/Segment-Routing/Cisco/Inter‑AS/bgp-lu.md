# Inter-AS: BGP-LU entre o PoP-PB e o backbone Rede Ipê

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/inter-as/bgp-lu">`labs/cisco/sr-mpls/inter-as/bgp-lu`</a>.

!!! info "Pré-requisitos"
    [conceitos de Inter-AS](index.md), [base Cisco](../02-base-sr-mpls.md) e [ambiente XRd](../01-preparacao-do-ambiente.md).

## :material-bookmark: **O que este lab demonstra**

Dois domínios administrativos, cada um com seu próprio OSPF e seus próprios
Prefix-SIDs, unidos por uma fronteira eBGP labeled-unicast. Nenhum IGP cruza a
fronteira.

O ponto central é a **recursão de transporte**: a rota BGP-LU para a loopback do
PE remoto não é encaminhável sozinha. Ela traz um label e um next hop, mas esse
next hop ainda precisa ser resolvido pelo transporte SR do domínio local. O
resultado é uma pilha de dois labels imposta pelo CEF - um do OSPF/SR, outro do
BGP - e é essa combinação, não a existência da sessão BGP, que o lab serve para
tornar visível.

Sobre esse substrato o lab acrescenta proteção TI-LFA em cada losango e uma SR
Policy explícita de cinco segmentos que atravessa os dois domínios usando um
PeerNode SID de BGP Egress Peer Engineering na fronteira.

## :material-alert-circle-outline: **O que este lab não demonstra**

Não é uma L3VPN inter-AS Option C completa: não há AF VPNv4/vpnv6, VRF, RD nem
RT. O lab implementa o **substrato de transporte** da Opção C e substitui a
camada VPN por uma rota LU para a loopback do PE remoto mais uma sessão eBGP
IPv4 unicast multihop entre os PEs. O prefix-set `LU_LOOPBACKS` é o limite entre
as duas camadas.

Também não mede convergência em 50 ms nem capacidade de encaminhamento. Não há
BFD configurado, e a imagem XRd Control Plane não é uma plataforma de dados. O
estágio 5 prova a **instalação** do repair path no CEF, não um SLA.

!!! warning "Atenção"
    Este lab não reproduz a configuração da RNP. O AS 1916 identifica o papel do
    backbone no ambiente isolado; o AS 65001 é privado e identifica o PoP
    didático. Endereços, custos, SIDs e configurações não descrevem a produção.
    Somente os quatro enlaces do losango PB-RN/BA-CE vêm do mapa público. Método,
    evidências e limites da analogia em [`recorte-rede-ipe.md`](recorte-rede-ipe.md).

## :material-lightbulb-on-outline: **Conceitos aplicados**

- **BGP-LU (RFC 8277)**: BGP carregando o prefixo com um label MPLS. Estende o
  alcance MPLS entre domínios que não compartilham IGP.
- **Recursão de transporte**: o next hop de uma rota LU é resolvido pela rota
  SR do domínio local; o CEF empilha o Node-SID sobre o label BGP.
- **`next-hop-self` no ASBR**: sem ele o PE recebe um next hop que seu IGP não
  conhece, e a rota LU não resolve.
- **PeerNode SID (BGP-EPE, RFC 9087)**: label local do ASBR de saída cuja
  semântica é "encaminhe ao peer BGP X", e não "alcance o Node-SID de X".
- **SRGB compartilhado**: `16000-23999` nos oito nós. Label = `16000 + índice`.
  O mesmo valor numérico só tem semântica global dentro do domínio que anuncia
  aquele SID.

## :material-lan: **Topologia**

![Topologia lógica: o PoP-PB em AS 65001, com ramo primário de custo 10 e alternativo de custo 20, ligado por eBGP labeled-unicast ao recorte PB-RN/BA-CE do backbone em AS 1916](images/bgp-lu/topology-bgp-lu.svg#only-light)
![Topologia lógica: o PoP-PB em AS 65001, com ramo primário de custo 10 e alternativo de custo 20, ligado por eBGP labeled-unicast ao recorte PB-RN/BA-CE do backbone em AS 1916](images/bgp-lu/topology-bgp-lu-escuro.svg#only-dark)

Cada domínio é um losango: dois caminhos internos entre a borda de serviço e a
borda administrativa, um com custo 10 por enlace e outro com 20. Isso dá, em
cada lado, um caminho SPF previsível, um candidato natural a repair path do
TI-LFA e um ramo alternativo para a SR Policy forçar.

| Nó | Papel | AS | Loopback0 | SID index | Label |
|---|---|---:|---|---:|---:|
| `pe-pop-pb` | PE de ingresso | 65001 | `10.0.0.1/32` | 1 | `16001` |
| `p-pop-a` | P, ramo primário | 65001 | `10.0.0.2/32` | 2 | `16002` |
| `p-pop-b` | P, ramo alternativo | 65001 | `10.0.0.3/32` | 3 | `16003` |
| `asbr-pop-pb` | ASBR e headend EPE | 65001 | `10.0.0.4/32` | 4 | `16004` |
| `asbr-ipe-pb` | ASBR e headend EPE | 1916 | `10.0.0.5/32` | 5 | `16005` |
| `p-ipe-rn` | P, ramo primário | 1916 | `10.0.0.6/32` | 6 | `16006` |
| `p-ipe-ba` | P, ramo alternativo | 1916 | `10.0.0.7/32` | 7 | `16007` |
| `pe-ipe-ce` | PE de saída | 1916 | `10.0.0.8/32` | 8 | `16008` |

As siglas PB, RN, BA e CE identificam vértices do grafo público, não
equipamentos reais. Os nomes do domínio do PoP são deliberadamente funcionais
porque sua topologia interna não é pública.

| Enlace | Interfaces XR | Prefixo | Endereços | Custo |
|---|---|---|---|---:|
| `instituicao-pb`-`pe-pop-pb` | - / Gi0/0/0/0 | `198.51.100.0/24` | `.10` / `.1` | - |
| `pe-pop-pb`-`p-pop-a` | Gi0/0/0/1 / Gi0/0/0/0 | `192.0.2.0/31` | `.0` / `.1` | 10 |
| `pe-pop-pb`-`p-pop-b` | Gi0/0/0/2 / Gi0/0/0/0 | `192.0.2.2/31` | `.2` / `.3` | 20 |
| `p-pop-a`-`asbr-pop-pb` | Gi0/0/0/1 / Gi0/0/0/0 | `192.0.2.4/31` | `.4` / `.5` | 10 |
| `p-pop-b`-`asbr-pop-pb` | Gi0/0/0/1 / Gi0/0/0/1 | `192.0.2.6/31` | `.6` / `.7` | 20 |
| `asbr-pop-pb`-`asbr-ipe-pb` | Gi0/0/0/2 / Gi0/0/0/2 | `192.0.2.8/31` | `.8` / `.9` | fora do OSPF |
| `asbr-ipe-pb`-`p-ipe-rn` | Gi0/0/0/0 / Gi0/0/0/1 | `192.0.2.10/31` | `.10` / `.11` | 10 |
| `asbr-ipe-pb`-`p-ipe-ba` | Gi0/0/0/1 / Gi0/0/0/1 | `192.0.2.12/31` | `.12` / `.13` | 20 |
| `p-ipe-rn`-`pe-ipe-ce` | Gi0/0/0/0 / Gi0/0/0/1 | `192.0.2.14/31` | `.14` / `.15` | 10 |
| `p-ipe-ba`-`pe-ipe-ce` | Gi0/0/0/0 / Gi0/0/0/2 | `192.0.2.16/31` | `.16` / `.17` | 20 |
| `pe-ipe-ce`-`servico-ce` | Gi0/0/0/0 / - | `203.0.113.0/24` | `.1` / `.10` | - |

Os enlaces usam `192.0.2.0/24` em `/31` conforme a RFC 3021; as redes de cliente
usam `198.51.100.0/24` e `203.0.113.0/24`. Os três blocos são reservados pela
RFC 5737 para documentação. As loopbacks ficam em `10.0.0.0/24`, o mesmo esquema
da topologia de referência da [base Cisco](../02-base-sr-mpls.md).

O enlace `asbr-pop-pb`-`asbr-ipe-pb` é o único fora do OSPF: ali só existe eBGP
labeled-unicast.

### Sessões BGP

| Sessão | Tipo | AF | Next hop |
|---|---|---|---|
| `pe-pop-pb`-`asbr-pop-pb` | iBGP 65001 | IPv4 LU | loopbacks; ASBR usa `next-hop-self` |
| `asbr-pop-pb`-`asbr-ipe-pb` | eBGP 65001↔1916 | IPv4 LU | endereços diretamente conectados |
| `asbr-ipe-pb`-`pe-ipe-ce` | iBGP 1916 | IPv4 LU | loopbacks; ASBR usa `next-hop-self` |
| `pe-pop-pb`-`pe-ipe-ce` | eBGP multihop | IPv4 unicast | loopbacks |

As três sessões LU usam a route-policy `LU_ONLY`, que admite exclusivamente
`10.0.0.1/32` e `10.0.0.8/32`. Redes de cliente nunca recebem label.

## :material-rocket-launch: **Deploy**

```bash
git clone https://github.com/rnpbr/LabRedes-segmentrouting.git
cd LabRedes-segmentrouting
cd labs/cisco/sr-mpls/inter-as/bgp-lu
sudo clab deploy -t lab.clab.yml
```

Oito roteadores XRd mais dois clientes Alpine. Reserve cerca de 12 GB de RAM e
oito CPUs - é o maior lab do repositório. Gerência em `172.20.26.0/24`:

| Nó | Gerência | Nó | Gerência |
|---|---|---|---|
| `pe-pop-pb` | `172.20.26.11` | `asbr-ipe-pb` | `172.20.26.15` |
| `p-pop-a` | `172.20.26.12` | `p-ipe-rn` | `172.20.26.16` |
| `p-pop-b` | `172.20.26.13` | `p-ipe-ba` | `172.20.26.17` |
| `asbr-pop-pb` | `172.20.26.14` | `pe-ipe-ce` | `172.20.26.18` |
| `instituicao-pb` | `172.20.26.21` | `servico-ce` | `172.20.26.22` |

Acesso: `ssh clab@172.20.26.11`, senha `clab@123`. Ou:

```bash
sudo docker exec -it clab-inter-as-bgp-lu-pe-pop-pb /pkg/bin/xr_cli.sh
```

O boot do XR leva alguns minutos. Container em `running` não significa CLI
pronta, e o BGP precisa de mais tempo ainda para estabilizar - ver
[Tempo de estabilização](#tempo-de-estabilizacao).

```bash
# Derrubar o lab
sudo clab destroy -t lab.clab.yml --cleanup
```

## Arquivos do laboratório

Todos os arquivos estão no repositório, em <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/inter-as/bgp-lu">`labs/cisco/sr-mpls/inter-as/bgp-lu`</a>. Os blocos abaixo mostram o conteúdo completo de cada um para consulta rápida.

??? example "lab.clab.yml"

    ```yaml
    # Inter-AS BGP-LU
    #
    # Deploy:
    #   sudo clab deploy -t lab.clab.yml
    #
    # Cada no le seu arquivo de configuracao em configs/<no>.cfg, ao lado deste
    # arquivo. O containerlab entrega o .cfg ao XRd como first-boot.cfg.
    #
    # Repositorio: https://github.com/rnpbr/LabRedes-segmentrouting.git
    #
    # Para servir os .cfg direto do GitHub em vez de copiar configs/ para o disco,
    # troque o caminho de cada no por uma URL raw:
    #   startup-config: https://raw.githubusercontent.com/rnpbr/LabRedes-segmentrouting/main/labs/cisco/sr-mpls/inter-as/bgp-lu/configs/pe-pop-pb.cfg
    # Ref: https://containerlab.dev/manual/config-mgmt/#remote
    #
    # enforce-startup-config faz todo deploy reaplicar o .cfg, em vez de reusar a
    # config gravada por uma execucao anterior.
    #
    # Dois dominios administrativos, cada um com dois caminhos internos, unidos por
    # uma fronteira eBGP labeled-unicast. Os dois nos linux sao clientes de teste:
    # nao rodam roteamento, so apontam a default para o PE do seu lado.

    name: inter-as-bgp-lu

    mgmt:
      network: inter-as-bgp-lu-mgmt
      ipv4-subnet: 172.20.26.0/24

    topology:
      defaults:
        kind: cisco_xrd

      kinds:
        cisco_xrd:
          image: ios-xr/xrd-control-plane:7.10.2
          enforce-startup-config: true
        linux:
          image: alpine:3.20

      nodes:
        # --- Dominio PoP-PB / AS 65001 -----------------------------------------
        pe-pop-pb:
          mgmt-ipv4: 172.20.26.11
          startup-config: configs/pe-pop-pb.cfg
        p-pop-a:
          mgmt-ipv4: 172.20.26.12
          startup-config: configs/p-pop-a.cfg
        p-pop-b:
          mgmt-ipv4: 172.20.26.13
          startup-config: configs/p-pop-b.cfg
        asbr-pop-pb:
          mgmt-ipv4: 172.20.26.14
          startup-config: configs/asbr-pop-pb.cfg

        # --- Dominio backbone / AS 1916 ----------------------------------------
        asbr-ipe-pb:
          mgmt-ipv4: 172.20.26.15
          startup-config: configs/asbr-ipe-pb.cfg
        p-ipe-rn:
          mgmt-ipv4: 172.20.26.16
          startup-config: configs/p-ipe-rn.cfg
        p-ipe-ba:
          mgmt-ipv4: 172.20.26.17
          startup-config: configs/p-ipe-ba.cfg
        pe-ipe-ce:
          mgmt-ipv4: 172.20.26.18
          startup-config: configs/pe-ipe-ce.cfg

        # --- Clientes de teste --------------------------------------------------
        instituicao-pb:
          kind: linux
          mgmt-ipv4: 172.20.26.21
          exec:
            - apk add --no-cache iproute2 iputils traceroute iperf3
            - ip address replace 198.51.100.10/24 dev eth1
            - ip route replace default via 198.51.100.1

        servico-ce:
          kind: linux
          mgmt-ipv4: 172.20.26.22
          exec:
            - apk add --no-cache iproute2 iputils traceroute iperf3
            - ip address replace 203.0.113.10/24 dev eth1
            - ip route replace default via 203.0.113.1

      links:
        # instituicao-pb-pe-pop-pb: acesso do cliente, 198.51.100.0/24
        - endpoints: ["instituicao-pb:eth1", "pe-pop-pb:Gi0-0-0-0"]

        # --- Losango do PoP-PB: custo 10 no ramo A, 20 no ramo B ---------------
        # pe-pop-pb-p-pop-a: ramo primario, custo 10
        - endpoints: ["pe-pop-pb:Gi0-0-0-1", "p-pop-a:Gi0-0-0-0"]
        # pe-pop-pb-p-pop-b: ramo alternativo, custo 20
        - endpoints: ["pe-pop-pb:Gi0-0-0-2", "p-pop-b:Gi0-0-0-0"]
        # p-pop-a-asbr-pop-pb: ramo primario, custo 10
        - endpoints: ["p-pop-a:Gi0-0-0-1", "asbr-pop-pb:Gi0-0-0-0"]
        # p-pop-b-asbr-pop-pb: ramo alternativo, custo 20
        - endpoints: ["p-pop-b:Gi0-0-0-1", "asbr-pop-pb:Gi0-0-0-1"]

        # --- Fronteira inter-AS: fora do OSPF, so eBGP labeled-unicast ---------
        - endpoints: ["asbr-pop-pb:Gi0-0-0-2", "asbr-ipe-pb:Gi0-0-0-2"]

        # --- Losango do backbone: custo 10 via RN, 20 via BA -------------------
        # asbr-ipe-pb-p-ipe-rn: ramo primario, custo 10
        - endpoints: ["asbr-ipe-pb:Gi0-0-0-0", "p-ipe-rn:Gi0-0-0-1"]
        # asbr-ipe-pb-p-ipe-ba: ramo alternativo, custo 20
        - endpoints: ["asbr-ipe-pb:Gi0-0-0-1", "p-ipe-ba:Gi0-0-0-1"]
        # p-ipe-rn-pe-ipe-ce: ramo primario, custo 10
        - endpoints: ["p-ipe-rn:Gi0-0-0-0", "pe-ipe-ce:Gi0-0-0-1"]
        # p-ipe-ba-pe-ipe-ce: ramo alternativo, custo 20
        - endpoints: ["p-ipe-ba:Gi0-0-0-0", "pe-ipe-ce:Gi0-0-0-2"]

        # pe-ipe-ce-servico-ce: acesso do cliente, 203.0.113.0/24
        - endpoints: ["pe-ipe-ce:Gi0-0-0-0", "servico-ce:eth1"]
    ```

??? example "configs/asbr-ipe-pb.cfg"

    ```text
    !
    ! ============================================================================
    ! Bloco base do containerlab para o kind cisco_xrd.
    ! Espelha nodes/xrd/xrd.cfg do containerlab: sem ele o no sobe sem hostname,
    ! sem usuario clab, sem SSH e sem rota default de gerencia.
    ! Nao editar: as variaveis {{ .ShortName }} e {{ .MgmtIPv4Gateway }} sao
    ! resolvidas pelo containerlab em tempo de deploy.
    ! ============================================================================
    !
    hostname {{ .ShortName }}
    !
    username clab
     group root-lr
     group cisco-support
     secret clab@123
    !
    grpc
     port 9339
     no-tls
     address-family dual
    !
    line default
     transport input ssh
    !
    netconf-yang agent
     ssh
    !
    interface MgmtEth0/RP0/CPU0/0
    !
    ssh server v2
    ssh server netconf
    !
    router static
     address-family ipv4 unicast
      0.0.0.0/0 MgmtEth0/RP0/CPU0/0 {{ .MgmtIPv4Gateway }}
      192.0.2.8/32 GigabitEthernet0/0/0/2
     !
    !
    !
    ! ==========================================================================
    ! Lab Inter-AS BGP-LU - Rede Ipe / no asbr-ipe-pb
    ! ASBR e headend EPE - dominio backbone / AS 1916
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block 15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.5 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description asbr-ipe-pb to p-ipe-rn (ramo primario)
     ipv4 address 192.0.2.10 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description asbr-ipe-pb to p-ipe-ba (ramo alternativo)
     ipv4 address 192.0.2.12 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/2
     description asbr-ipe-pb to asbr-pop-pb (fronteira eBGP-LU)
     ipv4 address 192.0.2.9 255.255.255.254
     no shutdown
    !
    router ospf 1
     router-id 10.0.0.5
     segment-routing mpls
     area 0
      segment-routing mpls
      interface Loopback0
       passive enable
       prefix-sid index 5
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 10
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 20
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
     !
    !
    route-policy PASS
     pass
    end-policy
    !
    prefix-set LU_LOOPBACKS
     10.0.0.1/32,
     10.0.0.8/32
    end-set
    !
    prefix-set LOCAL_PE_LOOPBACK
     10.0.0.8/32
    end-set
    !
    route-policy LU_ONLY
     if destination in LU_LOOPBACKS then
      pass
     else
      drop
     endif
    end-policy
    !
    route-policy OSPF_TO_BGP_LU
     if destination in LOCAL_PE_LOOPBACK and route-has-label then
      pass
     else
      drop
     endif
    end-policy
    !
    router bgp 1916
     bgp router-id 10.0.0.5
     address-family ipv4 unicast
      redistribute ospf 1 match internal route-policy OSPF_TO_BGP_LU
      allocate-label all
     !
     neighbor 10.0.0.8
      remote-as 1916
      update-source Loopback0
      address-family ipv4 labeled-unicast
       next-hop-self
       route-policy LU_ONLY in
       route-policy LU_ONLY out
      !
     !
     neighbor 192.0.2.8
      remote-as 65001
      egress-engineering
      peer-node-sid index 100
      address-family ipv4 labeled-unicast
       route-policy LU_ONLY in
       route-policy LU_ONLY out
      !
     !
    !
    mpls static
     interface GigabitEthernet0/0/0/2
     !
    !
    end
    ```

??? example "configs/asbr-pop-pb.cfg"

    ```text
    !
    ! ============================================================================
    ! Bloco base do containerlab para o kind cisco_xrd.
    ! Espelha nodes/xrd/xrd.cfg do containerlab: sem ele o no sobe sem hostname,
    ! sem usuario clab, sem SSH e sem rota default de gerencia.
    ! Nao editar: as variaveis {{ .ShortName }} e {{ .MgmtIPv4Gateway }} sao
    ! resolvidas pelo containerlab em tempo de deploy.
    ! ============================================================================
    !
    hostname {{ .ShortName }}
    !
    username clab
     group root-lr
     group cisco-support
     secret clab@123
    !
    grpc
     port 9339
     no-tls
     address-family dual
    !
    line default
     transport input ssh
    !
    netconf-yang agent
     ssh
    !
    interface MgmtEth0/RP0/CPU0/0
    !
    ssh server v2
    ssh server netconf
    !
    router static
     address-family ipv4 unicast
      0.0.0.0/0 MgmtEth0/RP0/CPU0/0 {{ .MgmtIPv4Gateway }}
      192.0.2.9/32 GigabitEthernet0/0/0/2
     !
    !
    !
    ! ==========================================================================
    ! Lab Inter-AS BGP-LU - Rede Ipe / no asbr-pop-pb
    ! ASBR e headend EPE - dominio PoP-PB / AS 65001
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block 15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.4 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description asbr-pop-pb to p-pop-a (ramo primario)
     ipv4 address 192.0.2.5 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description asbr-pop-pb to p-pop-b (ramo alternativo)
     ipv4 address 192.0.2.7 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/2
     description asbr-pop-pb to asbr-ipe-pb (fronteira eBGP-LU)
     ipv4 address 192.0.2.8 255.255.255.254
     no shutdown
    !
    router ospf 1
     router-id 10.0.0.4
     segment-routing mpls
     area 0
      segment-routing mpls
      interface Loopback0
       passive enable
       prefix-sid index 4
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 10
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 20
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
     !
    !
    route-policy PASS
     pass
    end-policy
    !
    prefix-set LU_LOOPBACKS
     10.0.0.1/32,
     10.0.0.8/32
    end-set
    !
    prefix-set LOCAL_PE_LOOPBACK
     10.0.0.1/32
    end-set
    !
    route-policy LU_ONLY
     if destination in LU_LOOPBACKS then
      pass
     else
      drop
     endif
    end-policy
    !
    route-policy OSPF_TO_BGP_LU
     if destination in LOCAL_PE_LOOPBACK and route-has-label then
      pass
     else
      drop
     endif
    end-policy
    !
    router bgp 65001
     bgp router-id 10.0.0.4
     address-family ipv4 unicast
      redistribute ospf 1 match internal route-policy OSPF_TO_BGP_LU
      allocate-label all
     !
     neighbor 10.0.0.1
      remote-as 65001
      update-source Loopback0
      address-family ipv4 labeled-unicast
       next-hop-self
       route-policy LU_ONLY in
       route-policy LU_ONLY out
      !
     !
     neighbor 192.0.2.9
      remote-as 1916
      egress-engineering
      peer-node-sid index 100
      address-family ipv4 labeled-unicast
       route-policy LU_ONLY in
       route-policy LU_ONLY out
      !
     !
    !
    mpls static
     interface GigabitEthernet0/0/0/2
     !
    !
    end
    ```

??? example "configs/p-ipe-ba.cfg"

    ```text
    !
    ! ============================================================================
    ! Bloco base do containerlab para o kind cisco_xrd.
    ! Espelha nodes/xrd/xrd.cfg do containerlab: sem ele o no sobe sem hostname,
    ! sem usuario clab, sem SSH e sem rota default de gerencia.
    ! Nao editar: as variaveis {{ .ShortName }} e {{ .MgmtIPv4Gateway }} sao
    ! resolvidas pelo containerlab em tempo de deploy.
    ! ============================================================================
    !
    hostname {{ .ShortName }}
    !
    username clab
     group root-lr
     group cisco-support
     secret clab@123
    !
    grpc
     port 9339
     no-tls
     address-family dual
    !
    line default
     transport input ssh
    !
    netconf-yang agent
     ssh
    !
    interface MgmtEth0/RP0/CPU0/0
    !
    ssh server v2
    ssh server netconf
    !
    router static
     address-family ipv4 unicast
      0.0.0.0/0 MgmtEth0/RP0/CPU0/0 {{ .MgmtIPv4Gateway }}
     !
    !
    !
    ! ==========================================================================
    ! Lab Inter-AS BGP-LU - Rede Ipe / no p-ipe-ba
    ! P do ramo alternativo - dominio backbone / AS 1916
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block 15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.7 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description p-ipe-ba to pe-ipe-ce (ramo alternativo)
     ipv4 address 192.0.2.16 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description p-ipe-ba to asbr-ipe-pb (ramo alternativo)
     ipv4 address 192.0.2.13 255.255.255.254
     no shutdown
    !
    router ospf 1
     router-id 10.0.0.7
     segment-routing mpls
     area 0
      segment-routing mpls
      interface Loopback0
       passive enable
       prefix-sid index 7
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 20
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 20
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
     !
    !
    end
    ```

??? example "configs/p-ipe-rn.cfg"

    ```text
    !
    ! ============================================================================
    ! Bloco base do containerlab para o kind cisco_xrd.
    ! Espelha nodes/xrd/xrd.cfg do containerlab: sem ele o no sobe sem hostname,
    ! sem usuario clab, sem SSH e sem rota default de gerencia.
    ! Nao editar: as variaveis {{ .ShortName }} e {{ .MgmtIPv4Gateway }} sao
    ! resolvidas pelo containerlab em tempo de deploy.
    ! ============================================================================
    !
    hostname {{ .ShortName }}
    !
    username clab
     group root-lr
     group cisco-support
     secret clab@123
    !
    grpc
     port 9339
     no-tls
     address-family dual
    !
    line default
     transport input ssh
    !
    netconf-yang agent
     ssh
    !
    interface MgmtEth0/RP0/CPU0/0
    !
    ssh server v2
    ssh server netconf
    !
    router static
     address-family ipv4 unicast
      0.0.0.0/0 MgmtEth0/RP0/CPU0/0 {{ .MgmtIPv4Gateway }}
     !
    !
    !
    ! ==========================================================================
    ! Lab Inter-AS BGP-LU - Rede Ipe / no p-ipe-rn
    ! P do ramo primario - dominio backbone / AS 1916
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block 15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.6 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description p-ipe-rn to pe-ipe-ce (ramo primario)
     ipv4 address 192.0.2.14 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description p-ipe-rn to asbr-ipe-pb (ramo primario)
     ipv4 address 192.0.2.11 255.255.255.254
     no shutdown
    !
    router ospf 1
     router-id 10.0.0.6
     segment-routing mpls
     area 0
      segment-routing mpls
      interface Loopback0
       passive enable
       prefix-sid index 6
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 10
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 10
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
     !
    !
    end
    ```

??? example "configs/p-pop-a.cfg"

    ```text
    !
    ! ============================================================================
    ! Bloco base do containerlab para o kind cisco_xrd.
    ! Espelha nodes/xrd/xrd.cfg do containerlab: sem ele o no sobe sem hostname,
    ! sem usuario clab, sem SSH e sem rota default de gerencia.
    ! Nao editar: as variaveis {{ .ShortName }} e {{ .MgmtIPv4Gateway }} sao
    ! resolvidas pelo containerlab em tempo de deploy.
    ! ============================================================================
    !
    hostname {{ .ShortName }}
    !
    username clab
     group root-lr
     group cisco-support
     secret clab@123
    !
    grpc
     port 9339
     no-tls
     address-family dual
    !
    line default
     transport input ssh
    !
    netconf-yang agent
     ssh
    !
    interface MgmtEth0/RP0/CPU0/0
    !
    ssh server v2
    ssh server netconf
    !
    router static
     address-family ipv4 unicast
      0.0.0.0/0 MgmtEth0/RP0/CPU0/0 {{ .MgmtIPv4Gateway }}
     !
    !
    !
    ! ==========================================================================
    ! Lab Inter-AS BGP-LU - Rede Ipe / no p-pop-a
    ! P do ramo primario - dominio PoP-PB / AS 65001
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block 15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.2 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description p-pop-a to pe-pop-pb (ramo primario)
     ipv4 address 192.0.2.1 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description p-pop-a to asbr-pop-pb (ramo primario)
     ipv4 address 192.0.2.4 255.255.255.254
     no shutdown
    !
    router ospf 1
     router-id 10.0.0.2
     segment-routing mpls
     area 0
      segment-routing mpls
      interface Loopback0
       passive enable
       prefix-sid index 2
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 10
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 10
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
     !
    !
    end
    ```

??? example "configs/p-pop-b.cfg"

    ```text
    !
    ! ============================================================================
    ! Bloco base do containerlab para o kind cisco_xrd.
    ! Espelha nodes/xrd/xrd.cfg do containerlab: sem ele o no sobe sem hostname,
    ! sem usuario clab, sem SSH e sem rota default de gerencia.
    ! Nao editar: as variaveis {{ .ShortName }} e {{ .MgmtIPv4Gateway }} sao
    ! resolvidas pelo containerlab em tempo de deploy.
    ! ============================================================================
    !
    hostname {{ .ShortName }}
    !
    username clab
     group root-lr
     group cisco-support
     secret clab@123
    !
    grpc
     port 9339
     no-tls
     address-family dual
    !
    line default
     transport input ssh
    !
    netconf-yang agent
     ssh
    !
    interface MgmtEth0/RP0/CPU0/0
    !
    ssh server v2
    ssh server netconf
    !
    router static
     address-family ipv4 unicast
      0.0.0.0/0 MgmtEth0/RP0/CPU0/0 {{ .MgmtIPv4Gateway }}
     !
    !
    !
    ! ==========================================================================
    ! Lab Inter-AS BGP-LU - Rede Ipe / no p-pop-b
    ! P do ramo alternativo - dominio PoP-PB / AS 65001
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block 15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.3 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description p-pop-b to pe-pop-pb (ramo alternativo)
     ipv4 address 192.0.2.3 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description p-pop-b to asbr-pop-pb (ramo alternativo)
     ipv4 address 192.0.2.6 255.255.255.254
     no shutdown
    !
    router ospf 1
     router-id 10.0.0.3
     segment-routing mpls
     area 0
      segment-routing mpls
      interface Loopback0
       passive enable
       prefix-sid index 3
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 20
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 20
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
     !
    !
    end
    ```

??? example "configs/pe-ipe-ce.cfg"

    ```text
    !
    ! ============================================================================
    ! Bloco base do containerlab para o kind cisco_xrd.
    ! Espelha nodes/xrd/xrd.cfg do containerlab: sem ele o no sobe sem hostname,
    ! sem usuario clab, sem SSH e sem rota default de gerencia.
    ! Nao editar: as variaveis {{ .ShortName }} e {{ .MgmtIPv4Gateway }} sao
    ! resolvidas pelo containerlab em tempo de deploy.
    ! ============================================================================
    !
    hostname {{ .ShortName }}
    !
    username clab
     group root-lr
     group cisco-support
     secret clab@123
    !
    grpc
     port 9339
     no-tls
     address-family dual
    !
    line default
     transport input ssh
    !
    netconf-yang agent
     ssh
    !
    interface MgmtEth0/RP0/CPU0/0
    !
    ssh server v2
    ssh server netconf
    !
    router static
     address-family ipv4 unicast
      0.0.0.0/0 MgmtEth0/RP0/CPU0/0 {{ .MgmtIPv4Gateway }}
     !
    !
    !
    ! ==========================================================================
    ! Lab Inter-AS BGP-LU - Rede Ipe / no pe-ipe-ce
    ! PE de saida - dominio backbone / AS 1916
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block 15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.8 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description pe-ipe-ce to servico-ce
     ipv4 address 203.0.113.1 255.255.255.0
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description pe-ipe-ce to p-ipe-rn (ramo primario)
     ipv4 address 192.0.2.15 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/2
     description pe-ipe-ce to p-ipe-ba (ramo alternativo)
     ipv4 address 192.0.2.17 255.255.255.254
     no shutdown
    !
    router ospf 1
     router-id 10.0.0.8
     segment-routing mpls
     area 0
      segment-routing mpls
      interface Loopback0
       passive enable
       prefix-sid index 8
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 10
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
      interface GigabitEthernet0/0/0/2
       network point-to-point
       cost 20
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
     !
    !
    route-policy PASS
     pass
    end-policy
    !
    prefix-set PE_UNICAST_EXPORT
     203.0.113.0/24
    end-set
    !
    route-policy PE_UNICAST_EXPORT_ONLY
     if destination in PE_UNICAST_EXPORT then
      pass
     else
      drop
     endif
    end-policy
    !
    prefix-set LU_LOOPBACKS
     10.0.0.1/32,
     10.0.0.8/32
    end-set
    !
    route-policy LU_ONLY
     if destination in LU_LOOPBACKS then
      pass
     else
      drop
     endif
    end-policy
    !
    router bgp 1916
     bgp router-id 10.0.0.8
     address-family ipv4 unicast
      network 10.0.0.8/32
      network 203.0.113.0/24
      allocate-label all
     !
     neighbor 10.0.0.5
      remote-as 1916
      update-source Loopback0
      address-family ipv4 labeled-unicast
       route-policy LU_ONLY in
       route-policy LU_ONLY out
      !
     !
     neighbor 10.0.0.1
      remote-as 65001
      update-source Loopback0
      ebgp-multihop 10
      address-family ipv4 unicast
       route-policy PASS in
       route-policy PE_UNICAST_EXPORT_ONLY out
      !
     !
    !
    end
    ```

??? example "configs/pe-pop-pb.cfg"

    ```text
    !
    ! ============================================================================
    ! Bloco base do containerlab para o kind cisco_xrd.
    ! Espelha nodes/xrd/xrd.cfg do containerlab: sem ele o no sobe sem hostname,
    ! sem usuario clab, sem SSH e sem rota default de gerencia.
    ! Nao editar: as variaveis {{ .ShortName }} e {{ .MgmtIPv4Gateway }} sao
    ! resolvidas pelo containerlab em tempo de deploy.
    ! ============================================================================
    !
    hostname {{ .ShortName }}
    !
    username clab
     group root-lr
     group cisco-support
     secret clab@123
    !
    grpc
     port 9339
     no-tls
     address-family dual
    !
    line default
     transport input ssh
    !
    netconf-yang agent
     ssh
    !
    interface MgmtEth0/RP0/CPU0/0
    !
    ssh server v2
    ssh server netconf
    !
    router static
     address-family ipv4 unicast
      0.0.0.0/0 MgmtEth0/RP0/CPU0/0 {{ .MgmtIPv4Gateway }}
     !
    !
    !
    ! ==========================================================================
    ! Lab Inter-AS BGP-LU - Rede Ipe / no pe-pop-pb
    ! PE de ingresso - dominio PoP-PB / AS 65001
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block 15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.1 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description pe-pop-pb to instituicao-pb
     ipv4 address 198.51.100.1 255.255.255.0
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description pe-pop-pb to p-pop-a (ramo primario)
     ipv4 address 192.0.2.0 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/2
     description pe-pop-pb to p-pop-b (ramo alternativo)
     ipv4 address 192.0.2.2 255.255.255.254
     no shutdown
    !
    router ospf 1
     router-id 10.0.0.1
     segment-routing mpls
     area 0
      segment-routing mpls
      interface Loopback0
       passive enable
       prefix-sid index 1
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 10
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
      interface GigabitEthernet0/0/0/2
       network point-to-point
       cost 20
       fast-reroute per-prefix
       fast-reroute per-prefix ti-lfa enable
      !
     !
    !
    extcommunity-set opaque COLOR_100
     100 co-flag 01
    end-set
    !
    route-policy PASS
     pass
    end-policy
    !
    prefix-set PE_UNICAST_EXPORT
     198.51.100.0/24
    end-set
    !
    route-policy PE_UNICAST_EXPORT_ONLY
     if destination in PE_UNICAST_EXPORT then
      pass
     else
      drop
     endif
    end-policy
    !
    prefix-set LU_LOOPBACKS
     10.0.0.1/32,
     10.0.0.8/32
    end-set
    !
    route-policy LU_ONLY
     if destination in LU_LOOPBACKS then
      pass
     else
      drop
     endif
    end-policy
    !
    route-policy COLOR_100
     set extcommunity color COLOR_100
     pass
    end-policy
    !
    router bgp 65001
     bgp router-id 10.0.0.1
     address-family ipv4 unicast
      network 10.0.0.1/32
      network 198.51.100.0/24
      allocate-label all
     !
     neighbor 10.0.0.4
      remote-as 65001
      update-source Loopback0
      address-family ipv4 labeled-unicast
       route-policy LU_ONLY in
       route-policy LU_ONLY out
      !
     !
     neighbor 10.0.0.8
      remote-as 1916
      update-source Loopback0
      ebgp-multihop 10
      address-family ipv4 unicast
       route-policy COLOR_100 in
       route-policy PE_UNICAST_EXPORT_ONLY out
      !
     !
    !
    segment-routing
     traffic-eng
      segment-list INTERAS-BACKUP
       index 10 mpls label 16003
       index 20 mpls label 16004
       index 30 mpls label 15100
       index 40 mpls label 16007
       index 50 mpls label 16008
      !
      policy INTERAS-COLOR-100
       color 100 end-point ipv4 10.0.0.8
       candidate-paths
        preference 100
         explicit segment-list INTERAS-BACKUP
         !
        !
       !
      !
     !
    !
    end
    ```

---


## :material-cog: **O mecanismo central, em detalhe**

Trecho relevante de `configs/pe-pop-pb.cfg` e `configs/asbr-pop-pb.cfg` (o resto
segue a [base SR-MPLS no IOS-XR](../02-base-sr-mpls.md)):

```text
! pe-pop-pb - PE de ingresso
router bgp 65001
 address-family ipv4 unicast
  network 10.0.0.1/32
  allocate-label all
 !
 neighbor 10.0.0.4
  remote-as 65001
  update-source Loopback0
  address-family ipv4 labeled-unicast
   route-policy LU_ONLY in
   route-policy LU_ONLY out

! asbr-pop-pb - ASBR
prefix-set LOCAL_PE_LOOPBACK
 10.0.0.1/32
end-set

route-policy OSPF_TO_BGP_LU
 if destination in LOCAL_PE_LOOPBACK and route-has-label then
  pass
 else
  drop
 endif
end-policy

router bgp 65001
 address-family ipv4 unicast
  redistribute ospf 1 match internal route-policy OSPF_TO_BGP_LU
  allocate-label all
 !
 neighbor 10.0.0.1
  address-family ipv4 labeled-unicast
   next-hop-self
 !
 neighbor 192.0.2.9
  remote-as 1916
  address-family ipv4 labeled-unicast
   route-policy LU_ONLY in
   route-policy LU_ONLY out
```

Para a loopback `10.0.0.8/32`, originada por `pe-ipe-ce`:

1. `asbr-ipe-pb` possui a rota OSPF/SR rotulada para o PE, com Prefix-SID
   `16008`, e a importa no BGP pela policy `OSPF_TO_BGP_LU`.
2. Essa rota local redistribuída vence, dentro do BGP, a cópia recebida por
   iBGP do próprio PE. O ASBR anuncia ao peer eBGP o binding já instalado
   `16008`, em vez de alocar um binding sem entrada correspondente na LFIB.
3. `asbr-pop-pb` aprende a rota por eBGP, instala a continuidade para o label
   recebido e a anuncia a `pe-pop-pb` com next hop `10.0.0.4` por causa de
   `next-hop-self`.
4. `pe-pop-pb` resolve `10.0.0.4` no OSPF/SR pelo Node-SID `16004`; o CEF
   combina os dois resultados e impõe `{16004, 16008}` por `p-pop-a`.
5. Depois do PHP de `16004`, `asbr-pop-pb` encaminha `16008` pela fronteira.
6. Em `asbr-ipe-pb`, `16008` já é uma chave válida da LFIB SR e continua pelo
   domínio do backbone até `pe-ipe-ce`.

![Recursão de transporte para 10.0.0.8/32: o BGP-LU dá o label e o next hop, o OSPF/SR dá o Prefix-SID 16004, e o CEF impõe a pilha {16004 16008}, reduzida por PHP e encaminhada pela fronteira até o backbone](images/bgp-lu/diagram-pilha-recursiva.svg#only-light)
![Recursão de transporte para 10.0.0.8/32: o BGP-LU dá o label e o next hop, o OSPF/SR dá o Prefix-SID 16004, e o CEF impõe a pilha {16004 16008}, reduzida por PHP e encaminhada pela fronteira até o backbone](images/bgp-lu/diagram-pilha-recursiva-escuro.svg#only-dark)

`next-hop-self` é decisivo. Sem ele, `pe-pop-pb` receberia como next hop o
endereço de fronteira `192.0.2.9`, que não existe em seu OSPF - a rota LU seria
recebida mas nunca resolveria.

O valor `16008` não é uma coincidência com um label dinâmico: ele pertence à
SRGB e é o Prefix-SID que a redistribuição leva da rota OSPF/SR para o anúncio
BGP-LU. A semântica continua local em cada salto, mas o ASBR remoto anuncia um
label que já possui ação válida na própria LFIB. A policy exige
`route-has-label` para não exportar a loopback se ela perder o binding SR.

## :material-stairs: **Progressão em seis estágios**

`configs/` é o estado final, com tudo ligado. Para percorrer o lab por partes,
suba o estado final e remova o que ainda não entrou, ou monte cada estágio
retirando dos `.cfg` os blocos listados abaixo. Cada estágio é cumulativo e só
deve ser passado depois que seus critérios de aceite fecharem.

![Seis estágios cumulativos, do OSPFv2 à SR Policy, cada um com o que entra e o respectivo gate de aceite](images/bgp-lu/diagram-progressao-estagios.svg#only-light)
![Seis estágios cumulativos, do OSPFv2 à SR Policy, cada um com o que entra e o respectivo gate de aceite](images/bgp-lu/diagram-progressao-estagios-escuro.svg#only-dark)

### Estágio 1 - underlay OSPF

Interfaces, endereçamento, `Loopback0`, OSPFv2 área 0 em cada domínio, custos 10
e 20. Fora: todo o resto.

```text
show ospf neighbor
show route 10.0.0.4/32 detail
show route 10.0.0.8/32 detail
```

Aceite: dois vizinhos `FULL` em cada roteador; `pe-pop-pb` alcança as quatro
loopbacks do PoP e **nenhuma** do backbone; a rota para `10.0.0.4/32` sai por
`192.0.2.1` (`p-pop-a`); `asbr-ipe-pb` alcança `10.0.0.8/32` via `p-ipe-rn`.

O custo de uma rota para loopback pode incluir o custo do prefixo stub além dos
enlaces. O dado decisivo é o next hop, não o número.

### Estágio 2 - SR-MPLS intradomínio

Entra: `segment-routing global-block` / `local-block`, `segment-routing mpls` no
processo e na área OSPF, `prefix-sid index <N>` em cada `Loopback0`.

```text
show ospf database opaque-area self-originate
show mpls forwarding
show mpls label table 0 label 16004 detail
```

Aceite: cada loopback anuncia seu Prefix-SID; `pe-pop-pb` vê `10.0.0.4/32` como
rota SR rotulada; os nós de trânsito têm LFIB para os SIDs do próprio domínio;
não existe LDP nem RSVP.

Os SIDs `16005`-`16008` **não** aparecem no domínio do PoP. Não há flooding OSPF
entre os domínios - é exatamente o problema que o estágio 3 resolve.

### Estágio 3 - transporte BGP labeled-unicast

Entra: `prefix-set LU_LOOPBACKS`, `route-policy LU_ONLY`, os prefix-sets
`LOCAL_PE_LOOPBACK` e as policies `OSPF_TO_BGP_LU` em cada ASBR, `router bgp`
com redistribuição OSPF interna filtrada e `allocate-label all`, as três sessões
LU, `next-hop-self` nos ASBRs em direção aos PEs, `mpls static` na interface de
fronteira e uma rota estática `/32` para o endereço de fronteira do ASBR oposto:

```text
! asbr-pop-pb
router static
 address-family ipv4 unicast
  192.0.2.9/32 GigabitEthernet0/0/0/2

! asbr-ipe-pb
router static
 address-family ipv4 unicast
  192.0.2.8/32 GigabitEthernet0/0/0/2
```

O IOS XR precisa dessa rota host na fronteira Inter-AS para vincular o label
MPLS a um FEC `/32`. Sem ela, a sessão BGP-LU pode ficar operacional e trocar
labels enquanto o tráfego rotulado não é encaminhado. Esse comportamento e a
rota estática requerida no ASBR IOS XR são descritos pela Cisco em
[Configure Inter-AS Option C MPLS VPN With Cisco IOS and Cisco IOS-XR](https://www.cisco.com/c/en/us/support/docs/multiprotocol-label-switching-mpls/mpls/200523-Configuration-and-Verification-of-Layer.html).

Em `pe-pop-pb`:

```text
show bgp ipv4 labeled-unicast summary
show bgp ipv4 labeled-unicast 10.0.0.8/32
show cef 10.0.0.8/32 detail
```

Em cada ASBR:

```text
show bgp ipv4 labeled-unicast summary
show bgp ipv4 labeled-unicast 10.0.0.1/32 detail
show bgp ipv4 labeled-unicast 10.0.0.8/32 detail
show route 192.0.2.9/32
show mpls forwarding
```

Em `asbr-ipe-pb`, consulte `192.0.2.8/32` na verificação da rota de fronteira.

Aceite: as três sessões LU `Established`; em cada ASBR, a rota OSPF redistribuída
para o PE local é o best path BGP e anuncia o Prefix-SID correspondente
(`16001` ou `16008`); o CEF de `pe-pop-pb` recursa pelo next hop `10.0.0.4` e
impõe `{16004, 16008}`; `16008` existe na LFIB de `asbr-ipe-pb`; e
`198.51.100.0/24` e `203.0.113.0/24` estão **ausentes** da tabela LU.

### Estágio 4 - sobreposição de serviço

Entra: eBGP IPv4 unicast multihop `pe-pop-pb`-`pe-ipe-ce`, o `network` das
redes de cliente e `route-policy PE_UNICAST_EXPORT_ONLY` na saída de cada PE.
O filtro anuncia somente `198.51.100.0/24` de `pe-pop-pb` e somente
`203.0.113.0/24` de `pe-ipe-ce`. As loopbacks continuam na AF unicast local
para receber um binding de label, mas não vazam pela sessão de serviço
AFI 1/SAFI 1; entre domínios elas são transportadas apenas por BGP-LU.

```text
show bgp ipv4 unicast summary
show bgp ipv4 unicast 203.0.113.0/24
```

```bash
docker exec clab-inter-as-bgp-lu-instituicao-pb ping -c 5 203.0.113.10
docker exec clab-inter-as-bgp-lu-servico-ce ping -c 5 198.51.100.10
docker exec clab-inter-as-bgp-lu-instituicao-pb traceroute -e 203.0.113.10
```

Aceite: sessão multihop `Established` com um prefixo recebido; as redes de
cliente presentes **somente** na família IPv4 unicast; ping cliente-cliente nos
dois sentidos sem perda; traceroute alcançando o cliente remoto.

Há uma dependência circular aparente - a sessão PE-PE precisa do transporte que
o estágio 3 construiu, e é por isso que ela vem depois.

### Estágio 5 - TI-LFA

Entra, em toda interface OSPF de core:

```text
fast-reroute per-prefix
fast-reroute per-prefix ti-lfa enable
```

```text
show route 10.0.0.4/32 detail
show cef 10.0.0.4/32 detail
```

Aceite: primário de `pe-pop-pb` para `asbr-pop-pb` via `p-pop-a` e repair
instalado via `p-pop-b`; simetricamente, primário de `asbr-ipe-pb` para
`pe-ipe-ce` via `p-ipe-rn` e repair via `p-ipe-ba`.

![Losango do PoP-PB com falha no enlace primário: o reparo pré-computado desvia por p-pop-b e aparece no CEF como backup Local-LFA; ao lado, a lista do que não está provado - tempo de restauração, detecção sem BFD e encaminhamento real](images/bgp-lu/diagram-ti-lfa-reparo.svg#only-light)
![Losango do PoP-PB com falha no enlace primário: o reparo pré-computado desvia por p-pop-b e aparece no CEF como backup Local-LFA; ao lado, a lista do que não está provado - tempo de restauração, detecção sem BFD e encaminhamento real](images/bgp-lu/diagram-ti-lfa-reparo-escuro.svg#only-dark)

**É esperado que a saída classifique o reparo como `Local-LFA`, mesmo com TI-LFA
habilitado.** Neste losango o vizinho do outro ramo já satisfaz a condição de
LFA clássico, então não é preciso uma lista de reparo com segmentos remotos. Não
há contradição. Para ver uma repair list de múltiplos segmentos é preciso uma
topologia onde nenhum LFA local atenda - é o que fazem os labs de
[TI-LFA](../TI‑LFA/index.md).

O que **não** é aceitável é inferir reparo a partir de uma segunda rota na RIB
sem confirmar CEF/FRR.

Ensaio de falha, com `shutdown` na interface primária: em XRd CP dá para
observar a mudança de RIB/CEF, mas não medir perda. Sem BFD, timestamps e uma
plataforma de forwarding, o ensaio não sustenta nenhuma afirmação sobre 50 ms.

### Estágio 6 - SR Policy explícita e EPE

Entra: `egress-engineering` e `peer-node-sid index 100` nos dois ASBRs;
`extcommunity-set opaque COLOR_100` e `route-policy COLOR_100` em `pe-pop-pb`; a
segment-list e a policy de cor 100.

```text
segment-routing
 traffic-eng
  segment-list INTERAS-BACKUP
   index 10 mpls label 16003
   index 20 mpls label 16004
   index 30 mpls label 15100
   index 40 mpls label 16007
   index 50 mpls label 16008
  !
  policy INTERAS-COLOR-100
   color 100 end-point ipv4 10.0.0.8
   candidate-paths
    preference 100
     explicit segment-list INTERAS-BACKUP
```

![A SR Policy de cor 100 força o caminho pe-pop-pb, p-pop-b, asbr-pop-pb, peer eBGP, p-ipe-ba, pe-ipe-ce; abaixo, os cinco segmentos 16003, 16004, 15100, 16007 e 16008 alinhados ao nó em que cada um se torna ativo](images/bgp-lu/diagram-sr-policy-epe.svg#only-light)
![A SR Policy de cor 100 força o caminho pe-pop-pb, p-pop-b, asbr-pop-pb, peer eBGP, p-ipe-ba, pe-ipe-ce; abaixo, os cinco segmentos 16003, 16004, 15100, 16007 e 16008 alinhados ao nó em que cada um se torna ativo](images/bgp-lu/diagram-sr-policy-epe-escuro.svg#only-dark)

| Ordem | Label | Semântica quando ativo |
|---:|---:|---|
| 1 | `16003` | alcançar `p-pop-b` pelo domínio do PoP |
| 2 | `16004` | alcançar `asbr-pop-pb` pelo domínio do PoP |
| 3 | `15100` | PeerNode SID local de `asbr-pop-pb`: enviar ao peer `asbr-ipe-pb` |
| 4 | `16007` | alcançar `p-ipe-ba` pelo domínio do backbone |
| 5 | `16008` | alcançar `pe-ipe-ce` pelo domínio do backbone |

Um único Node-SID por domínio seguiria o SPF primário. Os cinco segmentos são o
mínimo para forçar os **dois** ramos alternativos e o peer de saída.

O label `15100` vem do índice 100 na SRLB iniciada em `15000`. Diferente de um
Prefix-SID, ele é **local** a `asbr-pop-pb`, e significa "encaminhe ao peer BGP",
não "alcance o Node-SID de `asbr-ipe-pb`". A lista cruza domínios porque `16004`
entrega o pacote ao nó que entende `15100` antes de esse label chegar ao topo.

Em `asbr-pop-pb`:

```text
show bgp egress-engineering
show mpls forwarding labels 15100 detail
```

Em `pe-pop-pb`:

```text
show segment-routing traffic-eng policy color 100
show cef 203.0.113.0/24 detail
```

Aceite: PeerNode SID `15100` associado ao peer `192.0.2.9`; policy Admin e
Operational `up`; candidate path explícito válido com os cinco segmentos na
ordem; Binding SID presente; rota `203.0.113.0/24` associada à cor 100 e ao BSID
da policy; traceroute exibindo, no primeiro salto MPLS, a sequência
`{16004, 15100, 16007, 16008}` depois de o SID inicial sofrer PHP.

Se a sessão de serviço do estágio 4 não formar, o CEF do prefixo de cliente não
recursa na policy: a estrutura pode estar correta e ainda assim o steering não
acontece.

Este exercício configura EPE e policy localmente. Não implementa a solução
centralizada da RFC 9087 - não há controlador, exportação BGP-LS da topologia de
peering nem programação remota. O objeto de data plane demonstrado é o BGP
Peering SID.

## :material-check-decagram: **Verificação**

Cadeia mínima no estado final, a partir de `pe-pop-pb`. Nenhuma saída isolada
prova tudo.

| Comando | O que confirmar |
|---|---|
| `show ospf neighbor` | `FULL` em toda interface de core |
| `show mpls forwarding` | uma entrada por Node-SID do domínio local |
| `show bgp ipv4 labeled-unicast summary` | as três sessões LU `Established` |
| `show bgp ipv4 labeled-unicast 10.0.0.8/32` | rota best, com label e next hop `10.0.0.4` |
| `show cef 10.0.0.8/32 detail` | pilha `{16004, <label BGP>}` via `p-pop-a` |
| `show mpls forwarding labels 16008 detail` em `asbr-ipe-pb` | Prefix-SID anunciado por LU tem ação SR até o PE |
| `show cef 10.0.0.4/32 detail` | backup instalado via `p-pop-b` |
| `show bgp ipv4 unicast summary` | sessão multihop PE-PE `Established` |
| `show bgp egress-engineering` | PeerNode SID `15100` no peer `192.0.2.9` (em `asbr-pop-pb`) |
| `show segment-routing traffic-eng policy color 100` | Admin/Oper `up`, cinco segmentos |
| `show cef 203.0.113.0/24 detail` | prefixo de cliente resolvido pelo BSID da policy |

E o encaminhamento fim a fim:

```bash
docker exec clab-inter-as-bgp-lu-instituicao-pb ping -c 5 203.0.113.10
docker exec clab-inter-as-bgp-lu-instituicao-pb traceroute -e 203.0.113.10
```

Cada pergunta tem sua evidência própria: `show route` responde se o OSPF conhece
o caminho, `show bgp ... labeled-unicast` se o BGP recebeu NLRI e label,
`show mpls label table` quais labels locais existem, `show mpls forwarding` como
um label será encaminhado, e `show cef ... detail` qual recursão e qual pilha um
prefixo usa. Adjacência OSPF `FULL` não prova label forwarding; rota LU válida
não prova que uma sessão multihop atravessa a imagem; SR Policy operacional não
prova que houve tráfego.

### Tempo de estabilização

Este lab é sensível a captura precoce. A sessão eBGP multihop PE-PE depende de
pacotes TCP gerados no próprio PE atravessarem o LSP construído pelos estágios
anteriores. Uma captura feita cedo demais encontra a sessão em `Active`.

Se isso acontecer, **não** conclua que a imagem não encaminha. Confirme primeiro
a recursão do transporte e aguarde a estabilização, esperando estes cinco em
conjunto:

```text
show bgp ipv4 labeled-unicast summary
show bgp ipv4 labeled-unicast 10.0.0.8/32
show cef 10.0.0.8/32 detail
show bgp ipv4 unicast summary
show bgp ipv4 unicast 203.0.113.0/24
```

O gate é estado e alcance, não um temporizador fixo. O que a execução de
referência efetivamente observou está em [`validacao.md`](validacao.md).

## :material-file-document-multiple: **Documentos deste lab**

| Documento | Para que serve |
|---|---|
| [Conceitos de Inter-AS](index.md) | Planos, recursão, Option C e EPE |
| [`guia-aprofundado.md`](guia-aprofundado.md) | Da configuração ao fio: RIB/LIB/LFIB/CEF e pilhas salto a salto |
| [`recorte-rede-ipe.md`](recorte-rede-ipe.md) | Evidência do mapa, método de seleção e limites da analogia |
| [`validacao.md`](validacao.md) | O que a execução de referência confirmou, e o que não |

## :material-book-open-variant: **Referências**

- [Panorama de Tráfego da Rede Ipê](https://redeipe.rnp.br/panorama)
- RFC 8277 - *Using BGP to Bind MPLS Labels to Address Prefixes*: <https://www.rfc-editor.org/rfc/rfc8277.html>
- RFC 9087 - *Segment Routing Centralized BGP Egress Peer Engineering*: <https://www.rfc-editor.org/rfc/rfc9087.html>
- RFC 9256 - *Segment Routing Policy Architecture*: <https://www.rfc-editor.org/rfc/rfc9256.html>
- RFC 9855 - *Topology Independent Fast Reroute Using Segment Routing*: <https://www.rfc-editor.org/rfc/rfc9855.html>
- RFC 4364 seção 10 - contexto das opções inter-AS: <https://www.rfc-editor.org/rfc/rfc4364.html>
- Cisco - [Configure Inter-AS Option C MPLS VPN With Cisco IOS and Cisco IOS-XR](https://www.cisco.com/c/en/us/support/docs/multiprotocol-label-switching-mpls/mpls/200523-Configuration-and-Verification-of-Layer.html)
- [Containerlab - Cisco XRd kind](https://containerlab.dev/manual/kinds/xrd/)

Lista completa das fontes, incluindo as do recorte público, em
[documento conceitual de Inter-AS](index.md#referencias).
