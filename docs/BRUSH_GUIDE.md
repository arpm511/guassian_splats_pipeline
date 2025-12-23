# Brush - Gaussian Splatting Training GUI

Brush is a user-friendly GUI application for training Gaussian Splats with real-time visualization.

## What is Brush?

[Brush](https://github.com/ArthurBrussee/brush) is an interactive Gaussian Splatting training application that provides:
- **Real-time visualization** during training
- **Interactive controls** for adjusting parameters
- **Easy export** to PLY format
- **Cross-platform** support (Windows, Linux, macOS)
- **User-friendly interface** - no command line needed

## Installation

### Windows

1. **Download Brush**
   - Visit [Brush Releases](https://github.com/ArthurBrussee/brush/releases)
   - Download the latest Windows release (e.g., `brush-windows.zip`)
   - Extract to a folder (e.g., `C:\Tools\brush`)

2. **Run Brush**
   - Double-click `brush.exe` to launch

### Linux

1. **Download Brush**
   ```bash
   # Download latest release
   wget https://github.com/ArthurBrussee/brush/releases/latest/download/brush-linux.tar.gz
   
   # Extract
   tar -xzf brush-linux.tar.gz
   cd brush
   
   # Make executable
   chmod +x brush
   ```

2. **Run Brush**
   ```bash
   ./brush
   ```

### macOS

1. **Download Brush**
   - Visit [Brush Releases](https://github.com/ArthurBrussee/brush/releases)
   - Download the latest macOS release (e.g., `brush-macos.dmg`)
   - Open DMG and drag Brush to Applications

2. **Run Brush**
   - Open from Applications folder

## Using Brush for Training

### Step 1: Load Your COLMAP Data

1. **Launch Brush**
   - Open the Brush application

2. **Select Data Directory**
   - Click the `Directory` button or `File` → `Open Directory`
   - Navigate to your COLMAP output folder
   - Select the **parent folder** containing the `sparse/` directory
   - Example: `data/processed/colmap/my_project`

3. **Verify Data Loaded**
   - You should see the sparse point cloud appear
   - Camera positions should be visible

### Step 2: Configure Training Settings

Brush provides several training presets:

**Quick Preview (Fast, lower quality)**
- Iterations: ~7,000
- Training time: 10-15 minutes
- Good for testing and quick previews

**Balanced (Default)**
- Iterations: ~15,000
- Training time: 20-30 minutes
- Good quality for most use cases

**High Quality**
- Iterations: ~30,000
- Training time: 45-90 minutes
- Best quality for final renders

**Custom Settings**
- You can adjust iterations manually
- Modify learning rates
- Change optimization parameters

### Step 3: Train Your Gaussian Splat

1. **Start Training**
   - Click `Start` button
   - Training progress will show in real-time

2. **Monitor Progress**
   - Watch the Gaussian Splat quality improve
   - View loss metrics
   - Navigate through camera views
   - Use WASD keys to move around
   - Use QE keys to move up/down

3. **Interactive Viewing**
   - While training, click the expand icon to see camera views
   - Scrub through different camera positions
   - Assess quality from multiple angles

4. **Stop Training**
   - Training will auto-stop at target iterations
   - Or click `Stop` to end early
   - Can resume from checkpoint if needed

### Step 4: Export Your Gaussian Splat

1. **Open Export Menu**
   - Click `Export` or `File` → `Export`

2. **Choose Format**
   - Select PLY format (compatible with Blender)

3. **Select Output Location**
   - Navigate to: `data/output/splats/my_project/`
   - Save as: `point_cloud.ply`

4. **Export**
   - Click `Save`
   - Wait for export to complete

## Brush vs Command-Line Training

| Feature | Brush (GUI) | gaussian-splatting (CLI) |
|---------|-------------|--------------------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Very Easy | ⭐⭐⭐ Moderate |
| **Real-time Visualization** | ✅ Yes | ❌ No |
| **Interactive** | ✅ Yes | ❌ No |
| **Parameter Tuning** | ✅ Easy UI | ⚠️ Command line flags |
| **Cross-platform** | ✅ Windows, Linux, macOS | ⚠️ Requires compilation |
| **Installation** | ✅ Simple download | ⚠️ Complex setup |
| **Automation** | ❌ Manual process | ✅ Scriptable |
| **Advanced Options** | ⚠️ Limited | ✅ Full control |
| **Training Speed** | 🔄 Similar | 🔄 Similar |

## When to Use Brush vs CLI

**Use Brush When:**
- You want to see results in real-time
- You're learning Gaussian Splatting
- You want to experiment with settings
- You prefer GUI over command line
- You're creating one-off projects
- You want to inspect quality during training

**Use CLI (gaussian-splatting) When:**
- You need to automate multiple trainings
- You need advanced customization
- You're running on a headless server
- You want to batch process many scenes
- You need to integrate with other scripts

## Tips for Best Results with Brush

1. **Check Data First**
   - Ensure COLMAP reconstruction succeeded
   - Verify sparse point cloud looks reasonable
   - Check camera positions are correct

2. **Start with Preview**
   - Train a quick preview (7k iterations)
   - Verify data quality before long training
   - Adjust COLMAP if results are poor

3. **Monitor Training**
   - Watch for convergence
   - Check multiple camera angles
   - Stop early if quality plateaus

4. **Hardware Considerations**
   - GPU: Brush will auto-detect and use GPU
   - RAM: Ensure 8GB+ available
   - VRAM: 6GB+ recommended for good quality

## Keyboard Shortcuts

While training in Brush:
- **W/A/S/D**: Move camera forward/left/backward/right
- **Q/E**: Move camera down/up
- **Mouse**: Look around
- **Space**: Pause/resume training
- **ESC**: Stop training

## Troubleshooting

**Brush won't start**
- Ensure GPU drivers are updated
- Try running as administrator (Windows)
- Check system requirements

**Data won't load**
- Verify COLMAP sparse/0/ directory exists
- Select the correct parent folder
- Check file permissions

**Slow training**
- Close other GPU-intensive applications
- Reduce resolution in settings
- Use Quick Preview preset first

**Export fails**
- Ensure output directory is writable
- Check sufficient disk space
- Try different output location

**Quality is poor**
- Increase iteration count
- Check COLMAP reconstruction quality
- Ensure sufficient image overlap
- Try adjusting training parameters

## Integration with This Pipeline

Brush fits into the pipeline as an alternative to command-line training:

```
Video → Frame Extraction → COLMAP/GLOMAP → [Brush GUI OR CLI Training] → Blender
```

**Workflow:**
1. Extract frames: `python scripts/extract_frames.py`
2. Run COLMAP: `python scripts/run_colmap.py`
3. **Option A - Brush (GUI)**: Open Brush, load data, train, export
4. **Option B - CLI**: `python scripts/train_gaussian_splat.py`
5. Import to Blender: Use Kiri 3DGS addon

## Resources

- **Brush GitHub**: https://github.com/ArthurBrussee/brush
- **Documentation**: See Brush repository README
- **Issues**: Report bugs on Brush GitHub issues
- **Community**: Discuss in Brush discussions

---

For command-line training, see [train_gaussian_splat.py](../scripts/train_gaussian_splat.py) documentation.
