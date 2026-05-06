# :material-bookmark: Multivendor Logs ELK

This lab simulates, via Containerlab, the interconnection between three routers — Juniper, Huawei, and Cisco — with dynamic routing via OSPF, and log export via Syslog to an observability infrastructure based on the ELK stack (Elasticsearch, Logstash, Kibana), using Elastic Agents managed by Fleet for data collection and sending.

---

## :material-bookmark: 1. Description

### :octicons-goal-16: 1.1 Lab Objective

The objective of this lab is to simulate the export and centralized collection of logs from routers of different manufacturers (Juniper, Huawei, and Cisco) using the Syslog protocol (UDP 514).
The collection is performed by Elastic Agents, configured to receive logs directly from the devices and forward the events to Elasticsearch, under the management of the Fleet Server.
The visualization and analysis of logs occur through Kibana, enabling a modern approach to multivendor observability.

### :material-lan: 1.2 Lab Topology

![Lab Topology](../../../../img/labs_imgs/Topologia_Logs_ELK.svg)

**Topology Description**

 * Three routers (Juniper, Cisco, Huawei) interconnected in a ring topology with point-to-point /31 links.
 * Dynamic routing via OSPF between the routers.
 * Log export via Syslog (UDP/514) to the monitoring server.
 * Elastic Agent acts as a collector, listening on port 514/UDP, parsing the events and sending them to Elasticsearch.
 * Fleet Server manages and monitors Elastic agents.
 * Elasticsearch stores and indexes the received logs.
 * Kibana provides the graphical interface for viewing, searching, and correlating logs.
 * External network br-lab connects the routers to the ELK-based monitoring infrastructure.

---

## :octicons-search-16: 2. Applications

### Application Examples

This lab constitutes a basis for academic and applied experimentation in monitoring, observability, and event analysis in multivendor environments, focusing on the use of the Elastic Stack and Fleet Management.

#### Possible Applications:

* **Multivendor NOC/SOC training** – Practical simulation of log export and analysis in a Juniper, Huawei, and Cisco environment.
* **Syslog collection validation** – Compatibility testing and log parsing via Elastic Agents without the use of Logstash.
* **Real-time visualization** – Creation of dashboards in Kibana for network events and metrics.
* **Centralized monitoring** – Use of Fleet to manage agents and collection policies in a unified way.
* **Observability integration teaching** – Educational application about Syslog, Elastic Agents, Fleet, Elasticsearch, and Kibana in multivendor networks.
---

## :material-tools: 3. Requirements

Below are listed the minimum hardware and software requirements needed to run the lab. Be sure to include essential tools like **Containerlab** and **Docker**, in addition to the previously created `br-lab` network.
To learn more about these items, access:

- [Creating the br-lab Network](../../../../Ferramentas/Primeiros passos - preparando o ambiente.md)
-  <a target="_blank" href="https://www.docker.com/get-started/">Docker Installation</a>
-  <a target="_blank" href="https://containerlab.dev/install/">Containerlab Installation</a>

And have the ELK stack previously installed and configured for log ingestion, to learn more about the installation access: [Configuring Syslog in ELK](../../../../Ferramentas/Elasticsearch/Configurando Syslog no ELK.md)

### :material-alert: Minimum Requirements Table:

| Requirement           | Details                                                                             |
| ------------------- |--------------------------------------------------------------------------------------|
| **CPUs**            | 6 vCPUs                                                                              |
| **RAM Memory**      | 16 GB                                                                                |
| **Disk Space**      | 20 GB (recommended)                                                                  |
| **Containerlab**    | 0.45.0 or higher                                                                   |
| **Docker Engine**   | 23.0.3 or higher                                                                   |
| **Images**          | `vr-vjunos:23.2R1.14`, `vrnetlab/huawei_vrp:ne40e-8.180`, `xrd-control-plane:7.10.2` |
| **Docker Network**  | `br-lab`                                                                             |

!!! warning "Attention" 
    Verify that your processor has **hardware virtualization support** and that this feature is **enabled in the BIOS/UEFI**.
    - In **Intel** processors, this technology is called **VT-x** (Intel Virtualization Technology).
    - In **AMD** processors, it is known as **AMD-V** (AMD Virtualization).

    Without this feature enabled, images such as **vJunos-router** will not work correctly.
---

## :fontawesome-solid-prescription-bottle: 4. Deploying the Lab

You can deploy using a ready-made script or manually configure the lab files.

### :material-git: 4.1 Ready Deployment

This method allows the user to **download a pre-assembled version** of the lab, with the topology and configurations already defined. Simply download the repository and proceed to the beginning of the execution.

