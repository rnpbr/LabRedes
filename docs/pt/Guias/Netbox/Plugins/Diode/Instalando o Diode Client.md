# :material-power-plug-outline: Instalando o Diode Client

O Diode Client é responsável por enviar os dados coletados para o Diode Server utilizando gRPC/Protobuf, permitindo a posterior ingestão dessas informações no NetBox.

Existem diferentes formas de utilizar o Client. Nesta documentação, será apresentado o uso do Orb Agent, desenvolvido pela NetBox Labs. Esse agente não só realiza a descoberta automatizada de redes e dispositivos, como também oferece funcionalidades de observabilidade sobre os equipamentos monitorados.

Alternativamente, conforme descrito na <a target="_blank" href="https://docs.netboxlabs.com/netbox-extensions/diode/diode-client/">documentação oficial do NetBox</a>, o Diode Client também pode ser utilizado como um SDK Python, ideal para integrar scripts personalizados que coletam e enviam dados para o Diode Server.

## :simple-git: **Repositório do Plugin**
Copie o link abaixo ou clique a seguir para acessar o <a target="_blank" href="https://github.com/netboxlabs/orb-agent">Repositório do Github</a>

```
https://github.com/netboxlabs/orb-agent
```

---

## :material-scale-balance: **1. Requisitos para instalação**
Esta documentação utilizou os seguintes componentes com suas respectivas versões:

| Componentes           | Versões |
| --------------------- | ------- |
| **Netbox**            | v4.1.11 |
| **Orb Agent**         | v1.2.0  |

---

## :material-arrow-down-box: **2. Arquivos necessários para instalação**

1. Primeiro, vamos criar uma nova pasta para baixar os arquivos do Diode Server.
```bash
mkdir orb-agent
cd orb-agent
```

Agora, vamos criar os arquivos necessários para a instalação do Orb-Agent

### :simple-docker: **2.1. `docker-compose.yml`**
1. Primeiro, vamos criar o arquivo com o seguinte comando:
```bash
nano docker-compose.yml
```
2. Agora copie o conteúdo abaixo e cole no arquivo.
```bash
services:
  orb-agent:
    image: docker.io/netboxlabs/orb-agent:${ORB_TAG:-latest}
    command: run -c /opt/orb/agent.yaml
    volumes: 
      - ./:/opt/orb/
    networks:
      - orb-net
networks:
  orb-net:
    external: true
    name: ${DOCKER_NETWORK}
```

O agente precisa estar na mesma rede que contém dispositivos a serem importados, como estamos em um ambiente docker, vamos adiciona-ló a rede padrão dos laboratórios `br-lab`.

### :fontawesome-solid-square-root-variable: **2.2. `.env`**
O arquivo que contém as variáveis responsáveis para configuração do Orb-Agent.

1. Primeiro, vamos criar o arquivo com o seguinte comando:
```bash
nano .env
```

2. Para preencher a variável `DOCKER_SUBNET` com a subnet da rede `br-lab`, use o comando:
```bash
docker network inspect br-lab | grep "Subnet"
```

3. Agora copie o conteúdo abaixo e cole no arquivo.
```bash
ORB_TAG=1.2.0
DOCKER_NETWORK=br-lab # docker network

# Rede Docker onde o agente irá coletar os IP's
DOCKER_SUBNET=172.10.10.0/24
 
# Chave de API para conexão com o Diode Server -> diode-ingestion
DIODE_API_KEY=507006398ea55f210835a66ee98b2a301d9abf6d

# Url do Diode Server
DIODE_HOST=172.10.10.120:80 

# De sua escolha
AGENT_NAME=agent1 # nome do Agente
SITE_NAME=RNP # Nome do Site a ser adicionado/criado no Netbox
SCHEDULE='"*/10 * * * *"' # Tempo que será realizada novamente a coleta
```

4. Após definir as variáveis, use os comandos abaixo para permitir e exportar as variáveis no seu ambiente:
```bash
set -o allexport
source .env
```

