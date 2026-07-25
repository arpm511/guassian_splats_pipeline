# Gaussian Splatting Pipeline for Blender

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete educational resource for creating 3D Gaussian Splats from video footage and visualizing them in Blender. This repository provides **two clear workflow paths** to accommodate different skill levels and use cases, making it easy for students and researchers to get started with Gaussian Splatting.

## Overview

This repository helps you create photorealistic 3D Gaussian Splats from video or images through **two workflow approaches**:

### **Path 1: SkySplat (Recommended for Beginners)**
An all-in-one Blender addon that automates the entire pipeline within Blender's familiar interface:
- Frame extraction, COLMAP processing, model transformation, and Brush training
- Visual, interactive workflow with minimal command-line work
- Perfect for learning and experimentation
- **Best for**: Students, artists, first-time users, quick prototyping

### **Path 2: Manual Pipeline (For Advanced Users)**
Full control over each step with Python scripts, Docker, and command-line tools:
- Customizable parameters at every stage
- Scriptable and automatable for batch processing
- Better for understanding the underlying technology
- **Best for**: Researchers, developers, production workflows, batch processing

Both paths produce the same high-quality results and can be visualized in Blender!

### What are Gaussian Splats?

Gaussian Splatting is a novel 3D representation technique that uses 3D Gaussians to represent scenes. Unlike traditional meshes or NeRF, Gaussian Splats offer:
- **Fast rendering** (real-time capable)
- **High quality** photorealistic reconstruction
- **Efficient training** compared to Neural Radiance Fields
- **Direct 3D editing** capabilities

## Table of Contents

