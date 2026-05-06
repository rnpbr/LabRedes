### CLAB Template Structure

CLAB templates follow a specific structure, which allows NetReplica to interpret and apply the configurations correctly. Here is an example of a CLAB template for a ceos device:

```yaml

  {{ name }}:
    kind: ceos
    image: ceos:latest
    {% if configuration_file is defined %}
    startup-config: {{ configuration_file }}
    {% endif %}
    {% if interface_map is defined %}
    binds:
        - {{ interface_map }}:/mnt/flash/EosIntfMapping.json:ro
    {% endif %}
    {% include 'clab/labels.j2' %}
```

In this example:

- `{{ name }}` is a variable that will be replaced by the device name.
- `kind` defines the type of device, in this case, "ceos".
- `image` specifies the device image.
- `startup-config` allows you to define an initial configuration file.
- `binds` allows you to map volumes, such as interface mapping.
- `include` is used to include additional labels from the CLAB template.

### Creating CLAB Templates

To create your own CLAB templates, follow the example structure and format provided. You can create `.j2` files, remembering that the filename should be the platform name for each device type, and customize the configurations as needed. Save your templates in the `templates/clab/kinds/` directory of your NetReplica environment.

By creating and using CLAB templates, you have the flexibility to define how devices will be provisioned and configured within the CLAB environment, allowing for precise replication of your network.

Example of the junos template junos.j2

```yaml
{{ name }}:
            kind: crpd
            image: crpd:23.1R1.8
            {% if configuration_file is defined %}
            startup-config: {{ configuration_file }}
            {% endif %}
            {% if interface_map is defined %}
            binds:
                - {{ interface_map }}:/mnt/flash/EosIntfMapping.json:ro
            {% endif %}
            {% include 'clab/labels.j2' %}

```

## Step 2: Running NetReplica with the Configuration File

---

Once you have created and configured the `.conf` file with the desired options, you are ready to run NetReplica and start replicating and analyzing networks based on the NetBox information. Follow the steps below to run NetReplica:

1. **Configuration File Location**: Make sure the `.conf` file is in the correct location. If you are using NetReplica via Docker, remember that the `.conf` file must be inside the "conf" directory that is created after running the compose.
2. **Starting NetReplica**: Open a terminal or command prompt and navigate to the directory where NetReplica is installed. If you are using NetReplica via Docker, make sure you are in the directory where the `docker-compose.yml` file is located.
3. **Running NetReplica**: Execute the command to start NetReplica, passing the path to the `.conf` file as an argument. For example, if the `.conf` file is in the current directory and is named `netreplica.conf`, the command might be:

    ```bash
    nrx -c <file>.conf
    ```

   If you are using NetReplica via Docker, the command to run might be:

    ```bash
    docker exec -it nrx ./nrx -c conf/<file>.conf
    ```

4. **Monitoring Execution**: During execution, NetReplica will use the settings from the `.conf` file to access NetBox and start the network replication and analysis. Monitor the terminal output to see the progress and any relevant messages.
5. **Execution Results**: After the execution is complete, the replication and analysis results will be available in the output directory specified in the `.conf` file (usually the `OUTPUT_DIR` directory). You will be able to find the exported files, such as images, device configurations, and other data, according to the defined settings.

Remember that NetReplica is a powerful tool for replicating and analyzing networks based on NetBox information. By running NetReplica with the correctly configured configuration file, you will be exploring the integration capabilities between these two tools to gain valuable insights into your network.

## **Sources**

1. NetReplica (NRX) GitHub Repository. Available at: **<a target="_blank" href="https://github.com/netreplica/nrx">https://github.com/netreplica/nrx</a>**
2. NetReplica Templates GitHub Repository. Available at: **<a target="_blank" href="https://github.com/netreplica/templates">https://github.com/netreplica/templates</a>**
3. ContainerLab Manual - Kinds. Available at: **<a target="_blank" href="https://containerlab.dev/manual/kinds/">https://containerlab.dev/manual/kinds/</a>**