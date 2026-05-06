# Edgeshark Installation and Usage Guide

## 1. Introduction

**Edgeshark** is an innovative solution designed to facilitate the capture and analysis of network traffic in containerized environments. It consists of two main containerized services, <a target="_blank" href="https://github.com/siemens/ghostwire">Ghostwire</a> and <a target="_blank" href="https://github.com/siemens/packetflix">Packetflix</a>, which work together to monitor network traffic within Docker containers. In addition, it offers an optional plugin for Wireshark, called <a target="_blank" href="https://github.com/siemens/cshargextcap">csharg external capture plugin</a>, which allows remote live capture of network traffic.

## 2. Installing Edgeshark

Edgeshark offers multi-architecture Docker images for the `linux/amd64` and `linux/arm64` architectures.

!!! warning "WARNING"
    Make sure you have a Linux kernel of at least version 4.11 installed. However, we strongly recommend using version 5.6 or higher.

=== "Using Docker Compose v2"

    1. **Install Docker Compose v2:**

    Make sure the Docker Compose v2 plugin is installed. Verify by running `docker compose version`, which should display the plugin version without errors. For Debian users, we recommend installing the `docker-ce` packages instead of `docker.io`, as they are updated more frequently.

    2. **Deploying Edgeshark services:**
    
       Copy and paste the command below into a terminal to deploy the services:
    
         
        wget -q --no-cache -O - \
        https://github.com/siemens/edgeshark/raw/main/deployments/wget/docker-compose-localhost.yaml \
        | DOCKER_DEFAULT_PLATFORM= docker compose -f - up
        
    
       3. **Access the interface:**
    
          After deployment, visit <a target="_blank" href="http://localhost:5001/">http://localhost:5001</a> in your browser to explore the virtual network of your container host.
    
    
    !!! note "NOTE"
        Using DOCKER_DEFAULT_PLATFORM= ensures correct deployment of multi-architecture images and avoids issues, especially with Apple's Rosetta, which may have difficulties with read-only image deployments.
    
    
    !!! warning "WARNING"
        The following quick deployments will expose TCP port 5001 (or 5500) to clients external to your host. Make sure your network is properly protected.
    

=== "Using Bash"

    If your system does not support Docker Compose v2, you can use a Bash script as an alternative.

    1. **Deployment via Bash:**
    
       Execute the command below to deploy the services using a Bash script:

        wget -q --no-cache -O - \\
          <https://github.com/siemens/edgeshark/raw/main/deployments/nocomposer/edgeshark.sh> \\
          | DOCKER_DEFAULT_PLATFORM= bash -s up
    
    2. **Access the interface:**

        Visit <a target="_blank" href="http://localhost:5001/">http://localhost:5001</a> in your browser to explore the virtual network of your container host.
    
    
    !!! warning "WARNING"
        This quick deployment will expose TCP port 5001 to clients external to your host. Make sure your network is properly protected.
    

=== "Using Industrial Edge"

    1. **Download the Edgeshark application:**
    
        Download the <a href="https://github.com/siemens/edgeshark/releases/latest" target="_blank">latest `.zip` file</a> in the project releases section.

    2. **Extract the file:**   

        Unzip the `edgeshark.app` file contained in the `.zip` archive.

    3. **Import to the IEM:**

         Import the `edgeshark.app` file into your Industrial Edge Management (IEM) system.

    4. **Deployment on the IED:**

         In your IEM catalog, deploy the Edgeshark application to your Industrial Edge Devices (IEDs).

        !!! warning "WARNING" 
            The Edgeshark UI and services are exposed on port 5001 on your IED hosts without any user authorization. This is required to support remote packet capture from the user interface.
    

    5. **Access the interface:**

        Navigate to the HTTP port 5001 on your IED: `http://<ied-ip-address>:5001` (make sure to use `http:` and **not** `https:`). You should now see the Edgeshark user interface.

### 2.1 Optional Plugin for Packet Capture

If you need to capture live network traffic inside the containers, you need to install the external <a target="_blank" href="https://github.com/siemens/cshargextcap">cshargextcap</a> plugin for Wireshark.

=== "Windows 64bit"

    1. **Check Wireshark:**  
       Make sure you have a recent version of <a target="_blank" href="https://wireshark.org">Wireshark (64 bits)</a> installed. The minimum recommended version is 3.0.2.
    
    2. **Install the plugin:**  
        Download and run the latest plugin installer, available <a target="_blank" href="https://github.com/siemens/cshargextcap/releases/latest">here</a>.
    
    3. **Start the capture:**  
        In the Edgeshark web interface, click on one of the Wireshark buttons to start a capture session.

=== "Linux 64bit"

    1. **Install Wireshark:**  
       Install Wireshark from your distribution's repositories and allow it to be used by non-root users.
    
    2. **Add your user to the wireshark group:**  
        Execute the command below:

            sudo gpasswd -a $USER wireshark

    3. **Install the plugin:**  
       Download and install the appropriate plugin package for your distribution.
    
    4. **Start the capture:**  
        In the Edgeshark web interface, click on one of the Wireshark buttons to start a capture session.

=== "macOS 64bit"

    1. **Download the plugin:**  
        Download the latest plugin for macOS <a href="https://github.com/siemens/cshargextcap/releases/latest" target="_blank">here</a>

    2. **Install the plugin:**  
         Follow the installation instructions provided in the downloaded file.

    3. **Start the capture:**  
        Navigate to the Edgeshark web interface and click on a Wireshark button to start a live capture.


## Next Steps

Now that Edgeshark is installed, the next step is to learn how to use it effectively. To do this, access the detailed usage page by clicking [here](#) and discover how to capture network traffic in your containers using Edgeshark. Take advantage of the available resources to optimize data collection and improve the visibility of your network.

## References

For more information and additional resources about Edgeshark, visit the <a href="https://edgeshark.siemens.io/#/getting-started" target="_blank">Official Documentation</a>.