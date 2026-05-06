# :material-bookmark: Multivendor Logs Telegraf

This lab simulates, via Containerlab, the interconnection between three routers Juniper, Huawei and Cisco, with dynamic routing via OSPF, log export via Syslog using Telegraf, InfluxDB, Chronograf and Grafana.

---

## :material-bookmark: 1. Description

### :octicons-goal-16: 1.1 Lab Objective

The objective of the lab is to simulate the export of logs from three routers of different manufacturers (Juniper, Huawei and Cisco) to a centralized monitoring server, using the Syslog protocol. The monitoring system is composed of Telegraf, InfluxDB, Chronograf and Grafana, allowing the collection, storage and visualization of network metrics in real time.

### :material-lan: 1.2 Lab Topology

![Lab Topology](../../../../img/labs_imgs/Topologia_Logs_Telegraf.svg)

**Topology Description**

* Three routers (Juniper, Cisco, Huawei) interconnected in a ring topology with point-to-point /31 links.
* Dynamic routing via OSPF between routers.
* Log collection via Syslog udp (514).
* Observability with the TICK stack (Telegraf, InfluxDB, Chronograf) and Grafana.
* External network `br-lab` connects the nodes to the monitoring infrastructure.

---

## :octicons-search-16: 2. Applications

### Application Examples

This lab can be explored in various academic and applied research scenarios, serving as a basis for experimentation in monitoring and traffic visualization in networks with multiple routers.

#### Possible Applications:

* **Training NOC teams in a multivendor environment**: Simulates real operations with Juniper, Huawei and Cisco routers, using OSPF and log export via Syslog, allowing analysis of connectivity and troubleshooting.
* **Validation and testing of log collection via Syslog**: Allows you to verify the compatibility and behavior of different vendors in sending logs to Telegraf.
* **Real-time metric visualization and analysis**: Validate and test Grafana template forms to work with logs.
* **Centralized monitoring with Telegraf**: Evaluates Telegraf's ability to receive and process logs from heterogeneous devices, ensuring data integrity and consistency.
* **Teaching the integration of monitoring systems**: Provides practical learning on configuring Syslog, collecting metrics, and visualization in TICK stacks and Grafana in a multivendor scenario.
---

## :material-tools: 3. Requirements

Below are listed the minimum hardware and software requirements to run the lab. Be sure to include essential tools such as **Containerlab** and **Docker**, in addition to the previously created `br-lab` network.
to learn more about these items access:

- [Creation of the br-lab Network](../../../../Ferramentas/Primeiros passos - preparando o ambiente.md)
-  <a target="_blank" href="https://www.docker.com/get-started/">Docker Installation</a>
-  <a target="_blank" href="https://containerlab.dev/install/">Containerlab Installation</a>

And have the telegraf stack previously installed, to learn more about installing zabbix access: [Telegraf Installation](../../../../Ferramentas/Telegraf/index.md)

### :material-alert: Minimum Requirements Table:

| Requirement           | Details              |
| ------------------- |-----------------------|
| **CPUs**            | 4 vCPUs               |
| **RAM Memory**     | 8 GB                  |
| **Disk Space** | 10 GB (recommended)   |
| **Containerlab**    | 0.45.0 or higher    |
| **Docker Engine**   | 23.0.3 or higher    |
| **Images**         | `vr-vjunos:23.2R1.14`, `vrnetlab/huawei_vrp:ne40e-8.180`, `xrd-control-plane:7.10.2` |
| **Docker Network**     | `br-lab`              |

!!! warning "Attention"
    Check if your processor has **hardware virtualization support** and if this feature is **enabled in the BIOS/UEFI**.
    - In **Intel** processors, this technology is called **VT-x** (Intel Virtualization Technology).
    - In **AMD** processors, it is known as **AMD-V** (AMD Virtualization).

    Without this feature enabled, images such as the **vJunos-router** will not work correctly.
---

## :fontawesome-solid-prescription-bottle: 4. Deploying the Lab

You can perform the deployment via a ready-made script or manually configure the lab files.

### :material-git: 4.1 Ready-Made Deployment

This method allows the user to **download a pre-assembled version** of the laboratory, with the topology and configurations already defined. Simply download the repository and proceed to the start of execution.

