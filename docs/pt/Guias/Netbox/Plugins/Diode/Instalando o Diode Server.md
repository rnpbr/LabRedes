# :material-power-plug-outline: Instalando o Diode Server

O Diode Server é o componente central da arquitetura do Diode. Ele é responsável por receber, processar e reconciliar os dados enviados pelos clientes (scripts ou agentes) e integrá-los ao NetBox. Utilizando protocolos modernos como gRPC e formatos eficientes como Protobuf, o Diode Server valida as informações recebidas e executa a atualização automatizada do inventário no NetBox por meio da API exposta pelo plugin.

Esse servidor atua como um intermediário inteligente, garantindo que os dados inseridos estejam corretos, completos e sincronizados com os registros existentes.

## :simple-git: **Repositório do Plugin**
Copie o link abaixo ou clique a seguir para acessar o <a target="_blank" href="https://github.com/netboxlabs/diode-netbox-plugin">Repositório do Github</a>

```
https://github.com/netboxlabs/diode-netbox-plugin
```

---

## :material-scale-balance: **1. Requisitos para instalação**
Esta documentação utilizou os seguintes componentes com suas respectivas versões:

| Componentes           | Versões |
| --------------------- | ------- |
| **Netbox**            | v4.1.11 |
| **Diode Server**      | v0.6.0  |

---

## :material-arrow-down-box: **2. Baixando os arquivos para instalação**

1. Primeiro, vamos criar uma nova pasta para baixar os arquivos do Diode Server.
```bash
mkdir diode-server
cd diode-server
```

2. Agora, faça o download dos arquivos necessários para instalação
```bash
curl -o docker-compose.yaml https://raw.githubusercontent.com/netboxlabs/diode/refs/tags/diode-reconciler/v0.6.0/diode-server/docker/docker-compose.yaml
curl -o .env https://raw.githubusercontent.com/netboxlabs/diode/refs/tags/diode-reconciler/v0.6.0/diode-server/docker/sample.env
```
___

## :fontawesome-solid-gear: **3. Configurando o Diode Server**
Vamos alterar o arquivo de variáveis `.env` e criar um novo arquivo `docker-compose.override.yml` para sobrescrever as configurações do docker-compose.

### `.env`
Aqui vamos precisar alterar algumas variáveis para conectar o servidor do Diode ao nosso ambiente:

```bash
# Padrão, não precisa alterar
REDIS_PASSWORD=@FmnLoA*VnebyVnZoL.!-.6z
REDIS_HOST=diode-redis
REDIS_PORT=6378
RECONCILER_GRPC_HOST=diode-reconciler
RECONCILER_GRPC_PORT=8081
LOGGING_LEVEL=DEBUG
MIGRATION_ENABLED=true
MIGRATION_ENABLED=true
DIODE_TAG=0.6.0

# Caso você não use o Graphite, pode deixar a porta padrão 8080
DIODE_NGINX_PORT=81

# URL da API do Diode Plugin no Netbox
NETBOX_DIODE_PLUGIN_API_BASE_URL=http://172.10.10.5:8080/api/plugins/diode 

NETBOX_DIODE_PLUGIN_SKIP_TLS_VERIFY=true # Se estiver usando Https, pode deixar como false

# Chave API gerada na instalação do Diode plugin -> diode-to-netbox
DIODE_TO_NETBOX_API_KEY= 

# Chave API gerada na instalação do Diode plugin -> netbox-to-diode
NETBOX_TO_DIODE_API_KEY= 

# Chave API gerada na instalação do Diode plugin -> diode-ingestion
DIODE_API_KEY= 

# Chave API para autorizar as chamadas RPC entre o Ingester e o Reconciler.
# Exemplo de comando shell para geração: openssl rand -base64 40 | head -c 40
INGESTER_TO_RECONCILER_API_KEY=sXjJZe6BBzVuovrVyyH4Q3vbceqvDwh2kC3DRpML 
```
!!! tip "Dica" 
    As chaves de API `DIODE_TO_NETBOX_API_KEY`, `NETBOX_TO_DIODE_API_KEY` e `DIODE_API_KEY`, podem ser visualizadas no Netbox em: Menu Lateral > Diode > Configurações

### `docker-compose.override.yml`
Este arquivo é responsável para alterarmos as configurações do `docker-compose` sobreescrevendo as configurações do mesmo.

1. Primeiro, vamos criar o arquivo com o seguinte comando:
```bash
nano docker-compose.override.yml
```
2. Agora copie o conteúdo abaixo e cole no arquivo.
```bash
services:
  ingress-nginx:
    networks:
      br-lab:
        ipv4_address: 172.10.10.120
  diode-ingester:
    networks:
      - br-lab
  diode-reconciler:
    networks:
      - br-lab
  diode-redis:
    networks:
      - br-lab
networks:
  br-lab:
    external: true
```

___

## :simple-docker: **4. Deploy!**
Com o servidor do Diode devidamente configurado, agora é hora de colocá-lo em execução.

- Execute o comando abaixo para iniciar todos os serviços definidos no docker-compose.yml:
```bash
docker compose up -d
```

- Verifique se todos os serviços estão com o status UP
```bash
docker compose ps
```
```bash
NAME                       IMAGE                                STATUS
diode-diode-ingester-1     netboxlabs/diode-ingester:0.6.0      Up 
diode-diode-reconciler-1   netboxlabs/diode-reconciler:0.6.0    Up 
diode-diode-redis-1        redis/redis-stack-server:latest      Up 
diode-ingress-nginx-1      nginx:latest                         Up 
```

---

## :octicons-rocket-24: **5. Próximos Passos**
Com o servidor do Diode em funcionamento, estamos quase concluindo a automatização da descoberta e importação de dispositivos da rede no NetBox.

O próximo passo é configurar o Diode Client, componente responsável por coletar as informações diretamente dos dispositivos e enviá-las ao servidor do Diode para processamento.

Próximo: [Instalando o Diode Client](./Instalando%20o%20Diode%20Client.md)