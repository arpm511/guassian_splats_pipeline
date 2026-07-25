# Quick Test Guide

Use this guide to verify all updates are working correctly.

## 1. Environment Check

### Test Python 3.11
```bash
python3 --version  # Should show 3.11.x
```

### Test uv Installation (if using)
```bash
uv --version  # Should show uv version
```

### Test COLMAP 4.1+ with global mapper
```bash
colmap -h                    # Should work
colmap global_mapper -h      # Should show help for global mapper
```

## 2. Python Dependencies Test

### Using uv (recommended)
```bash
cd /home/artemis/projects/guassian_splats_pipeline
uv venv --python 3.11
source .venv/bin/activate  # On Linux/Mac

# Install PyTorch first with CUDA support
uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install project dependencies from pyproject.toml
uv pip install -e .
```

### Using pip (alternative)
```bash
python3 -m venv .venv
source .venv/bin/activate

# Install PyTorch first with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install project dependencies from pyproject.toml
pip install -e .
```

### Verify PyTorch CUDA
```bash
python3 -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

Expected output:
```
PyTorch: 2.1.x+cu121
CUDA available: True
```

## 3. Script Tests

### Test environment check
```bash
python3 scripts/check_environment.py
```

Expected: All checks should pass ✓

### Test frame extraction (dry run)
```bash
# Create test video first or use existing
python3 scripts/extract_frames.py --help
```

Expected: Help message with updated documentation

### Test COLMAP script
```bash
python3 scripts/run_colmap.py --help
```

Expected output should include:
- `--use_global_mapper` flag (not `--use_glomap`)
- Help text mentioning COLMAP 4.0+ global mapper

### Test running with global mapper flag
```bash
# This will fail without actual images, but should show correct usage
python3 scripts/run_colmap.py \
    --images_dir test_dir \
    --output_dir test_out \
    --use_global_mapper 2>&1 | head -20
```

Expected: Should show error about missing directory, but command parsing should work

## 4. Docker Tests

### Build Docker image
```bash
docker-compose build
```

Expected: 
- Should build without errors
- Python 3.11 installed
- COLMAP with global_mapper built
- No separate GLOMAP installation

### Verify Docker image
```bash
docker-compose run --rm gaussian-pipeline bash -c "
    python3 --version && \
    colmap -h && \
    colmap global_mapper -h && \
    python3 -c 'import torch; print(torch.cuda.is_available())'
"
```

Expected output:
```
Python 3.11.x
<COLMAP help>
<global_mapper help>
True (if NVIDIA GPU available)
```

## 5. Full Pipeline Test

If you have a test video:

```bash
# Make sure environment is activated
source .venv/bin/activate

# Run full pipeline
./scripts/pipeline.sh data/input/videos/test.mp4 test_project

# Check outputs
ls data/processed/frames/test_project/     # Should have frames
ls data/processed/colmap/test_project/     # Should have COLMAP database
ls data/output/splats/test_project/        # Should have trained model
```

## 6. SkySplat Path Test (if testing Blender workflow)

1. Open Blender 5.2 LTS or 4.5 LTS
2. Install SkySplat addon from: https://github.com/kyjohnso/skysplat_blender
3. Follow SkySplat workflow in README
4. Verify it can process a video end-to-end

## Common Issues and Solutions

### Issue: "python3: command not found" or wrong version
**Solution**: 
```bash
# On Ubuntu
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

### Issue: "colmap: command not found"
**Solution**: Build COLMAP from source following README instructions

### Issue: "colmap global_mapper: command not found"
**Solution**: Your COLMAP version is too old. Need 4.0+
```bash
colmap --version  # Check version
# Rebuild from latest source if < 4.0
```

### Issue: PyTorch CUDA not available
**Solution**: 
```bash
# Check NVIDIA driver
nvidia-smi

# Reinstall PyTorch with correct CUDA version
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### Issue: Docker build fails at COLMAP
**Solution**: 
```bash
# Make sure you have enough disk space (need ~10GB)
df -h

# Try building with more verbose output
docker-compose build --progress=plain
```

## Success Criteria

✅ All tests pass when:
- Python 3.11 is default
- COLMAP 4.1+ with global_mapper works
- PyTorch detects CUDA
- Scripts run without import errors
- Docker builds successfully
- Pipeline script completes end-to-end (with test video)

## Report Results

After testing, please report:
1. Which tests passed ✓
2. Which tests failed ✗
3. Any error messages
4. Your environment (Ubuntu version, GPU model, etc.)

This will help identify any remaining issues!
