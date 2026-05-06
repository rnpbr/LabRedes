# :material-power-plug-outline: Installing the Diode Server

The Diode Server is the central component of the Diode architecture. It is responsible for receiving, processing, and reconciling data sent by clients (scripts or agents) and integrating it into NetBox. Utilizing modern protocols such as gRPC and efficient formats such as Protobuf, the Diode Server validates the received information and executes the automated update of the inventory in NetBox via the API exposed by the plugin.

This server acts as an intelligent intermediary, ensuring that the entered data is correct, complete, and synchronized with existing records.

## :simple-git: **Plugin Repository**
Copy the link below or click to access the <a target="_blank" href="https://github.com/netboxlabs/diode-netbox-plugin">Github Repository</a>

```
https://github.com/netboxlabs/diode-netbox-plugin
```

---

## :material-scale-balance: **1. Installation Requirements**
This documentation used the following components with their respective versions:

| Components           | Versions |
| --------------------- | ------- |
| **Netbox**            | v4.1.11 |
| **Diode Server**      | v0.6.0  |

---

## :material-arrow-down-box: **2. Downloading the Installation Files**

1. First, let's create a new folder to download the Diode Server files.
```bash
mkdir diode-server
cd diode-server
```

2. Now, download the necessary files for installation
```bash
curl -o docker-compose.yaml https://raw.githubusercontent.com/netboxlabs/diode/refs/tags/diode-reconciler/v0.6.0/diode-server/docker/docker-compose.yaml
curl -o .env https://raw.githubusercontent.com/netboxlabs/diode/refs/tags/diode-reconciler/v0.6.0/diode-server/docker/sample.env
```
___

## :fontawesome-solid-gear: **3. Configuring the Diode Server**
Let's change the `.env` variables file and create a new `docker-compose.override.yml` file to override the docker-compose configurations.

### `.env`
Here we need to change some variables to connect the Diode server to our environment:

```bash
# Default, no need to change
REDIS_PASSWORD=@FmnLoA*VnebyVnZoL.!-.6z
REDIS_HOST=diode-redis
REDIS_PORT=6378
RECONCILER_GRPC_HOST=diode-reconciler
RECONCILER_GRPC_PORT=8081
LOGGING_LEVEL=DEBUG
MIGRATION_ENABLED=true
MIGRATION_ENABLED=true
DIODE_TAG=0.6.0

# If you are not using Graphite, you can leave the default port 8080
DIODE_NGINX_PORT=81

# Diode Plugin API URL in Netbox
NETBOX_DIODE_PLUGIN_API_BASE_URL=http://172.10.10.5:8080/api/plugins/diode

NETBOX_DIODE_PLUGIN_SKIP_TLS_VERIFY=true # If using Https, can leave as false

# API Key generated in the Diode plugin installation -> diode-to-netbox
DIODE_TO_NETBOX_API_KEY=

# API Key generated in the Diode plugin installation -> netbox-to-diode
NETBOX_TO_DIODE_API_KEY=

# API Key generated in the Diode plugin installation -> diode-ingestion
DIODE_API_KEY=

# API Key to authorize RPC calls between the Ingester and the Reconciler.
# Example shell command to generate: openssl rand -base64 40 | head -c 40
INGESTER_TO_RECONCILER_API_KEY=sXjJZe6BBzVuovrVyyH4Q3vbceqvDwh2kC3DRpML
```
!!! tip "Tip"
    The API keys `DIODE_TO_NETBOX_API_KEY`, `NETBOX_TO_DIODE_API_KEY` and `DIODE_API_KEY` can be viewed in Netbox under: Side Menu > Diode > Configurations

### `docker-compose.override.yml`
This file is responsible for changing the `docker-compose` settings by overwriting its configurations.

1. First, let's create the file with the following command:
```bash
nano docker-compose.override.yml
```
2. Now copy the content below and paste it into the file.
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
With the Diode server properly configured, it's now time to put it into operation.

- Run the command below to start all services defined in docker-compose.yml:
```bash
docker compose up -d
```

- Check if all services have the UP status
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

## :octicons-rocket-24: **5. Next Steps**
With the Diode server running, we are almost finishing the automation of network device discovery and import into NetBox.

The next step is to configure the Diode Client, the component responsible for collecting information directly from the devices and sending it to the Diode server for processing.

Next: [Installing the Diode Client](./Instalando%20o%20Diode%20Client.md)