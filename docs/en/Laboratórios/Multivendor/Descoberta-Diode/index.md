# Diode Multivendor Discovery

## :material-bookmark: **Introduction**

This lab simulates a network with 3 routers from different vendors (Juniper, Cisco, and Huawei) configured with OSPF and SNMP, integrating Diode components (plugin, server, and agent) and Netbox for automated device import and management.

---

## :fontawesome-solid-prescription-bottle: 1. **Description**

### :octicons-goal-16: 1.1 **Lab Objective**

The objective of this lab is to practically demonstrate the process of automated discovery and import of multivendor network devices, encompassing different models and manufacturers, and their respective configurations into Netbox, using the diode-plugin, diode-server, and orb-agent.

![Topologia.svg](../../../../img/labs_imgs/Diagrama_fluxo_diode_multivendor.svg)


### :material-lan: 1.2 **Lab Topology**
Below is the topology showing the three routers — Juniper, Cisco, and Huawei — in addition to the servers involved in the architecture.

![Topologia.svg](../../../../img/labs_imgs/Topologia_discovery_lab_diode_multivendor.svg)

The routers are configured with the following technologies:

- **OSPF (Open Shortest Path First)**: Used for dynamic routing, allowing devices (regardless of manufacturer) to exchange information about routes and topology.
- **SNMP (Simple Network Management Protocol)**: Used for telemetry collection and discovery, ensuring compatibility with Juniper, Cisco, and Huawei devices.
---

## :octicons-search-16: **2. Applications**

### Examples of Applications

This lab demonstrates a realistic architecture for automatic device discovery in environments where multiple vendors coexist.

#### Possible Applications:

- **Multivendor discovery automation:** Automatic detection of Juniper, Cisco, and Huawei devices and registration of their inventories in Netbox.
- **Standardization of heterogeneous inventory:** Creation of a unified device database regardless of the vendor.
- **Creation of a centralized device repository:** Building a reliable database of real-time network data.
- **Practical study of SNMP in hybrid environments:** Practical comparison between different MIBs and manufacturer standards.
- **Diode + Netbox integration in real-world scenarios:** Practice in collecting and integrating network data.


---


## :material-tools: **3. Requirements**
### :material-alert: 3.1 Prerequisites

To start the lab, it is necessary to install and configure the following components:

- Netbox
- Diode Plugin
- Diode Server
- Orb Agent
- Containerlab
- Docker

If your environment is not configured, follow the steps in [Configuration Guide](../../../../Getting%20Started.md)


### :material-alert: 3.2 Computational Requirements Table

| Requirement           | Details |
|---------------------| --- |
| **CPUs**            | 4 vCPUs (minimum recommended) |
| **RAM Memory**     | 12 GB |
| **Disk Space** | 10 GB |
| **Containerlab**    | 0.64.0 |
| **Created Network**     | br-lab |

!!! tip "Tip"
    Verify that the Docker and Containerlab versions are compatible to avoid errors during deployment.

!!! warning "Attention"
    Verify that your processor has **hardware virtualization support** and that this functionality is **enabled in the BIOS/UEFI**.
    - In **Intel** processors, this technology is called **VT-x** (Intel Virtualization Technology).
    - In **AMD** processors, it is known as **AMD-V** (AMD Virtualization).

    Without this feature enabled, images like **vJunos-router** will not function correctly.
---

## :octicons-tools-16: 4. Installation

### :material-network-strength-4-cog: 4.1 Configuring the Docker Network

Before starting the containers, create the bridge network that will interconnect the devices:

```bash
docker network create \
  --driver=bridge \
  --opt com.docker.network.bridge.name=br-lab \
  --subnet=172.10.10.0/24 \
  br-lab
```

### :material-git: 4.2 Cloning the Lab Repository

