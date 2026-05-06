# Juniper vJuniper Discovery

## :material-bookmark: **Introduction**

This lab simulates a network with 3 routers configured with OSPF and SNMP, integrating the Diode components (plugin, server, and agent) and Netbox for automated device import and management.

---

## :fontawesome-solid-prescription-bottle: 1. **Description**

### :octicons-goal-16: 1.1 **Lab Objective**

The objective of this lab is to demonstrate, in a practical way, the process of automated import of network devices and their respective configurations into Netbox, using the diode-plugin, diode-server, and orb-agent.

![Topology.svg](../../../../../img/labs_imgs/Diagrama_fluxo_diode.svg)

### :material-lan: 1.2 **Lab Topology**
Below is the topology in image format, representing the routers, servers, and their connections.

![Topology.svg](../../../../../img/labs_imgs/Topologia_discovery_lab_diode.svg)

The routers are configured with the following technologies:

- **OSPF (Open Shortest Path First)**: Used for dynamic routing in the network, allowing routers to exchange information about routes and topology updates.
- **SNMP (Simple Network Management Protocol)**: Used for network monitoring and management, allowing access to telemetry information from devices.
---

## :octicons-search-16: **2. Applications**

### Application Examples

This lab is focused on practical experimentation with discovery and automatic import of devices in IP networks, integrating Diode and Netbox.

#### Possible Applications:

- **Network discovery automation:** Automatic identification of devices and registration in Netbox.
- **Training in NetDevOps and inventory management:** Training in the integration of network documentation tools via API.
- **Creation of a centralized device repository:** Building a reliable database of network data in real time.
- **Study of Diode + Netbox integration via API:** Demonstrates how the agent collects, the server processes, and the plugin registers in the inventory.
- **Teaching SNMP discovery and centralized management:** Practice in collecting and integrating network data.

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
    Check if the Docker and Containerlab versions are compatible to avoid errors during deployment.

