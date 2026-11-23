# Preparação do ambiente

!!! info "Repositório"
    Os laboratórios e roteiros originais estão no repositório **<a target="_blank" href="https://github.com/rnpbr/LabRedes-segmentrouting">github.com/rnpbr/LabRedes-segmentrouting</a>**.

## :material-bookmark: **Introdução**

Esta página reúne tudo o que é preciso para executar os laboratórios de Segment Routing: primeiro os requisitos comuns (Docker e Containerlab), depois a preparação específica do Cisco XRd.

Caso ainda não conheça o Containerlab, veja também a página [Laboratórios](../../index.md) do LabRedes.

---

## :material-docker: **Ambiente comum: Docker e Containerlab**

### Requisitos

- Linux bare-metal ou uma VM com virtualização aninhada;
- Docker Engine;
- Containerlab;
- recursos de CPU e memória compatíveis com a quantidade de nós do cenário.

### Docker e Containerlab

```bash
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER   # encerre a sessão e entre novamente
bash -c "$(curl -sL https://get.containerlab.dev)"
```

Confira a instalação:

```bash
docker --version
containerlab version
```

### Obter o projeto

```bash
git clone https://github.com/rnpbr/LabRedes-segmentrouting.git
cd LabRedes-segmentrouting
```

Cada laboratório é autocontido. Entre no diretório escolhido e use a topologia
que está ao lado das configurações:

```bash
cd labs/<fabricante>/<data-plane>/<categoria>/<lab>
sudo clab deploy -t lab.clab.yml
```

Para encerrar o cenário:

```bash
sudo clab destroy -t lab.clab.yml --cleanup
```

O `--cleanup` remove o estado gerado pelo Containerlab dentro do diretório do
lab. Consulte o roteiro do cenário antes de usá-lo se quiser preservar mudanças
feitas durante a execução.

---

## :material-router-network: **Ambiente Cisco XRd**

Preparação específica para os laboratórios Cisco.

Os labs usam de quatro a dez roteadores, com consumo aproximado de 1,5 a 2,2 GB
de RAM por nó XRd. Reserve de 6 a 12 GB para a maioria. O `bgp-lu` tem oito
roteadores e dois contêineres Alpine, aproximadamente 12 GB de RAM e oito CPUs.
O `flex-algo-anycast` é o maior: dez roteadores, cerca de 22 GB de RAM medidos.

### Imagem XRd

