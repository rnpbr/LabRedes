# SR-TE: Explicit Policy sobre a Rede Ipê

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/sr-te/explicit-policy">`labs/cisco/sr-mpls/sr-te/explicit-policy`</a>.

!!! info "Pré-requisitos"
    [conceitos de SR-TE](index.md), [base Cisco](../02-base-sr-mpls.md) e [ambiente XRd](../01-preparacao-do-ambiente.md).

## :material-bookmark: **O que este lab demonstra**

O caminho IGP entre Fortaleza (CE) e Rio de Janeiro (RJ) passa pelo hub em São Paulo (SP), custo 20, ~40ms de latência. Existe um caminho alternativo via Salvador (BA) e Belo Horizonte (MG), custo 38, ~26ms - mais longo em custo IGP, mais curto em latência real. O IGP nunca escolheria essa rota sozinho.

Uma SR Policy no PoP-CE força o tráfego sensível a latência (videoconferência, VoIP) por CE -> BA -> MG -> RJ via segment list explícita, enquanto o tráfego best-effort continua pelo caminho padrão CE -> SP -> RJ. Os dois caminhos coexistem: o IGP não é alterado, e apenas o headend (PoP-CE) carrega a policy.

!!! note "Observação"
    As métricas OSPF deste lab são deliberadamente opostas ao delay real (custo baixo no caminho de maior latência), para reproduzir de forma determinística um cenário onde o caminho de menor custo IGP não é o de menor latência - situação comum quando um hub tem capacidade/prioridade de roteamento mas não é o mais próximo fisicamente.

## :material-lightbulb-on-outline: **Conceitos aplicados**

- **Waypoint**: nó intermediário incluído explicitamente na segment list. Aqui, PoP-BA e PoP-MG.
- **DSCP EF / Color**: em produção a policy seria selecionada por Color BGP e o tráfego direcionado por marcação DSCP; este lab simplifica o steering via rota estática `sr-policy`.
- **SRGB compartilhado**: SRGB 16000-23999 em todos os PoPs. Label = `16000 + SID index`.

## :material-lan: **Topologia**

![Topologia SR-TE Rede Ipê](images/explicit-policy/topology-explicit-policy.png)

Caminho em destaque (CE -> BA -> MG -> RJ): forçado pela SR Policy. Caminho padrão (CE -> SP -> RJ): ativo para tráfego best-effort.

| PoP | Papel | Localização | Loopback0 | SID index | Label |
|---|---|---|---|---:|---:|
| PoP-CE | Headend | Fortaleza | 10.0.0.1/32 | 100 | 16100 |
| PoP-SP | Hub IGP | São Paulo | 10.0.0.2/32 | 200 | 16200 |
| PoP-BA | Waypoint 1 | Salvador | 10.0.0.3/32 | 300 | 16300 |
| PoP-MG | Waypoint 2 | Belo Horizonte | 10.0.0.4/32 | 350 | 16350 |
| PoP-RJ | Egress | Rio de Janeiro | 10.0.0.5/32 | 400 | 16400 |

| Enlace | IP A | IP B | Custo OSPF | Delay real (simulado) |
|---|---|---|---:|---:|
| CE <-> SP | 192.0.2.0/31 | 192.0.2.1/31 | 10 | ~30ms |
| CE <-> BA | 192.0.2.2/31 | 192.0.2.3/31 | 20 | ~8ms |
| SP <-> RJ | 192.0.2.4/31 | 192.0.2.5/31 | 10 | ~10ms |
| BA <-> MG | 192.0.2.6/31 | 192.0.2.7/31 | 8 | ~8ms |
| MG <-> RJ | 192.0.2.8/31 | 192.0.2.9/31 | 10 | ~10ms |

Caminho IGP (best-path): CE-SP-RJ, custo 20, ~40ms. Caminho SR-TE (forçado): CE-BA-MG-RJ, custo 38, ~26ms.

Os SID index saltam de 100 em 100 (100/200/300/350/400) de propósito - reserva faixa para SIDs por algoritmo (Flex-Algo) ou por serviço sem precisar renumerar os PoPs existentes.

## :material-rocket-launch: **Deploy**

```bash
git clone https://github.com/rnpbr/LabRedes-segmentrouting.git
cd LabRedes-segmentrouting
cd labs/cisco/sr-mpls/sr-te/explicit-policy
sudo clab deploy -t lab.clab.yml
```

Cinco nós pedem de 6 a 8 GB de RAM. Gerência de `172.20.20.11` a `172.20.20.15`, na ordem CE, SP, BA, MG, RJ.

A SR Policy está só em `configs/pop-ce.cfg`. Os outros PoPs sobem com a base SR-MPLS e as métricas ajustadas.

