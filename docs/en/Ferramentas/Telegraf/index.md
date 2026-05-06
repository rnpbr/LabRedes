# Telegraf Installation Guide

## :octicons-book-24: 1. Introduction

This guide presents the installation of **Telegraf**, a metrics collection tool that will be used in the **br-lab** laboratory. Telegraf provides support for various protocols and plugins for collecting metrics, allowing its integration with different systems and devices. The installation uses Docker Compose to automatically provision the necessary services, ensuring a practical and efficient implementation in the laboratory environment.

---

## :material-network: 2. What is Telegraf?

Telegraf is a highly configurable metrics collection agent developed by **InfluxData**. It is compatible with a wide variety of protocols and plugins, which makes it possible to capture and process metrics from systems, devices, applications, and services in real-time.

### Main Components:

1. **Telegraf**: Configurable data collection agent.
2. **InfluxDB**: Time series database where Telegraf data will be stored.
3. **Grafana**: Tool for visualization and analysis of collected data.
4. **Chronograf**: Additional graphical interface for querying and analyzing data in InfluxDB.

This architecture integrates metric capture, storage, and visualization, ensuring flexibility and efficiency in monitoring the environment.

---

## :octicons-checklist-24: 3. Prerequisites

Make sure you meet the following prerequisites before installation:

1. **br-lab network configured**:
    - The **br-lab** network is required to isolate services in the environment. For more details on this configuration, see the [**First Steps: Preparing the Environment**](../Primeiros passos - preparando o ambiente.md) guide.

2. **Required Packages**:
    - `docker`, `docker-compose`, `curl`.


## :fontawesome-brands-docker: 4. Preparing the Environment

### 4.1. Downloading the Installation Script

Execute the command below to download and configure the necessary services:
=== "Linux/ Mac"

    ```bash
        curl -L -o get.sh "https://git.rnp.br/redes-abertas/docker-composes/-/raw/main/Telegraf/get.sh?inline=false" && sh get.sh && cd Telegraf
    ```

=== "Windows"
    ```bash
        curl -L -o get.bat "https://git.rnp.br/redes-abertas/docker-composes/-/raw/main/Telegraf/get.bat?inline=false" && call get.bat && cd Telegraf
    ```

This command will:

- Download the Docker Compose file containing the service configuration.
- Create the **Telegraf** directory, where the necessary files will be stored.

---

## :octicons-container-24: 5. Starting the Containers

To start the Telegraf services and its components, execute:

```bash
docker compose up -d
```

This will start the following containers:

1. **Telegraf**: Data collection agent with support for various protocols and formats.
    - **IP**: `172.10.10.114`
    - **Mapped volumes**:
        - Telegraf configuration.
        - Host system directories (*proc*, *sys*, *etc*).
    - **Documentation**: <a href="https://docs.influxdata.com/telegraf/v1/get-started/" target="_blanck">Telegraf Documentation</a>

2. **InfluxDB**: Database to store metrics collected by Telegraf.
    - **IP**: `172.10.10.112`
    - **Access credentials**:
        - **Username**: `admin`
        - **Password**: `admin`
    - **Default database**: `telemetry`
    - **Documentation**: <a href="https://docs.influxdata.com/influxdb/v1/" target="_blanck">InfluxDB Documentation</a>

3. **Grafana**: Graphical interface for visualizing metrics stored in InfluxDB.
    - **IP**: `172.10.10.111`
    - **Default Port**: `3000`
    - **Credentials**:
        - **Username**: `admin`
        - **Password**: `admin`
    - **Documentation**: <a href="https://grafana.com/docs/grafana/latest/fundamentals/" target="_blanck">Grafana Documentation</a>

4. **Chronograf**: Additional tool for visual queries and analysis in InfluxDB.
    - **IP**: `172.10.10.113`
    - **Default Port**: `8888`
    - **Documentation**: <a href="https://docs.influxdata.com/chronograf/v1/" target="_blanck">Chronograf Documentation</a>

To check the execution status of the containers:

```bash
docker compose ps
```

---

## :fontawesome-solid-chart-line: 6. Accessing the Components

### 6.1. Grafana Access

After initializing the services, Grafana will be accessible at:

```
http://<SERVER_IP>:3000
```

Log in using the default credentials below:

- **Username**: `admin`
- **Password**: `admin`

### 6.2. Chronograf Access

Chronograf can be accessed at:

```
http://<SERVER_IP>:8888
```

Use the credentials configured in InfluxDB to access and configure queries.

## :octicons-rocket-24: 8. Next Steps

- **Create custom Dashboards in Grafana**: Explore the metrics to create specific visualizations for your needs.
- **Add Data Sources to Telegraf**: Expand the usage by configuring Telegraf to collect metrics from other sources of interest in the laboratory.

For more information about Telegraf, see the <a target="_blank" href="https://github.com/influxdata/telegraf">official Telegraf documentation</a>.