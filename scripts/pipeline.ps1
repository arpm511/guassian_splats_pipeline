# Gaussian Splatting Pipeline - Complete Workflow
# Usage: .\pipeline.ps1 -VideoPath "path\to\video.mp4" -ProjectName "my_scene"

param(
    [Parameter(Mandatory=$true)]
    [string]$VideoPath,
    
    [Parameter(Mandatory=$true)]
    [string]$ProjectName,
    
    [int]$Fps = 2,
    [int]$Iterations = 30000,
    [string]$Quality = "high"
)

$ErrorActionPreference = "Stop"

Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Gaussian Splatting Pipeline" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "Video: $VideoPath"
Write-Host "Project: $ProjectName"
Write-Host "======================================" -ForegroundColor Cyan

# Setup directories
$FramesDir = "data\processed\frames\$ProjectName"
$ColmapDir = "data\processed\colmap\$ProjectName"
$ModelDir = "data\output\splats\$ProjectName"

New-Item -ItemType Directory -Force -Path $FramesDir, $ColmapDir, $ModelDir | Out-Null

# Step 1: Extract frames
Write-Host "`nStep 1/3: Extracting frames from video..." -ForegroundColor Yellow
python scripts\extract_frames.py `
    $VideoPath `
    --output_dir $FramesDir `
    --fps $Fps `
    --quality 95

if ($LASTEXITCODE -ne 0) { throw "Frame extraction failed" }

# Step 2: Run COLMAP
Write-Host "`nStep 2/3: Running COLMAP reconstruction..." -ForegroundColor Yellow
python scripts\run_colmap.py `
    --images_dir $FramesDir `
    --output_dir $ColmapDir `
    --camera_model OPENCV `
    --quality $Quality

if ($LASTEXITCODE -ne 0) { throw "COLMAP reconstruction failed" }

# Step 3: Train Gaussian Splatting
Write-Host "`nStep 3/3: Training Gaussian Splatting model..." -ForegroundColor Yellow
python scripts\train_gaussian_splat.py `
    --source_path $ColmapDir `
    --model_path $ModelDir `
    --iterations $Iterations `
    --export_ply "$ModelDir\point_cloud.ply"

if ($LASTEXITCODE -ne 0) { throw "Training failed" }

Write-Host "`n======================================" -ForegroundColor Green
Write-Host "Pipeline Complete!" -ForegroundColor Green
Write-Host "======================================" -ForegroundColor Green
Write-Host "Model saved to: $ModelDir"
Write-Host "PLY file for Blender: $ModelDir\point_cloud.ply"
Write-Host "======================================" -ForegroundColor Green
