# Gaussian Splatting Pipeline for Blender

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A complete end-to-end pipeline for creating Gaussian Splats from video footage and visualizing them in Blender. This project demonstrates the full workflow from video capture to 3D reconstruction using state-of-the-art Gaussian Splatting technology.

![Pipeline Overview](docs/images/pipeline_overview.png)
<!-- TODO: Add pipeline overview diagram -->

## 🎯 Overview

This repository provides a streamlined workflow for:
1. **Video Processing**: Extract frames from video footage
2. **Structure-from-Motion**: Use COLMAP for feature extraction and GLOMAP for fast reconstruction
3. **Gaussian Splatting**: Train with Brush (interactive GUI) or command-line tools
4. **Blender Visualization**: Import and render the Gaussian Splat in Blender with Kiri 3DGS addon

### What are Gaussian Splats?

Gaussian Splatting is a novel 3D representation technique that uses 3D Gaussians to represent scenes. Unlike traditional meshes or NeRF, Gaussian Splats offer:
- **Fast rendering** (real-time capable)
- **High quality** photorealistic reconstruction
- **Efficient training** compared to Neural Radiance Fields
- **Direct 3D editing** capabilities

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Option 1: Docker (Recommended)](#option-1-docker-recommended)
  - [Option 2: Local Installation](#option-2-local-installation)
- [Quick Start](#quick-start)
- [Detailed Workflow](#detailed-workflow)
  - [Step 1: Video Capture](#step-1-video-capture)
  - [Step 2: Frame Extraction](#step-2-frame-extraction)
  - [Step 3: COLMAP Reconstruction](#step-3-colmap-reconstruction)
  - [Step 4: Gaussian Splatting Training](#step-4-gaussian-splatting-training)
    - [Option A: Brush (Interactive GUI)](#option-a-brush-interactive-gui)
    - [Option B: Command-Line Training](#option-b-command-line-training)
  - [Step 5: Blender Visualization](#step-5-blender-visualization)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Credits](#credits)
- [License](#license)

## ✨ Features

- **Automated Pipeline**: Complete scripts for end-to-end processing
- **GLOMAP Integration**: Faster reconstruction than traditional COLMAP (10-50x speedup)
- **Multiple Training Options**: Choose between Brush GUI (interactive) or CLI (automated)
- **Docker Support**: Pre-configured Docker environment with all dependencies
- **CPU Support**: Alternative setup for systems without NVIDIA GPU
- **Flexible Input**: Works with video files or image sequences
- **Quality Controls**: Adjustable settings for speed vs. quality tradeoffs
- **Blender Integration**: Ready-to-import PLY files for 3D visualization with Kiri 3DGS addon
- **Well Documented**: Comprehensive guides with images and examples

## 📦 Requirements

### Hardware Requirements
- **GPU**: NVIDIA GPU with CUDA support (8GB+ VRAM recommended)
  - *CPU-only option available* - see [CPU Setup Guide](docs/CPU_SETUP.md)
- **RAM**: 16GB+ system RAM recommended
- **Storage**: 10GB+ free space per project

### Software Requirements
- **Docker** (recommended) OR
- **CUDA 12.1+** with compatible drivers (for GPU)
- **Python 3.10+**
- **COLMAP 3.8+** and **GLOMAP** (latest)
- **Blender 4.5+** (for visualization, 4.2+ compatible)

## 🚀 Installation

### Option 1: Docker (Recommended)

Docker provides the easiest setup with all dependencies pre-configured.

**For GPU systems (NVIDIA CUDA):**

1. **Install Docker Desktop**
   - Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Linux: [Docker Engine](https://docs.docker.com/engine/install/)

2. **Install NVIDIA Container Toolkit**
   ```bash
   # Ubuntu/Debian
   distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
   curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
   curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
       sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
       sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
   sudo apt-get update
   sudo apt-get install -y nvidia-container-toolkit
   sudo systemctl restart docker
   ```

3. **Clone and Build**
   ```bash
   git clone https://github.com/arpm511/gaussian-splats.git
   cd gaussian-splats
   docker-compose build
   docker-compose up -d
   docker-compose exec gaussian-splatting /bin/bash
   ```

**For CPU-only systems (no NVIDIA GPU):**
```bash
# Build CPU-only Docker image
docker-compose -f docker-compose-cpu.yml build
docker-compose -f docker-compose-cpu.yml up -d
docker-compose -f docker-compose-cpu.yml exec gaussian-splatting-cpu /bin/bash
```

**Note**: CPU processing is significantly slower. See [CPU Setup Guide](docs/CPU_SETUP.md) for details and optimization tips.

See [docker/README.md](docker/README.md) for detailed Docker setup instructions including Docker CLI (free alternative to Docker Desktop).

### Option 2: Local Installation

<details>
<summary>Click to expand local installation instructions</summary>

#### Install CUDA and Drivers

1. Install [NVIDIA CUDA Toolkit 12.1](https://developer.nvidia.com/cuda-downloads)
2. Verify installation: `nvidia-smi`

#### Install COLMAP

**Ubuntu/Debian:**
```bash
sudo apt-get install \
    git cmake build-essential libboost-all-dev \
    libeigen3-dev libsuitesparse-dev libfreeimage-dev \
    libmetis-dev libgoogle-glog-dev libgflags-dev \
    libglew-dev qtbase5-dev libqt5opengl5-dev libcgal-dev \
    libceres-dev

git clone https://github.com/colmap/colmap.git
cd colmap
mkdir build && cd build
cmake .. -DCMAKE_CUDA_ARCHITECTURES=native
make -j
sudo make install
```

**Windows:**
Download pre-built binaries from [COLMAP Releases](https://github.com/colmap/colmap/releases)

#### Install GLOMAP (for faster reconstruction)

**Ubuntu/Debian:**
```bash
git clone https://github.com/colmap/glomap.git
cd glomap
mkdir build && cd build
cmake .. -DCMAKE_CUDA_ARCHITECTURES=native
make -j
sudo make install
```

**Windows:**
Download pre-built binaries from [GLOMAP Releases](https://github.com/colmap/glomap/releases)

**Note**: GLOMAP is optional but recommended - it's 10-50x faster than COLMAP's mapper for reconstruction.

#### Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install other requirements
pip install -r requirements.txt
```

#### Install Gaussian Splatting

```bash
git clone https://github.com/graphdeco-inria/gaussian-splatting --recursive
cd gaussian-splatting
pip install -r requirements.txt
```

</details>

## 🎬 Quick Start

### Using the Automated Pipeline

**Linux/Mac:**
```bash
./scripts/pipeline.sh data/input/videos/your_video.mp4 my_project
```

**Windows (PowerShell):**
```powershell
.\scripts\pipeline.ps1 -VideoPath "data\input\videos\your_video.mp4" -ProjectName "my_project"
```

This will automatically:
1. Extract frames from your video
2. Run COLMAP reconstruction
3. Train the Gaussian Splatting model
4. Export PLY file for Blender

### Manual Step-by-Step

If you prefer more control, run each step individually:

```bash
# 1. Extract frames
python scripts/extract_frames.py data/input/videos/scene.mp4 \
    --output_dir data/processed/frames/scene \
    --fps 2

# 2. Run COLMAP
python scripts/run_colmap.py \
    --images_dir data/processed/frames/scene \
    --output_dir data/processed/colmap/scene

# 3. Train Gaussian Splat
python scripts/train_gaussian_splat.py \
    --source_path data/processed/colmap/scene \
    --model_path data/output/splats/scene \
    --iterations 30000 \
    --export_ply data/output/splats/scene/point_cloud.ply
```

## 📖 Detailed Workflow

### Step 1: Video Capture

For best results when capturing video:
- **Movement**: Move slowly and smoothly around the object/scene
- **Coverage**: Capture from multiple angles (360° if possible)
- **Lighting**: Use consistent, even lighting
- **Duration**: 30-60 seconds of footage is usually sufficient
- **Resolution**: 1080p or higher
- **Frame Rate**: 30fps or 60fps

![Video Capture Tips](docs/images/video_capture_tips.png)
<!-- TODO: Add video capture best practices image/gif -->

### Step 2: Frame Extraction

Extract frames from your video:

```bash
python scripts/extract_frames.py <video_path> \
    --output_dir data/processed/frames/<project_name> \
    --fps 2 \
    --max_frames 300 \
    --quality 95
```

**Parameters:**
- `--fps`: Frames per second to extract (lower = fewer frames, faster processing)
- `--max_frames`: Maximum number of frames to extract
- `--quality`: JPEG quality (0-100, higher = better quality, larger files)

**Recommendations:**
- For static scenes: 1-2 FPS
- For dynamic scenes: 2-5 FPS
- Aim for 100-300 frames total

### Step 3: COLMAP + GLOMAP Reconstruction

COLMAP performs feature extraction and matching, while GLOMAP performs fast reconstruction to create camera poses and a sparse 3D point cloud:

```bash
python scripts/run_colmap.py \
    --images_dir data/processed/frames/<project_name> \
    --output_dir data/processed/colmap/<project_name> \
    --camera_model OPENCV \
    --quality high
```

**Parameters:**
- `--camera_model`: Camera model (OPENCV, PINHOLE, RADIAL)
- `--quality`: Processing quality (high, medium, low)
- `--no_gpu`: Disable GPU acceleration (for CPU-only systems)
- `--no_glomap`: Use COLMAP mapper instead of GLOMAP (slower but more compatible)

**This step can take 10-60 minutes depending on:**
- Number of images
- Image resolution
- Quality settings
- Hardware (GPU vs CPU)

**GLOMAP vs COLMAP**: GLOMAP is automatically used for the reconstruction step if available, providing 10-50x faster processing. COLMAP handles feature extraction and matching.

![COLMAP Process](docs/images/colmap_process.png)
<!-- TODO: Add COLMAP visualization image -->

### Step 4: Gaussian Splatting Training

You have two options for training: **Brush (GUI)** for interactive training with real-time visualization, or **Command-Line** for automated/scripted workflows.

#### Option A: Brush (Interactive GUI)

[Brush](https://github.com/ArthurBrussee/brush) provides an intuitive interface with real-time visualization during training.

1. **Download and Install Brush**
   - Visit [Brush Releases](https://github.com/ArthurBrussee/brush/releases)
   - Download for your platform (Windows/Linux/macOS)
   - Extract and run the executable

2. **Load Your Data**
   - Launch Brush
   - Click `Directory` button
   - Navigate to your COLMAP output: `data/processed/colmap/<project_name>`
   - Select the parent folder (containing `sparse/` directory)

3. **Configure and Train**
   - Choose training preset (Quick/Balanced/High Quality)
   - Click `Start` to begin training
   - Watch real-time progress in viewport
   - Navigate with WASD/QE keys during training

4. **Export**
   - Click `Export` when training completes
   - Save to: `data/output/splats/<project_name>/point_cloud.ply`

**Brush Benefits:**
- ✅ Real-time visualization
- ✅ Interactive parameter adjustment
- ✅ No command line needed
- ✅ Easy to learn

See [docs/BRUSH_GUIDE.md](docs/BRUSH_GUIDE.md) for detailed Brush instructions.

#### Option B: Command-Line Training

For automated workflows and scripting:

```bash
python scripts/train_gaussian_splat.py \
    --source_path data/processed/colmap/<project_name> \
    --model_path data/output/splats/<project_name> \
    --iterations 30000 \
    --resolution 1 \
    --export_ply data/output/splats/<project_name>/point_cloud.ply
```

**Parameters:**
- `--iterations`: Training iterations (7000 = fast preview, 30000 = high quality)
- `--resolution`: Resolution downscale (1 = full, 2 = half, 4 = quarter)
- `--export_ply`: Export PLY file after training

**CLI Benefits:**
- ✅ Scriptable and automatable
- ✅ Advanced parameter control
- ✅ Works on headless servers
- ✅ Batch processing support

**Training times (both methods):**
- 7,000 iterations: ~10-20 minutes
- 30,000 iterations: ~30-60 minutes

**Which to choose?**
- **First time?** → Use Brush for visual feedback
- **Experimenting?** → Use Brush to tune parameters
- **Production?** → Use CLI for automation
- **Multiple scenes?** → Use CLI for batch processing

![Training Progress](docs/images/training_progress.png)
<!-- TODO: Add training progress visualization (can show Brush or CLI) -->

### Step 5: Blender Visualization

#### Installing the Kiri 3DGS Render Add-on

1. **Download the Blender Add-on**
   - Get the [Kiri 3DGS Render add-on](https://github.com/KIRI-Innovation/kiri-3dgs-blender-addon)
   - Go to [Releases](https://github.com/KIRI-Innovation/kiri-3dgs-blender-addon/releases)
   - For Blender 4.5+: Download latest version
   - For Blender 4.2-4.4: Download version 4.0

2. **Install in Blender**
   - Open Blender 4.5 (or 4.2+)
   - Drag and drop the ZIP file into Blender
   - Click `OK` to install
   - Or: `Edit` → `Preferences` → `Add-ons` → `Install...`

![Blender Addon Install](docs/images/blender_addon_install.gif)
<!-- TODO: Add gif showing addon installation -->

#### Importing the Gaussian Splat

1. **Open Blender 4.5** (or 4.2+)

2. **Open the 3DGS Panel**
   - Press `N` to open the properties panel
   - Click on the `3DGS Render` tab

3. **Import PLY File**
   - In the 3DGS Render panel, click `Import PLY`
   - Navigate to `data/output/splats/<project_name>/point_cloud.ply`
   - Click `Import PLY`

![Import Splat](docs/images/blender_import.gif)
<!-- TODO: Add gif showing import process -->

4. **View the Gaussian Splat**
   - Press `Z` and select `Rendered` mode
   - The splat will render in real-time in the viewport
   - Adjust settings in the 3DGS Render panel as needed

![Blender Settings](docs/images/blender_settings.png)
<!-- TODO: Add screenshot of settings panel -->

5. **Render Setup**
   - The 3DGS Render panel has options for rendering
   - Use `Render` to create single frames
   - Use `Combined with native render` to mix with 3D objects
   - Set up lighting and camera as desired

For complete Blender instructions, see [docs/BLENDER_GUIDE.md](docs/BLENDER_GUIDE.md).

![Final Render](docs/images/blender_render.png)
<!-- TODO: Add final render example -->

## 📁 Project Structure

```
gaussian_splats/
├── data/
│   ├── input/
│   │   ├── videos/          # Input video files
│   │   └── images/          # Or input image sequences
│   ├── processed/
│   │   ├── frames/          # Extracted frames
│   │   └── colmap/          # COLMAP reconstruction data
│   └── output/
│       └── splats/          # Trained Gaussian Splat models
├── scripts/
│   ├── extract_frames.py    # Frame extraction script
│   ├── run_colmap.py        # COLMAP wrapper script
│   ├── train_gaussian_splat.py  # Training script
│   ├── pipeline.sh          # Complete pipeline (Linux/Mac)
│   └── pipeline.ps1         # Complete pipeline (Windows)
├── docs/
│   └── images/              # Documentation images
├── example/                 # Example data and results
├── docker/
│   └── README.md            # Docker setup guide
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose configuration
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## 🔧 Troubleshooting

### Common Issues

**1. CUDA/GPU Not Detected**
```bash
# Check NVIDIA driver
nvidia-smi

# Check CUDA in Docker
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

**2. COLMAP Fails to Reconstruct**
- Ensure images have sufficient overlap (70%+ recommended)
- Check image quality (not too dark/bright, not blurry)
- Try reducing `--quality` to `medium` or `low`
- Use `--camera_model SIMPLE_RADIAL` for simple cameras
- If GLOMAP fails, use `--no_glomap` to fall back to COLMAP mapper

**3. Training Crashes (Out of Memory)**
- Reduce `--resolution` (try 2 or 4)
- Reduce number of input images
- Close other GPU-intensive applications
- Use a GPU with more VRAM
- Consider CPU-only for preprocessing, then cloud GPU for training

**4. Blender Import Issues**
- Ensure you have Kiri 3DGS addon version 4.0+ for Blender 4.2+
- Ensure you have Blender 4.5 for latest addon features
- Try re-exporting the PLY file
- Check file path doesn't contain special characters

**5. No GPU Available**
- See [CPU Setup Guide](docs/CPU_SETUP.md) for CPU-only workflows
- Consider using cloud GPU services for training step
- Brush can work on CPU but will be slower

**6. Brush Issues**
- Ensure GPU drivers are updated
- Check COLMAP data loaded correctly
- See [Brush Guide](docs/BRUSH_GUIDE.md) for detailed troubleshooting

### Getting Help

- **GitHub Issues**: [Report bugs or request features](https://github.com/arpm511/gaussian-splats/issues)
- **Discussions**: [Ask questions and share results](https://github.com/arpm511/gaussian-splats/discussions)

## 🎓 Credits

This project builds upon amazing work from the research community:

- **Gaussian Splatting**: [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) by Inria
- **COLMAP**: [Structure-from-Motion and Multi-View Stereo](https://colmap.github.io/)
- **GLOMAP**: [Fast and Robust Structure-from-Motion](https://github.com/colmap/glomap) by COLMAP team
- **Brush**: [Interactive Gaussian Splatting Training](https://github.com/ArthurBrussee/brush) by Arthur Brussee
- **Tutorial Reference**: [nicko16's YouTube Tutorial](https://www.youtube.com/watch?v=A1T9uJtq0cI)
- **Blender Add-on**: [Kiri 3DGS Render](https://github.com/KIRI-Innovation/kiri-3dgs-blender-addon)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Showcase

<!-- TODO: Add showcase section with example renders -->

If you create something cool with this pipeline, please share it! Open a PR to add your work to our showcase.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📮 Contact

<!-- TODO: Add your contact information -->
- **GitHub**: [@arpm511](https://github.com/arpm511)
- **Email**: your.email@example.com

---

**⭐ If you find this project helpful, please consider giving it a star!**
