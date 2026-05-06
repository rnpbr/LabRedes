# Auto Discovery in Zabbix

## :octicons-book-24: 1. Introduction

Zabbix **Auto Discovery** is an advanced feature that allows you to dynamically detect hosts and services on a network, eliminating the need to manually register devices. This functionality is especially useful in dynamic environments, such as the **br-lab** laboratory, where new devices can be added frequently.

In this guide, you will learn how to configure a discovery rule in Zabbix to automatically identify network assets using the **SNMPv2** protocol, as well as create an **auto-registration action** to add the discovered devices to monitoring.

---

## :octicons-tools-24: 2. Prerequisites

Before starting, verify the following prerequisites:

1. **Zabbix properly installed** on the `br-lab` network.
   If you have not yet installed it, follow the [Zabbix Installation Guide](../../../pt/Ferramentas/Zabbix/index.md).

2. The `br-lab` network must be functional and with devices configured to respond to SNMPv2 requests.

3. The user used must have administrative permissions in the Zabbix frontend.

---

## :octicons-checklist-24: 3. Configuring Auto Discovery

Auto discovery in Zabbix works based on two entities:

* **Discovery Rule**: Defines the range of IPs to be scanned, the type of check (e.g. SNMP, ICMP), and how to extract the host name.
* **Discovery Action**: Applies rules after detection (e.g. add to monitoring, apply template, move to group).

---

## :octicons-tools-24: 3.1 Creating the Discovery Rule

To create a new rule:

1. Access the **Zabbix Frontend** and go to:
   `Data Collection → Discovery`
   Click on **Create discovery rule**.

2. Configure the following parameters:

| Field                          | Value                               |
| ------------------------------ | ----------------------------------- |
| **Name**                       | `br-lab`                            |
| **Discovery by proxy**         | `Zabbix server`                     |
| **IP range**                   | `172.10.10.1-254`                   |
| **Update interval**            | `1m`                                |
| **Device uniqueness criteria** | `IP address`                        |
| **Host name**                  | `SNMPv2 agent ".1.3.6.1.2.1.1.5.0"` |
| **Visible name**               | `SNMPv2 agent ".1.3.6.1.2.1.1.5.0"` |

3. Add a **Check** with the following parameters:

| Field          | Value                                        |
| -------------- | -------------------------------------------- |
| **Check type** | `SNMPv2 agent`                               |
| **Community**  | `public`                                     |
| **Port**       | `161`                                        |
| **SNMP OID**   | `.1.3.6.1.2.1.1.5.0` (Host name via SNMP) |

4. Save the rule after configuration.

> ✅ When configured correctly, the rule will scan the entire `172.10.10.0/24` subnet every minute, looking for devices that respond to SNMP on port 161 with the `public` community.

---

### :material-image: Reference Images (example)

#### 📸 General Rule Configuration:
---
![Discovery Rule](../../../img/tools_imgs/zabbix_discovery_rule.png)

#### 📸 SNMP Check Configuration:
---
  ![Discovery Check](../../../img/tools_imgs/zabbix_discovery_check.png)
---

!!! info "Note"
    remember to activate the rule for it to work correctly. You can do this on the discovery rule configuration tab by checking the "Enable" option.
---

## :octicons-gear-24: 3.2 Creating the Auto-Registration Action

### 🧠 What is a *Discovery Action*?

A **discovery action** in Zabbix is ​​a set of instructions that define **what should be done automatically after a host is detected** by a *Discovery Rule*. This mechanism allows the automation of infrastructure management, avoiding manual device registration.

With a discovery action configured, it is possible to:

* Automatically insert the detected host into the monitoring database;
* Associate the host with one or more **host groups**;
* **Apply monitoring templates** (e.g. ICMP, SNMP, operating systems);
* Mark inventory fields and activate the host for immediate monitoring.

---

### 🔧 Steps to Create the Action

1. In the **Zabbix Frontend**, navigate to:
   `Alerts → Actions → Discovery actions`.

2. Click on **Create action** and configure as below:

---

#### 🧩 "Action" Tab

| Field          | Value                                                                                         |
| -------------- |-----------------------------------------------------------------------------------------------|
| **Name**       | `Auto Discovery: Network Devices`                                                             |
| **Conditions** | <ul><li>`Discovery rule equals br-lab`</li><li>`Discovery status equals Discovered`</li></ul> |

> 💡 These conditions ensure that the action will only be executed for hosts successfully discovered by the `br-lab` rule.

---

#### ⚙️ "Operations" Tab

Add the following operations:

| Operation Type             | Parameters                                                    |
| ---------------------------- | ------------------------------------------------------------- |
| **Add host**                 | Automatically adds the discovered host to the Zabbix database |
| **Add to host groups**       | `Discovered hosts`                                            |
| **Link to templates**        | `Juniper MX by SNMP`                                          |


!!! info "Info"
    The `Juniper MX by SNMP` template is located within the `Templates/Network Devices` group. It is ideal for monitoring Juniper MX line equipment via SNMP.
    If you use other network devices (Cisco, Mikrotik, Dell, etc.), choose an appropriate template or create a custom one according to your needs.

---

### :material-image: Example Images

#### 📸 "Action" Tab Screen

![Discovery Action - Action Tab](../../../img/tools_imgs/zabbix_actions.png)

#### 📸 "Operations" Tab Screen

![Discovery Action - Operations Tab](../../../img/tools_imgs/zabbix_actions_operations.png)

---

With this action configured, every device detected on the `br-lab` network with SNMP support will be automatically added to Zabbix, with defined template and monitoring group, allowing scalability and agility in infrastructure management.