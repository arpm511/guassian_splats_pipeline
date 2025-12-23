# Docker Setup Guide

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- NVIDIA GPU with CUDA support
- NVIDIA Docker runtime ([nvidia-docker2](https://github.com/NVIDIA/nvidia-docker))

## Installation

### Windows

#### Option 1: Docker Desktop (Easier, but requires subscription for some use cases)

1. Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)
2. Install [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html)
3. Enable WSL2 backend in Docker Desktop settings

#### Option 2: Docker CLI via WSL2 (Free and Open Source)

1. **Install WSL2**
   ```powershell
   # Run in PowerShell as Administrator
   wsl --install
   # Restart your computer if prompted
   ```

2. **Install Docker Engine in WSL2**
   ```bash
   # Inside WSL2 Ubuntu terminal
   # Update package list
   sudo apt-get update
   
   # Install dependencies
   sudo apt-get install -y ca-certificates curl gnupg lsb-release
   
   # Add Docker's official GPG key
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   
   # Set up repository
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   
   # Install Docker Engine
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   
   # Start Docker service
   sudo service docker start
   
   # Add your user to docker group
   sudo usermod -aG docker $USER
   newgrp docker
   ```

3. **Install NVIDIA Container Toolkit**
   ```bash
   # Inside WSL2
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
   curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
   sudo apt-get update && sudo apt-get install -y nvidia-docker2
   sudo service docker restart
   ```

4. **Verify Installation**
   ```bash
   # Test Docker
   docker run hello-world
   
   # Test NVIDIA support
   docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
   ```

### Linux

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update && sudo apt-get install -y nvidia-docker2
sudo systemctl restart docker
```

## Building and Running

```bash
# Build the Docker image
docker-compose build

# Start the container
docker-compose up -d

# Access the container shell
docker-compose exec gaussian-splatting /bin/bash

# Stop the container
docker-compose down
```

## Troubleshooting

- **GPU not detected**: Ensure NVIDIA drivers are installed and `nvidia-smi` works
- **Build errors**: Check CUDA version compatibility with your GPU
- **Permission issues**: Add your user to the docker group: `sudo usermod -aG docker $USER`