### :material-face-agent: **2.3. `agent.yaml`**
No Orb-Agent, as configurações são definidas por meio do arquivo `agent.yaml`. É nesse arquivo que configuramos a conexão com o **Diode Server**, especificamos o local de importação de variáveis ou credenciais de acesso e definimos os tipos de descoberta que o agente deverá executar.

#### :fontawesome-solid-gear: **2.3.1. Config Manager**
A seção `config_manager` define como o Orb-Agent deve obter suas informações de configuração. O gerenciador de configuração é responsável por processar esses dados, recuperar as políticas definidas e repassá-las ao backend apropriado. Veja outros métodos na <a target="_blank" href="https://github.com/netboxlabs/orb-agent?tab=readme-ov-file#config-manager">documentação</a>

```bash
orb:
  config_manager:
    active: local
  ...
```

#### :material-key-wireless: **2.3.2. Secrets Manager**
A seção secrets_manager define como o Orb-Agent deve obter e injetar segredos (como senhas e tokens) nas políticas. Esse gerenciador pode se conectar a repositórios externos de segredos, como o HashiCorp Vault, para buscar informações sensíveis de forma segura, evitando que elas sejam escritas diretamente nos arquivos de configuração. Veja outros métodos na <a target="_blank" href="https://github.com/netboxlabs/orb-agent?tab=readme-ov-file#secrets-manager">documentação</a>

```bash
orb:
  secrets_manager:
    active: vault
    sources:
      vault:
        address: "https://vault.example.com:8200"
        namespace: "my-namespace"
        timeout: 60
        auth: "token"
        auth_args:
          token: "${VAULT_TOKEN}"
        schedule: "*/5 * * * *"
  ...
```

**Em nosso caso não iremos utilizar esta seção**

#### :material-server: **2.3.3. Backends**
Esta seção define como o Orb-Agent backends deve ser ativado. Nele temos as seguintes opções:

- Device Discovery
- Network Discovery
- Worker

```bash
orb:
  ...
  backends:
    network_discovery:
    ...
```

#### :material-vector-square-close: **2.3.4. Common**
A subseção especial `common`, dentro da seção backends, define configurações que são compartilhadas entre todos os backends. Atualmente, essa seção permite repassar as configurações de conexão com o servidor Diode para todos os backends de forma centralizada.

```bash
backends:
  ...
  common:
    diode:
      target: grpc://${DIODE_HOST}/diode
      client_id: ${DIODE_CLIENT_ID}
      client_secret: ${DIODE_CLIENT_SECRET}
      agent_name: agent01

```

#### :material-police-badge-outline: **2.3.5. Policies**
A seção `policies` define quais políticas de descoberta devem ser atribuídas a cada backend. Cada política descreve configurações específicas para o tipo de descoberta, como agendamento, propriedades padrão e o escopo (alvos).

Cada backend pode executar múltiplas políticas ao mesmo tempo, desde que cada uma tenha um nome único dentro daquele backend. Essas políticas são agrupadas em subseções de acordo com o backend responsável.

```bash
orb:
 ...
 policies:
   device_discovery:
     device_policy_1:
       # Veja docs/backends/device_discovery.md
   network_discovery:
     network_policy_1:
      # Veja docs/backends/network_discovery.md
   worker:
     worker_policy_1:
      # Veja docs/backends/worker.md
```

Links:

- <a target="_blank" href="https://github.com/netboxlabs/orb-agent/blob/develop/docs/backends/device_discovery.md">Device Discovery</a>

- <a target="_blank" href="https://github.com/netboxlabs/orb-agent/blob/develop/docs/backends/network_discovery.md">Network Discovery</a>

- <a target="_blank" href="https://github.com/netboxlabs/orb-agent/blob/develop/docs/backends/worker.md">Worker</a>

### :octicons-repo-template-16: **3. `agent.template.yaml`**
Depois de entender um pouco da estrutura do Orb-Agent, vamos para um exemplo prático com um template simples que pode ser utlizado para mapear a rede docker `br-lab` e alguns dispositivos nela. Nesse arquivo vamo utilizar os backends: `network_discovery` e `device_discovery`.