!!! tip "Tip"
    Ready-made deployment is useful for those who want to get started quickly with a configured environment.

#### :octicons-download-16: Downloading the Lab

Run the script below to automatically download and configure the lab:

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/logs-telegraf-multvendor/get.sh" && sh get.sh && cd logs-telegraf-multvendor
    ```

=== "Windows"

    ```bat
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/logs-telegraf-multvendor/get.bat" && call get.bat && cd logs-telegraf-multvendor
    ```

!!! tip "Tip"
    On Linux/Mac, use `chmod +x get.sh` before running the script, if it does not have execute permission.

---

## :octicons-play-16: 5. Initializing the Lab

After downloading or customizing, follow the steps below to **start the lab**.
Run the command below inside the downloaded directory.

```bash
sudo containerlab deploy
```

This command will create the router containers, configure the links, and start the monitoring services.

!!! tip "Debugging"
    Use `docker logs -f <container_name>` to check the status of the services, if something does not work.

---

## :material-access-point: 6. Access to Devices

### :material-table: 6.1 IPs and Ports of Services

| Device     | Access IP  | Port(s) | Service            |
| --------------- | ------------- |-----| ------------------ |
| **node1**           | 172.10.10.201 | 22      | SSH               |
| **node2**           | 172.10.10.202 | 22      | SSH               |
| **node3**           | 172.10.10.203 | 22      | SSH               |
| **Telegraf**    | 172.10.10.114 | 161 | Metrics collection |
| **InfluxDB**    | 172.10.10.112 | 8086 | Time series database    |
| **Chronograf**  | 172.10.10.113 | 8888 | Analysis UI      |
| **Grafana**     | 172.10.10.111 | 3000 | Web Dashboard      |
| **Graphite** | 172.10.10.119 | 8080    | Web UI (Graphite) |

### :material-key-link: 6.2 Access Passwords

| Service          | User | Password             |
| ---------------- | ------- |-------------------|
| **node1 (SSH)**     | `admin`  | `admin@123`      |
| **node2 (SSH)**     | `clab`   | `clab@123`       |
| **node3 (SSH)**     | `admin`  | `admin`          |
| Grafana          | `admin` | `admin`           |
| InfluxDB         | `admin` | `influxpassword`  |

!!! warning "Initialization Verification"
    Before accessing the services, use `docker ps` and check the container logs to ensure they are working correctly.

---

## :octicons-browser-16: 7. Observability and Visualization

!!! Warning "Attention"
    Due to the way the configurations are applied in the vJunos-router, the syslog configuration must be done manually.
    Follow the step by step below to send all system logs to the remote log server.

### Step by step

Access node1 via ssh and execute:

```junos
configure
```

* Enters **configuration mode** of Junos.
* All subsequent commands will change the equipment configuration.

```junos
set system syslog host 172.10.10.114 any any
```

* Defines the remote log server (**172.10.10.114**) as the destination.
* `any any` means: send **any facility** (system, kernel, daemon, auth etc.) at **any severity level** (emergency, alert, critical, warning, info, debug).
* In practice: **all system events will be sent to this server**.

```junos
set system syslog source-address 172.10.10.201
```

* Defines the **source IP** of the log packets as **172.10.10.201** (the IP of the vJunos-router).
* This ensures that the syslog traffic leaves through the interface that has that address.
* It is important for the log server to correctly recognize the origin of the messages.

```junos
commit
```

* Applies the changes made to the configuration.

!!! warning "attention"
    After the start of Vjunos, it can take between 3 to 6 minutes to upload all routes and the configuration to work correctly.


* Only after this command do logs begin to be sent to the configured destination.

### 7.1 Telegraf

Telegraf is configured to collect metrics via:

* **syslog**: log export
* **IPFIX**: traffic flow export.

### 7.2 InfluxDB

Time series database where Telegraf metrics are stored. It can be accessed through port 8086.

### 7.3 Chronograf

Web interface for analyzing metrics stored in InfluxDB. Accessible at `http://172.10.10.113:8888`.

### 7.4 Grafana

Interactive visualization platform where data is presented in custom dashboards.