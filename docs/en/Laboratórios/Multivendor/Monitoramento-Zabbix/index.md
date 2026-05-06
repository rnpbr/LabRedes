# :material-bookmark: Multivendor Zabbix Monitoring

This lab, using Containerlab, simulates the interconnection of three routers from different manufacturers: vJunos (Juniper), Huawei VRP, and Cisco XRD.

---

## :material-bookmark: 1. Description

### :octicons-goal-16: 1.1 Lab Objective

The "Multivendor Zabbix Monitoring" lab demonstrates the simulation of the interconnection of three routers from different manufacturers — vJunos (Juniper), Huawei VRP, and Cisco XRD — using Containerlab. The devices are interconnected in a ring topology, and routing is performed by the OSPF protocol, enabling dynamic route exchange. Communication with Zabbix occurs via SNMP, enabling real-time monitoring.

### :material-lan: 1.2 Lab Topology

![Lab Topology](../../../../img/labs_imgs/Topologia_Multvendor_Zabbix.svg)

The topology of this lab consists of three routers interconnected in a ring topology, allowing direct communication between the devices. Each router is configured with OSPF, ensuring dynamic routing between interfaces. Monitoring is performed from an external network called br-lab, to which the routers are connected by virtual interfaces. This configuration allows Zabbix to monitor network connectivity and performance in real-time, using SNMP as the metric collection protocol.

## :octicons-search-16: 2. Applications

### **Application Example**

This lab can be used in various academic and professional contexts. It is useful for simulating real-world network operation and monitoring scenarios, serving as an environment for validating configurations and testing interoperability between routing protocols and monitoring tools.

**Possible Applications:**

* **Training NOC (Network Operations Center) teams**:
    Replicates real-world connectivity situations between Juniper, Huawei, and Cisco routers in a ring topology, using OSPF and SNMP, allowing technicians to learn how to detect, analyze, and resolve faults.
* **Evaluation of interoperability between vendors**:
Allows testing how different manufacturers interact via OSPF, analyzing route convergence, and identifying inconsistencies in the dynamic exchange of routing information.
* **Validation of SNMP templates in Zabbix**:
Controlled environment to validate, adjust, or develop SNMP monitoring templates for multiple router manufacturers, ensuring compatibility and accuracy in metric collection.
* **Teaching dynamic routing protocols**:
Provides practical learning on configuration, maintenance, and route exchange via OSPF in point-to-point and ring topologies, including fault analysis and reconvergence.
  * **Monitoring and automatic discovery tests**:
Allows evaluating the automatic device discovery functionality via SNMP and the real-time monitoring of connectivity and performance, simulating various network scenarios.
  * **Simulation of network policies and ACLs**:
Enables the application of traffic filtering rules and verifying their impact on communication and monitoring, with analysis of logs and SNMP traps in Zabbix.
---

## :material-tools: 3. Requirements

Below are the minimum hardware and software requirements needed to run the lab. Be sure to include the essential tools, such as **Containerlab** and **Docker**, in addition to the previously created `br-lab` network.
To learn more about these items, access:

- [Creating the br-lab Network](../../../../Ferramentas/Primeiros passos - preparando o ambiente.md)
-  <a target="_blank" href="https://www.docker.com/get-started/">Docker Installation</a>
-  <a target="_blank" href="https://containerlab.dev/install/">Containerlab Installation</a>
-
And have Zabbix previously installed. To learn more about installing Zabbix, access: [Zabbix Installation](../../../../Ferramentas/Zabbix/index.md)

### :material-alert: Minimum Requirements Table:

| Requirement           | Details                |
| ------------------- |-------------------------|
| **CPUs**            | 4 vCPUs                 |
| **RAM Memory**     | 8 GB                    |
| **Disk Space** | 10 GB (recommended)     |
| **Containerlab**    | 0.45.0                  |
| **Docker Engine**   | 23.0.3                  |
| **Images**         | `vr-vjunos:23.2R1.14`, `vrnetlab/huawei_vrp:ne40e-8.180`, `xrd-control-plane:7.10.2` |
| **Created Network**     | `br-lab`                |


