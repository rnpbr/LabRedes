# :material-bookmark: Multvendor logs ELK

Este laboratório simula, via Containerlab, a interligação entre três roteadores — Juniper, Huawei e Cisco — com roteamento dinâmico via OSPF, e exportação de logs via Syslog para uma infraestrutura de observabilidade baseada na pilha ELK (Elasticsearch, Logstash, Kibana), utilizando Elastic Agents gerenciados pelo Fleet para coleta e envio dos dados.

---

## :material-bookmark: 1. Descrição

### :octicons-goal-16: 1.1 Objetivo do Lab

O objetivo deste laboratório é simular a exportação e coleta centralizada de logs provenientes de roteadores de diferentes fabricantes (Juniper, Huawei e Cisco) utilizando o protocolo Syslog (UDP 514).
A coleta é realizada por Elastic Agents, configurados para receber logs diretamente dos dispositivos e encaminhar os eventos para o Elasticsearch, sob gerenciamento do Fleet Server.
A visualização e análise dos logs ocorrem por meio do Kibana, possibilitando uma abordagem moderna de observabilidade multivendor.

### :material-lan: 1.2 Topologia do Lab

![Topologia do Lab](../../../../img/labs_imgs/Topologia_Logs_ELK.svg)

**Descrição da Topologia**

 * Três roteadores (Juniper, Cisco, Huawei) interligados em topologia em anel com links ponto a ponto /31.
 * Roteamento dinâmico via OSPF entre os roteadores.
 * Exportação de logs via Syslog (UDP/514) para o servidor de monitoramento.
 * Elastic Agent atua como coletor, escutando na porta 514/UDP, parseando os eventos e enviando-os ao Elasticsearch.
 * Fleet Server gerencia e monitora os agentes Elastic.
 * Elasticsearch armazena e indexa os logs recebidos.
 * Kibana fornece a interface gráfica para visualização, busca e correlação dos logs.
 * Rede externa br-lab conecta os roteadores à infraestrutura de monitoramento baseada em ELK.

---

## :octicons-search-16: 2. Aplicações

### Exemplos de Aplicações

Este laboratório constitui uma base para experimentação acadêmica e aplicada em monitoramento, observabilidade e análise de eventos em ambientes multivendor, com foco no uso do Elastic Stack e Fleet Management.

#### Possíveis Aplicações:

* **Treinamento NOC/SOC multivendor** – Simulação prática de exportação e análise de logs em ambiente Juniper, Huawei e Cisco.
* **Validação da coleta Syslog** – Teste de compatibilidade e parsing de logs via Elastic Agents sem uso de Logstash.
* **Visualização em tempo real** – Criação de dashboards no Kibana para eventos e métricas de rede.
* **Monitoramento centralizado** – Uso do Fleet para gerenciar agentes e políticas de coleta de forma unificada.
* **Ensino de integração de observabilidade** – Aplicação educacional sobre Syslog, Elastic Agents, Fleet, Elasticsearch e Kibana em redes multivendor.
---

## :material-tools: 3. Requisitos

Abaixo estão listados os requisitos mínimos de hardware e software necessários para executar o laboratório. Certifique-se de incluir as ferramentas essenciais, como **Containerlab** e **Docker**, além da rede `br-lab` previamente criada.
para saber mais sobre este itens acesse:

- [Criação da Rede br-lab](../../../../Ferramentas/Primeiros passos - preparando o ambiente.md)
-  <a target="_blank" href="https://www.docker.com/get-started/">Instalação do Docker</a>
-  <a target="_blank" href="https://containerlab.dev/install/">Instalação do containerlab</a>

E tenha a stack ELK previamente instalado e configurado para ingestão de logs, para saber mais sobre a instalação acesse: [Configurando Syslog no ELK](../../../../Ferramentas/Elasticsearch/Configurando Syslog no ELK.md)

### :material-alert: Tabela de Requisitos Minimos:

| Requisito           | Detalhes                                                                             |
| ------------------- |--------------------------------------------------------------------------------------|
| **CPUs**            | 6 vCPUs                                                                              |
| **Memória RAM**     | 16 GB                                                                                |
| **Espaço em Disco** | 20 GB (recomendado)                                                                  |
| **Containerlab**    | 0.45.0 ou superior                                                                   |
| **Docker Engine**   | 23.0.3 ou superior                                                                   |
| **Imagens**         | `vr-vjunos:23.2R1.14`, `vrnetlab/huawei_vrp:ne40e-8.180`, `xrd-control-plane:7.10.2` |
| **Rede Docker**     | `br-lab`                                                                             |

!!! warning "Atenção" 
    Verifique se o seu processador possui **suporte à virtualização por hardware** e se essa funcionalidade está **ativada na BIOS/UEFI**.  
    - Em processadores **Intel**, essa tecnologia é chamada de **VT-x** (Intel Virtualization Technology).  
    - Em processadores **AMD**, é conhecida como **AMD-V** (AMD Virtualization).  

    Sem essa funcionalidade ativada, as imagens como o **vJunos-router** não funcionarão corretamente.
---

## :fontawesome-solid-prescription-bottle: 4. Implantando o Lab

Você pode realizar a implantação por meio de um script pronto ou configurar manualmente os arquivos do lab.

### :material-git: 4.1 Implantação Pronta

Este método permite ao usuário **baixar uma versão pré-montada** do laboratório, com a topologia e as configurações já definidas. Basta baixar o repositório e seguir para o início da execução.

