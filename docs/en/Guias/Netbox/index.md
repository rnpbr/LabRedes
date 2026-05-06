# Netbox

## 1. Netbox Installation and Imports

NetBox is an open-source web application for managing network and data center infrastructure. It allows you to document devices, racks, connections, IP addresses, circuits, and other resources, facilitating the control and automation of the IT environment.

### 1.1 Prerequisites

* **Docker** installed → <a href="https://docs.docker.com/get-docker/" target="_blank">Official Guide</a>
* **Docker Compose** installed → <a href="https://docs.docker.com/compose/install/" target="_blank">Official Guide</a>
*
* Access to **Git** to clone repositories.

> **Note:** This procedure is suitable for testing or homologation environments. For production, review security configurations before publishing.

### 1.2 Clone the Official Repository

```bash
git clone https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
```

### 1.3 Environment Variable Configuration

The repository has example `.env` files.

1. Access the `env/` folder:

   ```bash
   cd env
   ```
2. Edit the files as needed:

   * `netbox.env` → NetBox configurations (email, secret key, language, timezone).
   * `postgres.env` → Database credentials.
   * `redis-cache.env` → Redis credentials.
   * `redis.env` → Redis credentials.

> **Recommendation:**
> Even for test environments, change default passwords and credentials before putting into production.

### 1.4 Change the NetBox Version (Optional)

To change the version:

* Edit the `docker-compose.yml` or `docker-compose.override.yml` and adjust the image:

  ```yaml
  image: netboxcommunity/netbox:<version>
  ```
* Consult the compatible versions at: <a target="_blank" href="https://github.com/netbox-community/netbox-docker/releases">Netbox Docker Releases</a>

> **Caution:** Changes between very distant versions may require adjustments to the database or configurations.

### 1.5 Port Configuration (Optional)

Create the `docker-compose.override.yml` file to expose a specific port:

```bash
tee docker-compose.override.yml <<EOF
version: '3.4'
services:
  netbox:
    ports:
      - 8000:8080
EOF
```

> Change `8000` if the port is in use (e.g., `8080` or `8081`).

### 1.6 Build and Start the Containers

```bash
docker compose pull
docker compose up -d
```

!!! alert "Attention"
    The containers may take a few minutes to start. If the Netbox container is in a loop always starting, use this command to restart this container:

    ```bash
        docker compose restart netbox
    ```
    And to access the logs, simply use the command:

    ```bash
        docker compose logs -f
    ```

### 1.7 Create an Administrator User

After the containers are initialized:

```bash
docker compose exec netbox /opt/netbox/netbox/manage.py createsuperuser
```

Follow the instructions to define **user, email, and password**.

### 1.8 Access the Web Interface

* Local URL: <a target="_blank" href="http://localhost:8000">http://localhost:8000</a>
* From another host: `http://<SERVER_IP>:8000`

> Replace the port if you changed it in step 5.

### 1.9 Summary of Best Practices for Production

* Change all default credentials in the `.env` files.
* Configure TLS (HTTPS) certificates with Nginx or Traefik.
* Activate regular backups of the PostgreSQL database.
* Monitor logs and resource consumption of the containers.

## 2. Access

After completing the installation of NetBox in Docker, you can access it via a web browser. By default, NetBox will be available locally at <a target="_blank" href="http://localhost:8000/">http://localhost:8000/</a>. However, if you want to access NetBox securely through an SSH tunnel, follow the steps below:

### 2.1 Access via SSH Tunnel

1. Now, to access NetBox securely through an SSH tunnel, you will need a remote server with SSH access, where Docker does not need to be installed.
2. On the remote server, run the following command to create an SSH tunnel to NetBox:

    ```
    ssh -N -L 8080:localhost:8080 user@server_address
    ```

    - Replace `user` with the username of the remote server.
    - Replace `server_address` with the IP address or domain name of the remote server.
3. After entering your SSH password, the tunnel will be established. Now, the remote server will redirect requests from port 8080 to NetBox on port 8000.
4. On your local computer, open your web browser and go to:

    ```
    http://localhost:8080/
    ```

    You will be redirected to NetBox that is running on the remote server via the SSH tunnel. Now you can access NetBox securely.

