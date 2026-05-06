# ELK (Elasticsearch) Installation Guide

## :octicons-book-24: 1. Introduction

In this guide, we will cover the setup of the **ELK** stack (Elasticsearch, Logstash, and Kibana) for data monitoring and analysis in laboratory environments. ELK is a powerful combination of tools that allows the collection, storage, analysis, and visualization of data in real-time, being widely used for log management and system monitoring.

## :simple-elastic: 2. What is ELK?

![Flow_Fleet_Elasticsearch.png](../../../img/tools_imgs/flow_fleet_elasticsearch.png)
Source: <a target="_blank" href="https://www.elastic.co/guide/en/fleet/current/add-fleet-server-on-prem.html">Elastic Documentation</a>

The image above illustrates the data flow and integration of the ELK Stack components for centralized monitoring and real-time analysis.

- **Elasticsearch**: Responsible for storing and indexing data received from the Fleet Server. With real-time search and analysis capabilities, Elasticsearch is the core of the ELK Stack, enabling efficient queries on large volumes of data and facilitating detailed analysis.

- **Kibana**: Kibana offers a graphical interface where data in Elasticsearch can be visualized and analyzed. Kibana also manages the packages and integrations available for agents, which can be loaded from the Package Registry. With it, you can create dashboards, reports, and charts, transforming raw data into visual insights.

- **Elastic Agent**: Located on the devices to be monitored, Elastic Agents collect data from logs, metrics, and events and send them to the Fleet Server Cluster. These agents are configured and managed by policies that control what data is collected and where it is sent.

- **Fleet Server Cluster**: Using a load balancer for high availability, the Fleet Server Cluster centralizes the management of Elastic Agents. It distributes policies to the agents, ensuring consistent data collection, and then forwards them to Elasticsearch for storage and analysis.

This flow ensures that network data is collected in a unified manner, stored in an optimized way, and made available for visualization and analysis, offering a complete and robust solution for monitoring and analyzing complex and distributed networks.

!!! warning "Note"
    In this installation, we will not use **Logstash**, but rather the more modern collection version, which is **Fleet Server** and **Fleet Agent**.
    To learn more, access the official documentation about Fleet: <a href="https://www.elastic.co/guide/en/fleet/current/fleet-overview.html" target="_blank">Elastic Documentation - Fleet</a>

---

## :octicons-checklist-24: 4. Prerequisites

Before proceeding with the ELK configuration, it is necessary to configure the **br-lab** network. For details on this configuration, refer to the [**First Steps: Preparing the Environment**](../Primeiros passos - preparando o ambiente.md) guide.

---

## :octicons-tools-24: 5. Preparing the Environment

After ensuring that the **br-lab** network is configured, follow the steps below to prepare the work environment.

## :fontawesome-brands-docker: 6. Downloading Docker Compose

To download Docker Compose, run the following command:

=== "Linux/ Mac"

    ```bash
        curl -L -o get.sh "https://git.rnp.br/redes-abertas/docker-composes/-/raw/main/ELK-Stack/get.sh?inline=false" && sh get.sh && cd ELK-Stack
    ```

=== "Windows"
    ```bash
        curl -L -o get.bat "https://git.rnp.br/redes-abertas/docker-composes/-/raw/main/ELK-Stack/get.bat?inline=false" && call get.bat && cd ELK-Stack
    ```

This command downloads the installation script and then navigates to the **ELK-Stack** directory.

## :octicons-container-24: 7. Starting the Containers

After downloading Docker Compose, run the command below to start the ELK services:

```bash
docker compose up -d
```

This command will start three essential containers for the operation of the ELK stack:

1. **Elasticsearch**
    - **Description**: Search engine and data storage. It allows the storage of documents in JSON format and provides a RESTful API for search and analysis. Ideal for searching in large volumes of data.
    - **IP**: `172.10.10.201`
    - **Default Port**: `9200`
    - **Documentation**: <a href="https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html" target="_blanck">Elasticsearch Documentation</a>
2. **Kibana**
    - **Description**: Graphical interface for visualizing data stored in Elasticsearch. Kibana allows users to create interactive dashboards and real-time data visualizations, facilitating data analysis and interpretation.
    - **IP**: `172.10.10.202`
    - **Default Port**: `5601`
    - **Documentation**: <a href="https://www.elastic.co/guide/en/kibana/current/index.html" target="_blanck">Kibana Documentation</a>
3. **Fleet Server**
    - **Description**: Agent responsible for collecting metrics and logs from different sources and sending them to Elasticsearch. Fleet Server facilitates the centralized management of collection agents, such as the Elastic Agent, allowing efficient data collection and sending.
    - **IP**: `172.10.10.203`
    - **Documentation**: <a href="https://www.elastic.co/guide/en/fleet/current/index.html" target="_blanck">Fleet Server Documentation</a>
!!! info "Access"
    :material-access-point: Default username and password
    - **Default username**: `elastic`
    - **Default password**: `admin@123`

!!! tip "Configuration"
    To change the password or Elasticsearch version, edit the **.env** file.

## :simple-kibana: 8. Accessing the Kibana Interface

To access the Kibana interface, use the following link:

```
https://<your-ip>:5601
```

Log in with the default username and password.

## :material-skip-next-outline: Next Steps

- **Configure IPFIX Collection**: After configuring ELK, the next step will be to configure data collection using IPFIX, with our [IPFIX configuration](Configurando IPFIX no ELK.md) guide.