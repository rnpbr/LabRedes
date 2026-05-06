# Descoberta Diode Multivendor

## :material-bookmark: **Introdução**

Este laboratório simula uma rede com 3 roteadores de diferentes fabricantes (Juniper, Cisco e Huawei) configurados com OSPF e SNMP, integrando os componentes do Diode (plugin, server e agent) e o Netbox para importação e gerenciamento automatizado de dispositivos.

---

## :fontawesome-solid-prescription-bottle: 1. **Descrição**

### :octicons-goal-16: 1.1 **Objetivo do Lab**

O objetivo deste laboratório é demonstrar, de forma prática, o processo de descoberta e importação automatizada de dispositivos de rede multivendor, abrangendo diferentes modelos e fabricantes, e suas respectivas configurações para o Netbox, utilizando o diodo-plugin, o diode-server e o orb-agent.

![Topologia.svg](/img/labs_imgs/Diagrama_fluxo_diode_multivendor.svg)


### :material-lan: 1.2 **Topologia do Lab**
Abaixo está a topologia mostrando os três roteadores — Juniper, Cisco e Huawei — além dos servidores envolvidos na arquitetura.

![Topologia.svg](/img/labs_imgs/Topologia_discovery_lab_diode_multivendor.svg)

Os roteadores estão configurados com as seguintes tecnologias:

- **OSPF (Open Shortest Path First)**: Utilizado para roteamento dinâmico, permitindo que dispositivos (independentemente do fabricante) troquem informações sobre rotas e topologia.
- **SNMP (Simple Network Management Protocol)**: Usado para coleta de telemetria e descoberta, garantindo compatibilidade com dispositivos Juniper, Cisco e Huawei.
---

## :octicons-search-16: **2. Aplicações**

### Exemplos de Aplicações

Este laboratório demonstra uma arquitetura realista de descoberta automática de dispositivos em ambientes onde coexistem múltiplos fabricantes.

#### Possíveis Aplicações:

- **Automação da descoberta multivendor:** Detecção automática de dispositivos Juniper, Cisco e Huawei e registro de seus inventários no Netbox.
- **Padronização de inventário heterogêneo:** Criação de uma base unificada de dispositivos independentemente do fornecedor.
- **Criação de repositório centralizado de dispositivos:** Construção de uma base confiável de dados da rede em tempo real.
- **Estudo prático de SNMP em ambientes híbridos:** Comparação na prática entre diferentes MIBs e padrões dos fabricantes.
- **Integração Diode + Netbox em cenários reais:** Prática de coleta e integração de dados de rede.


---


## :material-tools: **3. Requisitos**
### :material-alert: 3.1 Pré requisitos

Para iniciar o laboratório, é necessário a instalação e configuração dos seguintes componentes:

- Netbox
- Diode Plugin
- Diode Server
- Orb Agent
- Containerlab
- Docker

Caso o seu ambiente não esteja configurado, siga os passos [Guia de Configuração](../../../../Getting%20Started.md)


### :material-alert: 3.2 Tabela de Requisitos Computacionais

| Requisito           | Detalhes |
|---------------------| --- |
| **CPUs**            | 4 vCPUs (mínimo recomendado) |
| **Memória RAM**     | 12 GB |
| **Espaço em Disco** | 10 GB |
| **Containerlab**    | 0.64.0 |
| **Rede Criada**     | br-lab |

!!! tip "Dica" 
    Verifique se a versão do Docker e do Containerlab são compatíveis para evitar erros durante a implantação.

!!! warning "Atenção" 
    Verifique se o seu processador possui **suporte à virtualização por hardware** e se essa funcionalidade está **ativada na BIOS/UEFI**.  
    - Em processadores **Intel**, essa tecnologia é chamada de **VT-x** (Intel Virtualization Technology).  
    - Em processadores **AMD**, é conhecida como **AMD-V** (AMD Virtualization).  

    Sem essa funcionalidade ativada, as imagens como o **vJunos-router** não funcionarão corretamente.
