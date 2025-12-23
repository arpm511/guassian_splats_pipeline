# Gaussian Splatting Environment Dockerfile
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    cmake \
    build-essential \
    libboost-program-options-dev \
    libboost-filesystem-dev \
    libboost-graph-dev \
    libboost-system-dev \
    libeigen3-dev \
    libflann-dev \
    libfreeimage-dev \
    libmetis-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libsqlite3-dev \
    libglew-dev \
    qtbase5-dev \
    libqt5opengl5-dev \
    libcgal-dev \
    libceres-dev \
    python3.10 \
    python3-pip \
    python3-dev \
    ffmpeg \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install COLMAP
RUN git clone https://github.com/colmap/colmap.git /tmp/colmap && \
    cd /tmp/colmap && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_CUDA_ARCHITECTURES=native && \
    make -j$(nproc) && \
    make install && \
    rm -rf /tmp/colmap

# Install GLOMAP (faster reconstruction than COLMAP)
RUN git clone https://github.com/colmap/glomap.git /tmp/glomap && \
    cd /tmp/glomap && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_CUDA_ARCHITECTURES=native && \
    make -j$(nproc) && \
    make install && \
    rm -rf /tmp/glomap

# Set up Python environment
WORKDIR /workspace
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install PyTorch with CUDA support
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Clone and setup Gaussian Splatting repository
RUN git clone https://github.com/graphdeco-inria/gaussian-splatting /workspace/gaussian-splatting --recursive

# Install Gaussian Splatting dependencies
WORKDIR /workspace/gaussian-splatting
RUN pip3 install -r requirements.txt

# Set working directory back to main workspace
WORKDIR /workspace/project

# Expose port for viewers if needed
EXPOSE 6006

CMD ["/bin/bash"]
