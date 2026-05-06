# :material-power-plug-outline: Instalando o Diode Plugin

O Diode Plugin é um componente essencial para habilitar a ingestão automatizada de dados no NetBox. Ele fornece integração direta com o ORM do NetBox e gerencia as chaves de API, permitindo que o servidor Diode envie dados estruturados de forma segura e validada. Com esse plugin, o NetBox passa a receber atualizações de inventário em tempo real, facilitando a descoberta, documentação e sincronização contínua da infraestrutura de rede.

## :simple-git: **Repositório do Plugin**
Copie o link abaixo ou clique a seguir para acessar o [Repositório do Github](https://github.com/netboxlabs/diode-netbox-plugin)

```
https://github.com/netboxlabs/diode-netbox-plugin
```

---

## :material-scale-balance: **1. Requisitos para instalação**
Esta documentação utilizou os seguintes componentes com suas respectivas versões:

| Componentes           | Versões |
| --------------------- | ------- |
| **Netbox**            | v4.1.11 |
| **Diode Plugin**      | v0.6.0  |

---

## :material-file-document-arrow-right: **2. Instalando e Configurando o Plugin no Netbox**
Para instalarmos o plugin no Netbox, precisamos alterar e adicionar alguns arquivos 
que são responsáveis pela configuração do Netbox.

Os arquivos são:

- `plugin_requirements.txt`.
- `DockerFile-Plugins`.
- `docker-compose.override.yml`.
- `configuration/plugins.py`.

### :fontawesome-solid-gear: **2.1. Configurando a versão do Netbox:**

1. Primeiro, vamos clonar o repositório do Netbox:
```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
```

2. Acesse o diretório clonado:
```bash
cd netbox-docker
```

3. Agora, mude para a release 3.0.0
```bash
git checkout 3.0.0
```
!!! tip "Informação" 
    Alteramos a branch do repositório para termos acesso à versão 4.1.11 do Netbox.

!!! tip "Dica" 
    Todos os comandos abaixos serão executados dentro diretório raiz do netbox `netbox-docker/`.


### :material-text-box: **2.2. plugin_requirements.txt**
Este arquivo contém ama lista dos plugins do Netbox (como pacotes Python do PyPO) que devem ser instalados durante a construção da imagem Docker.

Execute o seguinte comando para escrever o pacote dentro do arquivo `plugin_requirements.txt`.

```bash
echo "netboxlabs-diode-netbox-plugin" > plugin_requirements.txt
```

### :material-docker: **2.3. DockerFile-Plugins**
Esse é o DockerFile usado para construir a imagem docker customizada.

1. Crie o arquivo e acesse com um editor: 
```bash
nano DockerFile-Plugins
```

2. Copie o conteúdo abaixo e cole no arquivo:
```bash
FROM netboxcommunity/netbox:v4.1

COPY ./plugin_requirements.txt /opt/netbox/
RUN pip install -r /opt/netbox/plugin_requirements.txt
```

### :material-docker: **2.4. docker-compose.override.yml**
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
      br-lab:
        ipv4_address: 172.10.10.5

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

### :material-power-plug-outline: **2.5. plugins.py**
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
        # Auto-provision users for Diode plugin
        "auto_provision_users": True, 

        # Diode gRPC target for communication with Diode server
        "diode_target_override": "grpc://172.10.10.120:80/diode",

        # User allowed for Diode to NetBox communication
        "diode_to_netbox_username": "diode-to-netbox",

        # User allowed for NetBox to Diode communication
        "netbox_to_diode_username": "netbox-to-diode",

        # User allowed for data ingestion
        "diode_username": "diode-ingestion",
    },
}
```

!!! tip "Dica" 
    Indicamos que deixe a configuração `auto_provision_users` como `True` para automatizar a criação de usuário, grupos e chaves de API que são responsáveis pela integração com o Diode Server.

---

## :simple-docker: **3. Build e Deploy!**
Agora seu Netbox está configurado e pronto para o deploy, siga os comandos abaixo e construa a nova instancia do Netbox!

1. Construa a imagem:
```bash
docker compose build --no-cache
```

2. Suba os containeres:
```bash
docker compose up -d
```

---

## :octicons-rocket-24: **4. Próximos Passos**
Com o plugin do Diode instalado, seu ambiente NetBox agora está preparado para receber dados do servidor Diode, permitindo a ingestão automatizada de informações da rede.

O próximo passo é configurar o Diode Server, responsável por processar e encaminhar esses dados para o NetBox.

Próximo: [Instalando o Diode Server](./Instalando%20o%20Diode%20Server.md)