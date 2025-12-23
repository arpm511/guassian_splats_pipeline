#!/bin/bash
# Complete pipeline script for Gaussian Splatting
# Usage: ./pipeline.sh <video_path> <project_name>

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
echo "Gaussian Splatting Pipeline"
echo "======================================"
echo "Video: $VIDEO_PATH"
echo "Project: $PROJECT_NAME"
echo "======================================"

# Setup directories
FRAMES_DIR="data/processed/frames/${PROJECT_NAME}"
COLMAP_DIR="data/processed/colmap/${PROJECT_NAME}"
MODEL_DIR="data/output/splats/${PROJECT_NAME}"

mkdir -p "$FRAMES_DIR" "$COLMAP_DIR" "$MODEL_DIR"

# Step 1: Extract frames from video
echo ""
echo "Step 1/3: Extracting frames from video..."
python3 scripts/extract_frames.py \
    "$VIDEO_PATH" \
    --output_dir "$FRAMES_DIR" \
    --fps 2 \
    --quality 95

# Step 2: Run COLMAP
echo ""
echo "Step 2/3: Running COLMAP reconstruction..."
python3 scripts/run_colmap.py \
    --images_dir "$FRAMES_DIR" \
    --output_dir "$COLMAP_DIR" \
    --camera_model OPENCV \
    --quality high

# Step 3: Train Gaussian Splatting
echo ""
echo "Step 3/3: Training Gaussian Splatting model..."
python3 scripts/train_gaussian_splat.py \
    --source_path "$COLMAP_DIR" \
    --model_path "$MODEL_DIR" \
    --iterations 30000 \
    --export_ply "${MODEL_DIR}/point_cloud.ply"

echo ""
echo "======================================"
echo "Pipeline Complete!"
echo "======================================"
echo "Model saved to: $MODEL_DIR"
echo "PLY file for Blender: ${MODEL_DIR}/point_cloud.ply"
echo "======================================"