Execute the script below to download and configure the lab automatically:

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/discovery-lab-diode-multivendor/get.sh?ref_type=heads&inline=false" && sh get.sh && cd discovery-lab
    ```

=== "Windows"

    ```bat
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/discovery-lab-diode-multivendor/get.bat?ref_type=heads&inline=false" && call get.bat && cd discovery-lab
    ```

!!! tip "Tip"
    On Linux/Mac, use `chmod +x get.sh` before running the script if it does not have execute permissions.


---

## :fontawesome-solid-house-chimney: 5. Environment Deployment

### :material-router-wireless: 5.1 Starting the Routers with Containerlab

Here, the three Juniper/Cisco/Huawei devices will be initialized.
The boot time may vary depending on the manufacturer.

```bash
sudo clab deploy -t clab/discovery-lab.clab.yaml
```

!!! warning "Debug"
    The devices may take about 10 minutes to become fully operational.
    If an error occurs, check the command output for possible error messages. Use `docker logs <container_name>` to debug.


### :material-server: 5.2 Starting the Diode Server
!!! tip "Tip"
    If you already have the Diode server configured, just skip this step.

1. Let's create a new folder to store the diode-server files:
```bash
mkdir diode-server
cd diode-server
```

2. Now, let's download the quick start script:
```bash
curl -sSfLo quickstart.sh https://raw.githubusercontent.com/netboxlabs/diode/release/diode-server/docker/scripts/quickstart.sh
chmod +x quickstart.sh
```

3. Then, just run the script passing the url of your netbox:
```bash
./quickstart.sh https://<netbox-server>
```

4. Finally, just start the containers:
```bash
docker compose up -d
```

5. To extract the credentials needed to install the plugin, execute the command below:
```bash
echo $(jq -r '.[] | select(.client_id == "netbox-to-diode") | .client_secret' ./oauth2/client/client-credentials.json)
```

!!! tip "Tip"
    **Store the token**, you will need to add it to the configuration below.


---
### :material-relation-one-to-one: 5.3 Installing the Plugin in Netbox
In this step, we will install the diode plugin, which is responsible for establishing the connection between the diode-server and Netbox.

#### :fontawesome-solid-gear: **5.3.1 Configuring the Netbox version:**

1. First, let's clone the Netbox Docker repository:
```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
```
2. Now, let's go to Release 3.2.1:
```bash
cd netbox-docker/
git checkout 3.2.1
```

!!! tip "Information"
    We changed the repository branch to have access to Netbox version 4.2.4.

!!! tip "Tip"
    All commands below will be executed inside the netbox root directory `netbox-docker/`.


#### :material-text-box: **5.3.2 plugin_requirements.txt**
This file contains a list of Netbox plugins (as PyPI Python packages) that must be installed during the Docker image build.

Execute the following command to write the package inside the `plugin_requirements.txt` file.

```bash
echo "netboxlabs-diode-netbox-plugin" >> plugin_requirements.txt
```

#### :material-docker: **5.3.3 DockerFile-Plugins**
This is the DockerFile used to build the custom docker image.

1. Create the file and access it with an editor:
```bash
nano DockerFile-Plugins
```

2. Copy the content below and paste it into the file:
```bash
FROM netboxcommunity/netbox:v4.2.4