!!! warning "Attention"
    Verify that your processor has **hardware virtualization support** and that this feature is **enabled in the BIOS/UEFI**.
    - In **Intel** processors, this technology is called **VT-x** (Intel Virtualization Technology).
    - In **AMD** processors, it is known as **AMD-V** (AMD Virtualization).

    Without this feature enabled, images like **vJunos-router** will not work correctly.
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
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/discovery-lab-diode/get.sh?ref_type=heads&inline=false" && sh get.sh && cd discovery-lab
    ```

=== "Windows"

    ```bat
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/discovery-lab-diode/get.bat?ref_type=heads&inline=false" && call get.bat && cd discovery-lab
    ```

!!! tip "Tip"
    In Linux/Mac, use `chmod +x get.sh` before running the script if it does not have execution permission.

---

## :fontawesome-solid-house-chimney: 5. Environment Deployment

### :material-router-wireless: 5.1 Spinning up the Routers with Containerlab

Start the topology with the command:

```bash
sudo clab deploy -t clab/discovery-lab.clab.yaml
```

!!! warning "Debug"
    The devices may take about 10 minutes to be fully operational.
    If an error occurs, check the command output for possible error messages. Use `docker logs <container_name>` to debug.

### :material-server: 5.2 Launching the Diode Server
!!! tip "Tip"
    If you already have the Diode server configured, simply skip this step.

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

3. Then, simply run the script passing the URL of your Netbox:
```bash
./quickstart.sh https://<netbox-server>
```

4. Finally, just start the containers:
```bash
docker compose up -d
```

5. To extract the credentials required for plugin installation, execute the command below:
```bash
echo $(jq -r '.[] | select(.client_id == "netbox-to-diode") | .client_secret' ./oauth2/client/client-credentials.json)
```

!!! tip "Tip"
    **Store the token**, you will need to add it in the following configuration.

---
### :material-relation-one-to-one: 5.3 Installing the Plugin in Netbox
In this step, we will install the Diode plugin, responsible for establishing the connection between the Diode server and Netbox.

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
    All commands below will be executed within the Netbox root directory `netbox-docker/`.

#### :material-text-box: **5.3.2 plugin_requirements.txt**
This file contains a list of Netbox plugins (as PyPO Python packages) that should be installed during the Docker image build.

Execute the following command to write the package inside the `plugin_requirements.txt` file.

```bash
echo "netboxlabs-diode-netbox-plugin" >> plugin_requirements.txt
```

#### :material-docker: **5.3.3 DockerFile-Plugins**
This is the DockerFile used to build the customized Docker image.

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
As the name implies, this file contains the configurations that will override `docker-compose.yml`.

If you have not yet configured the `br-lab` network. Access: [Configuring the Docker Network](../../../../Laboratórios/Juniper/vJunos/Descoberta/index.md/#41-configuring-the-docker-network)

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

- Adding Netbox to the `br-lab` network.
- Changing the dockerfile to `Dockerfile-Plugins`, created previously.
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
    The token stored during the diode-server installation must be passed in the option: `netbox_to_diode_client_secret`.

---

#### :simple-docker: **5.3.6 Build and Deploy!**
Now your Netbox is configured and ready for deployment, follow the commands below and build the new Netbox instance!

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
We need to create credentials for the Diode agent to communicate and pass the collected data from the devices to the Diode server.

1. Access your Netbox and go to the side menu.
2. Go to `Diode` > `Client Credentials`.
3. Click the `Add Credential` button at the top.
4. Enter a name for your credential.
5. Store the `Client Id` and `Client Secret`.

---

## :octicons-key-16: 6. Orb-Agent
The orb-agent is a diode component responsible for collecting data from devices.

### 6.1 **Configuring the agent**

1. Access the `orb-agent` folder:
```bash
cd ./orb-agent
```

2. In the `.env` file, configure the variables according to your environment.
```bash
DOCKER_NETWORK=br-lab           # Container Network
DOCKER_SUBNET=172.10.10.0/24    # Devices Network
DIODE_CLIENT_ID=                # Diode Client Id
DIODE_CLIENT_SECRET=            # Diode Client Secret
DIODE_HOST=<your-ip>:8080       # Diode Server Url
AGENT_NAME=agent1               # Agent Name
SITE_NAME=RNP                   # Netbox Site Name
DEVICE_USERNAME=admin           # Device username
JUNIPER_PASSWORD=admin@123      # Device Password
JUNIPER_COMMUNITY="public"      # Device Community
```

Here are the `Client Id` and `Client Secret` generated in the Diode plugin in Netbox.

3. Now, let's apply the variables to the Juniper import template with the command:
```bash
set -o allexport && source .env && envsubst < ./juniper/agent.device.template.yaml > agent.yaml
```

### 6.2 **Starting data collection**
Finally, just bring up the container to start importing devices into Netbox!

```bash
docker compose up
```

✅ Follow in real time on Netbox the devices being collected by the agent.

⏱️ In addition, you can configure a collection interval so that the agent performs the import automatically and periodically, without the need for manual intervention.
___

## :material-access-point: 7. Access

After the lab is started, you can access the devices and services configured on the network.

### :material-table: 7.1 Table of IPs and Service Ports

Here is the table of devices, IPs, and service ports available in the lab.

| Device | Access IP | Port | Service |
| --- | --- | --- | --- |
| **GO** | 172.10.10.12 | 22 | SSH |
| **MS** | 172.10.10.17 | 22 | SSH |
| **MT** | 172.10.10.18 | 22 | SSH |
| **Monitoring Server** | 172.20.20.1 | 8081 | Web (Graphite) |
| **Netbox** | localhost | 8000 | Zabbix |

### :material-key-link: 7.2 Access Passwords

Here is the table with the access passwords for the services configured in the lab.

| Service | User | Password |
| --- | --- | --- |
| **AC (SSH)** | admin | admin@123 |
| **MS (SSH)** | admin | admin@123 |
| **MT (SSH)** | admin | admin@123 |
| **Graphite (Web)** | admin | admin@123 |
| **Netbox (Web)** | Admin | Admin |

!!! warning "Attention"
    Before accessing, check the log of a device to verify that it has been started and configured correctly.
---

## :octicons-rocket-24: 8. Next Steps
With the lab completed, you can follow some steps below as **extra**.

- Explore other types of import, such as Network and SNMP discovery.
- Explore Netbox to view and manage the network inventory.
- Modify the topology as needed (in future custom versions).
- Consult the settings imported by the agent.
---

### :fontawesome-solid-paintbrush: 9. Conclusion

✅ Ready! Now you know how to use the Diode components to import your own network into Netbox, so you can also generate your own Digital Twin through Netreplica!