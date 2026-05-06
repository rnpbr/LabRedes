# :material-power-plug-outline: Installing the Diode Client

The Diode Client is responsible for sending the collected data to the Diode Server using gRPC/Protobuf, allowing for the subsequent ingestion of this information into NetBox.

There are different ways to use the Client. This documentation will present the use of the Orb Agent, developed by NetBox Labs. This agent not only performs automated network and device discovery, but also offers observability features on the monitored equipment.

Alternatively, as described in the <a target="_blank" href="https://docs.netboxlabs.com/netbox-extensions/diode/diode-client/">official NetBox documentation</a>, the Diode Client can also be used as a Python SDK, ideal for integrating custom scripts that collect and send data to the Diode Server.

## :simple-git: **Plugin Repository**
Copy the link below or click to access the <a target="_blank" href="https://github.com/netboxlabs/orb-agent">Github Repository</a>

```
https://github.com/netboxlabs/orb-agent
```

---

## :material-scale-balance: **1. Installation Requirements**
This documentation used the following components with their respective versions:

| Components           | Versions |
| --------------------- | ------- |
| **Netbox**            | v4.1.11 |
| **Orb Agent**         | v1.2.0  |

---

## :material-arrow-down-box: **2. Files Required for Installation**

1. First, let's create a new folder to download the Diode Server files.
```bash
mkdir orb-agent
cd orb-agent
```

Now, let's create the necessary files for the Orb-Agent installation

### :simple-docker: **2.1. `docker-compose.yml`**
1. First, let's create the file with the following command:
```bash
nano docker-compose.yml
```
2. Now copy the content below and paste it into the file.
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

The agent needs to be on the same network as the devices to be imported. Since we are in a docker environment, let's add it to the default laboratory network `br-lab`.

### :fontawesome-solid-square-root-variable: **2.2. `.env`**
The file containing the variables responsible for configuring the Orb-Agent.

1. First, let's create the file with the following command:
```bash
nano .env
```

2. To fill the `DOCKER_SUBNET` variable with the subnet of the `br-lab` network, use the command:
```bash
docker network inspect br-lab | grep "Subnet"
```

3. Now copy the content below and paste it into the file.
```bash
ORB_TAG=1.2.0
DOCKER_NETWORK=br-lab # docker network

# Docker network where the agent will collect IPs
DOCKER_SUBNET=172.10.10.0/24
 
# API Key for connection with Diode Server -> diode-ingestion
DIODE_API_KEY=507006398ea55f210835a66ee98b2a301d9abf6d

# Diode Server URL
DIODE_HOST=172.10.10.120:80 

# Your choice
AGENT_NAME=agent1 # Agent name
SITE_NAME=RNP # Site name to be added/created in Netbox
SCHEDULE='"*/10 * * * *"' # Time interval for re-collecting data
```

4. After defining the variables, use the commands below to allow and export the variables in your environment:
```bash
set -o allexport
source .env
```

### :material-face-agent: **2.3. `agent.yaml`**
In the Orb-Agent, configurations are defined through the `agent.yaml` file. It is in this file that we configure the connection with the **Diode Server**, specify the location for importing variables or access credentials, and define the types of discovery that the agent should perform.

#### :fontawesome-solid-gear: **2.3.1. Config Manager**
The `config_manager` section defines how the Orb-Agent should obtain its configuration information. The configuration manager is responsible for processing this data, retrieving the defined policies, and passing them on to the appropriate backend. See other methods in the <a target="_blank" href="https://github.com/netboxlabs/orb-agent?tab=readme-ov-file#config-manager">documentation</a>

```bash
orb:
  config_manager:
    active: local
  ...
```

#### :material-key-wireless: **2.3.2. Secrets Manager**
The `secrets_manager` section defines how the Orb-Agent should obtain and inject secrets (such as passwords and tokens) into policies. This manager can connect to external secret repositories, such as HashiCorp Vault, to securely retrieve sensitive information, preventing it from being written directly in the configuration files. See other methods in the <a target="_blank" href="https://github.com/netboxlabs/orb-agent?tab=readme-ov-file#secrets-manager">documentation</a>

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

**In our case we will not use this section**

#### :material-server: **2.3.3. Backends**
This section defines how the Orb-Agent backends should be activated. It has the following options:

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
The special `common` subsection, within the backends section, defines settings that are shared among all backends. Currently, this section allows passing the Diode server connection settings to all backends in a centralized manner.

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
The `policies` section defines which discovery policies should be assigned to each backend. Each policy describes specific settings for the discovery type, such as scheduling, default properties, and scope (targets).

Each backend can execute multiple policies at the same time, as long as each has a unique name within that backend. These policies are grouped into subsections according to the responsible backend.

```bash
orb:
 ...
 policies:
   device_discovery:
     device_policy_1:
       # See docs/backends/device_discovery.md
   network_discovery:
     network_policy_1:
      # See docs/backends/network_discovery.md
   worker:
     worker_policy_1:
      # See docs/backends/worker.md
```

Links:

- <a target="_blank" href="https://github.com/netboxlabs/orb-agent/blob/develop/docs/backends/device_discovery.md">Device Discovery</a>

- <a target="_blank" href="https://github.com/netboxlabs/orb-agent/blob/develop/docs/backends/network_discovery.md">Network Discovery</a>

- <a target="_blank" href="https://github.com/netboxlabs/orb-agent/blob/develop/docs/backends/worker.md">Worker</a>

### :octicons-repo-template-16: **3. `agent.template.yaml`**
After understanding a bit of the Orb-Agent structure, let's move on to a practical example with a simple template that can be used to map the `br-lab` docker network and some devices in it. In this file we will use the backends: `network_discovery` and `device_discovery`.

!!! tip "Tip" 
    Remember: the `Orb-Agent` uses the `agent.yaml` file as a configuration base. **This file must be generated in your local environment** and, when uploading the container, it needs to be copied into it.

1. Let's create the `agent.template.yaml` file.
```bash
nano agent.template.yaml
```

2. Now, copy and paste the content into the created file:
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

3. Now let's generate the `agent.yaml` file according to the variables defined in `.env`.
```bash
envsubst < agent.template.yaml > agent.yaml
```

4. Check if the file fills all variable spaces with their respective values. Your output should be something similar to:
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
With the Orb-Agent compose configured and the `agent.yaml` file generated, it's now time to put it into execution.

- Run the command below to start all services defined in docker-compose.yml:
```bash
docker compose up # or to run in the background
docker compose up -d 
```

- This configuration should return the IPs of the `172.10.10.0/24` network and the data of the three devices defined every 10 minutes.

---

## :octicons-rocket-24: **5. Conclusion**
With the Orb-Agent properly configured and running, you have a powerful automation and active discovery tool in your network. It allows the continuous and structured collection of data about devices and infrastructure, sending this information directly to NetBox via Diode Server, securely and flexibly.

Whether using custom policies or integrating with secrets and configuration managers, the Orb-Agent facilitates the scalability of network asset management and significantly contributes to keeping your environment updated, consistent, and documented.

In the next steps, you will be able to expand the discoveries, refine specific policies for different backends, and take advantage of the potential of NetBox as the source of truth for your infrastructure.