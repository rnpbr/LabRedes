# :material-bookmark: Juniper vJunos ELK Monitoring

This lab simulates, via Containerlab, the interconnection between three routers representing the GO-MS-MT connection in the RNP backbone, with dynamic routing via OSPF, flow export via IPFIX, and analysis/visualization via Elastic Stack (Elasticsearch, Kibana, Fleet Server, and Elastic Agent).

---

## :material-bookmark: 1. Description

### :octicons-goal-16: 1.1 Lab Objective

The main objective of the `elk-lab` is to simulate the sending and analysis of IPFIX traffic flows in a topology of three interconnected routers (GO, MS, and MT), using OSPF for dynamic routing and Elastic Stack tools for real-time observability and traffic analysis.

### :material-lan: 1.2 Lab Topology

![Lab Topology](../../../../../img/labs_imgs/Topologia_ELK.svg)

**Topology Description**

* Three routers (GO, MS, MT) interconnected in a linear topology with point-to-point /31 links.
* Dynamic routing via OSPF.
* IPFIX flow export to the **Fleet Server**.
* Elastic Agent installed to receive flows and send them to Elasticsearch.
* Data visualization and analysis via Kibana.
* `br-lab` external network connects the network elements to the ELK stack.

---

## :octicons-search-16: 2. Applications

### Application Examples

The `elk-lab` can be applied to different educational and research contexts, allowing the simulation of real-world traffic export and analysis scenarios with Elastic Stack.

#### Possible Applications:

* **Teaching IPFIX in real environments**: Practical application of flow export to analysis tools.
* **Elastic Stack training for networks**: Demonstrates IPFIX integration with Elastic Agent and the use of dashboards in Kibana.
* **Network traffic and forensic analysis**: Support for studies on traffic patterns, anomalies, and threats.
* **Integration with Elasticsearch-based SIEMs**: Evaluation of data pipelines for use with network security.
* **Traffic flow visualization**: Composition of dynamic real-time dashboards.

---

## :material-tools: 3. Requirements

Below are the minimum hardware and software requirements to run the lab. Make sure to include the essential tools like **Containerlab** and **Docker**, as well as the previously created `br-lab` network.
To learn more about these items, access:

- [Creating the br-lab Network](../../../../Ferramentas/Primeiros passos - preparando o ambiente.md)
-  <a target="_blank" href="https://www.docker.com/get-started/">Docker Installation</a>
-  <a target="_blank" href="https://containerlab.dev/install/">Containerlab Installation</a>

And have the ELK stack previously installed. To learn more about installing Zabbix, access: [ELK Installation](../../../../Ferramentas/Elasticsearch/index.md)

### :material-alert: Minimum Requirements Table:

| Requirement           | Details              |
| ------------------- |-----------------------|
| **CPUs**            | 6 vCPUs               |
| **RAM Memory**     | 16 GB                 |
| **Disk Space** | 15 GB (recommended)   |
| **Containerlab**    | 0.45.0 or higher    |
| **Docker Engine**   | 23.0.3 or higher    |
| **Images**         | `vr-vjunos:23.2R1.14` |
| **Docker Network**     | `br-lab`              |

!!! warning "Attention"
    Check if your processor has **hardware virtualization support** and if this feature is **enabled in the BIOS/UEFI**.
    - In **Intel** processors, this technology is called **VT-x** (Intel Virtualization Technology).
    - In **AMD** processors, it is known as **AMD-V** (AMD Virtualization).

    Without this feature enabled, images like **vJunos-router** will not work correctly.
---

## :fontawesome-solid-prescription-bottle: 4. Lab Deployment

This method allows the user to **download a pre-assembled version** of the lab, with the topology and settings already defined. Simply download the repository and proceed to start the execution.

!!! tip "Tip"
    Ready-made deployment is useful for those who want to get started quickly with a configured environment.

#### :octicons-download-16: Downloading the Lab

Execute the script below to download the lab files:

=== "Linux/Mac"

    ```bash
    curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/elk-lab/get.sh?ref_type=heads&inline=false" && sh get.sh && cd elk-lab
    ```


=== "Windows"

    ```bash
    curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/elk-lab/get.bat?ref_type=heads&inline=false" && call get.bat && cd elk-lab
    ```

---

##  :octicons-play-16: 5. Starting the Lab

After downloading or customizing, follow the steps below to **start the lab**.
Run the command below inside the downloaded directory.

```bash
sudo containerlab deploy

```

This command will start the topology defined in the lab and create all the necessary containers.

!!! tip "Debugging"
    Use `docker logs -f <container_name>` to check the status of services if something is not working.


## :material-access-point: 6. Accessing the Devices

### :material-table: 6.1 IPs and Ports

| Device       | Access IP  | Port(s) | Service           |
| ----------------- |---------------| -------- | ----------------- |
| **Router GO**   | 172.10.10.6   | 22       | SSH               |
| **Router MS**   | 172.10.10.7   | 22       | SSH               |
| **Router MT**   | 172.10.10.8   | 22       | SSH               |
| **Fleet Server**  | 172.10.10.110 | 8220     | Data Ingestion |
| **Elasticsearch** | 172.10.10.108 | 9200     | Database    |
| **Kibana**        | 172.10.10.109 | 5601     | Web Interface     |

### :material-key-link: 6.2 Access Credentials

| Service        | User                                            | Password         |
| -------------- | -------------------------------------------------- |---------------|
| SSH Routers | `admin`                                            | `admin@123`   |
| Kibana         | `elastic`                                          | `admin@123`   |

---

## :fontawesome-solid-retweet: 7. Flow Collection and Export
To configure data collection using IPFIX, use our [IPFIX configuration guide](../../../../Ferramentas/Elasticsearch/Configurando%20IPFIX%20no%20ELK.md).
without changing the documentation structure, adding anything, or altering links or references.