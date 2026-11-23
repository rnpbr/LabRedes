# Lab Cisco XRd SR-MPLS de 5 nós (referência)

!!! info "Repositório"
    Este conteúdo vem do repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**. Arquivos deste laboratório: <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/tree/main/docs/references/cisco-sr-mpls-5node/labs-aprendizado">`docs/references/cisco-sr-mpls-5node/labs-aprendizado`</a>.

!!! info "Material de referência"
    Material de origem desta trilha, escrito originalmente em inglês, traduzido aqui e preservado como referência histórica. A versão canônica em português dos conceitos e convenções está na [base SR-MPLS no IOS-XR](02-base-sr-mpls.md). A topologia deste material está em <a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting/blob/main/docs/references/cisco-sr-mpls-5node/labs-aprendizado/lab.clab.yml">`docs/references/cisco-sr-mpls-5node/labs-aprendizado/lab.clab.yml`</a>.

Este laboratório usa cinco roteadores Cisco XRd control-plane com a imagem `xrd-control-plane:7.10.2`.

```text
             p1
          /      \
       pe1        pe2
          \      /
             p2

          p1 -- p3 -- p2
```

O caminho adicional por `p3` permite testar ECMP, caminhos de SR Policy diferentes do mais curto, caminhos de backup do TI-LFA e restrições de Flex-Algo sem aumentar demais o laboratório.

## O que este laboratório cobre

- Prefix-SIDs e Node-SIDs SR-MPLS no OSPFv2
- Comportamento do SRGB e do SRLB
- Adjacency-SIDs do OSPF
- ECMP e alteração de métricas OSPF
- Políticas SR-TE explícitas com segment lists de labels MPLS
- Direcionamento de tráfego para uma SR Policy por rota estática
- Proteção de enlace e de nó com TI-LFA
- Fundamentos de Flexible Algorithm no OSPF
- Comandos de verificação e OAM de SR/MPLS

Este laboratório, só com XRd, não cobre por completo L3VPN, EVPN, fluxos com SR-PCE/controlador, SR interdomínio, SRv6 nem medições de convergência em hardware. Esses são os próximos laboratórios naturais.

## Subir o laboratório

```bash
git clone https://github.com/rnpbr/LabRedes-segmentrouting.git
cd LabRedes-segmentrouting/docs/references/cisco-sr-mpls-5node/labs-aprendizado
sudo containerlab deploy -t lab.clab.yml
```

Acessar o IOS XR:

```bash
docker exec -it clab-cisco-sr-mpls-5node-pe1 /pkg/bin/xr_cli.sh
docker exec -it clab-cisco-sr-mpls-5node-p1 /pkg/bin/xr_cli.sh
docker exec -it clab-cisco-sr-mpls-5node-p2 /pkg/bin/xr_cli.sh
docker exec -it clab-cisco-sr-mpls-5node-p3 /pkg/bin/xr_cli.sh
docker exec -it clab-cisco-sr-mpls-5node-pe2 /pkg/bin/xr_cli.sh
```

O acesso por SSH também está disponível, com usuário `clab` e senha `clab@123`.

## Interfaces e endereços

O Containerlab usa nomes de interface XRd separados por hífen, como `Gi0-0-0-0`. O IOS XR enxerga a mesma porta como `GigabitEthernet0/0/0/0`.

| Enlace | Lado A | Endereço | Lado B | Endereço |
| --- | --- | --- | --- | --- |
| pe1-p1 | pe1 Gi0/0/0/0 | 192.0.2.0/31 | p1 Gi0/0/0/0 | 192.0.2.1/31 |
| pe1-p2 | pe1 Gi0/0/0/1 | 192.0.2.2/31 | p2 Gi0/0/0/0 | 192.0.2.3/31 |
| p1-pe2 | p1 Gi0/0/0/1 | 192.0.2.4/31 | pe2 Gi0/0/0/0 | 192.0.2.5/31 |
| p2-pe2 | p2 Gi0/0/0/1 | 192.0.2.6/31 | pe2 Gi0/0/0/1 | 192.0.2.7/31 |
| p1-p3 | p1 Gi0/0/0/2 | 192.0.2.8/31 | p3 Gi0/0/0/0 | 192.0.2.9/31 |
| p3-p2 | p3 Gi0/0/0/1 | 192.0.2.10/31 | p2 Gi0/0/0/2 | 192.0.2.11/31 |