---

## :octicons-tools-16: 4. Instalação

### :material-network-strength-4-cog: 4.1 Configurando a Rede Docker

Antes de iniciar os containers, crie a rede bridge que interligará os dispositivos:

```bash
docker network create \
  --driver=bridge \
  --opt com.docker.network.bridge.name=br-lab \
  --subnet=172.10.10.0/24 \
  br-lab
```

### :material-git: 4.2 Clonando o Repositório do Lab

Execute o script abaixo para baixar e configurar o laboratório automaticamente:

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/discovery-lab-diode-multivendor/get.sh?ref_type=heads&inline=false" && sh get.sh && cd discovery-lab
    ```

=== "Windows"

    ```bat
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/discovery-lab-diode-multivendor/get.bat?ref_type=heads&inline=false" && call get.bat && cd discovery-lab
    ```

!!! tip "Dica"
    No Linux/Mac, use `chmod +x get.sh` antes de executar o script, caso ele não esteja com permissão de execução.


---

## :fontawesome-solid-house-chimney: 5. Implantação do Ambiente

### :material-router-wireless: 5.1 Subindo os Roteadores com Containerlab

Aqui, os três dispositivos Juniper/Cisco/Huawei serão inicializados.
O tempo de boot pode variar conforme o fabricante.

```bash
sudo clab deploy -t clab/discovery-lab.clab.yaml
```
    
!!! warning "Debug" 
    Os dispositivos podem levar cerca de 10 minutos para estarem totalmente operacionais.
    Caso ocorra algum erro, verifique a saída do comando para possíveis mensagens de erro. Use `docker logs <container_name>` para depurar.


### :material-server: 5.2 Levantando o Diode Server
!!! tip "Dica" 
    Caso você já possua o servidor do Diode configurado, basta pular esse passo.

1. Vamos criar uma nova pasta para armazenar os arquivos do diode-server:
```bash
mkdir diode-server
cd diode-server
```

2. Agora, vamos realizar o download do script de início rápido:
```bash
curl -sSfLo quickstart.sh https://raw.githubusercontent.com/netboxlabs/diode/release/diode-server/docker/scripts/quickstart.sh
chmod +x quickstart.sh
```

3. Então, basta executar o script passando a url do seu netbox:
```bash
./quickstart.sh https://<netbox-server>
```

4. Por fim, basta iniciar os containers:
```bash
docker compose up -d
```

5. Para extrair as credenciais necessárias na instalação do plugin, execute o comando abaixo:
```bash
echo $(jq -r '.[] | select(.client_id == "netbox-to-diode") | .client_secret' ./oauth2/client/client-credentials.json)
```

!!! tip "Dica"
    **Armazene o token**, você vai precisar adicioná-lo na configuração a seguir.


---
### :material-relation-one-to-one: 5.3 Instalando o Plugin no Netbox
Neste passo, vamos instalar o plugin do diode, responsável por estabelecer a conexão entre o diode-server e o Netbox.

#### :fontawesome-solid-gear: **5.3.1 Configurando a versão do Netbox:**

1. Primeiro, vamos clonar o repositório do Netbox Docker:
```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
```
2. Agora, vamos para a Release 3.2.1:
```bash
cd netbox-docker/
git checkout 3.2.1
```

!!! tip "Informação" 
    Alteramos a branch do repositório para termos acesso à versão 4.2.4 do Netbox.

!!! tip "Dica" 
    Todos os comandos abaixos serão executados dentro diretório raiz do netbox `netbox-docker/`.


#### :material-text-box: **5.3.2 plugin_requirements.txt**
Este arquivo contém ama lista dos plugins do Netbox (como pacotes Python do PyPO) que devem ser instalados durante a construção da imagem Docker.

Execute o seguinte comando para escrever o pacote dentro do arquivo `plugin_requirements.txt`.

```bash
echo "netboxlabs-diode-netbox-plugin" >> plugin_requirements.txt
```

#### :material-docker: **5.3.3 DockerFile-Plugins**
Esse é o DockerFile usado para construir a imagem docker customizada.

1. Crie o arquivo e acesse com um editor: 
```bash
nano DockerFile-Plugins
```

2. Copie o conteúdo abaixo e cole no arquivo:
```bash
FROM netboxcommunity/netbox:v4.2.4

