# Containerlab

**Containerlab** is a powerful tool for creating and managing virtualized network labs. With it, you can simulate complex network topologies using Docker containers. Below, you will find information about the prerequisites, recommended tools, and how to document your labs.

---

## Prerequisites

Before you start using Containerlab, make sure you have the following prerequisites installed:

### Docker

- Docker is used by Containerlab to create and run the containers that make up the virtualized network.
- **Link**: <a target="_blank" href="https://www.docker.com/get-started/">Official Docker Documentation</a>.

### Containerlab

- Install Containerlab according to the instructions provided in the official documentation.
- **Link**: <a target="_blank" href="https://containerlab.dev/install/">Official Containerlab Documentation</a>.

---

## Available Labs

Here is an example of a configured lab to simulate OSPF using Junos:

### OSPF Routing (Junos)

- OSPF simulation with Junos, one of the most used routing technologies.
- **Link**: [OSPF Routing (Junos) Lab](Juniper/vMX/Roteamento-OSPF/index.md).

### Discovery (Junos)

- Router import with scripts, using Zabbix and Netbox.
- **Link**: [Discovery (Junos) Lab](Juniper/vJunos/Descoberta/index.md).

### ELK Monitoring (Junos)
- Export IPFIX flows to Elasticsearch with Elastic Agent.
- Real-time flow visualization with dashboards in Kibana.
- **Link**: [ELK Monitoring (Junos)](Juniper/vJunos/Monitoramento-ELK/index.md).

### Telegraf Monitoring (Junos)
- Export traffic flows via Telegraf/IPFIX to InfluxDB.
- Ready-made dashboards in Grafana for traffic analysis by interface and protocol.
- **Link**: [Telegraf Monitoring (Junos)](Juniper/vJunos/Monitoramento-Telegraf/index.md).

### Zabbix Monitoring (Junos)
- Monitoring routers via SNMP with centralized collection by the Zabbix Server.
- Allows real-time visualization of metrics and alerts in the Zabbix frontend.
- **Link**: [Zabbix Monitoring (Junos)](Juniper/vJunos/Monitoramento-Zabbix/index.md).
---

## Recommended Analysis Tools

In addition to Containerlab, you can use the following analysis tools to monitor and debug your virtualized network:

### LibreNMS

- A web-based network monitoring platform that provides insights into network performance and health. Ideal for continuous real-time network monitoring.

### Wireshark

- Packet capture and analysis tool that allows you to examine network traffic in detail. Essential for debugging and analyzing network protocols.

In addition to these tools mentioned there are others that can be configured according to your needs, to learn more go to: [Analysis Tools](../Ferramentas/index.md).

---

## Documenting Your Labs

To ensure your labs are well documented and easy to understand, see the section on **Lab Documentation**. There, you will find best practices and examples for creating clear and useful documentation for your simulated environments.

- **Link**: [Lab Documentation](Contribua/index.md).