| Nó | Loopback0 | Índice do Prefix-SID | Label com SRGB 16000 |
| --- | --- | ---: | ---: |
| pe1 | 10.0.0.1/32 | 1 | 16001 |
| p1 | 10.0.0.2/32 | 2 | 16002 |
| p2 | 10.0.0.3/32 | 3 | 16003 |
| p3 | 10.0.0.4/32 | 4 | 16004 |
| pe2 | 10.0.0.5/32 | 5 | 16005 |

O laboratório usa o SRLB padrão, `15000-15999`, para segmentos locais alocados manualmente, como Adjacency-SIDs e Binding-SIDs.

## Configuração base OSPFv2 SR-MPLS

Cole o bloco correspondente em cada roteador.

### pe1

```text
configure
hostname pe1
segment-routing global-block 16000 23999
segment-routing local-block 15000 15999
!
interface Loopback0
 ipv4 address 10.0.0.1 255.255.255.255
!
interface GigabitEthernet0/0/0/0
 description pe1 to p1
 ipv4 address 192.0.2.0 255.255.255.254
 no shutdown
!
interface GigabitEthernet0/0/0/1
 description pe1 to p2
 ipv4 address 192.0.2.2 255.255.255.254
 no shutdown
!
router ospf 1
 router-id 10.0.0.1
 segment-routing mpls
 segment-routing sr-prefer
 area 0
  segment-routing mpls
  interface Loopback0
   passive enable
   prefix-sid index 1
  !
  interface GigabitEthernet0/0/0/0
   network point-to-point
  !
  interface GigabitEthernet0/0/0/1
   network point-to-point
  !
 !
!
commit
end
```

### p1

```text
configure
hostname p1
segment-routing global-block 16000 23999
segment-routing local-block 15000 15999
!
interface Loopback0
 ipv4 address 10.0.0.2 255.255.255.255
!
interface GigabitEthernet0/0/0/0
 description p1 to pe1
 ipv4 address 192.0.2.1 255.255.255.254
 no shutdown
!
interface GigabitEthernet0/0/0/1
 description p1 to pe2
 ipv4 address 192.0.2.4 255.255.255.254
 no shutdown
!
interface GigabitEthernet0/0/0/2
 description p1 to p3
 ipv4 address 192.0.2.8 255.255.255.254
 no shutdown
!
router ospf 1
 router-id 10.0.0.2
 segment-routing mpls
 segment-routing sr-prefer
 area 0
  segment-routing mpls
  interface Loopback0
   passive enable
   prefix-sid index 2
  !
  interface GigabitEthernet0/0/0/0
   network point-to-point
  !
  interface GigabitEthernet0/0/0/1
   network point-to-point
  !
  interface GigabitEthernet0/0/0/2
   network point-to-point
  !
 !
!
commit
end
```

### p2

```text
configure
hostname p2
segment-routing global-block 16000 23999
segment-routing local-block 15000 15999
!
interface Loopback0
 ipv4 address 10.0.0.3 255.255.255.255
!
interface GigabitEthernet0/0/0/0
 description p2 to pe1
 ipv4 address 192.0.2.3 255.255.255.254
 no shutdown
!
interface GigabitEthernet0/0/0/1
 description p2 to pe2
 ipv4 address 192.0.2.6 255.255.255.254
 no shutdown
!
interface GigabitEthernet0/0/0/2
 description p2 to p3
 ipv4 address 192.0.2.11 255.255.255.254
 no shutdown
!
router ospf 1
 router-id 10.0.0.3
 segment-routing mpls
 segment-routing sr-prefer
 area 0
  segment-routing mpls
  interface Loopback0
   passive enable
   prefix-sid index 3
  !
  interface GigabitEthernet0/0/0/0
   network point-to-point
  !
  interface GigabitEthernet0/0/0/1
   network point-to-point
  !
  interface GigabitEthernet0/0/0/2
   network point-to-point
  !
 !
!
commit
end
```

### p3

```text
configure
hostname p3
segment-routing global-block 16000 23999
segment-routing local-block 15000 15999
!
interface Loopback0
 ipv4 address 10.0.0.4 255.255.255.255
!
interface GigabitEthernet0/0/0/0
 description p3 to p1
 ipv4 address 192.0.2.9 255.255.255.254
 no shutdown
!
interface GigabitEthernet0/0/0/1
 description p3 to p2
 ipv4 address 192.0.2.10 255.255.255.254
 no shutdown
!
router ospf 1
 router-id 10.0.0.4
 segment-routing mpls
 segment-routing sr-prefer
 area 0
  segment-routing mpls
  interface Loopback0
   passive enable
   prefix-sid index 4
  !
  interface GigabitEthernet0/0/0/0
   network point-to-point
  !
  interface GigabitEthernet0/0/0/1
   network point-to-point
  !
 !
!
commit
end
```