- [Which Path Should I Choose?](#which-path-should-i-choose)
- [Requirements](#requirements)
- [Path 1: SkySplat Workflow](#path-1-skysplat-workflow-recommended-for-beginners)
  - [Installation](#skysplat-installation)
  - [Quick Start](#skysplat-quick-start)
  - [Complete Workflow](#skysplat-complete-workflow)
- [Path 2: Manual Pipeline](#path-2-manual-pipeline-for-advanced-users)
  - [Installation Options](#manual-pipeline-installation)
  - [Quick Start](#manual-quick-start)
  - [Detailed Workflow](#manual-detailed-workflow)
- [Video Capture Tips](#video-capture-tips)
- [Blender Visualization](#blender-visualization)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)
- [License](#license)

## Which Path Should I Choose?

| Feature | SkySplat (Path 1) | Manual Pipeline (Path 2) |
|---------|-------------------|--------------------------|
| **Ease of Use** | Visual UI | Command line |
| **Setup Time** | ~15 minutes | ~30-60 minutes |
| **Learning Curve** | Gentle | Steep |
| **Customization** | Limited to UI options | Full control |
| **Automation** | Multi-instance in Blender | Scriptable CLI |
| **Best For** | Learning, single scenes | Production, batches |

**Recommendation**: Start with SkySplat to understand the workflow, then move to the manual pipeline if you need more control or automation.

## Requirements

### Hardware Requirements
- **GPU**: NVIDIA GPU with CUDA support (8GB+ VRAM recommended)
  - GTX 1060 or better (Pascal architecture or newer)
- **RAM**: 16GB+ system RAM recommended (32GB+ for large scenes)
- **Storage**: 10GB+ free space per project (SSD recommended)

### Software Requirements

#### For Both Paths:
- **OS**: Ubuntu 22.04/24.04 or WSL2 Ubuntu (Windows users can use WSL)
- **GPU**: NVIDIA drivers (535+ recommended) and CUDA 12.1+
- **Blender**: 5.2 LTS (or 4.5 LTS minimum for compatibility)

#### Path-Specific:
- **SkySplat**: COLMAP 4.1+, Blender with SkySplat addon
- **Manual Pipeline**: Python 3.11, Docker (optional), uv (for Python env management)

> **Note**: This guide focuses on Linux/WSL Ubuntu. The tools are cross-platform, but setup instructions are optimized for Ubuntu to reduce complexity. Mac and native Windows users should adapt accordingly or use Docker.

---

# Path 1: SkySplat Workflow (Recommended for Beginners)

SkySplat is a comprehensive Blender addon that streamlines the complete workflow for creating 3D Gaussian Splats. Everything happens within Blender's familiar interface!

## SkySplat Installation

### 1. Install Blender

Download and install [Blender 5.2 LTS](https://www.blender.org/download/) (or 4.5 LTS minimum):

```bash
# Ubuntu - Download from website or use snap
sudo snap install blender --classic
```

### 2. Install COLMAP

COLMAP 4.1+ is required for Structure-from-Motion reconstruction.

**Ubuntu 22.04/24.04:**
```bash
# Option A: Install from Ubuntu repositories (may be older version)
sudo apt update
sudo apt install colmap

# Option B: Build from source (recommended for latest 4.1+)
sudo apt install -y git cmake build-essential libboost-all-dev \
    libeigen3-dev libsuitesparse-dev libfreeimage-dev \
    libmetis-dev libgoogle-glog-dev libgflags-dev \
    libglew-dev qtbase5-dev libqt5opengl5-dev libcgal-dev \
    libceres-dev

git clone https://github.com/colmap/colmap.git
cd colmap
mkdir build && cd build
cmake .. -DCMAKE_CUDA_ARCHITECTURES=native
make -j$(nproc)
sudo make install

# Verify installation
colmap -h
```

> **Note**: GLOMAP functionality is now built into COLMAP 4.0+ as the `global_mapper` command. No separate GLOMAP installation needed!

### 3. Install SkySplat Addon

1. **Download the latest release**:
   - Visit [SkySplat Releases](https://github.com/kyjohnso/skysplat_blender/releases/latest)
   - Download the `.zip` file (e.g., `skysplat_blender-v0.4.2.zip`)

2. **Install in Blender**:
   - Open Blender
   - Go to `Edit` → `Preferences` → `Add-ons`
   - Click `Install...` and select the downloaded ZIP file
   - Enable the addon by checking the box next to "3D View: SkySplat: 3DGS Blender Toolkit"

3. **Configure Brush executable** (bundled with addon):
   
   On Linux, make the Brush binary executable:
   ```bash
   cd ~/.config/blender/5.2/scripts/addons/skysplat_blender/binaries/
   chmod +x brush_app_linux
   ```

4. **Access SkySplat**:
   - In Blender's 3D View, press `N` to open the sidebar
   - Click the `SkySplat` tab

**That's it!** You're ready to create Gaussian Splats in Blender.

## SkySplat Quick Start

### Basic Workflow (5 Steps)

1. **Load Video** → Import your video, extract frames
2. **Run COLMAP** → Reconstruct camera poses and 3D points
3. **Transform Model** → Align and scale in Blender 3D view
4. **Train Splat** → Run Brush training with visual progress
5. **Visualize** → Import PLY into Blender with KIRI 3DGS addon

### Example: Process Your First Scene

```bash
# 1. Prepare your video
# Place video in a known location, e.g., ~/Videos/my_scene.mp4
```

**In Blender with SkySplat:**

1. **Video Panel**:
   - Click `+` to add a video instance
   - Browse to your video file
   - Click `Load Video and SRT`
   - Adjust frame range if needed
   - Click `Extract Frames` (frames saved to auto-generated path)

2. **COLMAP Panel**:
   - Click `+` to add a COLMAP instance
   - Click the 🔗 (chain link icon) to link with video instance
   - Select camera model (OPENCV for most cameras)
   - Click `Run COLMAP` (this takes 10-30 mins)
   - Monitor progress in Blender's terminal/console

3. **Transform Panel**:
   - Click `Load COLMAP Model` (cameras and points appear in 3D view)
   - Transform the `COLMAP_Root` object (scale/rotate/translate)
   - Click `Export Transformed Model` when aligned

4. **Brush (3DGS) Panel**:
   - Click `Prepare Brush Dataset`
   - Click `+` to add a Splat instance
   - Configure training iterations (7000 for preview, 30000 for quality)
   - Click `Run Brush Training`
   - Wait for training (10-60 mins depending on iterations)

5. **Visualize**:
   - Install KIRI 3DGS Render addon (see [Blender Visualization](#blender-visualization))
   - Import the trained `.ply` file
   - Render in viewport or final render!

## SkySplat Complete Workflow

For detailed instructions, parameter explanations, and troubleshooting, see the [SkySplat GitHub repository](https://github.com/kyjohnso/skysplat_blender). Key features:

- **Multi-Instance Workflow**: Process multiple videos in one .blend file without conflicts
- **Camera Animation**: Auto-generate animated cameras from COLMAP poses
- **Real-time Monitoring**: See training progress in Blender console
- **Integrated Tools**: Brush binaries included for all platforms

**Benefits:**
- No command-line Python environment setup needed
- Visual feedback at every step
- Perfect for learning the pipeline
- Great for single scenes and experimentation

---

# Path 2: Manual Pipeline (For Advanced Users)

The manual pipeline gives you full control over each step with Python scripts, custom parameters, and optional Docker containerization.

## Manual Pipeline Installation

Choose between Docker (easiest) or local installation (more flexible).

### Option 1: Docker (Recommended for Manual Pipeline)

Docker provides a pre-configured environment with all dependencies.

**Prerequisites:**
```bash
# Install Docker Engine
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in for group changes

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
    sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Verify GPU access
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

**Build and run:**
```bash
git clone https://github.com/arpm511/gaussian-splats.git
cd gaussian-splats
docker-compose build
docker-compose up -d
docker-compose exec gaussian-splatting /bin/bash
```

### Option 2: Local Installation with uv (Recommended)

**Why uv?** Manages Python versions and dependencies in isolated environments, preventing conflicts with other projects.

#### Step 1: Install System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install CUDA (if not already installed)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get install -y cuda-toolkit-12-1

# Verify
nvidia-smi
nvcc --version

# Install COLMAP dependencies and build from source
sudo apt install -y git cmake build-essential libboost-all-dev \
    libeigen3-dev libsuitesparse-dev libfreeimage-dev \
    libmetis-dev libgoogle-glog-dev libgflags-dev \
    libglew-dev qtbase5-dev libqt5opengl5-dev libcgal-dev \
    libceres-dev ffmpeg

# Build COLMAP 4.1+ (includes GLOMAP functionality)
git clone https://github.com/colmap/colmap.git
cd colmap
mkdir build && cd build
cmake .. -DCMAKE_CUDA_ARCHITECTURES=native
make -j$(nproc)
sudo make install
cd ../..

# Verify COLMAP installation
colmap -h
colmap mapper -h  # Traditional incremental mapper
colmap global_mapper -h  # GLOMAP's global mapper (faster)
```

#### Step 2: Install uv and Setup Python Environment

```bash
# Install uv (fast Python package installer)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env  # Add uv to PATH

# Clone this repository
git clone https://github.com/arpm511/guassian_splats_pipeline.git
cd gaussian-splats

# Create Python 3.11 environment with uv
uv venv --python 3.11
source .venv/bin/activate

# Install PyTorch with CUDA support
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install project dependencies from pyproject.toml
uv pip install -e .

# Verify PyTorch CUDA
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

#### Step 3: Install Brush for Training

Brush is a fast, modern Gaussian Splatting trainer with both GUI and CLI:

```bash
# Option 1: Download pre-built binaries (easiest)
# Visit https://github.com/ArthurBrussee/brush/releases
# Download for your platform and make executable:
chmod +x brush_app
sudo mv brush_app /usr/local/bin/  # Or keep in project directory

# Option 2: Build from source (requires Rust)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
git clone https://github.com/ArthurBrussee/brush.git
cd brush
cargo build --release
# Executable: target/release/brush_app
sudo cp target/release/brush_app /usr/local/bin/  # Optional: install globally
cd ..

# Verify installation
brush_app --version
```

> **Note**: If you need the original GraphDeco implementation for research purposes, it requires conda and a separate environment. See the [GraphDeco repository](https://github.com/graphdeco-inria/gaussian-splatting) for installation instructions.

### Quick Environment Check

```bash
# Activate environment
source .venv/bin/activate  # if using uv
# or
docker-compose exec gaussian-splatting /bin/bash  # if using Docker

# Run environment check
python scripts/check_environment.py
```

This script verifies:
- CUDA/GPU availability
- COLMAP installation  
- Python packages
- Directory structure

## Manual Quick Start

### Using the Automated Pipeline Script

**Linux:**
```bash
source .venv/bin/activate  # Activate your uv environment
./scripts/pipeline.sh data/input/videos/your_video.mp4 my_project
```

This automated script will:
1. Extract frames from your video
2. Run COLMAP reconstruction (with global mapper option)
3. Train the Gaussian Splatting model with Brush
4. Export PLY file for Blender

### Manual Step-by-Step

For more control over parameters:

```bash
# Activate environment
source .venv/bin/activate

# 1. Extract frames
python scripts/extract_frames.py data/input/videos/scene.mp4 \
    --output_dir data/processed/frames/scene \
    --fps 2 \
    --quality 95

# 2. Run COLMAP with global mapper (faster, was GLOMAP)
python scripts/run_colmap.py \
    --images_dir data/processed/frames/scene \
    --output_dir data/processed/colmap/scene \
    --camera_model OPENCV \
    --use_global_mapper \
    --quality high

# 3. Train with Brush (or use gaussian-splatting repo)
# Using Brush CLI (recommended):
brush_app train \
    --data data/processed/colmap/scene \
    --output data/output/splats/scene \
    --iterations 30000
```

## Manual Detailed Workflow

### Step 1: Frame Extraction

Extract frames from your video with customizable parameters:

```bash
python scripts/extract_frames.py <video_path> \
    --output_dir data/processed/frames/<project_name> \
    --fps 2 \
    --max_frames 300 \
    --quality 95 \
    --start_time 0 \
    --end_time 60
```

**Parameters:**
- `--fps`: Frames per second to extract (lower = fewer frames, faster processing)
- `--max_frames`: Maximum number of frames to extract
- `--quality`: JPEG quality (0-100, higher = better quality, larger files)
- `--start_time`/`--end_time`: Extract specific video segment (in seconds)

**Recommendations:**
- For static scenes: 1-2 FPS (100-200 frames)
- For dynamic scenes: 2-5 FPS (200-300 frames)
- Aim for 100-300 frames total for best results

### Step 2: COLMAP Reconstruction

COLMAP 4.0+ includes the global mapper (formerly GLOMAP) for fast reconstruction:

```bash
python scripts/run_colmap.py \
    --images_dir data/processed/frames/<project_name> \
    --output_dir data/processed/colmap/<project_name> \
    --camera_model OPENCV \
    --quality high \
    --use_global_mapper  # Use global SfM (faster, was GLOMAP)
```

**Parameters:**
- `--camera_model`: Camera model (OPENCV, PINHOLE, SIMPLE_RADIAL)
- `--quality`: Processing quality (high, medium, low)
  - `high`: 4096px max, 8192 features (best quality, slower)
  - `medium`: 2048px max, 4096 features (balanced)
  - `low`: 1024px max, 2048 features (fastest)
- `--use_global_mapper`: Use global SfM (recommended, 10-50x faster)
- `--no_gpu`: Disable GPU acceleration

**Understanding COLMAP Mappers:**

COLMAP 4.0+ offers two reconstruction approaches:

1. **Global Mapper** (recommended, was GLOMAP):
   ```bash
   --use_global_mapper
   ```
   - 10-50x faster than incremental
   - Better for drone footage and large scenes
   - Requires more RAM

2. **Incremental Mapper** (traditional):
   ```bash
   # Default if --use_global_mapper not specified
   ```
   - More robust for challenging cases
   - Works with lower RAM
   - Slower but very reliable

**Processing Time:**
- 100 images: 5-15 minutes (global) or 20-45 minutes (incremental)
- 200 images: 10-30 minutes (global) or 45-90 minutes (incremental)
- GPU accelerates feature extraction and matching

### Step 3: Gaussian Splatting Training

Train using Brush for fast, high-quality results:

**Interactive GUI:**
```bash
# Launch Brush GUI
brush_app
# Load data/processed/colmap/<project_name> using File menu
# Configure training parameters visually
# Monitor training progress in real-time
```

**Command Line:**
```bash
brush_app train \
    --data data/processed/colmap/<project_name> \
    --output data/output/splats/<project_name> \
    --iterations 30000 \
    --eval  # Enable validation during training
```

**Training Parameters:**
- `--iterations`: Total training steps
  - 7,000: Quick preview (~10-15 mins)
  - 15,000: Good quality (~20-30 mins)
  - 30,000: High quality (~40-60 mins)
- `--resolution`: Downscale factor (1=full, 2=half, 4=quarter)

**Training Tips:**
- Start with 7,000 iterations to verify the reconstruction looks correct
- Use lower resolution (`--resolution 2`) for faster iteration
- Monitor GPU memory usage with `nvidia-smi`
- Expect 4-8GB VRAM usage depending on scene complexity

---

## Video Capture Tips

For best reconstruction results, follow these guidelines when capturing footage:

### Camera Movement
- **Move slowly and smoothly** - avoid jerky movements
- **Maintain consistent speed** - helps with motion blur
- **Overlap significantly** - 70-80% overlap between frames
- **Capture from multiple angles** - 360° coverage when possible
- **Avoid pure rotation** - include translation for better depth perception

### Scene Conditions
- **Consistent lighting** - avoid changing light conditions during capture
- **Avoid moving objects** - people, cars, animals create artifacts
- **Well-textured surfaces** - plain walls are difficult to reconstruct
- **Good contrast** - avoid overexposed or underexposed areas
- **Stable camera** - use gimbal or steady hands

### Technical Settings
- **Resolution**: 1080p minimum, 4K preferred
- **Frame rate**: 30fps or 60fps
- **Duration**: 30-60 seconds typically sufficient
- **Shutter speed**: Match frame rate to reduce motion blur
- **Focus**: Lock focus, avoid autofocus hunting

### Scene Types

| Scene Type | FPS to Extract | Total Frames | Notes |
|------------|----------------|--------------|-------|
| Small object | 2-5 | 100-200 | Rotate around object |
| Room interior | 1-2 | 150-250 | Walk through slowly |
| Building exterior | 1-2 | 200-300 | Circle building |
| Landscape | 1-3 | 200-400 | Drone or walking path |

---

## Blender Visualization

Both workflow paths produce `.ply` files that can be visualized in Blender using the KIRI 3DGS Render addon.

### Install KIRI 3DGS Render Addon

1. **Download the addon**:
   - Visit [KIRI 3DGS Render Releases](https://github.com/Kiri-Innovation/3dgs-render-blender-addon/releases)
   - Download the latest `.zip` file compatible with your Blender version
   - Blender 5.2 LTS: Use latest release
   - Blender 4.5 LTS: Check compatibility notes

2. **Install in Blender**:
   ```
   Blender → Edit → Preferences → Add-ons → Install...
   ```
   - Select the downloaded ZIP file
   - Enable "Render: 3DGS Render" addon

3. **Verify installation**:
   - Press `N` in 3D View to open sidebar
   - Look for "3DGS Render" tab

### Import and Visualize Gaussian Splat

1. **Open Blender** (5.2 LTS or 4.5 LTS)

2. **Import PLY file**:
   - Open the `3DGS Render` panel (press `N`, select tab)
   - Click `Import PLY`
   - Navigate to your splat file:
     - **SkySplat**: Check addon's export path
     - **Manual**: `data/output/splats/<project>/point_cloud.ply`
   - Click `Import PLY`

3. **View in viewport**:
   - Switch viewport shading to `Rendered` mode (press `Z` → Rendered)
   - The Gaussian Splat will render in real-time
   - Navigate with mouse/keyboard as usual

4. **Adjust settings**:
   - In the 3DGS Render panel:
     - **Splat Scale**: Adjust point sizes
     - **Opacity**: Control transparency
     - **Quality**: Set rendering quality

5. **Render output**:
   - Set up camera (`Add` → `Camera`)
   - Configure render settings
   - Render image: `F12`
   - Render animation: `Ctrl+F12`

### Tips for Best Results
- **Lighting**: Gaussian Splats are pre-lit, but can be combined with Blender lights
- **Compositing**: Use compositor to add effects, color grading
- **Animation**: Animate camera around splat for turntable renders
- **Scale**: Adjust imported splat scale to match Blender scene units
- **Performance**: Large splats may be slow in viewport - use lower quality preview

---

## Project Structure

```
gaussian_splats_pipeline/
├── data/
│   ├── input/
│   │   ├── videos/              # Input video files
│   │   └── images/              # Or input image sequences
│   ├── processed/
│   │   ├── frames/              # Extracted video frames
│   │   │   └── <project_name>/
│   │   └── colmap/              # COLMAP reconstruction output
│   │       └── <project_name>/
│   │           ├── database.db  # Feature database
│   │           └── sparse/      # Sparse 3D reconstruction
│   │               └── 0/       # Reconstruction model
│   └── output/
│       └── splats/              # Trained Gaussian Splat models
│           └── <project_name>/
│               └── point_cloud.ply
├── scripts/
│   ├── extract_frames.py        # Video → frames
│   ├── run_colmap.py            # Frames → COLMAP reconstruction
│   ├── train_gaussian_splat.py  # Training wrapper (legacy)
│   ├── pipeline.sh              # Complete automated pipeline
│   └── check_environment.py     # Verify setup
├── docs/
│   ├── BLENDER_GUIDE.md         # Detailed Blender instructions
│   ├── BRUSH_GUIDE.md           # Brush training guide
│   └── images/                  # Documentation images
├── docker/
│   ├── Dockerfile               # Docker image definition
│   ├── docker-compose.yml       # Docker Compose config
│   └── README.md                # Docker setup guide
├── requirements.txt             # Python dependencies (legacy, see pyproject.toml)
├── pyproject.toml               # Modern Python project config (use with uv)
├── .gitignore
├── LICENSE
└── README.md                    # This file
```

### Directory Management

**SkySplat users**: The addon manages paths automatically. Check addon settings for output locations.

**Manual pipeline users**: 
- Organize by project name for clarity
- Use consistent naming: `data/{input,processed,output}/<project_name>/`
- The automated script (`pipeline.sh`) creates directories automatically

---

## Troubleshooting

### Common Issues

#### 1. CUDA/GPU Not Detected

```bash
# Check NVIDIA driver
nvidia-smi

# Check CUDA installation
nvcc --version

# Test PyTorch CUDA
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"

# Docker: Test GPU access
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

**Solutions:**
- Update NVIDIA drivers: `sudo ubuntu-drivers autoinstall`
- Reinstall CUDA toolkit
- Verify Docker can access GPU with `--gpus all` flag

#### 2. COLMAP Fails to Reconstruct

**Symptoms**: No sparse reconstruction, empty output directory, or very few cameras

**Common causes and solutions:**
- **Insufficient overlap**: Ensure 70%+ overlap between consecutive frames
- **Poor image quality**: Check for motion blur, low light, or overexposure
- **Textureless scenes**: Add more visual features, avoid plain white walls
- **Wrong camera model**: Try `SIMPLE_RADIAL` instead of `OPENCV`

**Troubleshooting steps:**
```bash
# Try with lower quality first (faster debug)
python scripts/run_colmap.py --images_dir ... --quality low

# Use incremental mapper instead of global
python scripts/run_colmap.py --images_dir ... # omit --use_global_mapper

# Reduce feature count for difficult scenes
python scripts/run_colmap.py --images_dir ... --quality medium
```

#### 3. Training Crashes (Out of Memory)

**Error**: `CUDA out of memory` or process killed

**Solutions:**
- **Reduce resolution**: Use `--resolution 2` or `--resolution 4`
- **Reduce frame count**: Use fewer images (150-200 instead of 300)
- **Close other applications**: Free up GPU memory
- **Monitor usage**: Watch `nvidia-smi` during training
- **Use gradient checkpointing**: Some implementations support this

#### 4. SkySplat Issues

**Brush binary not executable (Linux):**
```bash
cd ~/.config/blender/5.2/scripts/addons/skysplat_blender/binaries/
chmod +x brush_app_linux
```

**COLMAP not found:**
- Ensure COLMAP is in PATH: `which colmap`
- In SkySplat UI, manually specify COLMAP executable path

**Addon not appearing:**
- Ensure Blender 4.0+
- Check addon is enabled in Preferences
- Restart Blender after installation

#### 5. uv Environment Issues

**uv command not found:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

**Wrong Python version:**
```bash
# Force Python 3.11
uv venv --python 3.11 --force
source .venv/bin/activate
python --version  # Should show 3.11.x
```

**Package conflicts:**
```bash
# Clean install
rm -rf .venv
uv venv --python 3.11
source .venv/bin/activate
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
uv pip install -e .
```

#### 6. Blender Visualization Issues

**PLY file won't import:**
- Verify file exists and isn't corrupted
- Check file size (should be > 1MB for typical scenes)
- Ensure KIRI 3DGS addon is enabled
- Try reimporting after restarting Blender

**Rendering is slow:**
- Reduce splat quality in 3DGS Render panel
- Use smaller viewport resolution
- Update GPU drivers

**Splat looks wrong:**
- Check scale - may need to adjust import scale
- Verify training completed successfully
- Ensure COLMAP reconstruction was good (check camera poses)

### Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/arpm511/gaussian-splats/issues)
- **Discussions**: [Ask questions and share results](https://github.com/arpm511/gaussian-splats/discussions)
- **SkySplat**: [SkySplat Issues](https://github.com/kyjohnso/skysplat_blender/issues) for addon-specific questions
- **COLMAP**: [COLMAP Discussions](https://github.com/colmap/colmap/discussions) for reconstruction issues

### Performance Tips

**Speed up reconstruction:**
- Use `--use_global_mapper` (10-50x faster than incremental)
- Reduce image resolution: `--quality medium` or `--quality low`
- Use fewer frames (150-200 is often sufficient)
- Enable GPU: ensure `--no_gpu` is NOT set

**Speed up training:**
- Start with 7000 iterations for preview
- Use `--resolution 2` to downscale images  
- Brush offers excellent GPU utilization and fast training
- Monitor GPU with `nvidia-smi` - ensure high utilization

**Optimize quality:**
- More frames = better coverage (but diminishing returns after ~300)
- Higher iterations = better detail (30000 is usually enough)
- Full resolution training gives best results (but slower)
- Good COLMAP reconstruction is critical - check sparse points before training

---

## Credits

This project builds upon amazing work from the research and open-source community:

### Core Technologies
- **Gaussian Splatting**: [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) by Inria
- **COLMAP**: [Structure-from-Motion and Multi-View Stereo](https://colmap.github.io/) - Essential SfM pipeline
- **GLOMAP** (now integrated): [Global Structure-from-Motion Revisited](https://github.com/colmap/glomap) - Fast global mapper
- **Brush**: [Interactive Gaussian Splatting](https://github.com/ArthurBrussee/brush) by Arthur Brussee
- **SkySplat**: [All-in-one Blender Pipeline](https://github.com/kyjohnso/skysplat_blender) by Kyle Johnson

### Visualization
- **KIRI 3DGS Render**: [Blender Gaussian Splat Renderer](https://github.com/Kiri-Innovation/3dgs-render-blender-addon)
- **Blender**: [Open Source 3D Creation Suite](https://www.blender.org/)

### Inspiration & Learning Resources
- [nicko16's YouTube Tutorial](https://www.youtube.com/watch?v=A1T9uJtq0cI) - Excellent walkthrough
- [RedShot AI 3DGS Tutorial](https://www.reshot.ai/3d-gaussian-splatting) - Comprehensive guide

### Citations

If you use this repository or Gaussian Splatting in your research, please cite:

```bibtex
@inproceedings{kerbl3Dgaussians,
  title={3D Gaussian Splatting for Real-Time Radiance Field Rendering},
  author={Kerbl, Bernhard and Kopanas, Georgios and Leimk{\"u}hler, Thomas and Drettakis, George},
  booktitle={ACM Transactions on Graphics},
  volume={42},
  number={4},
  year={2023}
}

@inproceedings{schoenberger2016sfm,
  title={Structure-from-Motion Revisited},
  author={Sch\"{o}nberger, Johannes Lutz and Frahm, Jan-Michael},
  booktitle={CVPR},
  year={2016}
}

@inproceedings{pan2024glomap,
  title={{Global Structure-from-Motion Revisited}},
  author={Pan, Linfei and Barath, Daniel and Pollefeys, Marc and Sch\"{o}nberger, Johannes Lutz},
  booktitle={ECCV},
  year={2024}
}
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Note**: This repository contains educational scripts and documentation. The actual reconstruction and training tools (COLMAP, Brush, gaussian-splatting) have their own licenses:
- COLMAP: BSD License
- Brush: Apache 2.0 License
- gaussian-splatting: Inria and Max Planck Gesellschaft license

---

## Contact & Support

**Maintainer**: [@arpm511](https://github.com/arpm511)  
**Email**: arpm511@gmail.com

### Getting Help

- **Documentation**: Read this README and docs/ folder first
- **Discussions**: [GitHub Discussions](https://github.com/arpm511/gaussian-splats/discussions) for questions
- **Bug Reports**: [GitHub Issues](https://github.com/arpm511/gaussian-splats/issues) for bugs
- **Show Support**: Star the repository if you find it helpful!

---

## Acknowledgments

This repository was created as an educational resource to lower the barrier to entry for Gaussian Splatting. The goal is to help students, researchers, and artists quickly get started without spending days on environment setup.

Special thanks to:
- The COLMAP team for reliable SfM software
- Arthur Brussee for the excellent Brush training tool
- Kyle Johnson for the SkySplat Blender addon
- The Inria GraphDeco team for pioneering 3D Gaussian Splatting
- The open-source community for continuous improvements

**Your feedback helps improve this resource!** If you found issues or have suggestions, please open an issue or discussion.

---

<div align="center">

**⭐ If this repository helped you, please consider giving it a star! ⭐**

*Making Gaussian Splatting accessible to everyone, one splat at a time.*

</div>
