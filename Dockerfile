# Gaussian Splatting Pipeline Docker Image
# Ubuntu 22.04 + CUDA 12.1 + Python 3.11 + COLMAP 4.1+
FROM nvidia/cuda:12.1.0-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

# Install Python 3.11 from deadsnakes PPA
RUN apt-get update && apt-get install -y \
    software-properties-common \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update

# Install the version of cmake required by colmap
RUN apt-get update && apt-get install -y \
    gpg wget \
    && wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor -o /usr/share/keyrings/kitware-archive-keyring.gpg \
    && echo 'deb [signed-by=/usr/share/keyrings/kitware-archive-keyring.gpg] https://apt.kitware.com/ubuntu/ jammy main' | tee /etc/apt/sources.list.d/kitware.list >/dev/null \
    && apt-get update && apt-get install -y cmake

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
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
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    ffmpeg \
    wget \
    xvfb \
    libopenimageio-dev \
    openimageio-tools \
    libopenexr-dev \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Python 3.11 as default
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

# Install pip for Python 3.11
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.11 get-pip.py && \
    rm get-pip.py

# Install COLMAP 4.1+ (includes global mapper, formerly GLOMAP)
# Building from source to get latest version with global mapper
RUN git clone https://github.com/colmap/colmap.git /tmp/colmap && \
    cd /tmp/colmap && \
    git checkout main && \
    mkdir build && cd build && \
    cmake .. \
        -DCMAKE_CUDA_ARCHITECTURES="75;80;86;89;90" \
        -DCMAKE_BUILD_TYPE=Release && \
    make -j$(nproc) && \
    make install && \
    cd / && rm -rf /tmp/colmap

# Verify COLMAP installation and global mapper
RUN colmap -h && colmap global_mapper -h

# Install uv for fast Python package management (optional but recommended)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.cargo/bin/uv /usr/local/bin/

# Set up Python environment
WORKDIR /workspace
COPY pyproject.toml .
COPY requirements.txt .
COPY scripts/ ./scripts/

# Install PyTorch with CUDA support first
RUN pip3 install --no-cache-dir \
    torch torchvision torchaudio \
    --index-url https://download.pytorch.org/whl/cu121

# Install project dependencies from pyproject.toml
RUN pip3 install --no-cache-dir -e .

# Verify PyTorch CUDA
RUN python3 -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"

# Note: GraphDeco gaussian-splatting uses conda and is not included in Docker
# Use Brush for training instead (binaries can be mounted as volume)
# Or install manually if needed

# Set working directory to project
WORKDIR /workspace/project

# Create data directories
RUN mkdir -p data/input/videos data/processed/{frames,colmap} data/output/splats

# Expose ports (for visualization tools if needed)
EXPOSE 6006 8080

# Default command
CMD ["/bin/bash"]

# Image info
LABEL org.opencontainers.image.title="Gaussian Splatting Pipeline"
LABEL org.opencontainers.image.description="Ubuntu 22.04 + CUDA 12.1 + Python 3.11 + COLMAP 4.1+ for Gaussian Splatting"
LABEL org.opencontainers.image.version="2.0"