### pe2

```text
configure
hostname pe2
segment-routing global-block 16000 23999
segment-routing local-block 15000 15999
!
interface Loopback0
 ipv4 address 10.0.0.5 255.255.255.255
!
interface GigabitEthernet0/0/0/0
 description pe2 to p1
 ipv4 address 192.0.2.5 255.255.255.254
 no shutdown
!
interface GigabitEthernet0/0/0/1
 description pe2 to p2
 ipv4 address 192.0.2.7 255.255.255.254
 no shutdown
!
router ospf 1
 router-id 10.0.0.5
 segment-routing mpls
 segment-routing sr-prefer
 area 0
  segment-routing mpls
  interface Loopback0
   passive enable
   prefix-sid index 5
  !
  interface GigabitEthernet0/0/0/0
   network point-to-point
  !
  interface GigabitEthernet0/0/0/1
   network point-to-point
  !
 !
!
commit
end
```

## Verificação inicial

Execute primeiro em `pe1`:

```text
show ospf neighbor
show ospf routes
show ospf segment-routing prefix-sid-map active-policy
show route 10.0.0.5/32 detail
show mpls forwarding
show mpls label table 0 label 16005 detail
ping 10.0.0.5 source 10.0.0.1
traceroute 10.0.0.5 source 10.0.0.1
```

Resultado esperado: `pe1` deve ter dois caminhos de mesmo custo até `pe2`, um por `p1` e outro por `p2`. O Prefix-SID de `pe2` tem índice `5`, então o label SR é `16005`.

## Lab 1: ECMP e métricas OSPF

A partir de `pe1`, os dois caminhos diretos pelo core devem ter o mesmo custo:

```text
show route 10.0.0.5/32 detail
```

Torne o caminho por `p2` menos preferido:

```text
configure
router ospf 1
 area 0
  interface GigabitEthernet0/0/0/1
   cost 50
  !
 !
!
commit
end
```

Confirme que `pe1` agora prefere `p1`:

```text
show ospf routes 10.0.0.5/32
show route 10.0.0.5/32 detail
show mpls forwarding labels 16005
```

Restaure o ECMP:

```text
configure
router ospf 1
 area 0
  interface GigabitEthernet0/0/0/1
   no cost
  !
 !
!
commit
end
```

## Lab 2: Adjacency-SIDs manuais

O OSPF cria Adjacency-SIDs dinâmicos automaticamente. Adjacency-SIDs manuais são úteis quando se quer labels locais estáveis para caminhos explícitos ou para fluxos com controlador. O label tem significado local e é alocado do SRLB.

Configure Adjacency-SIDs manuais protegidos em `pe1`:

```text
configure
router ospf 1
 area 0
  interface GigabitEthernet0/0/0/0
   adjacency-sid index 11 protected
  !
  interface GigabitEthernet0/0/0/1
   adjacency-sid index 12 protected
  !
 !
!
commit
end
```

Verifique:

```text
show mpls label table 0 detail
show ospf database opaque-area self-originate
show mpls forwarding
```

Os labels exatos são a base do SRLB mais o índice configurado. Com a base padrão `15000`, o índice `11` corresponde ao label `15011` e o índice `12`, ao label `15012`.

## Lab 3: SR Policy explícita passando por p3

Os caminhos mais curtos nativos de `pe1` até `pe2` são:

```text
pe1-p1-pe2
pe1-p2-pe2
```

Crie em `pe1` uma SR Policy que force o tráfego pelo caminho mais longo:

```text
pe1-p1-p3-p2-pe2
```

Esta segment list usa labels de Node-SID:

| Segmento | Significado |
| --- | --- |
| `16002` | alcançar `p1` |
| `16004` | em seguida, alcançar `p3` |
| `16003` | em seguida, alcançar `p2` |
| `16005` | em seguida, alcançar `pe2` |

Configure a policy em `pe1`:

```text
configure
segment-routing
 traffic-eng
  logging
   policy status
  !
  segment-list PE1_P1_P3_P2_PE2
   index 10 mpls label 16002
   index 20 mpls label 16004
   index 30 mpls label 16003
   index 40 mpls label 16005
  !
  policy PE1_TO_PE2_VIA_P3
   binding-sid mpls 15090
   color 100 end-point ipv4 10.0.0.5
   candidate-paths
    preference 100
     explicit segment-list PE1_P1_P3_P2_PE2
     !
    !
   !
  !
 !
!
commit
end
```

