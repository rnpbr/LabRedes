# Guide: Deploying Network Labs using VSCode and Containerlab

## Introduction

This guide presents the process of creating and deploying network labs using **Visual Studio Code (VSCode)** in conjunction with the **Containerlab** extension.
The goal is to demonstrate how this integration can **simplify network experiments**, approximating the experience of a real production environment.
For **infrastructure** professionals, the use of these tools represents:

* **Greater predictability** in network changes.
* **Agility** to create and destroy test environments.
* **Lower operational risk**, by pre-validating critical scenarios.

---

## What is VSCode?

**Visual Studio Code (VSCode)** is a lightweight and cross-platform code editor. Although widely used by developers, it also offers essential features for system administrators and network operators.
With support for **extensions**, VSCode can be transformed into a **centralized management platform**, where you edit configuration files, connect to remote servers, and now, with **Containerlab**, also manage complete network labs.

---

## Benefits for Infrastructure

### Production

* Validation of changes in isolated environments before actual deployment.
* Resilience testing against network failures.
* Reduced troubleshooting time.

### Research

* Creation of controlled test environments for protocol simulation.
* Reproducing adverse conditions (delay, jitter, packet loss).
* Support for academic experiments and scientific articles.

### Network Operators

* Less reliance on the command line for common tasks.
* Graphical visualization of the topology.
* Integration with documentation tools (TopoView, Draw.io).

---

## Requirements

Before starting, verify:

* **VSCode installed** on your machine.
* Prior reading of the documentation of the lab used as an example:
  [Zabbix Monitoring Lab](../../Laboratórios/Juniper/vJunos/Monitoramento-Zabbix/index.md).
* Basic familiarity with the VSCode interface:
  [Introduction to VSCode](index.md).

---

## Remote Usage with SSH

If you intend to run VSCode on a **remote host** (e.g., server or test VM):

* First, install the **Remote SSH** extension. It allows VSCode to access files and resources on the remote server as if they were local.
* After connecting to the remote host, proceed with installing the other extensions and configuring the environment.

This is useful in lab or production environments where hardware resources for containers are not available on your personal machine.

![SSH Mode](../../../img/vscode/2-ssh-mode.png)

---

## 1. Installing the Containerlab Extension

The first step is to install the **Containerlab** extension in VSCode.
This extension adds a side panel where you can:

* Create, destroy, and edit labs.
* Visualize topologies graphically.
* Monitor node logs and status.

![Install](../../../img/vscode/1-install.png)

---

## 1.1 Installing EdgeShark

**EdgeShark** is an integration that allows you to open traffic captures directly in VSCode, without relying on external Wireshark.
This simplifies packet analysis in network experiments, making VSCode a complete tool for experimentation.

To install:

* Open the top search bar in VSCode.
* Type:

  ```
  >containerlab: install Edgeshark
  ```
* Press Enter.

![EdgeShark](../../../img/vscode/1.1-edgeshark.png)

---

## 2. Deploying a Lab

In this section, we will **deploy the Zabbix monitoring lab**.

1. Open the Containerlab side tab in VSCode.
2. Click on **Open Folder** and choose the working directory.
3. In the integrated terminal, download the example lab with the commands below:

=== "Linux/Mac"

```bash
curl -L -o get.sh "https://git.rnp.br/redes-abertas/labs/-/raw/main/zabbix-lab/get.sh?ref_type=heads&inline=false" && sh get.sh && cd zabbix-lab
```

=== "Windows"

```bash
curl -L -o get.bat "https://git.rnp.br/redes-abertas/labs/-/raw/main/zabbix-lab/get.bat?ref_type=heads&inline=false" && call get.bat && cd zabbix-lab
```

This command downloads an installation script, executes it, and creates the folder with the lab.

After completion, the lab will appear in the **Local Labs** tab. Simply right-click on the lab and choose **Deploy**.

![Deploy](../../../img/vscode/6-Deploy.gif)

---

## 3. Main Features

### Visualization and editing

In **TopoView**, the topology is displayed graphically, allowing:

* Adding or removing nodes and links.
* Changing interfaces, IP addressing, and performance limitations.
* Associating configuration files directly to each node.
* Manually editing the `.clab` file, if you prefer.

This replaces time-consuming manual edits in YAML, giving greater agility to the process.

---

### Monitoring nodes and logs

Each node in the topology can be inspected directly in VSCode. It is possible to open **real-time logs**, which helps in diagnosing failures and validating the operation of services.

![Logs](../../../img/vscode/7-Logs.gif)

---

### Capturing and analyzing traffic

With **EdgeShark**, it is possible to capture packets from specific interfaces within the topology.
This functionality is equivalent to using Wireshark in a real environment, making it ideal for protocol analysis and troubleshooting.

![SSH Wireshark](../../../img/vscode/8-ssh-wireshark.gif)

---

### Failure simulation (Link Impairment)

The **Link Impairment** feature allows you to add adverse conditions to the simulated network:

![Link Imparciment](../../../img/vscode/9-Link-imparciment.gif)

* **Delay (ms)** – response time.
* **Jitter** – delay variation.
* **Loss (%)** – packet loss.
* **Rate-limit (Mbps)** – bandwidth limitation.
* **Corrupt (%)** – packet corruption.

This type of simulation is very valuable for assessing how production systems would behave in unstable scenarios.

---

### Other useful options

In the management tab, we find additional functionalities:

1. **Destroy (cleanup)** – removes the lab and all persistent data.
2. **Redeploy (cleanup)** – restarts the lab from scratch.
3. **Save config** – saves the current configuration of the nodes.
4. **Inspect** – shows image and network information.
5. **SSH (all nodes)** – opens SSH sessions to all nodes.
6. **Graph (draw.io)** – exports the topology for documentation.
7. **Graph (TopoView)** – opens the topology in the graphic viewer.
8. **Edit topology** – manual editing of the `.clab` topology.

![Lab Options](../../../img/vscode/10-lab-options.png)

These functions complement the lifecycle of a network lab, from creation to disposal and documentation.

---

## 4. Next Steps

After mastering the basic functionalities, it is recommended to:

* Deploy other labs available [here](../../Laboratórios/index.md) without altering the document structure, adding anything, or changing links or references.