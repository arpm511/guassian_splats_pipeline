# Example Project: Perth Elizabeth Quay

This example demonstrates the complete Gaussian Splatting pipeline using aerial footage of Elizabeth Quay in Perth, Western Australia. The project showcases the full workflow from video processing through COLMAP reconstruction to final Blender visualization.

## Source Footage

**Video Source**: [Aerial View of Perth's Modern Skyline by Sergey Guk](https://www.pexels.com/video/aerial-view-of-perth-s-modern-skyline-30598751/)  
**License**: Free to use (Pexels License)  
**Location**: Elizabeth Quay, Perth WA, Australia  
**Scene Type**: Aerial/Drone footage with smooth camera motion

### Video Specifications

| Property | Value |
|----------|-------|
| **Dimensions** | 3840 x 2160 (4K) |
| **Aspect Ratio** | 16:9 |
| **Duration** | 32 seconds |
| **Frame Rate** | 59.94 FPS |
| **Camera Motion** | Smooth aerial pan with consistent altitude |

**Sample Data**: A subset of 175 sample frames from the processed dataset is available for testing: [Download Sample Frames](https://drive.google.com/drive/folders/1bRoT-BXuYQ7ATdgYUeZf4asT-zcyG1wP?usp=sharing)

## Pipeline Steps

### 1. Frame Extraction

**Settings Used:**
```bash
python scripts/extract_frames.py data/input/perth_aerial.mp4 \
    --fps 2 \
    --quality 95 \
    --max_frames 200
```

**Parameters:**
- **FPS**: 2 frames per second (extracted ~64 frames from 32-second video)
- **Quality**: 95% JPEG quality for minimal compression artifacts
- **Max Frames**: Limited to 200 to keep dataset manageable

**Rationale**: Aerial footage with smooth motion doesn't require high frame rate extraction. 2 FPS provides sufficient coverage while maintaining reasonable processing times.

### 2. COLMAP/GLOMAP Reconstruction

**Settings Used:**
```bash
python scripts/run_colmap.py data/frames/perth_aerial data/colmap/perth_aerial
```

**Configuration:**
- **Matcher**: Sequential matcher (appropriate for continuous video footage)
- **Reconstruction**: GLOMAP used for sparse reconstruction (10x faster than COLMAP mapper)
- **GPU Acceleration**: Enabled for feature extraction and matching

**Results:**
- Successfully reconstructed camera poses for all frames
- Sparse point cloud generated with high-quality features
- Processing time: ~15 minutes for feature extraction and reconstruction

### 3. Gaussian Splatting Training

**Method**: Brush (Interactive GUI)

**Settings Used:**
- **Training Steps**: 90,000 iterations
- **Preset**: Default Brush settings
- **Resolution**: Auto (based on source resolution)
- **Refinement**: Enabled with default schedule

![Brush Training Settings](../media/settings.png)

**Training Process:**
1. Loaded COLMAP reconstruction data
2. Started training with default preset
3. Monitored real-time visualization for quality
4. Stopped at 90,000 iterations (optimal quality/time balance)
5. Exported to PLY format for Blender import

**Training Time**: 65 minutes on laptop GPU

### 4. Blender Visualization

**Addon**: Kiri 3DGS Render  
**Blender Version**: 4.5

**Import Settings:**
- Loaded PLY file directly through addon
- Adjusted point size for optimal appearance
- Configured camera for final render

## Hardware Specifications

**System**: MSI Thin GF63 12VF Gaming Laptop

| Component | Specification |
|-----------|--------------|
| **GPU** | NVIDIA® GeForce RTX™ 4060 Laptop (8GB GDDR6) |
| **RAM** | 16GB DDR4 |
| **CPU** | Intel Core i7 12th Gen |
| **Storage** | SSD (recommended for large datasets) |

## Performance Metrics

| Stage | Time | Notes |
|-------|------|-------|
| **Frame Extraction** | ~2 minutes | Fast, I/O bound |
| **COLMAP Feature Extraction** | ~10 minutes | GPU accelerated |
| **GLOMAP Reconstruction** | ~5 minutes | Significantly faster than COLMAP mapper |
| **Gaussian Splatting Training** | 65 minutes | 90,000 iterations with Brush |
| **Total Pipeline** | ~82 minutes | End-to-end processing time |

## Results

### Output Files

- **Point Cloud**: `point_cloud.ply` (~250-500MB depending on scene complexity)
- **Blender Renders**: Multiple still frames and animation sequences
- **Project Files**: COLMAP reconstruction data, training checkpoints

**Download Results**: The final PLY file and rendered images from Blender can be found [here](https://drive.google.com/drive/folders/1S0sX1l05AcQ3HabL6D-JfiKekRVCN2dY?usp=sharing)

### Quality Assessment

**Strengths:**
- Excellent reconstruction of buildings and waterfront structures
- Smooth camera motion preserved in training data
- High-detail capture of reflective surfaces on water
- Realistic rendering from novel viewpoints

**Challenges:**
- Sky areas have minimal features (expected with aerial footage)
- Some artifacts near image boundaries due to limited angle coverage
- Water reflections show minor flickering in animation

## Renders

### Final Animation

![Aerial Animation](../media/Animation.gif)

### Additional Renders

<!-- TODO: Add more render images -->
<!-- ![Render 1](../media/render_01.png) -->
<!-- ![Render 2](../media/render_02.png) -->

## Lessons Learned

### What Worked Well

1. **Brush for Training**: The interactive GUI made it easy to monitor quality and stop at optimal iteration count
2. **GLOMAP Integration**: Reconstruction was significantly faster than traditional COLMAP mapper
3. **Frame Rate Selection**: 2 FPS was sufficient for smooth aerial footage
4. **Hardware**: RTX 4060 Laptop GPU handled training well despite being mobile hardware

### Recommendations for Similar Projects

1. **Aerial Footage Tips:**
   - Ensure smooth camera motion (no sudden movements)
   - Maintain consistent altitude when possible
   - Overlap in frames is critical (2 FPS works for slow-moving footage)

2. **Training Parameters:**
   - 90,000 iterations provided good quality without overtraining
   - Monitor Brush visualization to stop when quality plateaus
   - Default settings work well for most aerial scenes

3. **Performance Optimization:**
   - Use GLOMAP instead of COLMAP mapper (10-50x speedup)
   - Limit frame extraction to 150-200 frames for faster processing
   - Consider reducing training iterations to 50,000-70,000 for faster results with minimal quality loss

## Reproducing This Example

To reproduce this example with your own system:

1. **Download the source video** from the Pexels link above
2. **Place it in** `data/input/perth_aerial.mp4`
3. **Run the pipeline** following the commands in this README
4. **Compare your results** with the settings and times documented here

For detailed setup instructions, see the main [README.md](../README.md) and [IMPLEMENTATION_GUIDE.md](../IMPLEMENTATION_GUIDE.md).

## Credits

- **Video Source**: Sergey Guk via [Pexels](https://www.pexels.com/)
- **Location**: Elizabeth Quay, Perth, Western Australia
- **Processing**: Completed using this Gaussian Splatting pipeline