Verifique a policy:

```text
show segment-routing traffic-eng policy color 100
show segment-routing traffic-eng policy name srte_c_100_ep_10.0.0.5
show mpls forwarding labels 15090
show mpls label table 0 label 15090 detail
```

A policy deve estar operacionalmente `up` e mostrar a segment list explícita. O label `15090` é o Binding-SID da policy. Um Binding-SID tem significado local no roteador headend e representa a policy inteira.

## Lab 4: Direcionamento para a SR Policy por rota estática

Adicione um destino de teste em `pe2`:

```text
configure
interface Loopback100
 description SR policy test endpoint
 ipv4 address 203.0.113.5 255.255.255.255
!
commit
end
```

Em `pe1`, direcione `203.0.113.5/32` para a SR Policy. O IOS XR usa na RIB o nome gerado da SR Policy, então confira o nome primeiro:

```text
show segment-routing traffic-eng policy color 100
```

Depois configure a rota estática:

```text
configure
router static
 address-family ipv4 unicast
  203.0.113.5/32 sr-policy srte_c_100_ep_10.0.0.5
 !
!
commit
end
```

Verifique:

```text
show route 203.0.113.5/32 detail
ping 203.0.113.5 source 10.0.0.1
traceroute 203.0.113.5 source 10.0.0.1
```

Resultado esperado: a rota deve ser conhecida via `static` e resolver pela policy SR-TE em direção a `10.0.0.5`.

## Lab 5: TI-LFA

O TI-LFA calcula caminhos de reparo pré-instalados para falhas de enlace, de nó ou de SRLG. Configure-o nas interfaces OSPF voltadas para o core.

Em `pe1`:

```text
configure
router ospf 1
 area 0
  interface GigabitEthernet0/0/0/0
   fast-reroute per-prefix
   fast-reroute per-prefix ti-lfa
   fast-reroute per-prefix tiebreaker node-protecting index 200
  !
  interface GigabitEthernet0/0/0/1
   fast-reroute per-prefix
   fast-reroute per-prefix ti-lfa
   fast-reroute per-prefix tiebreaker node-protecting index 200
  !
 !
!
commit
end
```

Repita o mesmo padrão em todas as interfaces OSPF que não sejam loopback em `p1`, `p2`, `p3` e `pe2`.

Verifique a partir de `pe1`:

```text
show route 10.0.0.5/32 detail
show cef ipv4 10.0.0.5/32 detail
show ospf routes 10.0.0.5/32
```

Depois derrube um dos caminhos e observe a rota continuar instalada por um caminho de reparo:

```text
configure
interface GigabitEthernet0/0/0/0
 shutdown
!
commit
end
```

Verifique e, em seguida, restaure:

```text
show ospf neighbor
show route 10.0.0.5/32 detail
show mpls forwarding labels 16005
```

```text
configure
interface GigabitEthernet0/0/0/0
 no shutdown
!
commit
end
```

## Lab 6: Flexible Algorithm

O Flex-Algo permite que o IGP calcule um SPF alternativo, com outro algoritmo e outras restrições. Este exemplo define o algoritmo `128` para excluir os enlaces marcados com a cor `red`.

O objetivo é fazer o algoritmo `128` evitar estes enlaces diretos:

```text
pe1-p2
p1-pe2
```

Isso deixa este caminho de `pe1` até `pe2`:

```text
pe1-p1-p3-p2-pe2
```

Configure a mesma definição de Flex-Algo e o mesmo mapa de afinidades em todos os roteadores:

```text
configure
router ospf 1
 flex-algo 128
  advertise-definition
  priority 200
  affinity exclude-any
   red
  !
 !
 affinity-map
  color red bit-position 10
 !
!
commit
end
```

Adicione Prefix-SIDs específicos do algoritmo. Use o índice correspondente em cada roteador:

| Nó | Índice do SID Flex-Algo 128 | Label com SRGB 16000 |
| --- | ---: | ---: |
| pe1 | 101 | 16101 |
| p1 | 102 | 16102 |
| p2 | 103 | 16103 |
| p3 | 104 | 16104 |
| pe2 | 105 | 16105 |

Exemplo para `pe1`:

```text
configure
router ospf 1
 area 0
  interface Loopback0
   prefix-sid algorithm 128 index 101
  !
 !
!
commit
end
```

Use `102` em `p1`, `103` em `p2`, `104` em `p3` e `105` em `pe2`.

