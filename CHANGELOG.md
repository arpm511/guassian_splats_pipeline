# Repository Update Summary - July 2026

## Overview
This repository has been comprehensively updated to reflect the current state of Gaussian Splatting tools and workflows. The update focuses on making the pipeline more accessible to beginners while maintaining advanced capabilities for researchers.

## Major Changes

### 1. **Two-Path Workflow Structure** ⭐ NEW
The README now presents two distinct workflow paths:

#### **Path 1: SkySplat (Recommended for Beginners)**
- All-in-one Blender addon for complete pipeline automation
- Visual, interactive workflow within Blender
- Minimal command-line setup required
- Perfect for learning and single-scene work
- Link: https://github.com/kyjohnso/skysplat_blender

#### **Path 2: Manual Pipeline (For Advanced Users)**
- Full control with Python scripts and CLI tools
- Scriptable and automatable for batch processing
- Updated for latest tool versions
- Better for production and research workflows

### 2. **COLMAP/GLOMAP Integration** 🔄 CRITICAL UPDATE
- **GLOMAP repository was archived in March 2026**
- GLOMAP functionality is now **integrated into COLMAP 4.0+** as `global_mapper`
- No separate GLOMAP installation needed anymore
- Updated all scripts to use `colmap global_mapper` instead of `glomap mapper`

**Changed commands:**
```bash
# OLD (deprecated):
glomap mapper --database_path ... --image_path ... --output_path ...

# NEW (COLMAP 4.0+):
colmap global_mapper --database_path ... --image_path ... --output_path ...
```

### 3. **Version Updates** 📦

| Component | Old Version | New Version | Notes |
|-----------|-------------|-------------|-------|
| Python | 3.10+ | **3.11** (required) | Better performance, standardized |
| COLMAP | 3.8+ | **4.1+** | Includes global mapper (GLOMAP) |
| Blender | 4.5+ | **5.2 LTS** (primary) | 4.5 LTS minimum |
| CUDA | 12.1 | **12.1** (unchanged) | Stable version |
| PyTorch | 2.0+ | **2.1+** | Better CUDA 12.1 support |
| pycolmap | 0.4+ | **0.6+** | Updated bindings |

### 4. **Python Environment Management with uv** 🚀 NEW
Introduced `uv` as the recommended Python package manager:

**Why uv?**
- Fast (10-100x faster than pip)
- Manages Python versions automatically
- Isolated environments prevent conflicts
- Perfect for managing multiple projects

**Installation:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv --python 3.11
source .venv/bin/activate
uv pip install -r requirements.txt
```

### 5. **Platform Focus** 🐧
Simplified instructions to focus on:
- **Primary**: Ubuntu 22.04/24.04 (native or WSL)
- Removed Windows/Mac specific instructions (tools are cross-platform, but setup varies too much)
- Docker remains cross-platform option

### 6. **Files Updated**

#### **README.md** - Complete restructure
- New two-path workflow introduction
- Comparison table for choosing between paths
- Expanded SkySplat installation and quick start
- Updated all version references
- Better troubleshooting section with specific solutions
- Performance optimization tips

#### **scripts/run_colmap.py** - Major refactor
- Removed separate GLOMAP support (now in COLMAP)
- Added `--use_global_mapper` flag (replaces `--no_glomap`)
- Updated documentation strings
- Better error messages
- Support for both global (fast) and incremental (robust) mapping

#### **requirements.txt** - Dependency updates
- Pinned versions for Python 3.11 compatibility
- Added comments about PyTorch installation
- Updated pycolmap to 0.6+
- Removed unnecessary dependencies

#### **Dockerfile** - Modernized
- Ubuntu 22.04 + CUDA 12.1 (unchanged base)
- Python 3.11 from deadsnakes PPA
- COLMAP 4.1+ built from source (includes global mapper)
- Removed separate GLOMAP build
- Added uv for fast package management
- Better layer caching for faster rebuilds
- Verification steps for CUDA and dependencies

#### **scripts/pipeline.sh** - Updated automation
- Uses `--use_global_mapper` flag
- Better error handling
- Checks for Brush availability
- More informative output messages

#### **pyproject.toml** - NEW file
- Modern Python project configuration
- uv-compatible setup
- Optional CUDA dependencies

## Breaking Changes ⚠️

### For Users

1. **GLOMAP command no longer exists**
   - If you have scripts calling `glomap`, update to `colmap global_mapper`
   - The `--no_glomap` flag is now `--no_global_mapper`

2. **Python 3.11 required**
   - Python 3.10 may work but is not tested
   - Use uv to manage Python versions easily

3. **COLMAP 4.0+ required**
   - Older COLMAP versions don't have global_mapper
   - Must build from source or use Ubuntu packages

### For Developers

1. **Script API changes**
   - `run_colmap(use_glomap=True)` → `run_colmap(use_global_mapper=True)`
   - Import paths unchanged

2. **Docker image changes**
   - New image doesn't have `glomap` command
   - Uses Python 3.11 instead of 3.10
   - Rebuild required: `docker-compose build`

## Migration Guide

### If you have existing setup with GLOMAP:

1. **Update COLMAP to 4.1+**:
   ```bash
   # Remove old COLMAP/GLOMAP
   sudo apt remove colmap
   
   # Build COLMAP 4.1+ from source (see README)
   git clone https://github.com/colmap/colmap.git
   # ... build instructions in README ...
   ```

2. **Update Python environment**:
   ```bash
   # Create new Python 3.11 environment with uv
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv venv --python 3.11
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

