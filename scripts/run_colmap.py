"""
COLMAP + GLOMAP Processing Script

Runs Structure-from-Motion (SfM) using COLMAP for feature extraction/matching
and GLOMAP for faster sparse reconstruction.
"""

import os
import subprocess
import argparse
import shutil
from pathlib import Path


def run_colmap(
    images_dir,
    output_dir,
    camera_model="OPENCV",
    quality="high",
    gpu=True,
    use_glomap=True
):
    """
    Run COLMAP + GLOMAP pipeline on images.
    
    Args:
        images_dir: Directory containing input images
        output_dir: Directory for COLMAP output
        camera_model: Camera model (OPENCV, PINHOLE, RADIAL, etc.)
        quality: Processing quality (high, medium, low)
        gpu: Use GPU acceleration
        use_glomap: Use GLOMAP for reconstruction (faster) instead of COLMAP mapper
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
    
    subprocess.run(feature_cmd, check=True)
    
    print("\n" + "=" * 60)
    print("COLMAP Feature Matching")
    print("=" * 60)
    
    # Feature matching
    matching_cmd = [
        "colmap", "exhaustive_matcher",
        "--database_path", str(database_path),
    ]
    
    if gpu:
        matching_cmd.extend(["--SiftMatching.use_gpu", "1"])
    
    subprocess.run(matching_cmd, check=True)
    
    # Sparse reconstruction - use GLOMAP or COLMAP mapper
    if use_glomap and shutil.which("glomap"):
        print("\n" + "=" * 60)
        print("GLOMAP Sparse Reconstruction (Faster)")
        print("=" * 60)
        
        # GLOMAP mapper (much faster than COLMAP)
        mapper_cmd = [
            "glomap", "mapper",
            "--database_path", str(database_path),
            "--image_path", str(images_dir),
            "--output_path", str(sparse_dir),
        ]
        
        subprocess.run(mapper_cmd, check=True)
    else:
        if use_glomap:
            print("\nWarning: GLOMAP not found, falling back to COLMAP mapper")
        
        print("\n" + "=" * 60)
        print("COLMAP Sparse Reconstruction")
        print("=" * 60)
        
        # COLMAP mapper (slower but reliable fallback)
        mapper_cmd = [
            "colmap", "mapper",
            "--database_path", str(database_path),
            "--image_path", str(images_dir),
            "--output_path", str(sparse_dir),
        ]
        
        subprocess.run(mapper_cmd, check=True)
    
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
        "--no_glomap",
        action="store_true",
        help="Use COLMAP mapper instead of GLOMAP (slower but more compatible)"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not Path(args.images_dir).exists():
        raise FileNotFoundError(f"Images directory not found: {args.images_dir}")
    
    # Run COLMAP + GLOMAP
    run_colmap(
        args.images_dir,
        args.output_dir,
        camera_model=args.camera_model,
        quality=args.quality,
        gpu=not args.no_gpu,
        use_glomap=not args.no_glomap
    parser.add_argument(
        "--no_gpu",
        action="store_true",
        help="Disable GPU acceleration"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not Path(args.images_dir).exists():
        raise FileNotFoundError(f"Images directory not found: {args.images_dir}")
    
    # Run COLMAP
    run_colmap(
        args.images_dir,
        args.output_dir,
        camera_model=args.camera_model,
        quality=args.quality,
        gpu=not args.no_gpu
    )


if __name__ == "__main__":
    main()