!!! tip "Dica" 
    Lembre-se: o `Orb-Agent` utiliza o arquivo `agent.yaml` como base de configuração. **Esse arquivo deve ser gerado no seu ambiente local** e, no momento de subir o container, precisa ser copiado para dentro dele.

1. Vamos criar o arquivo `agent.template.yaml`.
```bash
nano agent.template.yaml
```

2. Agora, copie e cole o conteúdo dentro do arquivo criado:
```bash
orb:
  config_manager:
    active: local
  backends:
	  device_discovery:
    network_discovery:
    common:
      diode:
        target: grpc://${DIODE_HOST}/diode
        api_key: ${DIODE_API_KEY}
        agent_name: ${AGENT_NAME}
  policies:
    network_discovery:
      policy_1:
        scope:
          targets:
            - ${DOCKER_SUBNET}
    device_discovery:
      discovery_1:
        config:
          schedule: ${SCHEDULE}
          defaults:
            site: ${SITE_NAME}
        scope:
          - driver: junos
            hostname: 172.10.10.101
            username: admin
            password: admin@123
            optional_args:
              insecure: True
          - driver: junos
            hostname: 172.10.10.102
            username: admin
            password: admin@123
            optional_args:
              insecure: True
          - driver: junos
            hostname: 172.10.10.103
            username: admin
            password: admin@123
            optional_args:
              insecure: True
```

3. Agora vamos gerar o arquivo `agent.yaml` de acordo com as variáveis deifnidas no `.env`.
```bash
envsubst < agent.template.yaml > agent.yaml
```

4. Verifique se o arquivo preencher todos os espaços de variáveis com os seus respectivos valores. A sua saída deve ser algo parecido como:
```bash
orb:
  config_manager:
    active: local
  backends:
    device_discovery:
    network_discovery:
    common:
      diode:
        target: grpc://172.10.10.120:80/diode
        api_key: 507006398ea55f210835a66ee98b2a301d9abf6d
        agent_name: agent1
  policies:
    network_discovery:
      policy_1:
        scope:
          targets:
            - 172.10.10.0/24
    device_discovery:
      discovery_1:
        config:
          schedule: "*/10 * * * *"
          defaults:
            site: RNP
        scope:
          - driver: junos
            hostname: 172.10.10.101
            username: admin
            password: admin@123
            optional_args:
              insecure: True
          - driver: junos
            hostname: 172.10.10.102
            username: admin
            password: admin@123
            optional_args:
              insecure: True
          - driver: junos
            hostname: 172.10.10.103
            username: admin
            password: admin@123
            optional_args:
              insecure: True
```

## :simple-docker: **4. Deploy!**
Com o compose do Orb-Agent configurado e o arquivo `agent.yaml` gerado, agora é hora de colocá-lo em execução.

- Execute o comando abaixo para iniciar todos os serviços definidos no docker-compose.yml:
```bash
docker compose up # ou para rodar em segundo plano
docker compose up -d 
```

- Esta configuração deve retornar os IP's da rede `172.10.10.0/24` e os dados dos três dispositivos definidos dentro de 10 em 10 minutos.

---

## :octicons-rocket-24: **5. Conclusão**
Com o Orb-Agent devidamente configurado e em execução, você tem uma poderosa ferramenta de automação e descoberta ativa em sua rede. Ele permite a coleta contínua e estruturada de dados sobre dispositivos e infraestrutura, enviando essas informações diretamente para o NetBox via Diode Server, de forma segura e flexível.

Seja utilizando políticas personalizadas ou integrando com gerenciadores de segredos e configuração, o Orb-Agent facilita a escalabilidade da gestão de ativos de rede e contribui significativamente para manter seu ambiente atualizado, consistente e documentado.

Nos próximos passos, você poderá expandir as descobertas, refinar políticas específicas para diferentes backends e aproveitar o potencial do NetBox como fonte de verdade da sua infraestrutura.