3. **Update scripts**:
   - Pull latest changes: `git pull origin main`
   - No code changes needed if using provided scripts

### If using Docker:

```bash
# Rebuild image with new setup
docker-compose build --no-cache
docker-compose up -d
```

## Testing Checklist

Before deploying to production, test:

- [ ] COLMAP 4.1+ installed and `colmap global_mapper -h` works
- [ ] Python 3.11 environment activated
- [ ] PyTorch CUDA check: `python -c "import torch; print(torch.cuda.is_available())"`
- [ ] Frame extraction: `python scripts/extract_frames.py ...`
- [ ] COLMAP with global mapper: `python scripts/run_colmap.py --use_global_mapper ...`
- [ ] Training (if using): `python scripts/train_gaussian_splat.py ...`
- [ ] Full pipeline: `./scripts/pipeline.sh <video> <project>`
- [ ] Docker build and run: `docker-compose build && docker-compose up`

## Known Issues

1. **COLMAP 4.1+ not in Ubuntu repositories yet**
   - Must build from source (instructions in README)
   - Should be available in Ubuntu 24.10+ repositories

2. **uv not widely known yet**
   - Falls back to pip if users prefer
   - Documentation includes both methods

3. **SkySplat is third-party**
   - Not maintained by this repository
   - Depends on external project updates
   - Link may need updates if project moves

## Future Work

Potential improvements for next iteration:

1. **Add example datasets** - Small sample videos for testing
2. **Video tutorials** - Screen recordings of full workflow
3. **Benchmarks** - Performance comparisons on different hardware
4. **Brush integration** - Better documentation for Brush training
5. **Cloud GPU guide** - Instructions for using services like Vast.ai, RunPod
6. **WSL optimization** - Specific tips for Windows users
7. **Memory profiling** - Help users understand RAM/VRAM usage

## Credits for This Update

Research sources:
- COLMAP GitHub repository and release notes
- GLOMAP repository deprecation notice
- SkySplat Blender addon documentation
- Blender release notes (5.2 LTS)
- Community feedback on Gaussian Splatting Discord/Reddit

Tools evaluated:
- COLMAP 4.1.1 (latest stable)
- Python 3.11 with uv package manager
- SkySplat v0.4.2
- Brush training app
- KIRI 3DGS Render addon

## Questions?

If you encounter issues or have questions about the updates:
1. Check the updated [README.md](README.md) first
2. Review this document for migration steps
3. Open a GitHub Discussion or Issue
4. Check if COLMAP 4.1+ is properly installed

## Acknowledgments

Thanks to:
- COLMAP team for integrating GLOMAP
- Kyle Johnson for SkySplat addon
- Arthur Brussee for Brush
- Community testers and feedback providers

---

**Last Updated**: July 25, 2026  
**Repository Version**: 2.0.0  
**Status**: ✅ Ready for testing