!!! warning "Attention"
    Check if your processor has **hardware virtualization support** and if this feature is **enabled in the BIOS/UEFI**.
    - In **Intel** processors, this technology is called **VT-x** (Intel Virtualization Technology).
    - In **AMD** processors, it is known as **AMD-V** (AMD Virtualization).

    Without this feature enabled, images such as **vJunos-router** will not work correctly.

---

## :fontawesome-solid-prescription-bottle: 4. Deploying the Lab

Here are the instructions to **deploy the lab**. You can choose between a **ready deployment** or a **customized** one.

### :material-git: 4.1 Ready Deployment

This method allows the user to **download a pre-assembled version** of the lab, with the topology and configurations already defined. Simply download the repository and proceed to the start of execution.

!!! tip "Tip"
    The ready deployment is useful for those who want to quickly start with a configured environment.

#### :octicons-download-16: Downloading the Lab

To download the lab, execute the command corresponding to your operating system.

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/monitoramento-zabbix-multvendor/get.sh" && sh get.sh && cd monitoramento-zabbix-multvendor
    ```


=== "Windows"

    ```bash
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/monitoramento-zabbix-multvendor/get.bat" && call get.bat && cd monitoramento-zabbix-multvendor
    ```

This command will download the installation script and direct you to the lab directory.

!!! tip "Tip"
    Before running the scripts, check if the execution permissions are correct (use `chmod +x get.sh` on Linux/Mac).

---

## :octicons-play-16: 5. Starting the Lab

After downloading or customizing, follow the steps below to **start the lab**.
Run the command below inside the downloaded directory.

```bash
sudo containerlab deploy

```

This command will start the topology defined in the lab and create all the necessary containers.

!!! tip "Tip"
    If any errors occur, check the command output for possible error messages. Use `docker logs <container_name>` to debug.

---

## :material-access-point: 6. Access

After the lab is started, you can access the devices and services configured in the network.

### :material-table: 6.1 Table of IPs and Service Ports

Here is an example table of devices, IPs, and service ports available in the lab.

| Device         | Access IP  | Port   | Service           |
|---------------------|---------------|---------| ----------------- |
| **node1**           | 172.10.10.201 | 22      | SSH               |
| **node2**           | 172.10.10.202 | 22      | SSH               |
| **node3**           | 172.10.10.203 | 22      | SSH               |
| **Zabbix Server**   | 172.10.10.115 | 10051   | Zabbix Server     |
| **Zabbix Frontend** | 172.10.10.116 | 880/443 | Web UI (Zabbix)   |
| **Zabbix Agent**    | 172.10.10.117 | 10050   | Zabbix Agent      |
| **Zabbix Database** | 172.10.10.118 | 5432    | PostgreSQL        |
| **Graphite**        | 172.10.10.119 | 8080    | Web UI (Graphite) |


### :material-key-link: 6.2 Access Passwords

| Service             | User  | Password            |
|---------------------|----------|------------------|
| **node1 (SSH)**     | `admin`  | `admin@123`      |
| **node2 (SSH)**     | `clab`   | `clab@123`       |
| **node3 (SSH)**     | `admin`  | `admin`          |
| **Zabbix (Web UI)** | `Admin`  | `zabbix`         |
| **Zabbix Database** | `zabbix` | `zabbixdatabase` |



!!! warning "Attention"
    Before accessing, access the log of a device to verify that it has been started and configured correctly.
---

## 7. :octicons-rocket-24: Next Steps

When starting the lab, Zabbix will be raw without templates. To configure automatic discovery and templates, access [Configuring Auto Discovery](../../../../Ferramentas/Zabbix/Configurando%20Auto%20Discovery.md)

!!! warning "Attention"
    Currently, automatic discovery is only adding the correct template for Juniper. For other manufacturers, you will need to add the template manually.
---
 without changing the structure of the documentation, adding anything, or changing the links or references.