Marque os dois lados do enlace `pe1-p2` com a cor `red`:

```text
! pe1
configure
router ospf 1
 area 0
  interface GigabitEthernet0/0/0/1
   flex-algo affinity
    color red
   !
  !
 !
!
commit
end
```

```text
! p2
configure
router ospf 1
 area 0
  interface GigabitEthernet0/0/0/0
   flex-algo affinity
    color red
   !
  !
 !
!
commit
end
```

Marque os dois lados do enlace `p1-pe2` com a cor `red`:

```text
! p1
configure
router ospf 1
 area 0
  interface GigabitEthernet0/0/0/1
   flex-algo affinity
    color red
   !
  !
 !
!
commit
end
```

```text
! pe2
configure
router ospf 1
 area 0
  interface GigabitEthernet0/0/0/0
   flex-algo affinity
    color red
   !
  !
 !
!
commit
end
```

Verifique:

```text
show ospf topology summary
show ospf routes flex-algo 128
show route 10.0.0.5/32 detail
show mpls label table 0 label 16105 detail
```

O algoritmo padrão continua usando o SPF normal do OSPF. O algoritmo `128` calcula um caminho restrito que exclui os enlaces `red`. O label Flex-Algo de `pe2` é `16105`.

## Lab 7: OAM de SR/MPLS

Alcançabilidade IP básica:

```text
ping 10.0.0.5 source 10.0.0.1
traceroute 10.0.0.5 source 10.0.0.1
```

Verificação do encaminhamento MPLS e dos labels:

```text
show mpls forwarding
show mpls forwarding labels 15090
show mpls label table 0 label 16005 detail
show mpls label table 0 label 16105 detail
```

O `ping` e o `traceroute` MPLS Nil-FEC testam uma pilha de labels escolhida. A partir de `pe1`, isto testa a pilha explícita do caminho `pe1-p1-p3-p2-pe2`:

```text
ping mpls nil-fec labels 16002,16004,16003,16005 output interface GigabitEthernet0/0/0/0 nexthop 192.0.2.1
traceroute mpls nil-fec labels 16002,16004,16003,16005 output interface GigabitEthernet0/0/0/0 nexthop 192.0.2.1
```

Se a imagem XRd control-plane aceitar os comandos mas não retornar resultados úteis de data plane, use as verificações de plano de controle:

```text
show ospf database opaque-area
show ospf segment-routing prefix-sid-map active-policy
show segment-routing traffic-eng policy color 100
show route 203.0.113.5/32 detail
```

## Desfazer as alterações

Remova a rota estática de direcionamento:

```text
configure
router static
 address-family ipv4 unicast
  no 203.0.113.5/32 sr-policy srte_c_100_ep_10.0.0.5
 !
!
commit
end
```

Remova a SR Policy:

```text
configure
segment-routing
 traffic-eng
  no policy PE1_TO_PE2_VIA_P3
  no segment-list PE1_P1_P3_P2_PE2
 !
!
commit
end
```

Derrube o laboratório:

```bash
sudo containerlab destroy -t lab.clab.yml --cleanup
```

## Referências

- Containerlab, kind Cisco XRd: <https://containerlab.dev/manual/kinds/xrd/>
- Cisco IOS XR 7.10.x, OSPF SR-MPLS: <https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/710x/configuration/guide/b-segment-routing-cg-cisco8000-710x/configuring-segment-routing-for-ospf-protocol.html>
- Cisco IOS XR 7.10.x, SRGB e SRLB: <https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/710x/configuration/guide/b-segment-routing-cg-cisco8000-710x/configuring-sr-global-block-and-sr-local-block.html>
- Cisco IOS XR 7.10.x, políticas SR-TE: <https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/710x/configuration/guide/b-segment-routing-cg-cisco8000-710x/configuring-sr-te-policy.html>
- Cisco IOS XR 7.10.x, TI-LFA: <https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/710x/configuration/guide/b-segment-routing-cg-cisco8000-710x/configuring-topology-independent-loop-free-alternate.html>
- Cisco IOS XR 7.10.x, Flexible Algorithm: <https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/710x/configuration/guide/b-segment-routing-cg-cisco8000-710x/enabling-segment-routing-flexible-algorithm.html>
- Cisco IOS XR 7.10.x, OAM de SR: <https://www.cisco.com/c/en/us/td/docs/iosxr/cisco8000/segment-routing/710x/configuration/guide/b-segment-routing-cg-cisco8000-710x/using-segment-routing-oam.html>
