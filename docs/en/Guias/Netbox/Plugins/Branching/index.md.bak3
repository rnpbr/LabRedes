# :material-power-plug-outline: Branching Plugin

The Branching plugin for NetBox is a solution that enables the creation of branches of the data stored in the system, allowing different teams or work environments to make changes, test, and validate without directly impacting the main database. With it, NetBox gains flexibility to manage versioning, experimentation, and collaboration scenarios, facilitating configuration comparison, change control, and the consolidation of updates in the documented infrastructure.

## :simple-git: Plugin Repository
Copy the link below or click to access the [Github Repository](https://github.com/netboxlabs/netbox-branching)

```
https://github.com/netboxlabs/netbox-branching
```

---

## :material-scale-balance: 1. Installation Requirements
This documentation used the following components with their respective versions:

| Components           | Versions |
| --------------------- | ------- |
| **Netbox**            | v4.2.4  |
| **Napalm Plugin**     | v0.5.7  |

---

## :material-file-document-arrow-right: 2. Installing and Configuring the Plugin in Netbox
To install the plugin in Netbox, we need to modify and add some files that are responsible for Netbox configuration.

The files are:

- `plugin_requirements.txt`.
- `DockerFile-Plugins`.
- `docker-compose.override.yml`.
- `configuration/plugins.py`.
- `configuration/local_settings.py`

### :fontawesome-solid-gear: 2.1 Configuring the Netbox Version:

1. First, let's clone the Netbox repository:
```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
```

2. Access the cloned directory:
```bash
cd netbox-docker
```

3. Now, switch to release 3.2.1
```bash
git checkout 3.2.1
```
!!! tip "Information"
    We changed the repository branch to access version 4.2.4 of Netbox.

!!! tip "Tip"
    All commands below will be executed inside the netbox root directory `netbox-docker/`.

### :material-text-box: 2.2 plugin_requirements.txt
This file contains a list of Netbox plugins (as Python packages from PyPI) that should be installed during the Docker image build.

Execute the following command to write the package into the `plugin_requirements.txt` file.

```bash
echo "netboxlabs-netbox-branching==0.5.7" >> plugin_requirements.txt
```

### :material-docker: 2.3 DockerFile-Plugins
This is the DockerFile used to build the custom docker image.

1. Create the file and access it with an editor:
```bash
nano DockerFile-Plugins
```

2. Copy the content below and paste it into the file:
```bash
FROM netboxcommunity/netbox:v4.2.4

COPY ./plugin_requirements.txt /opt/netbox/
RUN /usr/local/bin/uv pip install -r /opt/netbox/plugin_requirements.txt

# Netbox branching => copy local_settings to container
COPY ./configuration/local_settings.py /opt/netbox/netbox/netbox/local_settings.py
```

### :material-docker: 2.4 docker-compose.override.yml
As the name implies, this file contains the configurations that will override `docker-compose.yml`.

If you haven't configured the `br-lab` network yet. Access: [Configuring the Docker Network](../../../../Laboratórios/Juniper/vJunos/Descoberta/index.md/#31-configurando-a-rede-docker)

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

- Add Netbox to the `br-lab` network.
- Changed the dockerfile to `Dockerfile-Plugins`, created earlier.
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
    "netbox_branching"
]
```

### :fontawesome-solid-gear: 2.5 local_settings.py
Now, let's create the plugin configuration file that allows the Netbox database to create replicas of the tables.

1. First create the file in `./configuration/`, with the following command:
```bash
nano ./configuration/local_settings.py
```

2. Now, copy the content below, and paste it into the created file.
```bash
import sys
import os

# Adds the current directory to sys.path
sys.path.append(os.path.dirname(__file__))

from netbox_branching.utilities import DynamicSchemaDict
from configuration import DATABASE

# Wrap DATABASES with DynamicSchemaDict for dynamic schema support
DATABASES = DynamicSchemaDict({
    'default': DATABASE,
})

# Employ our custom database router
DATABASE_ROUTERS = [
    'netbox_branching.database.BranchAwareRouter',
]
```

---

## :simple-docker: 3. Build and Deploy!
Now your Netbox is configured and ready for deployment, follow the commands below and build the new Netbox instance!

1. Build the image:
```bash
docker compose build --no-cache
```

2. Start the containers:
```bash
docker compose up -d
```

3. After starting the containers, verify that the PostgreSQL user which NetBox uses to authenticate, has permission to create new schemas in the database. The result should be: `GRANT`.

```bash
docker exec -it netbox-docker-postgres-1 psql -U netbox -d netbox -c "GRANT CREATE ON DATABASE netbox TO netbox;"
```

## 4. Visualization

With the plugin installed you can view the interface that is provided for you to work with branches in Netbox

- Top bar
<br />
<img src="../../../../../img/netbox_imgs/branchingHeaderButton.png"/>

- Menu
<br />
<img src="../../../../../img/netbox_imgs/branchingMenu.png"/>

To validate that the plugin is installed correctly, just go to Menu > Admin > Plugins
<br />
<img src="../../../../../img/netbox_imgs/branchingPlugin.png"/>