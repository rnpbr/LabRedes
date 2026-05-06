# OSPF Routing

## :material-bookmark: **Introduction**

This lab simulates a network with 3 routers in a ring topology, configured using OSPF for dynamic routing and SNMP for sending telemetry across the network.

## :material-lan: **1. Topology and Configurations**

The topology consists of three routers (PB, PE, JPA) connected in a ring. Each router is configured with network interfaces and IP addresses, as well as OSPF protocols for routing and SNMP for monitoring, as we can see in the following image.

![Topology.png](../../../../../img/labs_imgs/Topologia_ospf_lab.png)

The routers are configured with the following technologies:

- **OSPF (Open Shortest Path First)**: Used for dynamic routing in the network, allowing routers to exchange information about routes and topology updates.
- **SNMP (Simple Network Management Protocol)**: Used for network monitoring and management, allowing access to telemetry information from devices.

## :material-tools: **2. Installation**
### :material-alert: 2.1 Prerequisites:

To start the lab, you need to install and configure the following components:

- Netbox
- Netreplica
- Containerlab

If your environment is not configured, follow the steps in [Configuration Guide](../../../../../Getting%20Started.md)

   
### :material-application-import: 2.2 Importing Template into Netbox:
Containerlab uses <a target="_blank" href="https://containerlab.dev/manual/nodes/#remote-startup-config ">startup-config</a> to import configurations to the equipment, these are defined in templates within Netbox.

1. :material-git: **In Netbox, create a Data source and add the git repository below:** 
```bash
https://git.rnp.br/gci/dev/inovacao-ciberinfraestrutura/config-templates-data-source
```
How to add: [Render Templates - #Remote Templates](../../Guias/Netbox/Render_Templates/index.md/#11-templates-remotos)

2. **Import the OSPF lab template:**
     1. Access your Netbox and go to **Provisioning** > **Configuration Templates**.
     2. Create a template and define a name of your choice.
     3. In **Data Source** choose the name of the data source created in step **1**.
     4. In **File** Select: ```Juniper/<image>/OSPF.jinja2```]
   
    !!! warning "Attention"
        Pay attention to the device image, as configuration templates are created differently for each image type.

3. :material-link-variant: **Associating Templates to Devices:**
      1. In your Netbox, access **Devices > Devices**.
      2. Select the device you want to associate with the template and click **edit**. 
      3. In the Management category, in **Configuration Template** select the name of the template defined in step **2.2**.
      4. Save the changes.


### :material-laptop: 2.3 **Setting up the Laboratory:**
Now, with Netreplica we will pull the information from Netbox to assemble
the `.clab` file that will be used by Containerlab to bring up the lab.

1. In the folder where the Netreplica container is, give the following command to import the Netbox configurations:
```bash
nrx -c conf/<file>.conf -n ospf-lab
```
2. Now with the `.clab` file created, use the command to bring up the lab:
```bash
sudo -E clab dep -t conf/lab/ospf-lab.clab.yaml
```
!!! warning "Attention"
    Devices need some time to be initialized and configured, the lab (graphite) may already be available and you will not be able to access the devices. </br>
!!! info "Tip"
    To view the container logs and check if it has been configured, you can use:
    ```bash
    docker logs <container_name> -f
    ```

## **3. Access**

There are two ways to access the devices on the network:

- **Access via SSH to the routers**: Use an SSH client to connect to the routers using the IP address of each device or the name assigned by Containerlab, along with the login credentials provided. The management IP address of each router is displayed after the lab is executed by Containerlab.

    Example:

    ```bash
    
    ssh admin@<router_IP_address>
    ```

    or

    ```bash
    
    ssh admin@<router_name>
    ```

- **Access to Graphite (Topology Server)**: Access Graphite through the browser using the IP address and port configured. You can also access it directly by clicking on the SSH icon on the desired router.

    URL: **`http://<Graphite_IP_address>:8080/graphite/`**

    Credentials:

  - Username: admin
  - Password: admin@123

## **4. Monitoring**

To monitor the network and devices, you can use tools like edgeshark for packet analysis or SNMP monitoring tools.

- **edgeshark**: Capture and analyze network traffic for troubleshooting and performance monitoring.
- **SNMP Monitoring**: Use SNMP-compatible tools to monitor network performance and health metrics.