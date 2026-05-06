# NetReplica - Configuration and Execution Guide in Container

This guide describes the necessary steps to configure and run NetReplica in a Docker container, using Docker Compose. NetReplica is a tool dedicated to automating network labs through software.

## Prerequisites

- Docker installed on your machine: <a target="_blank" href="https://docs.docker.com/get-docker/">Installation Instructions</a>
- Docker Compose installed on your machine: <a target="_blank" href="https://docs.docker.com/compose/install/">Installation Instructions</a>

## Step 1: Environment Preparation

1. Open a terminal and clone the NetReplica repository using the following command:

```bash
git clone https://git.rnp.br/redes-abertas/netreplica-docker.git
```

2. Navigate to the cloned NetReplica directory:

```bash
cd netreplica-docker
```

## Step 2: Container Initialization

1. To build the Docker image and start the NetReplica container, run:

```bash
docker compose up -d
```

This command will create and start the container in the background.

## Step 3: Using NetReplica

After the container initialization, you can interact with NetReplica using the commands below.

### Executing NetReplica

1. Place any necessary configuration files (`.conf` files) in the `conf` folder that is within the `nrx` directory where the repository was cloned.

2. To run NetReplica with the `.conf` file, use the following command:

```bash
docker exec -it nrx nrx -c conf/<arquivo.conf>
```

- Replace `<arquivo.conf>` with the name of the configuration file you want to use.
- The output directory for the execution results is already specified within the `.conf` file, so it is not necessary to specify it in the command.

### Alias for Agility

To further optimize the use of NetReplica, you can create an alias in your shell to simplify the execution command:

1. Open a terminal and edit the shell profile file corresponding to your system (for example, **`~/.bashrc`** for Bash or **`~/.zshrc`** for Zsh).
2. Add the following line to the end of the file:

```bash
alias nrx='docker exec -it nrx nrx'
```

3. Save the file and close it.
4. To activate the new alias without restarting the terminal, run the command:

```bash
source ~/.bashrc   # or source ~/.zshrc, depending on your shell
```

Now, you can use the simplified command **`nrx`** to run NetReplica more quickly. For example:

```bash
nrx -c conf/<arquivo.conf>
```

Now to test if NetReplica is working, execute the following command:

```bash
nrx -c conf/teste.conf
```

this command will perform a query on the demonstration netbox generating a result equal to the one shown below:

```bash
--> nrx -c conf/teste.conf
Reading platform map from: templates/platform_map.yaml
Connecting to NetBox at: https://demo.netbox.dev
Fetching devices from sites: ['DM-Akron']
Created clab topology: conf/lab/lab.clab.yaml
To deploy this topology, run: sudo -E clab dep -t conf/lab/lab.clab.yaml
```

### Monitoring the Execution

- During execution, NetReplica will use the settings in the `.conf` file to access NetBox, start network replication and analysis. Monitor the terminal output to track progress and view any relevant messages.
- After completion of the execution, the replication and analysis results will be available in the output directory specified within the `.conf` file.

### Stopping the Container

To stop the NetReplica container and release resources, run:

```bash
docker compose down
```

## Next Steps: `.conf` File Configuration

Now that you know how to configure and run NetReplica,
the next step is to understand how to correctly configure the `.conf` file to meet the needs of your network environment.

next steps [`.conf` File Configuration](NetReplica Guia Configuração e Execução com NetBox.md)