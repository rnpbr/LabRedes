# :material-bookmark: Juniper vJunos Zabbix Monitoring

This lab simulates, via Containerlab, the interconnection between two routers representing the BA–ES connection in the RNP, with monitoring via Zabbix and SNMPv2.

---

## :material-bookmark: 1. Description

### :octicons-goal-16: 1.1 Lab Objective

The “zabbix-rnp-lab” laboratory demonstrates the simulation of the connection between two routers representing the interconnection between BA and ES in the RNP backbone, using Containerlab. Routing between devices is performed using the OSPF protocol, ensuring dynamic route exchange. The main focus is to integrate this topology with Zabbix via SNMPv2, enabling real-time monitoring. In addition, the laboratory highlights the automatic device discovery functionality on the network.

### :material-lan: 1.2 Lab Topology

![Lab Topology](../../../../../img/labs_imgs/Topologia_Zabbix.svg)


The topology of this lab consists of two routers interconnected by a point-to-point /31 network, allowing direct communication between them. The routers are configured with OSPF to ensure dynamic routing between the interfaces. Network monitoring is done through an external network called br-lab, where the routers are connected by virtual interfaces. Through this configuration, Zabbix is able to monitor network connectivity and performance.

---

## :octicons-search-16: 2. Applications

### **Application Example**

This laboratory can be used in various academic and professional contexts. It is useful for simulating real-world network operation and monitoring scenarios, serving as an environment for validating configurations and testing interoperability between routing protocols and monitoring tools.

**Possible Applications:**

* **Training NOC (Network Operations Center) teams**: Replicates real-world connectivity situations between routers with OSPF and monitoring via SNMP to familiarize technicians with fault detection and analysis.
* **Performance evaluation of automatic discovery via SNMP**: Allows testing the operation of host discovery under different network and topology conditions.
* **Validation of SNMP templates in Zabbix**: Can be used to validate or develop SNMP monitoring templates for routers in controlled environments.
* **Teaching dynamic routing protocols**: Provides a practical learning environment about configuration and route exchange via OSPF in point-to-point networks.

---

## :material-tools: 3. Requirements

Below are listed the minimum hardware and software requirements necessary to run the lab. Be sure to include essential tools such as **Containerlab** and **Docker**, in addition to the previously created `br-lab` network.
To learn more about these items, access:

- [br-lab Network Creation](../../../../Ferramentas/Primeiros passos - preparando o ambiente.md)
-  <a target="_blank" href="https://www.docker.com/get-started/">Docker Installation</a>
-  <a target="_blank" href="https://containerlab.dev/install/">Containerlab Installation</a>
- 
And have Zabbix previously installed, to learn more about Zabbix installation, access: [Zabbix Installation](../../../../Ferramentas/Zabbix/index.md)

### :material-alert: Minimum Requirements Table:

| Requirement           | Details                                                                 |
| ------------------- | ------------------------------------------------------------------------ |
| **CPUs**            | 4 vCPUs                                                                  |
| **RAM Memory**     | 8 GB                                                                     |
| **Disk Space** | 10 GB (recommended)                                                      |
| **Containerlab**    | 0.45.0                                                                   |
| **Docker Engine**   | 23.0.3                                                                   |
| **Images**         | `vr-vjunos:23.2R1.14`                                                    |
| **Network Created**     | `br-lab`                                                                 |


!!! warning "Attention" 
    Check if your processor has **hardware virtualization support** and if this feature is **enabled in the BIOS/UEFI**.
    - In **Intel** processors, this technology is called **VT-x** (Intel Virtualization Technology).
    - In **AMD** processors, it is known as **AMD-V** (AMD Virtualization).

    Without this feature enabled, images such as **vJunos-router** will not work correctly.

---

## :fontawesome-solid-prescription-bottle: 4. Deploying the Lab

Here are the instructions to **deploy the lab**. You can choose a **ready-made deployment** or a **customized** one.

### :material-git: 4.1 Ready-made Deployment

This method allows the user to **download a pre-assembled version** of the laboratory, with the topology and configurations already defined. Simply download the repository and proceed to the start of execution.

!!! tip "Tip"
    The ready-made deployment is useful for those who want to get started quickly with a configured environment.

#### :octicons-download-16: Downloading the Lab

To download the lab, run the command corresponding to your operating system.

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/zabbix-lab/get.sh?ref_type=heads&inline=false" && sh get.sh && cd zabbix-lab
    ```


=== "Windows"

    ```bash
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/zabbix-lab/get.bat?ref_type=heads&inline=false" && call get.bat && cd zabbix-lab
    ```

This command will download the installation script and direct you to the lab directory.

!!! tip "Tip"
    Before running the scripts, check if the execution permissions are correct (use `chmod +x get.sh` in Linux/Mac).

---

## :octicons-play-16: 5. Starting the Lab

After downloading or customizing, follow the steps below to **start the lab**.
Run the command below inside the downloaded directory.

```bash
sudo containerlab deploy

```

This command will start the topology defined in the lab and create all the necessary containers.

!!! tip "Tip"
    If an error occurs, check the command output for possible error messages. Use `docker logs <container_name>` to debug.

---

## :material-access-point: 6. Access

After the lab is started, you will be able to access the devices and services configured on the network.

### :material-table: 6.1 Table of IPs and Service Ports

Here is an example of a table of devices, IPs and service ports available in the lab.

| Device | Access IP | Port | Service |
|---|---|---|---|
| **BA Router** | 172.10.10.6 | 22 | SSH |
| **ES Router** | 172.10.10.11 | 22 | SSH |
| **Zabbix Server** | 172.10.10.115 | 10051 | Zabbix Server |
| **Zabbix Frontend** | 172.10.10.116 | 880/443 | Web UI (Zabbix) |
| **Zabbix Agent** | 172.10.10.117 | 10050 | Zabbix Agent |
| **Zabbix Database** | 172.10.10.118 | 5432 | PostgreSQL |
| **Graphite** | 172.10.10.119 | 8080 | Web UI (Graphite) |


### :material-key-link: 6.2 Access Passwords

| Service | User | Password |
|---|---|---|
| **BA Router (SSH)** | `admin` | `admin@123` |
| **ES Router (SSH)** | `admin` | `admin@123` |
| **Zabbix (Web UI)** | `Admin` | `zabbix` |
| **Zabbix Database** | `zabbix` | `zabbixdatabase` |



!!! warning "Attention"
    Before accessing, access the log of a device to verify that it has been started and configured correctly.
---

## 7. :octicons-rocket-24: Next Steps

When starting the lab, Zabbix will be bare without templates, to configure automatic discovery and templates, access the [Configuring Auto Discovery](../../../../Ferramentas/Zabbix/Configurando%20Auto%20Discovery.md)

---