Remember that the SSH tunnel will keep the connection active as long as the remote server terminal is open. If you want to keep the tunnel running in the background, add the `-f` option to the SSH command in step 9:

```
ssh -f -N -L 8080:localhost:8000 user@server_address
```

With this, you can access NetBox securely through an SSH tunnel, ensuring the protection of your data during transmission.

## 3. Import

For the import, the files must be organized in correctly formatted CSV format, containing the fields indicated below. In addition, it is important that the import follows the order of the numbering of the files as stated in the data preparation.

### 3.1. Data Preparation

The import of CSV files must follow the established numbering and contain the indicated information. The names (**in bold**) indicate the import locations, and the information below (*in italics*) indicates the fields required for import.

1. **manufacturers**
*name, slug*
2. **platforms**
*name, slug, manufacturer, napalm_driver, description*

    **tags**
    *name, items, slug, color, description*

3. **device_roles**
*name, color, vm_role, description, slug, tag*

    **device_types**
    *model, manufacturer, part_number, u_height, is_full_depth, slug*

    **sites**
    *name, status, slug, latitude, longitude*

    **tenants**
    *name, slug*

4. **devices**
*name, status, device_role, manufacturer, device_type, site, platform, tag*
5. **interfaces**
*name, device, label, enabled, type, description*

    **VRFs**
    *name, rd, tenant, enforce_unique, description, import_targets, export_targets, comments, tags*

6. **circuit_types**
*name, slug*

    **IP_addresses**
    *address, vrf, tenant, status, role, device, interface, dns_name, description*

    **providers**
    *name, slug*

7. **circuits**
*cid, provider, type, status, tenant, description*

### 3.2. The Import

1. **Log in as superuser**: Access NetBox with admin credentials.
2. **Find the import option**: Check the section related to the data you want to import, and look for an import **icon** as we see in Figure 1 below:

    ![**Figure 1**: By clicking the import icon, you can upload the CSV file.](../../../img/netbox_imgs/import.png)
    **Figure 1**: By clicking the import icon, you can upload the CSV file.

3. **Select the CSV file**: Upload the CSV file with the prepared data, each CSV must contain the fields as described in Subsection 3.1.
4. **Start the import**: Click "Send" or "Import" to start the process.
5. **Check the results**: Analyze the import report to confirm success.

<aside>
💡 **Note:** After importing the files of item `7.`, it is necessary to include the terminations manually.
To do this, follow the instructions below to complete the configuration. click on the created circuit and the `edit` icon as highlighted in the image below
Then edit the `side*` and `interface*` information
</aside>

- Click on Circuits to see the circuits created in step 7. Select with 1 click one of the Circuit IDs created, as indicated in Figure 2.

    **Note**: The steps must be done for every existing Circuit ID.

![**Figure 2**: click on the circuit (arrow on the left), then select the Circuirt ID (detached and indicated with the arrow) to perform the configuration.](../../../img/netbox_imgs/circuitID.png)
**Figure 2**: click on the circuit (arrow on the left), then select the Circuirt ID (detached and indicated with the arrow) to perform the configuration.

- After clicking on one of the circuits, the circuit settings are similar to that presented in Figure 3. The terminations must be edited by clicking on the `Edit` icon as highlighted in the image below. When you click on the icon, Netbox forwards to the Cables part in Connections, as shown in Figure 4.

![Figure 3: screen of a Circuit ID. The editions of each Temination must be carried out by clicking on `Edit` (highlighted with the arrow).](../../../img/netbox_imgs/circuitEdit.png)
**Figure 3:** screen of a Circuit ID. The editions of each Temination must be carried out by clicking on `Edit` (highlighted with the arrow).

- Figure 4 presents the creation of the connection cables, the numbering of the cables follows only the creation order. The `Side*` and `Interface*` items must be filled in to complete the configuration of step 7.

![Figure 4: connection cable configuration screen for the connection between devices.](../../../img/netbox_imgs/circuitCable.png)
**Figure 4:** connection cable configuration screen for the connection between devices.

<aside>
💡 Remember to adapt the subcategories and import locations according to the specific functionalities of your NetBox. Each category may have unique fields and settings for import.
</aside>