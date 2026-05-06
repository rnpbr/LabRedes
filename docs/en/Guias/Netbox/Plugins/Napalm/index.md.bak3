# :material-power-plug-outline: Napalm Plugin

The Napalm plugin for NetBox allows you to integrate real-time data collection functionalities directly from network devices configured in the system. With it, you can obtain up-to-date information such as operational status, neighbors (LLDP/CDP), and equipment configurations, enriching the visualization and management of assets in NetBox. This integration makes the tool more dynamic, bringing the documentation closer to the current reality of the network.

## :simple-git: Plugin Repository
Copy the link below or click to access the [Github Repository](https://github.com/netbox-community/netbox-napalm-plugin)

```
https://github.com/netbox-community/netbox-napalm-plugin
```

---

## :material-scale-balance: 1. Installation Requirements
This documentation used the following components with their respective versions:

| Components           | Versions |
| --------------------- | ------- |
| **Netbox**            | v4.1.11 |
| **Napalm Plugin**     | v0.3.1  |

The following functionalities were tested in the documentation:

| Functionalities         | Working |
| ----------------------- | ----------- |
| **Status Page**         | ✅ |
| **LLDP Neighbors Page** | ✅ |
| **Config Page**         | ✅ |

---

## :material-file-document-arrow-right: 2. Installing and Configuring the Plugin in Netbox
To install the plugin in Netbox, we need to modify and add some files that are responsible for the Netbox configuration.

The files are:

- `plugin_requirements.txt`.
- `DockerFile-Plugins`.
- `docker-compose.override.yml`.
- `configuration/plugins.py`.

### :fontawesome-solid-gear: 2.1 Configuring the Netbox version:

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
    All commands below will be executed inside the root directory of netbox `netbox-docker/`.


### :material-text-box: 2.2 plugin_requirements.txt
This file contains a list of Netbox plugins (as Python packages from PyPI) that should be installed during the Docker image build.

Execute the following command to write the package inside the `plugin_requirements.txt` file.

```bash
echo "netbox-napalm-plugin" > plugin_requirements.txt
```

### :material-docker: 2.3 DockerFile-Plugins
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

### :material-docker: 2.4 docker-compose.override.yml
As the name implies, this file contains the settings that will override `docker-compose.yml`.

If you have not yet configured the `br-lab` network, access: [Configuring the Docker Network](../../../../Laboratórios/Juniper/vJunos/Descoberta/index.md/#31-configurando-a-rede-docker)

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
      - br-lab

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

- Adding Netbox to the `br-lab` network.
- Changing the dockerfile to `Dockerfile-Plugins`, created previously.
- Also changed the image of the services to: `netbox:latest-plugins`.

### :material-power-plug-outline: 2.5 plugins.py
This file is responsible for setting the specific configurations for each plugin.

1. Access the file with the editor:
```bash
nano configuration/plugins.py
```

2. Copy and paste the content into the file:
```bash
PLUGINS = [
    "netbox_napalm_plugin"
]

PLUGINS_CONFIG = {
    "netbox_napalm_plugin": {
        "NAPALM_USERNAME": "admin", # User for accessing the equipment
        "NAPALM_PASSWORD": "admin@123", # Password for accessing the equipment
    },
}
```

---

## :simple-docker: 3. Build and Deploy!
Now your Netbox is configured and ready for deployment, follow the commands below and build the new Netbox instance!

1. Build the image:
```bash
docker compose build --no-cache
```

2. Bring up the containers:
```bash
docker compose up -d
```

After the containers come up, execute the commands below to copy the static files requested by the Napalm plugin.

1. First, change the permissions of the files using the command below:
```bash
docker compose exec -it --user root netbox chmod -R a+w /opt/netbox/netbox/static
```

2. Then, execute the command to copy the static files:
```bash
docker compose exec netbox python3 manage.py collectstatic --noinput
```

---

## :fontawesome-solid-gear: 4. Configuring Napalm
Now, with Netbox already configured and working, let's configure and better understand how Napalm works.

**Important points, to activate the Napalm plugin we need the following requirements:**

- Napalm Platform Configs
- Device
    - Device Role
    - Device Type
    - Status: Active
    - Platform
    - Primary IPv4
    - Interfaces (To display the LLDP Neighbors tab)

### :material-file: 4.1 Napalm Platform Configs
Access your Netbox and follow the instructions below.

1. In the side menu, go to **Plugin** → **Napalm**.
2. Click the **Add** button.
3. `Platform`: Select a platform (e.g., **junos**)
4. `NAPALM driver`: Here is the name of the driver used by Napalm to collect data from devices. To see the available drivers, go to [Supported Devices](https://napalm.readthedocs.io/en/latest/support/#general-support-matrix). In this case, we will use **junos**.
5. `NAPALM arguments`(Optional): Arguments passed when initializing the NAPALM driver. Arguments at: [Optional Arguments](https://napalm.readthedocs.io/en/latest/support/#optional-arguments). In our case, we will not fill it in.
6. Click **Create**.

Ready! now we have the Platform Config created for accessing our devices!

### :fontawesome-solid-gears: 4.2 Configuring a Device
To test the Napalm plugin, we need devices to query, for that, we will use the Discovery laboratory [More information](../../../../Laboratórios/Juniper/vJunos/Descoberta/index.md). Therefore, add at least one device to Netbox.

#### :material-router-wireless: 4.2.1 Adding the Routers
1. Clone the lab repository:
```bash
git clone https://git.rnp.br/redes-abertas/labs/-/tree/main/discovery-lab
```

2. Enter the repository:
```bash
cd discovery-lab/
```

3. Start the topology with the command:
```bash
sudo clab deploy -t clab/discovery-lab.clab.yaml
```
!!! warning "Debug" 
    The devices may take about 10 minutes to become fully operational.
    If an error occurs, check the command output for possible error messages. Use `docker logs <container_name>` to debug.

#### :octicons-diff-added-16: 4.2.2 Adding the router to Netbox.
Create Site

1. Go to **Sites** → click **Add**.
2. Fill in the fields:
   - **Name**: `RNP`
3. Click on **Create**.

---

Create the Manufacturer

1. Go to **Devices** → **Manufacturers** → **Add**.
2. Fill in:
   - **Name**: `Juniper`
   - **Slug**: `juniper` (or automatically generated)
3. Click on **Create**.

---

Create the Device Type

1. Go to **Devices** → **Device Types** → **Add**.
2. Fill in:
   - **Manufacturer**: `Juniper`
   - **Model**: `VMX`
3. Click on **Create**.

---

Create the Device

1. Go to **Devices** → click **Add**.
2. Fill in:
   - **Name**: `JPA`
   - **Device Role**: `Router` (create if necessary)
   - **Device Type**: `VMX`
   - **Site**: `RNP`
   - **Status**: `Active`
3. Click on **Create**.

---

Create Interface

1. Access the `JPA` device.
2. Go to the **Interfaces** tab → click **Add Interface**.
3. Fill in:
   - **Name**: `ge-0/0/2`
   - **Type**: `Virtual`
4. Click on **Create**.

---

Create IP Address

1. Go to **IPAM** → **IP Addresses** → **Add**.
2. Fill in:
   - **Address**: `172.10.10.101/32`
   - **Status**: `Active`
   - **Interface Assignment**:
     - **Device**: `JPA`
     - **Interface**: `ge-0/0/2`
3. Click on **Create**.

---

Adding Primary IPv4 on the Device

1. Go to **Devices**
2. Click on **JPA** and then **Edit**
3. In **Management** → **Primary IPv4**: Select `172.10.10.101/32 (ge-0/0/2)`

---

## :material-eye: 5. Viewing the Plugin
After registration, on the device tab, access **JPA**.

Now you should be seeing the additional tabs of the Napalm plugin.

- Status
- LLDP Neighbors
- Config

### :simple-statuspage: 5.1 Status
The Status tab, enabled through the integration of NetBox with the NAPALM plugin, displays real-time operational information of the network device. This functionality allows the administrator to quickly monitor the current state of the equipment without leaving the NetBox interface.

:material-pin: **Key Information Presented**:

- **Device Facts**: Basic and static data of the device, such as:

    - `Hostname`: Device identification on the network (e.g., JPA)

    - `Vendor / Model`: Equipment manufacturer and model (e.g., Juniper VMX)

    - `Serial Number`: Hardware serial number

    - `OS Version`: Operating system version (e.g., 22.2R1.9)

    - `Uptime`: Time since the last boot, with recorded date and time

- **Environment**: Environmental and performance metrics that help in preventive maintenance and operation:

    - `CPU Usage`: Current usage of the CPU(s), presented per core

    - `Memory`: Amount of memory available and used

    - `Temperature, Fans, Power (PSUs)`: Status of sensors and power supplies (if the equipment provides this data)

![Status Tab Image](/img/netbox_imgs/napalmStatusPage.png)

:simple-target: **Purpose**:

This tab is especially useful for quick diagnostics, audits, and monitoring device health, eliminating the need for manual login via SSH or console. The information is updated dynamically through the NAPALM API, as long as it is correctly configured in NetBox.

### :material-connection: 5.2 LLDP Neighbors
This functionality displays the layer 2 neighbors detected through the LLDP (Link Layer Discovery Protocol) protocol. This functionality allows you to automatically identify devices connected directly to the monitored equipment.

:material-pin: **Important Behavior**:

- The visualization of neighbors is limited to the interfaces previously registered in NetBox.

- If an interface exists on the actual device but has not been created in NetBox, the neighbors discovered by it will not be displayed.

![LLDP Neighbors Tab Image](/img/netbox_imgs/napalmLldpNeighborsPage.png)

:simple-target: **Purpose**:

This tab is useful for validating physical connections between devices, checking the network topology in real time, and detecting cabling or port configuration errors, in an automated manner and integrated into the NetBox interface.

### :fontawesome-solid-gear: 5.3 Config
The Config tab allows direct viewing of the network device's configurations, extracted remotely via the API. It presents different versions of the configuration file, useful for comparison, auditing, and troubleshooting.

:material-file: **Types of Configurations Displayed**:

- `Startup Config`: The configuration that will be loaded when the device is restarted. Represents the persistent state.

- `Running Config`: The configuration currently running on the device. May include unsaved changes.

- `Candidate Config` (when supported by the operating system): Configuration being edited that has not yet been applied. Present on equipment that works with configuration staging (e.g., Juniper).

![Config Tab Image](/img/netbox_imgs/napalmConfigPage.png)

:simple-target: **Purpose**:

This tab is essential for managing and tracking changes in the configuration of devices, as well as providing a practical and secure way to validate whether persistent configurations are in accordance with those in execution — all within the NetBox interface. without changing the structure of the documentation. or add anything, and do not change the links or references.