Acesso: `ssh clab@172.20.20.11`, senha `clab@123`. Ou `sudo docker exec -it clab-sr-te-explicit-policy-pop-ce /pkg/bin/xr_cli.sh`.

![clab deploy do lab](images/explicit-policy/terminal-deploy.png)

!!! warning "Atenção"
    A captura é de uma execução anterior, quando o arquivo se chamava `sr-te-rede-ipe.clab.yml`. Rede de gerência, nomes de nó e IPs são os mesmos.

```bash
# Derrubar o lab
sudo clab destroy -t lab.clab.yml --cleanup
```

## Arquivos do laboratório

Todos os arquivos estão no repositório, em <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/labs/cisco/sr-mpls/sr-te/explicit-policy">`labs/cisco/sr-mpls/sr-te/explicit-policy`</a>. Os blocos abaixo mostram o conteúdo completo de cada um para consulta rápida.

??? example "lab.clab.yml"

    ```yaml
    # SR-TE Explicit Policy
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
    #   startup-config: https://raw.githubusercontent.com/rnpbr/LabRedes-segmentrouting/main/labs/cisco/sr-mpls/sr-te/explicit-policy/configs/pop-sp.cfg
    # Ref: https://containerlab.dev/manual/config-mgmt/#remote
    #
    # enforce-startup-config faz todo deploy reaplicar o .cfg, em vez de reusar a
    # config gravada por uma execucao anterior.

    name: sr-te-explicit-policy

    mgmt:
      network: mgmt-rede-ipe
      ipv4-subnet: 172.20.20.0/24

    topology:
      defaults:
        kind: cisco_xrd

      kinds:
        cisco_xrd:
          image: ios-xr/xrd-control-plane:7.10.2
          enforce-startup-config: false

      nodes:
        pop-ce:
          mgmt-ipv4: 172.20.20.11
    #      startup-config: configs/pop-ce.cfg
        pop-sp:
          mgmt-ipv4: 172.20.20.12
    #      startup-config: configs/pop-sp.cfg
        pop-ba:
          mgmt-ipv4: 172.20.20.13
          startup-config: configs/pop-ba.cfg
        pop-mg:
          mgmt-ipv4: 172.20.20.14
    #      startup-config: configs/pop-mg.cfg
        pop-rj:
          mgmt-ipv4: 172.20.20.15
    #      startup-config: configs/pop-rj.cfg

      links:
        # CE-SP: custo 10, ~30ms
        - endpoints: ["pop-ce:Gi0-0-0-0", "pop-sp:Gi0-0-0-0"]
        # CE-BA: custo 20, ~8ms
        - endpoints: ["pop-ce:Gi0-0-0-1", "pop-ba:Gi0-0-0-0"]
        # SP-RJ: custo 10, ~10ms
        - endpoints: ["pop-sp:Gi0-0-0-1", "pop-rj:Gi0-0-0-0"]
        # BA-MG: custo 8, ~8ms
        - endpoints: ["pop-ba:Gi0-0-0-1", "pop-mg:Gi0-0-0-0"]
        # MG-RJ: custo 10, ~10ms
        - endpoints: ["pop-mg:Gi0-0-0-1", "pop-rj:Gi0-0-0-1"]
    ```

??? example "configs/pop-ba.cfg"

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
    ! Lab SR-TE Explicit Policy - Rede Ipe / no POP-BA
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block  15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.3 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description pop-ba to pop-ce
     ipv4 address 192.0.2.3 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description pop-ba to pop-mg
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
       prefix-sid index 300
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 20
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 8
      !
     !
    !
    !
    end
    ```

??? example "configs/pop-ce.cfg"

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
      10.0.0.5/32 sr-policy srte_c_100_ep_10.0.0.5
     !
    !
    !
    ! ==========================================================================
    ! Lab SR-TE Explicit Policy - Rede Ipe / no POP-CE
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block  15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.1 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description pop-ce to pop-sp
     ipv4 address 192.0.2.0 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description pop-ce to pop-ba
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
       prefix-sid index 100
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 10
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 20
      !
     !
    !
    segment-routing
     traffic-eng
      segment-list SR-BEST-PATH
       index 10 mpls label 16300
       index 20 mpls label 16350
       index 30 mpls label 16400
      !
      policy LATENCIA-BAIXA
       color 100 end-point ipv4 10.0.0.5
       binding-sid mpls 15100
       candidate-paths
        preference 100
         explicit segment-list SR-BEST-PATH
        !
       !
      !
     !
    !
    !
    !
    end
    ```

