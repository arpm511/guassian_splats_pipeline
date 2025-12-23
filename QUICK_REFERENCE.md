# Project Quick Reference

## Essential Commands

### Docker Setup

**GPU (CUDA):**
```bash
# Build and start container
docker-compose build
docker-compose up -d
docker-compose exec gaussian-splatting /bin/bash

# Stop container
docker-compose down
```

**CPU-only:**
```bash
# Build and start CPU-only container
docker-compose -f docker-compose-cpu.yml build
docker-compose -f docker-compose-cpu.yml up -d
docker-compose -f docker-compose-cpu.yml exec gaussian-splatting-cpu /bin/bash
```

### Complete Pipeline

**Linux/Mac:**
```bash
./scripts/pipeline.sh data/input/videos/your_video.mp4 my_project
```

**Windows:**
```powershell
.\scripts\pipeline.ps1 -VideoPath "data\input\videos\your_video.mp4" -ProjectName "my_project"
```

### Individual Steps

```bash
# 1. Extract frames
python scripts/extract_frames.py <video_path> \
    --output_dir data/processed/frames/<project> \
    --fps 2

# 2. COLMAP + GLOMAP
python scripts/run_colmap.py \
    --images_dir data/processed/frames/<project> \
    --output_dir data/processed/colmap/<project>

# 3A. Train with Brush (GUI - Interactive)
# Download Brush: https://github.com/ArthurBrussee/brush/releases
# Launch Brush → Directory → Select data/processed/colmap/<project>
# Start → Train → Export to data/output/splats/<project>/point_cloud.ply

# 3B. Train with CLI (Automated)
python scripts/train_gaussian_splat.py \
    --source_path data/processed/colmap/<project> \
    --model_path data/output/splats/<project> \
    --export_ply data/output/splats/<project>/point_cloud.ply
```

## File Locations

| Item | Location |
|------|----------|
| Input videos | `data/input/videos/` |
| Extracted frames | `data/processed/frames/<project>/` |
| COLMAP output | `data/processed/colmap/<project>/` |
| Trained models | `data/output/splats/<project>/` |
| Final PLY | `data/output/splats/<project>/point_cloud.ply` |

## Key Settings

### Frame Extraction
- **FPS**: 1-5 (2 recommended)
- **Quality**: 85-95 (95 recommended)
- **Target frames**: 100-300

### COLMAP + GLOMAP
- **Camera model**: OPENCV (default) or SIMPLE_RADIAL
- **Quality**: high (recommended), medium, low
- **GLOMAP**: Enabled by default (10-50x faster reconstruction)
- **Use `--no_glomap`**: Fall back to COLMAP mapper if needed
- **Use `--no_gpu`**: For CPU-only systems

### Training

**Option A: Brush (GUI)**
- Download from: https://github.com/ArthurBrussee/brush/releases
- Real-time visualization
- Interactive parameter tuning
- Great for learning and experimentation

**Option B: CLI**
- **Iterations**: 7000 (quick), 30000 (high quality)
- **Resolution**: 1 (full), 2 (half), 4 (quarter)
- Best for automation and batch processing

## Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| GPU not detected | Run `nvidia-smi` to verify drivers |
| COLMAP fails | Ensure 70%+ image overlap, try lower quality |
| GLOMAP fails | Use `--no_glomap` to fall back to COLMAP mapper |
| Brush won't start | Update GPU drivers, check system requirements |
| Out of memory | Reduce resolution or number of images |
| Import fails in Blender | Ensure Kiri 3DGS addon installed (Blender 4.2+) |
| No GPU available | See [CPU Setup Guide](docs/CPU_SETUP.md) |

## Time Estimates

| Step | Duration (GPU) | Duration (CPU) |
|------|----------------|----------------|
| Frame extraction | 5-10 min | 5-10 min |
| COLMAP feature extraction | 3-5 min | 15-30 min |
| COLMAP matching | 2-5 min | 10-20 min |
| GLOMAP reconstruction | 1-2 min | 5-10 min |
| COLMAP mapper (if no GLOMAP) | 10-20 min | 60-120 min |
| Training (7k iter) | 10-20 min |
| Training (30k iter) | 30-90 min |
| Blender setup | 15-30 min |

## Quality vs Speed Tradeoffs

**Fast (30 min total)**
- FPS: 1
- Frames: 50-100
- COLMAP quality: low
- Iterations: 7000
- Resolution: 2

**Balanced (2 hours total)**
- FPS: 2
- Frames: 150-200
- COLMAP quality: medium
- Iterations: 15000
- Resolution: 1

**High Quality (4+ hours total)**
- FPS: 3-5
- Frames: 250-300
- COLMAP quality: high
- Iterations: 30000
- Resolution: 1

## Useful Links

- [Main README](README.md) - Complete documentation
- [Irush Guide](docs/BRUSH_GUIDE.md) - Interactive GUI training
- [Bmplementation Guide](IMPLEMENTATION_GUIDE.md) - Step-by-step completion
- [Blender Guide](docs/BLENDER_GUIDE.md) - Kiri 3DGS visualization help
- [CPU Setup Guide](docs/CPU_SETUP.md) - CPU-only workflows
- [Docker Guide](docker/README.md) - Docker setup details (including free Docker CLI)

## GPU Requirements by Quality

| Quality | VRAM | RAM | Time (30k iter) |
|---------|------|-----|-----------------|
| Preview | 4GB | 8GB | 20 min |
| Medium | 8GB | 16GB | 45 min |
| High | 12GB+ | 32GB+ | 90 min |

## Common Mistakes to Avoid

1. ❌ Moving camera too fast while recording
2. ❌ Insufficient overlap between frames
3. ❌ Inconsistent lighting in video
4. ❌ Too few frames (under 50)
5. ❌ Not verifying COLMAP success before training

## Success Checklist

- [ ] Video has good coverage of subject
- [ ] Extracted 100+ frames
- [ ] COLMAP created `sparse/0/` directory
- [ ] Training completed without errors
- [ ] PLY file exists and is >10MB
- [ ] Successfully imported into Blender

---

For detailed information, see [README.md](README.md) or [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)
