# **Home**

**Welcome to the Open Networks project!**

This project aims to provide a solid foundation for configuring and simulating networks using modern and efficient tools: **NetBox**, **Netreplica**, and **Containerlab**.

The **Open Networks** project was developed for networking professionals and enthusiasts who want to:

- **Explore**: Test different network configurations in a controlled environment.
- **Automate**: Use templates to standardize and automate network device configurations.
- **Replicate**: Reproduce real network environments in virtual labs for testing and validation.
- **Manage**: Centralize documentation and management of network infrastructures efficiently.

With these tools, the project aims to simplify the creation, management, and documentation of complex network topologies, providing flexibility and scalability.

---

## Containerlab Capabilities

**Containerlab** is a powerful tool for creating and managing virtualized network labs using Docker containers. With it, you can test and simulate complex network topologies in a controlled environment. The tool supports various network devices, allowing the configuration of **multivendor** networks, which is ideal for testing interactions between different vendors in the same lab.
Below is a list of the main vendors supported by Containerlab:
![Vendors](../img/vendors.svg)

---

## Lab Workflow

The flowchart illustrates the **Netreplica** workflow in the context of a network simulation environment, integrated with **Containerlab**:

![Workflow Netreplica](../img/tools_imgs/workflow-netreplica.gif)

---

## Workflow Structure

### 1. **Topology**

The network topology defines the structure and interconnection of network devices.

### 2. **NetBox**

The topology is documented and managed in **NetBox**, a centralized platform for network infrastructure management. NetBox stores detailed information about devices, IP addresses, and physical connections.

### 3. **Netreplica**

**Netreplica** synchronizes configuration information from NetBox and prepares the data for simulation. It retrieves data via API and generates YAML configuration files needed for simulation.

### 4. **Configurations**

**Netreplica** generates detailed YAML configuration files that describe how network devices should be configured.

### 5. **Containerlab**

**Containerlab** uses the generated configuration files to create and manage complex network topologies in Docker containers.

### 6. **Lab (Docker Stack)**

The simulation is executed in a lab environment using a Docker stack. The defined topology is reproduced, allowing tests and validations.

### 7. **Graphite**

To monitor and visualize simulation metrics and performance, **Graphite** is integrated into the lab. It collects and displays relevant data for analysis.

---

## Workflow Summary

1. **Topology Definition**: The structure and interconnection of network devices are defined.
2. **Documentation in NetBox**: The topology is documented and managed in **NetBox**.
3. **Synchronization with Netreplica**: **Netreplica** synchronizes information from **NetBox** via API and generates YAML configurations.
4. **Topology Creation with Containerlab**: **Containerlab** uses YAML configurations to create the network topology in Docker containers.
5. **Simulation Execution**: The topology is executed in a Docker lab environment.
6. **Monitoring with Graphite**: The simulation's performance and metrics are monitored and visualized with **Graphite**.

---

## Project Status

Project in progress.

---

## Getting Started
To get started, read the [Configuration Guide](./Getting%20Started.md) to learn how to use NetBox, Containerlab, and Netreplica tools together.

---

## Available Labs

- [OSPF Routing](Laboratórios/Juniper/vMX/Roteamento-OSPF/index.md) - OSPF Configuration Lab based on Juniper's MX platform in a ring topology.
- [Discovery](Laboratórios/Juniper/vJunos/Descoberta/index.md) - Network device discovery lab using OSPF and SNMP, integrating Zabbix and NetBox.
- [ELK Monitoring](Laboratórios/Juniper/vJunos/Monitoramento-ELK/index.md) - IPFIX flow monitoring lab using the Elastic Stack (Elasticsearch, Kibana, Fleet Server, and Elastic Agent).
- [Telegraf Monitoring](Laboratórios/Juniper/vJunos/Monitoramento-Telegraf/index.md) - Traffic flow monitoring lab via Telegraf/IPFIX to InfluxDB.
- [Zabbix Monitoring](Laboratórios/Juniper/vJunos/Monitoramento-Zabbix/index.md) - Router monitoring lab via SNMP with centralized collection by Zabbix Server.
- [NETCONF Configuration](Laboratórios/Multvendor/Configuração-NETCONF/index.md) - Device configuration lab via NETCONF.
---

## Tools

- [NetBox](Getting Started.md): Tool for network infrastructure management
- [Containerlab](Getting Started.md): Tool for simulating complex network topologies
- [Netreplica](Getting Started.md): Tool for replicating network environments from NetBox to Containerlab
- [ELK](Ferramentas/Elasticsearch/index.md): Stack for monitoring logs and data streams in real-time
- [Edgeshark](Ferramentas/Edgeshark/index.md): Tool for capturing and visualizing network traffic
- [LibreNMS](Ferramentas/LibreNMS/index.md): Tool for monitoring network devices

---

## Contribute

Contribute to the project by clicking [here](Contribua.md).