COPY ./plugin_requirements.txt /opt/netbox/
RUN /usr/local/bin/uv pip install -r /opt/netbox/plugin_requirements.txt
```

#### :material-docker: **5.3.4. docker-compose.override.yml**
As the name implies, this file contains the configurations that will overwrite the `docker-compose.yml`.

If you haven't configured the `br-lab` network yet. Access: [Configuring the Docker Network](../../../../Laboratórios/Juniper/vJunos/Descoberta/index.md/#41-configuring-the-docker-network)

1. Create the file and access it with an editor:
```bash
nano docker-compose.override.yml
```

2. Copy the content below and paste it into the file:
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

The changes made were:

- adding Netbox to the `br-lab` network.
- changing the dockerfile to `Dockerfile-Plugins`, created previously.
- Also changed the image of the services to: `netbox:latest-plugins`.

#### :material-power-plug-outline: **5.3.5. plugins.py**
This file is responsible for setting the specific configurations for each plugin.

1. Access the file with the editor:
```bash
nano configuration/plugins.py
```

2. Copy and paste the content into the file:
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

!!! tip "Tip"
    The token stored during diode-server installation must be passed in the option: `netbox_to_diode_client_secret`.

---

#### :simple-docker: **5.3.6 Build and Deploy!**
Now your Netbox is configured and ready for deploy, follow the commands below and build a new instance of Netbox!

1. Build the image:
```bash
docker compose build --no-cache
```

2. Start the containers:
```bash
docker compose up -d
```

3. Create the necessary migrations with the command below:
```bash
docker compose exec -it netbox ./manage.py migrate netbox_diode_plugin
```

#### :material-import: **5.3.7. Generating credentials for the agent**
We need to create credentials for the diode agent to communicate and forward the data collected from the devices to the diode-server.

1. Access your Netbox and go to the side menu.
2. Go to `Diode` > `Client Credentials`.
3. Click on the top button `Add Credential`.
4. Type a name for your credential.
5. Store the `Client Id` and `Client Secret`.

---

## :octicons-key-16: 6. Orb-Agent
The orb-agent is a diode component responsible for collecting data on devices.

### 6.1 **Configuring the agent**

1. Access the `orb-agent` folder:
```bash
cd ./orb-agent
```

2. In the `.env` file, configure the variables according to your environment.
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

Here are the `Client Id` and `Client Secret` generated in the diode plugin in Netbox.

3. Now, let's apply the variables to the juniper import template with the command:
```bash
set -o allexport && source .env && envsubst < agent.snmp.template.yaml > agent.yaml
```

### 6.2 **Starting Data Collection**
Finally, just bring up the container to start importing devices into Netbox!

```bash
docker compose up
```

✅ Track in real-time in Netbox the devices being collected by the agent.

⏱️ In addition, you can configure a collection interval for the agent to perform the import automatically and periodically, without the need for manual intervention.
___

## :material-access-point: 7. Access

After the lab is started, you can access the devices and services configured on the network.

### :material-table: 7.1 Table of IPs and Service Ports

Here is the table of devices, IPs, and service ports available in the lab.

| Device  | Manufacturer | IP            | Port | Service |
| ------------ | ---------- | ------------- | ----- | ------- |
| **node1**    | Juniper    | 172.10.10.201 | 22    | SSH     |
| **node2**    | Cisco      | 172.10.10.202 | 22    | SSH     |
| **node3**    | Huawei     | 172.10.10.203 | 22    | SSH     |
| **Diode**    | —          | localhost     | 8080  | API     |
| **Netbox**   | —          | localhost     | 8000  | Web UI  |
| **Graphite** | —          | 172.20.20.1   | 8081  | Web UI  |


### :material-key-link: 7.2 Access Passwords

Here is the table with the access passwords for the services configured in the lab.

| Service | User | Password |
| --- | --- | --- |
| **node1 (SSH)** | admin | admin@123 |
| **node2 (SSH)** | clab | clab@123 |
| **node3 (SSH)** | admin | admin |
| **Netbox (Web)** | Admin | Admin |

!!! warning "Attention"
    Before accessing, access the log of a device to verify that it has been started and configured correctly.
---

## :octicons-rocket-24: 8. Next Steps
With the lab completed, you can follow some of the steps below as **extra**.

- Test SNMP collection differences between Juniper, Cisco, and Huawei.
- Compare the structure of MIBs used in the import.
- Add new devices from any manufacturer to check compatibility.
---

### :fontawesome-solid-paintbrush: 9. Conclusion

✅ Now you have learned how to use Diode components to automatically import a network composed of Juniper, Cisco, and Huawei devices, building a complete inventory in Netbox and enabling the creation of your Digital Twin with Netreplica.