COPY ./plugin_requirements.txt /opt/netbox/
RUN /usr/local/bin/uv pip install -r /opt/netbox/plugin_requirements.txt
```

#### :material-docker: **5.3.4. docker-compose.override.yml**
Como o nome implica, esse arquivo contaim as configurações que vão sobrescrever o `docker-compose.yml`.

Caso você ainda não tenha configurado a rede `br-lab`. Acesse: [Configurando a Rede Docker](../../../../Laboratórios/Juniper/vJunos/Descoberta/index.md/#31-configurando-a-rede-docker)

1. Crie o arquivo e acesse com um editor:
```bash
nano docker-compose.override.yml
```

2. Copie o conteúdo abaixo e cole no arquivo:
```bash
services:
  netbox:
    image: netbox:latest-plugins
    pull_policy: never
    ports:
      - 8000:8080
    build:
      context: .
      dockerfile: Dockerfile-Plugins
    networks:
      - br-lab

  netbox-worker:
    image: netbox:latest-plugins
    pull_policy: never
    networks:
      - br-lab

  netbox-housekeeping:
    image: netbox:latest-plugins
    pull_policy: never
    networks:
      - br-lab

  postgres:
    networks:
      - br-lab

  redis:
    networks:
      - br-lab

  redis-cache:
    networks:
      - br-lab

networks:
  br-lab:
    external: true
```

As alterações feitas foram: 

- adicionar o Netbox na rede `br-lab`.
- alteração do dockerfile para o `Dockerfile-Plugins`, criado anteriormente.
- Também alterado a imagem dos serviços para: `netbox:latest-plugins`.

#### :material-power-plug-outline: **5.3.5. plugins.py**
Este arquivo é responsável por setar as configurações específicas de cada plugin.

1. Acesse o arquivo com o editor:
```bash
nano configuration/plugins.py
```

2. Copie e cole o conteúdo no arquivo:
```bash
PLUGINS = [
    "netbox_diode_plugin",
]