??? example "configs/pop-mg.cfg"

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
    ! Lab SR-TE Explicit Policy - Rede Ipe / no POP-MG
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block  15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.4 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description pop-mg to pop-ba
     ipv4 address 192.0.2.7 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description pop-mg to pop-rj
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
       prefix-sid index 350
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 8
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 10
      !
     !
    !
    !
    end
    ```

??? example "configs/pop-rj.cfg"

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
    ! Lab SR-TE Explicit Policy - Rede Ipe / no POP-RJ
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block  15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.5 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description pop-rj to pop-sp
     ipv4 address 192.0.2.5 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description pop-rj to pop-mg
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
       prefix-sid index 400
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 10
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 10
      !
     !
    !
    !
    end
    ```

??? example "configs/pop-sp.cfg"

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
    ! Lab SR-TE Explicit Policy - Rede Ipe / no POP-SP
    ! ==========================================================================
    !
    segment-routing global-block 16000 23999
    segment-routing local-block  15000 15999
    !
    interface Loopback0
     ipv4 address 10.0.0.2 255.255.255.255
    !
    interface GigabitEthernet0/0/0/0
     description pop-sp to pop-ce
     ipv4 address 192.0.2.1 255.255.255.254
     no shutdown
    !
    interface GigabitEthernet0/0/0/1
     description pop-sp to pop-rj
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
       prefix-sid index 200
      !
      interface GigabitEthernet0/0/0/0
       network point-to-point
       cost 10
      !
      interface GigabitEthernet0/0/0/1
       network point-to-point
       cost 10
      !
     !
    !
    !
    end
    ```

---



## :material-cog: **A policy, em detalhe**

Trecho relevante de `configs/pop-ce.cfg` (o restante segue a [base SR-MPLS no IOS-XR](../02-base-sr-mpls.md)):

```text
segment-routing
 traffic-eng
  segment-list SR-BEST-PATH
   index 10 mpls label 16300
   index 20 mpls label 16350
   index 30 mpls label 16400
  !
  policy LATENCIA-BAIXA
   color 100 end-point ipv4 10.0.0.5
   binding-sid mpls 15100
   candidate-paths
    preference 100
     explicit segment-list SR-BEST-PATH
!
router static
 address-family ipv4 unicast
  10.0.0.5/32 sr-policy srte_c_100_ep_10.0.0.5
```

A segment list `[16300, 16350, 16400]` é literalmente a sequência de Node-SIDs de BA, MG e RJ - o headend empilha os três, e cada nó intermediário faz pop do seu próprio label e encaminha nativamente para o próximo. A rota estática redireciona `10.0.0.5/32` (loopback de PoP-RJ) para a policy pelo nome gerado automaticamente pelo IOS-XR (`srte_c_<color>_ep_<endpoint>`).

## :material-check-decagram: **Verificação**

Executar em PoP-CE.

**Adjacências OSPF**

```
show ospf neighbor
```

![show ospf neighbor em PoP-CE](images/explicit-policy/terminal-ospf-neighbor.png)

Esperado: PoP-SP e PoP-BA em `FULL`.

**Policy ativa**

```
show segment-routing traffic-eng policy color 100
```

![show segment-routing traffic-eng policy color 100](images/explicit-policy/terminal-sr-policy.png)

Esperado: `Admin: up, Oper: up`, segment list `[16300, 16350, 16400]`.

**Forwarding**

```
show mpls forwarding
```

![show mpls forwarding em PoP-CE](images/explicit-policy/terminal-mpls-forwarding.png)

A entrada do label `16400` (PoP-RJ) aponta para `srte_c_100_e...` (a policy), não para PoP-SP como o IGP nativo escolheria - confirma que o steering está ativo.

**Caminho de dados**

```
traceroute 10.0.0.5 source 10.0.0.1
```

![traceroute de PoP-CE para PoP-RJ](images/explicit-policy/terminal-traceroute.png)

Esperado: caminho via PoP-BA e PoP-MG, nunca via PoP-SP. A rota estática já força `10.0.0.5/32` para a policy, então mesmo um traceroute IP comum reflete o caminho de TE.

`traceroute sr-mpls policy name` requer MPLS OAM completo, indisponível na imagem control-plane usada aqui - os comandos acima são o equivalente funcional para este lab.

## :material-book-open-variant: **Referências**

- [Panorama Rede Ipê](https://redeipe.rnp.br/panorama)
- [Containerlab - Cisco XRd kind](https://containerlab.dev/manual/kinds/xrd/)
- RFC 9256 - *Segment Routing Policy Architecture*: <https://datatracker.ietf.org/doc/html/rfc9256>
- [Cisco IOS-XR SR-TE Configuration Guide](https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/710x/configuration/guide/b-segment-routing-cg-cisco8000-710x/configure-sr-te-policies.html)
- [Segment Routing Traffic Engineering Tutorial](https://www.segment-routing.net/tutorials/2017-03-06-segment-routing-traffic-engineering-srte/)