!!! tip "Dica" 
    A implantação pronta é útil para quem deseja começar rapidamente com um ambiente configurado.

#### :octicons-download-16: Baixando o Lab

Execute o script abaixo para baixar e configurar o laboratório automaticamente:

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/logs-elk-multvendor/get.sh" && sh get.sh && cd logs-elk-multvendor
    ```

=== "Windows"

    ```bat
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/logs-elk-multvendor/get.bat" && call get.bat && cd logs-elk-multvendor
    ```

!!! tip "Dica"
    No Linux/Mac, use `chmod +x get.sh` antes de executar o script, caso ele não esteja com permissão de execução.

---

## :octicons-play-16: 5. Inicializando o Lab

Após o download ou personalização, siga as etapas abaixo para **iniciar o laboratório**.
Execute o comando abaixo dentro do diretório baixado.

```bash
sudo containerlab deploy
```

Esse comando criará os containers dos roteadores, configurará os links e iniciará os serviços de monitoramento.

!!! tip "Depuração"
    Use `docker logs -f <nome_container>` para verificar o estado dos serviços, caso algo não funcione.

---

## :material-access-point: 6. Acesso aos Dispositivos

### :material-table: 6.1 IPs e Portas dos Serviços

| Dispositivo      | IP de Acesso  | Porta(s) | Serviço            |
|------------------| ------------- |-----| ------------------ |
| **node1**        | 172.10.10.201 | 22      | SSH               |
| **node2**        | 172.10.10.202 | 22      | SSH               |
| **node3**        | 172.10.10.203 | 22      | SSH               |
| **Fleet Server** | 172.10.10.110 | 8220     | Ingestão de dados |
| **Elasticsearch** | 172.10.10.108 | 9200     | Banco de dados    |
| **Kibana**       | 172.10.10.109 | 5601     | Interface Web     |
| **Graphite**     | 172.10.10.119 | 8080    | Web UI (Graphite) |

### :material-key-link: 6.2 Senhas de Acesso

| Serviço         | Usuário | Senha          |
|-----------------| ------- |----------------|
| **node1 (SSH)** | `admin`  | `admin@123`    |
| **node2 (SSH)** | `clab`   | `clab@123`     |
| **node3 (SSH)** | `admin`  | `admin`        |
| **Kibana**      | `elastic`| `admin@123`    |

!!! warning "Verificação de Inicialização"
    Antes de acessar os serviços, use `docker ps` e verifique os logs dos containers para garantir que estão funcionando corretamente.

---

## :octicons-browser-16: 7. Observabilidade e Visualização

!!! Warning "Atenção"
    Devido à forma como as configurações são aplicadas no vJunos-router, a configuração do syslog deve ser feita manualmente.
    Siga o passo a passo abaixo para enviar todos os logs do sistema para o servidor de logs remoto.

### Passo a passo

Acesse o node1 via ssh e execute:

```junos
configure
```

* Entra no **modo de configuração** do Junos.
* Todos os comandos seguintes vão alterar a configuração do equipamento.

```junos
set system syslog host 172.10.10.110 any any
```

* Define o servidor de logs remoto (**172.10.10.110**) como destino.
* `any any` significa: enviar **qualquer facility** (sistema, kernel, daemon, auth etc.) em **qualquer nível de severidade** (emergency, alert, critical, warning, info, debug).
* Na prática: **todos os eventos do sistema serão enviados para esse servidor**.

```junos
set system syslog source-address 172.10.10.201
```

* Define o **IP de origem** dos pacotes de log como **172.10.10.201** (o IP do vJunos-router).
* Isso garante que o tráfego de syslog saia pela interface que possui esse endereço.
* É importante para o servidor de logs reconhecer corretamente a origem das mensagens.

```junos
commit
```

* Aplica as alterações feitas na configuração.

!!! warning "atenção"
    Após o inicio do Vjunos, pode levar entre 3 a 6 minutos para subir todas as rotas e a configuração funcionar corretamente.


* Somente após esse comando os logs começam a ser enviados para o destino configurado.

Ao final da implatação você vera os logs no Kibana desta forma:

![Exemplo do lab em produção](../../../../img/labs_imgs/example/Exemplo_Logs_ELK.png)

### 7.1 Elastic Agent

O **Elastic Agent** é responsável pela coleta e envio dos logs exportados via **Syslog (UDP/514)** pelos roteadores Juniper, Huawei e Cisco.
Atua como agente unificado sob gerenciamento do **Fleet Server**, realizando o parsing, enriquecimento e encaminhamento dos dados diretamente ao **Elasticsearch**.

---

### 7.2 Elasticsearch

Banco de dados orientado a documentos utilizado para armazenar e indexar os logs coletados pelos agentes.
Permite consultas, agregações e correlações entre eventos de diferentes dispositivos.
Acessível pela porta **9200**.

---

### 7.3 Kibana

Interface web de análise e visualização dos logs armazenados no Elasticsearch.
Permite a criação de dashboards, consultas em tempo real e gerenciamento do Fleet.
Acessível em `https://<seu IP ou localhost>:5601`.

---

### 7.4 Fleet Server

O **Fleet Server** é executado no mesmo contêiner do **Elastic Agent**, unificando as funções de coleta e gerenciamento.
Gerencia os agentes Elastic, aplica políticas de coleta, recebe logs via Syslog (UDP/514) e envia os dados ao Elasticsearch.
Opera na porta **8220/TCP** e é administrado através do **Kibana → Management → Fleet**.