A imagem não está em registry público. Baixe o tarball em [software.cisco.com](https://software.cisco.com) com login CCO, procurando por "IOS XRd Control-Plane Container".

```bash
docker load -i xrd-control-plane-x64-7.10.2.tgz
docker images | grep xrd
```

O `docker load` já cria a tag usada nos labs: `ios-xr/xrd-control-plane:7.10.2`. Se vier diferente:

```bash
docker tag <tag-original> ios-xr/xrd-control-plane:7.10.2
```

### Limites de inotify

O XRd consome muitos watches. Sem isso os nós travam no boot:

```bash
sudo sysctl -w fs.inotify.max_user_instances=524288
sudo sysctl -w fs.inotify.max_user_watches=524288
```

Para deixar permanente, grave em `/etc/sysctl.d/99-xrd.conf`.

### Subir um lab

Repositório: <https://github.com/rnpbr/LabRedes-segmentrouting.git>

Clone o repositório e entre no diretório do lab. A topologia e as configurações
ficam juntas no mesmo diretório:

```bash
git clone https://github.com/rnpbr/LabRedes-segmentrouting.git
cd LabRedes-segmentrouting
cd labs/cisco/sr-mpls/ti-lfa/00-zero-segment
sudo clab deploy -t lab.clab.yml
```

Estrutura final antes do deploy:

```text
00-zero-segment/
├── README.md
├── lab.clab.yml
└── configs/
    ├── sp.cfg
    ├── df.cfg
    ├── mg.cfg
    └── ba.cfg
```

O padrão é sempre o mesmo, trocando a categoria e o nome do lab:

```bash
cd labs/cisco/sr-mpls/<categoria>/<lab>
sudo clab deploy -t lab.clab.yml
```

`<categoria>` é `ti-lfa`, `sr-te`, `inter-as` ou `multidominio`. Cada roteiro informa o caminho
exato e os nomes dos nós.

Acesso: `ssh clab@<ip>`, senha `clab@123`. Cada lab documenta os IPs. Alternativa sem SSH:

```bash
sudo docker exec -it clab-tilfa-zero-segment-sp /pkg/bin/xr_cli.sh
```

Derrubar:

```bash
sudo clab destroy -t lab.clab.yml --cleanup
```

O `--cleanup` apaga o estado gerado pelo Containerlab, não os arquivos
versionados do laboratório. Sem ele, a configuração gravada pelo XRd pode ser
reutilizada no próximo deploy.

!!! note "Observação"
    Em geral, os `lab.clab.yml` usam `enforce-startup-config: true`, fazendo cada
    deploy reaplicar o `.cfg`. Consulte a topologia escolhida antes de contar com
    a preservação de mudanças manuais.



### Formato dos arquivos `.cfg`

São startup-configs completos de IOS-XR, não trechos para colar no terminal:

- não têm `conf t` nem `commit`, e terminam com `end`;
- incluem o bloco base do kind `cisco_xrd`: hostname, usuário `clab`, gRPC, netconf, SSH e rota default de gerência;
- usam `{{ .ShortName }}` e `{{ .MgmtIPv4Gateway }}`, que o containerlab resolve no deploy.

Para criar um lab novo, copie um `.cfg` existente e edite. Um arquivo só com a configuração de roteamento sobe um nó sem hostname, sem usuário e sem SSH.

Para aplicar algo à mão em um nó já rodando, aí sim vale o formato interativo:

```text
conf t
router ospf 1
 ...
commit
end
```

### Nomes de arquivo dentro de um lab

```text
labs/cisco/sr-mpls/<categoria>/<lab>/
├── README.md                 # roteiro do laboratório
├── lab.clab.yml              # topologia Containerlab
├── configs/<no>.cfg          # um por nó
└── images/
    ├── topology-<lab>.png    # diagrama
    └── terminal-<assunto>.png
```

O sufixo de `terminal-*.png` diz o comando que a captura mostra, não a ordem no texto:

| Arquivo | Comando |
|---|---|
| `terminal-deploy.png` | tabela de nós depois do `clab deploy` |
| `terminal-ospf-neighbor.png` | `show ospf neighbor` |
| `terminal-ospf-interface.png` | `show ospf interface <intf>` |
| `terminal-show-route.png` | `show route <prefixo>` |
| `terminal-show-cef.png` | `show cef <prefixo> detail` |
| `terminal-backup-path.png` | `show ospf routes <prefixo> backup-path` |
| `terminal-adjacency-sids.png` | `show ospf segment-routing adjacency-sids` |
| `terminal-mpls-forwarding.png` | `show mpls forwarding` |
| `terminal-sr-policy.png` | `show segment-routing traffic-eng policy` |
| `terminal-traceroute.png` | `traceroute` |

Não usar numeração de ordem (`1_topology`) nem nome genérico (`image-3.png`): os dois quebram quando um passo é inserido ou trocado de lugar.

No markdown, o texto alternativo descreve o comando:

```markdown
![show cef 10.0.1.251/32 detail em SP](./images/terminal-show-cef.png)
```

Os diagramas saem dos `.drawio` em `sr-mpls/ti-lfa/diagrams/` e
`sr-mpls/sr-te/diagrams/`, e do script `sr-mpls/multidominio/diagrams/gerar-figuras.py`.
Edite a fonte correspondente e reexporte.

Capturas de terminal são sempre `.png`. Diagramas podem ser `.svg`: é o caso do `bgp-lu`, cujas figuras têm variante clara e escura (`<nome>.svg` e `<nome>-escuro.svg`) servidas por `<picture>`/`prefers-color-scheme`, para continuarem legíveis no tema escuro do GitHub.

### Problemas comuns

| Sintoma | Causa provável |
|---|---|
| Nó travado em `starting` | RAM insuficiente ou limite de `inotify` baixo |
| Nó sem hostname, sem usuário `clab` e sem SSH | O `.cfg` não tem o bloco base do kind `cisco_xrd` |
| Config antiga volta depois de editar o `.cfg` | Diretório do lab preservado. Use `--cleanup` no destroy |
| Adjacência OSPF não sobe | Interface errada no `.clab.yml` (`Gi0-0-0-N` tem que casar com `GigabitEthernet0/0/0/N`), ou falta `network point-to-point` |
| Custo IGP diferente do documentado | Custo declarado em um lado só. OSPF usa o custo da interface de saída, então precisa nos dois |
| `docker load` com tag diferente | Remarcar com `docker tag` |
| `ping mpls` responde `% MPLS Embedded Management Subsystem is not running` | Falta `mpls oam` na configuração. Com ele, `ping mpls` e `traceroute sr-mpls` funcionam no XRd 7.10.2 (ver `flex-algo-anycast`); sem ele, use `traceroute` e `show cef` |
| `show configuration failed startup` mostra `grpc` / `port 9339` | O XRd 7.10.2 só aceita portas gRPC `57344-57999`. A linha é rejeitada e o gRPC sobe na porta padrão; o resto da configuração é aplicado |
| Todos os nós XRd acima de 100% de CPU, adjacências OSPF caindo | Tempestade na rede de gerência: o XRd roteia de volta quadros endereçados a outros MACs. Acontece quando o endereço de gerência de um nó serve de origem para tráfego do lab e esse nó não transmite pela gerência. Ver a ACL `MGMT-NO-TRANSIT` do `flex-algo-anycast` |
