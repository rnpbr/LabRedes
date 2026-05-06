# Documenting Labs

Contributing to the documentation of labs in **Containerlab** is a straightforward process, but it's important to follow a few steps to ensure all links and functionalities work correctly. This page provides the necessary instructions for documenting a lab, as well as setting up the essential scripts for the proper functioning of the deployment process.

---

## 1. Creating Lab Documentation

### Creating Images to Represent Labs

In the documentation, it's important for labs to have images representing the lab's network topology.

### Steps to Document a Lab

Here are the main steps for documenting your lab:

1. **Create Lab Description and Objective**:
    - Describe what the lab does and which protocol or functionality is being demonstrated.
2. **Document the Lab Topology**:
    - Use the created images to illustrate the lab's network topology. If necessary, insert additional diagrams explaining how the devices are interconnected.
3. **Include Usage Examples**:
    - Provide examples of commands and actions that users can execute within the lab to test the functionality.
4. **List Requirements**:
    - Clearly define hardware and software requirements, such as the Docker version, Containerlab version, and network configurations.
5. **Deployment Instructions**:
    - Document the lab's deployment, whether it's the ready-made or customized version. Be sure to follow the deployment guides with appropriate links.
6. **Access and Credentials**:
    - Create a table detailing the IPs of each device in the lab and their respective access credentials.

!!! tip "Tip"
    To follow a consistent documentation pattern, you can use the [template](Template lab.md) that is already structured with tips. It will serve as a basis for you to adapt the content of your lab, ensuring that all sections are correctly addressed.

To use the documentation template, simply go to **docs/pt/Laboratórios/Contribua/Template lab.md**, create a copy in the laboratorios folder, name it after your lab, and fill in the information.

---

## 2. Scripts for Quick Download

To ensure that the lab's download and deployment process works correctly, it's necessary to include two essential scripts within the lab's folder in GitLab. These scripts will allow the lab to be downloaded and configured automatically with a simple command.

### 2.1 `get.sh` Script

The `get.sh` script is used on Linux/Mac systems to automatically download and unpack the lab. It checks if the `tar` command is installed and, if not, installs the necessary package before downloading the file.

### How it Works:

1. **Dependency Verification**: The script checks if the `tar` package is installed. If not, it tries to install it using the system's package manager (`apt-get`, `dnf`, `yum`, or `pacman`).
2. **Download and Unpacking**: The script downloads the `.tar` file containing the lab and unpacks it in the destination directory.

### `get.sh` Script:

```bash
#!/bin/bash

# Function to check if a command is installed
check_command() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install packages
install_package() {
    if [ -x "$(command -v apt-get)" ]; then
        sudo apt-get update
        sudo apt-get install -y "$1"
    elif [ -x "$(command -v dnf)" ]; then
        sudo dnf install -y "$1"
    elif [ -x "$(command -v yum)" ]; then
        sudo yum install -y "$1"
    elif [ -x "$(command -v pacman)" ]; then
        sudo pacman -Sy --noconfirm "$1"
    else
        echo "Error: Unsupported package manager. Install '$1' manually."
        exit 1
    fi
}

if ! check_command tar; then
    echo "The 'tar' package is not installed. Installing..."
    install_package tar
fi

# URL of the tar file
URL="<https://git.rnp.br/redes-abertas/lab/-/archive/main/labs-main.tar?path=<lab-name>>"

# Name of the file to save
FILENAME="lab-main.tar"

# Directory where to unpack the files
DEST_DIR="./"

# Download the file
echo "Downloading $FILENAME..."
curl -L -o $FILENAME "$URL"

# Verify if the download was successful
if [ $? -ne 0 ]; then
    echo "Error downloading the file."
    exit 1
fi

# Unpack the file
echo "Unpacking $FILENAME..."
tar -xf $FILENAME -C $DEST_DIR --strip-components=1

# Verify if the unpacking was successful
if [ $? -ne 0 ]; then
    echo "Error unpacking the file."
    exit 1
fi

# Remove the tar file after unpacking
rm $FILENAME

echo "Download and unpacking completed successfully."

```

### Variables to Modify:

- **`URL`**: Change the URL to correspond to the repository and the path to the lab within GitLab.

---

### 2.2 `get.bat` Script

The `get.bat` script is used on Windows systems to download and unpack the lab in a similar way to `get.sh`, but with commands compatible with the Windows environment.

### `get.bat` Script:

```bat
@echo off
setlocal

REM URL of the tar file
set "URL=https://git.rnp.br/redes-abertas/docker-composes/-/archive/main/docker-composes-main.tar?path=<lab-name>"

REM Name of the file to save
set "FILENAME=lab-main.tar"

REM Directory where to unpack the files
set "DEST_DIR=."

echo Downloading %FILENAME%...
curl -L -o %FILENAME% %URL%

REM Verify if the download was successful
if not exist %FILENAME% (
    echo Error downloading the file.
    exit /b 1
)

echo Unpacking %FILENAME%...
tar -xf %FILENAME% -C %DEST_DIR% --strip-components=1

REM Verify if the unpacking was successful
if %errorlevel% neq 0 (
    echo Error unpacking the file.
    exit /b 1
)

REM Remove the tar file after unpacking
del %FILENAME%

echo Download and unpacking completed successfully.

endlocal
pause

```

### Variables to Modify:

- **`URL`**: Change the URL to the specific path of your lab in the GitLab repository.

---

## 3. Ensuring the Scripts are Correct

To ensure that the quick download process works correctly, **both scripts (get.sh and get.bat) must be included in the lab's folder within the lab repository**. This ensures that, when using the download links, users can download and unpack the lab efficiently, without any problems.

!!! tip "Tip"
    When including the scripts in GitLab, verify that the URLs are configured correctly with the names corresponding to the repository folder and the lab's name.

---

With these steps, you can effectively contribute to the lab documentation and ensure that all download links and scripts are working correctly without altering the documentation structure, adding anything new, or changing any links or references.