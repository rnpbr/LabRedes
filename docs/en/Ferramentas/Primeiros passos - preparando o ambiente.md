# Getting Started: Preparing the Environment

## :octicons-book-24: **1. Introduction**

In this guide, we will cover the initial steps to prepare the monitoring environment using the Docker br-lab network.
This network was created to facilitate access, monitoring, and use of analysis tools in laboratories managed by Containerlab.
Configuring the br-lab network is a necessary step for using most of the tools that will be shown in this guide.
After configuring the monitoring tools on the br-lab network, they can be used in any laboratory,
eliminating the need for reconfiguration with each new environment. This simplifies testing multiple configurations
and allows the use of various analysis tools more efficiently.

### :material-checkbox-marked-outline: **Advantages:**

- **Single configuration**: Monitoring tools only need to be configured once, regardless of the laboratory in use.
- **Ease of testing**: Enables the creation and testing of various laboratory configurations without the need for continuous adjustments to the tools.
- **Flexible integration**: Allows you to easily add new laboratories and devices to the network without impacting the already configured infrastructure.

---

### :octicons-graph-24: **Examples of Laboratories Using the br-lab Network**

---

### :fontawesome-solid-diagram-project: **Monitoring Network Diagram**

Below is a visual example that shows how the `br-lab` monitoring network is configured, connecting different laboratories and devices for a unified and efficient testing environment.
![br-lab_diagram.svg](../../img/tools_imgs/br-lab_diagram.svg)
---

## :material-tools:  **2. Creating the Docker Network**

### :octicons-terminal-24: **Command to Create the Network:**

```bash
docker network create \
  --driver=bridge \
  --opt com.docker.network.bridge.name=br-lab \
  --subnet=172.10.10.0/24 \
  br-lab

```

### :gear: **Parameter Explanation:**

- `docker network create`: Starts the creation of a new Docker network.
- `-driver=bridge`: Specifies the network driver (bridge).
- `-opt com.docker.network.bridge.name=br-lab`: Defines the name of the bridge network interface on the host.
- `-subnet=172.10.10.0/24`: Defines the subnet (up to 254 IPs available).
- `br-lab`: Network name.

## :octicons-diff-added-24: **3. Adding Containers to the Network**

### :material-docker: **Using Docker Run:**

Command to add a container to the network:

```bash
docker run -d \
  --name meu_container \
  --network br-lab \
  imagem_do_container

```

### :gear: **Parameter Explanation:**

- `docker run -d`: Runs the container in the background.
- `-name meu_container`: Container name.
- `-network br-lab`: Connects the container to the `br-lab` network.
- `imagem_do_container`: Specifies the container image to be used.

### :material-docker: **Using Docker Compose:**

If the network has already been created, use Docker Compose to configure containers with static IPs.

```yaml
version: '3.8'

networks:
  br-lab:
    external: true

services:
  meu_container:
    image: imagem_do_container
    networks:
      br-lab:
        ipv4_address: 172.10.10.101 # optional for static ip

```

!!! warning "Attention"
    When using static ips, be sure to use ips after `172.10.10.100` in order to avoid conflicts with existing containers.

### :gear: **Configuration Explanation:**

- `networks`: Defines the networks that the services will use.
- `br-lab`: Indicates that the network has already been created externally (external: true).
- `services`: Defines the containers to be executed.
- `ipv4_address`: Assigns a static IP to the container (recommended to use addresses after `172.10.10.100`).

## :material-help-network: **4. Network Operation**

The `br-lab` network uses the `bridge` driver, which allows internal communication between containers, keeping them isolated from the host system. This offers:

- **Isolation**: Containers do not interfere with other host processes.
- **Internal communication**: Containers can communicate using IPs in the specified subnet.

## :material-connection: **5. Connecting Routers with Virtual Cables**

To connect routers in the `br-lab` network using virtual cables via Containerlab, you can configure the connections between interfaces.

### :gear: **Connection Example:**

```yaml
br-lab:
  kind: bridge

links:
  - endpoints: ["route1:eth1", "br-lab:eth1"]
  - endpoints: ["route2:eth1", "br-lab:eth2"]
  - endpoints: ["route3:eth1", "br-lab:eth3"]
  - endpoints: ["route4:eth1", "br-lab:eth4"]

```

### :material-lan-connect: **Connection Explanation:**

- Each line defines a “virtual cable” connecting two network interfaces (for example, `route1:eth1` is connected to `br-lab:eth1`).
- This allows communication between devices (routers and monitoring tools) through these interfaces.

## :material-file-document-check: **6. Conclusion**

With this guide, you have learned how to create and use the Docker `br-lab` network, how to add containers to the network, and how to connect routers virtually. This configuration is ideal for efficient monitoring in laboratory environments.