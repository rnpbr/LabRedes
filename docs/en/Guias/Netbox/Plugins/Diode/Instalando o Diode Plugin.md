# :material-power-plug-outline: Installing the Diode Plugin

The Diode Plugin is an essential component to enable automated data ingestion into NetBox. It provides direct integration with the NetBox ORM and manages API keys, allowing the Diode server to send structured data securely and validated. With this plugin, NetBox receives real-time inventory updates, facilitating the discovery, documentation, and continuous synchronization of the network infrastructure.

## :simple-git: **Plugin Repository**
Copy the link below or click to access the <a target="_blank" href="https://github.com/netboxlabs/diode-netbox-plugin">Github Repository</a>

```
https://github.com/netboxlabs/diode-netbox-plugin
```

---

## :material-scale-balance: **1. Installation Requirements**
This documentation used the following components with their respective versions:

| Components           | Versions |
| --------------------- | ------- |
| **Netbox**            | v4.1.11 |
| **Diode Plugin**      | v0.6.0  |

---

## :material-file-document-arrow-right: **2. Installing and Configuring the Plugin in Netbox**
To install the plugin in Netbox, we need to change and add some files
that are responsible for the Netbox configuration.

The files are:

- `plugin_requirements.txt`.
- `DockerFile-Plugins`.
- `docker-compose.override.yml`.
- `configuration/plugins.py`.

### :fontawesome-solid-gear: **2.1. Configuring the Netbox version:**

1. First, let's clone the Netbox repository:
```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
```

2. Access the cloned directory:
```bash
cd netbox-docker
```

3. Now, switch to release 3.0.0
```bash
git checkout 3.0.0
```
!!! tip "Information"
    We changed the repository branch to have access to Netbox version 4.1.11.

!!! tip "Tip"
    All commands below will be executed within the root directory of netbox `netbox-docker/`.


### :material-text-box: **2.2. plugin_requirements.txt**
This file contains a list of Netbox plugins (as PyPI Python packages) to be installed during the Docker image build.

Execute the following command to write the package inside the `plugin_requirements.txt` file.

```bash
echo "netboxlabs-diode-netbox-plugin" > plugin_requirements.txt
```

### :material-docker: **2.3. DockerFile-Plugins**
This is the DockerFile used to build the customized docker image.

1. Create the file and access it with an editor:
```bash
nano DockerFile-Plugins
```

2. Copy the content below and paste it into the file:
```bash
FROM netboxcommunity/netbox:v4.1

COPY ./plugin_requirements.txt /opt/netbox/
RUN pip install -r /opt/netbox/plugin_requirements.txt
```

### :material-docker: **2.4. docker-compose.override.yml**
As the name implies, this file contains the settings that will override `docker-compose.yml`.

If you have not yet configured the `br-lab` network, access: [Configuring the Docker Network](../../../../Laboratórios/Juniper/vJunos/Descoberta/index.md/#41-configuring-the-docker-network)

1. Create the file and access it with an editor:
```bash
nano docker-compose.override.yml
```

2. Copy the content below and paste it into the file:
```bash
services:
  netbox:
    image: netbox:latest-plugins
    pull_policy: never
    ports:
      - 8000:8080
    build:
      context: .
      dockerfile: Dockerfile-Plugins
    networks:
      br-lab:
        ipv4_address: 172.10.10.5

  netbox-worker:
    image: netbox:latest-plugins
    pull_policy: never
    networks:
      - br-lab

  netbox-housekeeping:
    image: netbox:latest-plugins
    pull_policy: never
    networks:
      - br-lab

  postgres:
    networks:
      - br-lab

  redis:
    networks:
      - br-lab

  redis-cache:
    networks:
      - br-lab

networks:
  br-lab:
    external: true
```

The changes made were:

- adding Netbox to the `br-lab` network.
- changing the dockerfile to `Dockerfile-Plugins`, created previously.
- Also changed the image of the services to: `netbox:latest-plugins`.

### :material-power-plug-outline: **2.5. plugins.py**
This file is responsible for setting the specific configurations for each plugin.

1. Access the file with the editor:
```bash
nano configuration/plugins.py
```

2. Copy and paste the content into the file:
```bash
PLUGINS = [
    "netbox_diode_plugin",
]

PLUGINS_CONFIG = {
    "netbox_diode_plugin": {
        # Auto-provision users for Diode plugin
        "auto_provision_users": True,

        # Diode gRPC target for communication with Diode server
        "diode_target_override": "grpc://172.10.10.120:80/diode",

        # User allowed for Diode to NetBox communication
        "diode_to_netbox_username": "diode-to-netbox",

        # User allowed for NetBox to Diode communication
        "netbox_to_diode_username": "netbox-to-diode",

        # User allowed for data ingestion
        "diode_username": "diode-ingestion",
    },
}
```

!!! tip "Tip"
    We suggest leaving the `auto_provision_users` configuration as `True` to automate the creation of user, groups, and API keys that are responsible for integration with the Diode Server.

---

## :simple-docker: **3. Build and Deploy!**
Now your Netbox is configured and ready for deployment, follow the commands below and build the new Netbox instance!

1. Build the image:
```bash
docker compose build --no-cache
```

2. Start the containers:
```bash
docker compose up -d
```

---

## :octicons-rocket-24: **4. Next Steps**
With the Diode plugin installed, your NetBox environment is now ready to receive data from the Diode server, allowing automated ingestion of network information.

The next step is to configure the Diode Server, which is responsible for processing and forwarding this data to NetBox.

Next: [Installing the Diode Server](./Instalando%20o%20Diode%20Server.md)