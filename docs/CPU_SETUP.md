# CPU-Only Setup Guide

This guide is for users who don't have an NVIDIA GPU or want to run the pipeline on CPU only.

## ⚠️ Important Notes

- **Performance**: CPU processing is significantly slower than GPU processing
  - Frame extraction: Similar speed
  - COLMAP/GLOMAP: 5-10x slower
  - Gaussian Splatting training: 10-50x slower (not recommended on CPU)
  
- **Recommendations**:
  - Use CPU for COLMAP/GLOMAP reconstruction only
  - Consider using cloud GPU services for Gaussian Splatting training (Google Colab, Paperspace, etc.)
  - Reduce quality settings and number of frames for faster processing

## Installation Options

### Option 1: Docker (Recommended for CPU-only)

1. **Build the CPU-only Docker image**
   ```bash
   docker-compose -f docker-compose-cpu.yml build
   ```

2. **Start the container**
   ```bash
   docker-compose -f docker-compose-cpu.yml up -d
   ```

3. **Access the container**
   ```bash
   docker-compose -f docker-compose-cpu.yml exec gaussian-splatting-cpu /bin/bash
   ```

### Option 2: Local Installation (CPU-only)

#### Install COLMAP (CPU version)

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
cmake .. -DCUDA_ENABLED=OFF
make -j
sudo make install
```

**Windows:**
Download pre-built CPU-only binaries from [COLMAP Releases](https://github.com/colmap/colmap/releases)

#### Install GLOMAP (CPU version)

```bash
git clone https://github.com/colmap/glomap.git
cd glomap
mkdir build && cd build
cmake .. -DCUDA_ENABLED=OFF
make -j
sudo make install
```

#### Install Python Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install PyTorch (CPU version)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install other requirements
pip install -r requirements-cpu.txt
```

## Usage

### Running the Pipeline (CPU-only)

The scripts will automatically detect if GPU is not available and run on CPU.

**Extract frames (same speed as GPU):**
```bash
python scripts/extract_frames.py data/input/videos/your_video.mp4 \
    --output_dir data/processed/frames/my_project \
    --fps 1 \
    --max_frames 100
```

**Run COLMAP/GLOMAP (CPU mode, much slower):**
```bash
python scripts/run_colmap.py \
    --images_dir data/processed/frames/my_project \
    --output_dir data/processed/colmap/my_project \
    --no_gpu
```

**Training (NOT RECOMMENDED on CPU):**
```bash
# CLI Training - This will be extremely slow on CPU
# Consider using cloud GPU instead
python scripts/train_gaussian_splat.py \
    --source_path data/processed/colmap/my_project \
    --model_path data/output/splats/my_project \
    --iterations 7000  # Use fewer iterations on CPU

# Alternative: Brush (GUI) - May be easier to monitor progress
# Download from: https://github.com/ArthurBrussee/brush/releases
# Brush can run on CPU but will be significantly slower
# Visual feedback helps you stop early if quality is sufficient
```

### Optimization Tips for CPU

1. **Reduce Image Count**
   - Extract fewer frames: `--fps 1` or `--max_frames 100`
   - Less frames = faster processing

2. **Lower Quality Settings**
   ```bash
   python scripts/run_colmap.py \
       --images_dir data/processed/frames/my_project \
       --output_dir data/processed/colmap/my_project \
       --quality low \
       --no_gpu
   ```

3. **Use Smaller Resolution**
   - Resize images before processing
   - Use `--resolution 2` or `--resolution 4` in training

4. **Parallel Processing**
   - COLMAP/GLOMAP will use all CPU cores automatically
   - Close other applications for better performance

## Cloud GPU Alternatives

For Gaussian Splatting training, consider these free/low-cost GPU options:

### Google Colab (Free tier available)
```python
# In Colab notebook
!git clone https://github.com/graphdeco-inria/gaussian-splatting
!pip install -r gaussian-splatting/requirements.txt

# Upload your COLMAP data
# Run training
!python gaussian-splatting/train.py -s /content/your_data -m /content/output
```

### Kaggle (Free GPU)
- 30 hours/week of free GPU time
- Upload your COLMAP data as a dataset
- Run training notebook

### Paperspace Gradient (Pay-as-you-go)
- Starting at $0.51/hour for GPU instances
- Good for occasional use

### Vast.ai (Lowest cost)
- Rent GPUs starting at $0.10/hour
- Good for batch processing

## Hybrid Workflow (Recommended)

The most cost-effective approach:

1. **Local CPU**: Frame extraction and COLMAP/GLOMAP reconstruction
2. **Cloud GPU**: Gaussian Splatting training only
3. **Local**: Blender visualization and rendering

**Brush Alternative**: You can also download Brush locally and use it to train on cloud instances via remote desktop, giving you the visual feedback of Brush with cloud GPU power.

Example workflow:
```bash
# Step 1: Local (CPU) - Frame extraction
python scripts/extract_frames.py video.mp4 --output_dir frames

# Step 2: Local (CPU) - COLMAP reconstruction (slow but free)
python scripts/run_colmap.py --images_dir frames --output_dir colmap --no_gpu

# Step 3: Upload colmap/ folder to cloud GPU service

# Step 4: Cloud (GPU) - Training
python train_gaussian_splat.py --source_path colmap --iterations 30000

# Step 5: Download the resulting PLY file

# Step 6: Local - Blender visualization
# Import PLY into Blender and render
```

## Expected Processing Times (CPU vs GPU)

| Task | CPU (i7-10700K) | GPU (RTX 3080) | Speedup |
|------|----------------|----------------|---------|
| Extract 200 frames | ~2 min | ~2 min | 1x |
| COLMAP feature extraction | ~20 min | ~3 min | 6-7x |
| COLMAP matching | ~15 min | ~2 min | 7-8x |
| GLOMAP reconstruction | ~10 min | ~1 min | 10x |
| Gaussian Splat training (7k iter) | ~8 hours | ~15 min | 30x |
| Gaussian Splat training (30k iter) | ~24+ hours | ~60 min | 24x |

## Troubleshooting

**Out of Memory on CPU**
- Reduce number of images
- Close other applications
- Use `--quality low` setting

**Very Slow Processing**
- This is normal for CPU processing
- Consider using fewer frames
- Use cloud GPU for training step

**Dependencies Issues**
- Ensure you installed CPU version of PyTorch
- Verify COLMAP was built with `CUDA_ENABLED=OFF`

## Summary

- ✅ **Frame extraction**: Works great on CPU
- ✅ **COLMAP/GLOMAP**: Works on CPU but slower (still reasonable)
- ❌ **Gaussian Splatting training**: Not recommended on CPU (too slow)
- 💡 **Best approach**: Use CPU for preprocessing, GPU for training

For questions or issues, see the main [README](../README.md) or open an issue on GitHub.