!!! tip "Tip" 
    Ready deployment is useful for those who want to quickly start with a configured environment.

#### :octicons-download-16: Downloading the Lab

Execute the script below to download and configure the lab automatically:

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/logs-elk-multvendor/get.sh" && sh get.sh && cd logs-elk-multvendor
    ```

=== "Windows"

    ```bat
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/logs-elk-multvendor/get.bat" && call get.bat && cd logs-elk-multvendor
    ```

!!! tip "Tip"
    On Linux/Mac, use `chmod +x get.sh` before running the script if it does not have execute permission.

---

## :octicons-play-16: 5. Initializing the Lab

After downloading or customizing, follow the steps below to **start the lab**.
Execute the command below inside the downloaded directory.

```bash
sudo containerlab deploy
```

This command will create the router containers, configure the links, and start the monitoring services.

!!! tip "Debugging"
    Use `docker logs -f <container_name>` to check the status of the services if something does not work.

---

## :material-access-point: 6. Accessing the Devices

### :material-table: 6.1 IPs and Ports of Services

| Device           | Access IP     | Port(s) | Service            |
|------------------| ------------- |-----| ------------------ |
| **node1**        | 172.10.10.201 | 22      | SSH               |
| **node2**        | 172.10.10.202 | 22      | SSH               |
| **node3**        | 172.10.10.203 | 22      | SSH               |
| **Fleet Server** | 172.10.10.110 | 8220     | Data Ingestion |
| **Elasticsearch** | 172.10.10.108 | 9200     | Database          |
| **Kibana**       | 172.10.10.109 | 5601     | Web Interface     |
| **Graphite**     | 172.10.10.119 | 8080    | Web UI (Graphite) |

### :material-key-link: 6.2 Access Passwords

| Service         | User     | Password       |
|-----------------| ------- |----------------|
| **node1 (SSH)** | `admin`  | `admin@123`    |
| **node2 (SSH)** | `clab`   | `clab@123`     |
| **node3 (SSH)** | `admin`  | `admin`        |
| **Kibana**      | `elastic`| `admin@123`    |

!!! warning "Startup Verification"
    Before accessing the services, use `docker ps` and check the container logs to ensure they are working correctly.

---

## :octicons-browser-16: 7. Observability and Visualization

!!! Warning "Attention"
    Due to the way settings are applied on the vJunos-router, syslog configuration must be done manually.
    Follow the step-by-step instructions below to send all system logs to the remote log server.

### Step by step

Access node1 via ssh and run:

```junos
configure
```

* Enters **configuration mode** of Junos.
* All subsequent commands will change the device's configuration.

```junos
set system syslog host 172.10.10.110 any any
```

* Sets the remote log server (**172.10.10.110**) as the destination.
* `any any` means: send **any facility** (system, kernel, daemon, auth, etc.) at **any severity level** (emergency, alert, critical, warning, info, debug).
* In practice: **all system events will be sent to this server**.

```junos
set system syslog source-address 172.10.10.201
```

* Defines the **source IP** of the log packets as **172.10.10.201** (the IP of the vJunos-router).
* This ensures that the syslog traffic leaves through the interface that has this address.
* It is important for the log server to correctly recognize the origin of the messages.

```junos
commit
```

* Applies the changes made to the configuration.

!!! warning "attention"
    After starting the Vjunos, it may take between 3 to 6 minutes for all routes to come up and the configuration to work correctly.

* Only after this command do the logs start being sent to the configured destination.

At the end of the deployment you will see the logs in Kibana like this:

![Lab example in production](../../../../img/labs_imgs/example/Exemplo_Logs_ELK.png)

### 7.1 Elastic Agent

The **Elastic Agent** is responsible for collecting and sending logs exported via **Syslog (UDP/514)** by the Juniper, Huawei, and Cisco routers.
It acts as a unified agent under the management of the **Fleet Server**, performing the parsing, enrichment, and forwarding of data directly to **Elasticsearch**.

---

### 7.2 Elasticsearch

Document-oriented database used to store and index the logs collected by the agents.
Allows queries, aggregations, and correlations between events from different devices.
Accessible via port **9200**.

---

### 7.3 Kibana

Web interface for analyzing and visualizing logs stored in Elasticsearch.
Allows the creation of dashboards, real-time queries, and Fleet management.
Accessible at `https://<your IP or localhost>:5601`.

---

### 7.4 Fleet Server

The **Fleet Server** runs in the same container as the **Elastic Agent**, unifying the collection and management functions.
It manages Elastic agents, applies collection policies, receives logs via Syslog (UDP/514), and sends the data to Elasticsearch.
Operates on port **8220/TCP** and is administered through **Kibana → Management → Fleet**.