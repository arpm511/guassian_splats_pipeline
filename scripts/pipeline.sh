#!/bin/bash
# Complete pipeline script for Gaussian Splatting
# Usage: ./pipeline.sh <video_path> <project_name>
# 
# Updated for COLMAP 4.0+ with global mapper support

set -e  # Exit on error

# Check arguments
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <video_path> <project_name>"
    echo "Example: $0 data/input/videos/scene.mp4 my_scene"
    exit 1
fi

VIDEO_PATH=$1
PROJECT_NAME=$2

echo "======================================"
echo "Gaussian Splatting Pipeline v2.0"
echo "======================================"
echo "Video: $VIDEO_PATH"
echo "Project: $PROJECT_NAME"
echo "======================================"

# Verify video exists
if [ ! -f "$VIDEO_PATH" ]; then
    echo "Error: Video file not found: $VIDEO_PATH"
    exit 1
fi

# Setup directories
COLMAP_DIR="data/processed/colmap/${PROJECT_NAME}"
FRAMES_DIR="${COLMAP_DIR}/images"
MODEL_DIR="data/output/splats/${PROJECT_NAME}"

mkdir -p "$FRAMES_DIR" "$MODEL_DIR"

# Step 1: Extract frames from video
echo ""
echo "Step 1/3: Extracting frames from video..."
python3 scripts/extract_frames.py \
    "$VIDEO_PATH" \
    --output_dir "$FRAMES_DIR" \
    --fps 2 \
    --quality 95

# Step 2: Run COLMAP with global mapper (faster)
echo ""
echo "Step 2/3: Running COLMAP reconstruction with global mapper..."
python3 scripts/run_colmap.py \
    --images_dir "$FRAMES_DIR" \
    --output_dir "$COLMAP_DIR" \
    --camera_model OPENCV \
    --quality high \
    --use_global_mapper  # Use global mapper (was GLOMAP)

# Step 3: Train Gaussian Splatting
echo ""
echo "Step 3/3: Training Gaussian Splatting model..."
# Check if Brush is available
if command -v brush_app &> /dev/null; then
    echo "Using Brush for training..."
    RUST_BACKTRACE=1 brush_app \
        --export-path "$MODEL_DIR" \
        --total-steps 30000 \
        "$COLMAP_DIR"
else
    # Fall back to python training script
    echo "Using Python training script..."
    python3 scripts/train_gaussian_splat.py \
        --source_path "$COLMAP_DIR" \
        --model_path "$MODEL_DIR" \
        --iterations 30000
fi

echo ""
echo "======================================"
echo "Pipeline Complete!"
echo "======================================"
echo "Model saved to: $MODEL_DIR"
echo "Look for: ${MODEL_DIR}/point_cloud.ply"
echo "======================================"
echo ""
echo "Next steps:"
echo "1. Open Blender (5.2 LTS or 4.5 LTS)"
echo "2. Install KIRI 3DGS Render addon"
echo "3. Import the PLY file: ${MODEL_DIR}/point_cloud.ply"
echo "4. Render and create amazing visualizations!"
echo ""