PLUGINS_CONFIG = {
    "netbox_diode_plugin": {
        # Diode gRPC target for communication with Diode server
        "diode_target_override": "grpc://localhost:8080/diode",

        # Username associated with changes applied via plugin
        "diode_username": "diode",

        # netbox-to-diode client_secret created during diode bootstrap.
        "netbox_to_diode_client_secret": "..."
    },
}
```

!!! tip "Dica" 
    O token armazenado na instalação do diode-server deve ser passado na opção: `netbox_to_diode_client_secret`.

---

#### :simple-docker: **5.3.6 Build e Deploy!**
Agora seu Netbox está configurado e pronto para o deploy, siga os comandos abaixo e construa a nova instancia do Netbox!

1. Construa a imagem:
```bash
docker compose build --no-cache
```

2. Suba os containeres:
```bash
docker compose up -d
```

3. Crie as migrações necessárias com o comando abaixo:
```bash
docker compose exec -it netbox ./manage.py migrate netbox_diode_plugin
```

#### :material-import: **5.3.7. Gerando as credenciais para o agente**
Precisamos criar as credenciais para que o agente do diode se comunique e repasse os dados coletados dos dispositivos para o diode-server 

1. Acesse seu Netbox e vá no menu lateral.
2. Vá em `Diode` > `Client Credentials`.
3. Clique no botão superior `Adicionar Credencial`.
4. Digite um nome para sua credencial.
5. Armazene o `Client Id` e o `Client Secret`.

---

## :octicons-key-16: 6. Orb-Agent
O orb-agent é um component do diode responsável por realizar a coleta dos dados nos dispositivos.

### 6.1 **Configurando o agente**

1. Acesse a pasta do `orb-agent`:
```bash
cd ./orb-agent
```

2. No arquivo `.env`, configure as variáveis de acordo com o seu ambiente.
```bash
DOCKER_NETWORK=br-lab                      # Container Network
DOCKER_SUBNET=172.10.10.0/24               # Devices Network
DIODE_CLIENT_ID=                           # Diode Client Id
DIODE_CLIENT_SECRET=                       # Diode Client Secret
DIODE_HOST=<your-ip>:8080                  # Diode Server Url
AGENT_NAME=agent1                          # Agent Name
SITE_NAME=RNP                              # Netbox Site Name 
MULTIDEVICE_COMMUNITY="public"             # Device Community
```

Aqui fica o `Client Id` e o `Client Secret` gerados no plugin do diode no Netbox.

3. Agora, vamos aplicar as variáveis no template de importação do juniper com o comando:
```bash
set -o allexport && source .env && envsubst < agent.snmp.template.yaml > agent.yaml
```

### 6.2 **Iniciando a coleta dos dados**
Por fim, basta subir o container para iniciar a importação dos dispositivos para o Netbox!

```bash
docker compose up
```

✅ Acompanhe em tempo real no Netbox os dispositivos sendo coletados pelo agente.

⏱️ Além disso, você pode configurar um intervalo de coleta para que o agente realize a importação de forma automática e periódica, sem necessidade de intervenção manual.
___

## :material-access-point: 7. Acesso

Após o laboratório ser iniciado, você poderá acessar os dispositivos e serviços configurados na rede.

### :material-table: 7.1 Tabela de IPs e Portas de Serviço

Aqui está a tabela de dispositivos, IPs e portas de serviço disponíveis no laboratório.

| Dispositivo  | Fabricante | IP            | Porta | Serviço |
| ------------ | ---------- | ------------- | ----- | ------- |
| **node1**    | Juniper    | 172.10.10.201 | 22    | SSH     |
| **node2**    | Cisco      | 172.10.10.202 | 22    | SSH     |
| **node3**    | Huawei     | 172.10.10.203 | 22    | SSH     |
| **Diode**    | —          | localhost     | 8080  | API     |
| **Netbox**   | —          | localhost     | 8000  | Web UI  |
| **Graphite** | —          | 172.20.20.1   | 8081  | Web UI  |


### :material-key-link: 7.2 Senhas de Acesso

Aqui está a tabela com as senhas de acesso dos serviços configurados no laboratório.

| Serviço | Usuário | Senha |
| --- | --- | --- |
| **node1 (SSH)** | admin | admin@123 |
| **node2 (SSH)** | clab | clab@123 |
| **node3 (SSH)** | admin | admin |
| **Netbox (Web)** | Admin | Admin |

!!! warning "Atenção" 
    antes de acessar acesse o log de um dispositivo para verificar se ele foi iniciado e configurado corretamente.
---

## :octicons-rocket-24: 8. Próximos Passos
Com o laboratório finalizado, você pode seguir algum passos abaixo como **extra**.

- Testar diferenças de coleta SNMP entre Juniper, Cisco e Huawei.
- Comparar estrutura de MIBs utilizadas na importação.
- Adicionar novos dispositivos de qualquer fabricante para verificar compatibilidade.
---

### :fontawesome-solid-paintbrush: 9. Conclusão

✅ Agora você aprendeu como utilizar os componentes do Diode para importar automaticamente uma rede composta por dispositivos Juniper, Cisco e Huawei, construindo um inventário completo no Netbox e possibilitando a criação do seu Digital Twin com o Netreplica.