"""
COLMAP Processing Script (with Global Mapper support)

Runs Structure-from-Motion (SfM) using COLMAP 4.0+ which includes:
- Feature extraction and matching
- Global mapper (faster, was GLOMAP) or incremental mapper (traditional)
"""

import os
import subprocess
import argparse
import shutil
from pathlib import Path


def _run_with_display(cmd):
    """
    Run command with xvfb for headless operation.
    COLMAP requires display even in CPU mode due to Qt/OpenGL initialization.
    """
    if shutil.which("xvfb-run"):
        return ["xvfb-run", "-a", "--server-args=-screen 0 1024x768x24"] + cmd
    return cmd


def run_colmap(
    images_dir,
    output_dir,
    camera_model="OPENCV",
    quality="high",
    gpu=True,
    use_global_mapper=True
):
    """
    Run COLMAP pipeline on images with optional global mapper.
    
    Args:
        images_dir: Directory containing input images
        output_dir: Directory for COLMAP output
        camera_model: Camera model (OPENCV, PINHOLE, SIMPLE_RADIAL, etc.)
        quality: Processing quality (high, medium, low)
        gpu: Use GPU acceleration
        use_global_mapper: Use global mapper (faster, was GLOMAP) vs incremental
    """
    images_dir = Path(images_dir)
    output_dir = Path(output_dir)
    
    # Create output directories
    database_path = output_dir / "database.db"
    sparse_dir = output_dir / "sparse"
    sparse_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("COLMAP Feature Extraction")
    print("=" * 60)
    
    # Feature extraction
    feature_cmd = [
        "colmap", "feature_extractor",
        "--database_path", str(database_path),
        "--image_path", str(images_dir),
        "--ImageReader.camera_model", camera_model,
        "--ImageReader.single_camera", "1",
    ]
    
    # GPU mode (only add if GPU is enabled and available)
    if gpu:
        feature_cmd.extend(["--SiftExtraction.use_gpu", "1"])
    
    # Set quality parameters
    if quality == "high":
        feature_cmd.extend([
            "--SiftExtraction.max_image_size", "4096",
            "--SiftExtraction.max_num_features", "8192"
        ])
    elif quality == "medium":
        feature_cmd.extend([
            "--SiftExtraction.max_image_size", "2048",
            "--SiftExtraction.max_num_features", "4096"
        ])
    else:  # low
        feature_cmd.extend([
            "--SiftExtraction.max_image_size", "1024",
            "--SiftExtraction.max_num_features", "2048"
        ])
    
    subprocess.run(_run_with_display(feature_cmd), check=True)
    
    print("\n" + "=" * 60)
    print("COLMAP Feature Matching")
    print("=" * 60)
    
    # Feature matching
    matching_cmd = [
        "colmap", "exhaustive_matcher",
        "--database_path", str(database_path),
    ]
    
    # GPU mode (only add if GPU is enabled and available)
    if gpu:
        matching_cmd.extend(["--SiftMatching.use_gpu", "1"])
    
    subprocess.run(_run_with_display(matching_cmd), check=True)
    
    # Sparse reconstruction - use global mapper (fast) or incremental (robust)
    if use_global_mapper:
        print("\n" + "=" * 60)
        print("COLMAP Global Mapper (Fast, was GLOMAP)")
        print("=" * 60)
        print("Using global SfM - 10-50x faster than incremental")
        
        # COLMAP 4.0+ global mapper (was GLOMAP)
        mapper_cmd = [
            "colmap", "global_mapper",
            "--database_path", str(database_path),
            "--image_path", str(images_dir),
            "--output_path", str(sparse_dir),
        ]
        
        subprocess.run(_run_with_display(mapper_cmd), check=True)
    else:
        print("\n" + "=" * 60)
        print("COLMAP Incremental Mapper (Robust)")
        print("=" * 60)
        print("Using incremental SfM - slower but very reliable")
        
        # COLMAP incremental mapper (traditional)
        mapper_cmd = [
            "colmap", "mapper",
            "--database_path", str(database_path),
            "--image_path", str(images_dir),
            "--output_path", str(sparse_dir),
        ]
        
        subprocess.run(_run_with_display(mapper_cmd), check=True)
    
    # Find the reconstruction folder (usually '0')
    reconstruction_dirs = sorted([d for d in sparse_dir.iterdir() if d.is_dir()])
    
    if not reconstruction_dirs:
        raise RuntimeError("COLMAP reconstruction failed - no output generated")
    
    main_reconstruction = reconstruction_dirs[0]
    print(f"\nReconstruction saved to: {main_reconstruction}")
    
    print("\n" + "=" * 60)
    print("COLMAP Processing Complete!")
    print("=" * 60)
    
    return main_reconstruction


def main():
    parser = argparse.ArgumentParser(
        description="Run COLMAP Structure-from-Motion on images"
    )
    parser.add_argument(
        "--images_dir",
        type=str,
        default="data/processed/frames",
        help="Directory containing input images"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="data/processed/colmap",
        help="Output directory for COLMAP data"
    )
    parser.add_argument(
        "--use_global_mapper",
        action="store_true",
        default=True,
        help="Use global mapper (faster, was GLOMAP) instead of incremental"
    )
    parser.add_argument(
        "--no_global_mapper",
        action="store_true",
        help="Use incremental mapper instead of global (slower but more robust)"
    )
    parser.add_argument(
        "--camera_model",
        type=str,
        default="OPENCV",
        help="Camera model (OPENCV, PINHOLE, RADIAL, etc.)"
    )
    parser.add_argument(
        "--quality",
        type=str,
        default="high",
        choices=["high", "medium", "low"],
        help="Processing quality (high, medium, low)"
    )
    parser.add_argument(
        "--no_gpu",
        action="store_true",
        help="Disable GPU acceleration"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not Path(args.images_dir).exists():
        raise FileNotFoundError(f"Images directory not found: {args.images_dir}")
    
    # Run COLMAP reconstruction
    run_colmap(
        args.images_dir,
        args.output_dir,
        camera_model=args.camera_model,
        quality=args.quality,
        gpu=not args.no_gpu,
        use_global_mapper=args.use_global_mapper and not args.no_global_mapper
    )


if __name__ == "__main__":
    main()
