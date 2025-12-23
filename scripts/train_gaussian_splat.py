"""
Gaussian Splatting Training Wrapper Script

Wrapper for training Gaussian Splatting model using the COLMAP output.
"""

import os
import subprocess
import argparse
from pathlib import Path
import shutil


def train_gaussian_splatting(
    source_path,
    model_path,
    iterations=30000,
    resolution=1,
    test_iterations=None,
    save_iterations=None,
    checkpoint_iterations=None
):
    """
    Train Gaussian Splatting model.
    
    Args:
        source_path: Path to COLMAP data directory
        model_path: Output path for trained model
        iterations: Number of training iterations
        resolution: Resolution downscale factor (1 = full resolution)
        test_iterations: Iterations at which to evaluate test set
        save_iterations: Iterations at which to save model
        checkpoint_iterations: Iterations at which to save checkpoint
    """
    source_path = Path(source_path)
    model_path = Path(model_path)
    
    # Create model output directory
    model_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("Training Gaussian Splatting Model")
    print("=" * 60)
    print(f"Source path: {source_path}")
    print(f"Model path: {model_path}")
    print(f"Iterations: {iterations}")
    print("=" * 60)
    
    # Build training command
    train_cmd = [
        "python3",
        "/workspace/gaussian-splatting/train.py",
        "-s", str(source_path),
        "-m", str(model_path),
        "--iterations", str(iterations),
        "--resolution", str(resolution),
    ]
    
    if test_iterations:
        train_cmd.extend(["--test_iterations"] + [str(i) for i in test_iterations])
    else:
        train_cmd.extend(["--test_iterations", "7000", "30000"])
    
    if save_iterations:
        train_cmd.extend(["--save_iterations"] + [str(i) for i in save_iterations])
    else:
        train_cmd.extend(["--save_iterations", "7000", "30000"])
    
    if checkpoint_iterations:
        train_cmd.extend(["--checkpoint_iterations"] + [str(i) for i in checkpoint_iterations])
    
    # Run training
    try:
        subprocess.run(train_cmd, check=True)
        print("\n" + "=" * 60)
        print("Training Complete!")
        print("=" * 60)
        print(f"Model saved to: {model_path}")
    except subprocess.CalledProcessError as e:
        print(f"Training failed with error: {e}")
        raise


def export_ply(model_path, output_path=None, iteration=-1):
    """
    Export trained Gaussian Splat to PLY format for use in Blender.
    
    Args:
        model_path: Path to trained model
        output_path: Path to save PLY file (optional)
        iteration: Which iteration to export (-1 = latest)
    """
    model_path = Path(model_path)
    
    if output_path is None:
        output_path = model_path / "point_cloud.ply"
    else:
        output_path = Path(output_path)
    
    # The trained model already contains a point_cloud/iteration_XXXXX/point_cloud.ply
    # Find the latest or specified iteration
    point_cloud_dir = model_path / "point_cloud"
    
    if iteration == -1:
        # Find the latest iteration
        iteration_dirs = sorted([
            d for d in point_cloud_dir.iterdir() 
            if d.is_dir() and d.name.startswith("iteration_")
        ])
        if not iteration_dirs:
            raise FileNotFoundError("No point cloud iterations found")
        latest_dir = iteration_dirs[-1]
    else:
        latest_dir = point_cloud_dir / f"iteration_{iteration}"
    
    source_ply = latest_dir / "point_cloud.ply"
    
    if not source_ply.exists():
        raise FileNotFoundError(f"PLY file not found: {source_ply}")
    
    # Copy to output location
    shutil.copy(source_ply, output_path)
    print(f"Exported PLY to: {output_path}")
    
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Train Gaussian Splatting model"
    )
    parser.add_argument(
        "--source_path",
        type=str,
        required=True,
        help="Path to COLMAP reconstruction (parent of sparse/ directory)"
    )
    parser.add_argument(
        "--model_path",
        type=str,
        default="data/output/splats/model",
        help="Output path for trained model"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=30000,
        help="Number of training iterations"
    )
    parser.add_argument(
        "--resolution",
        type=int,
        default=1,
        help="Resolution downscale factor (1=full, 2=half, etc.)"
    )
    parser.add_argument(
        "--export_ply",
        type=str,
        default=None,
        help="Export PLY file to this path after training"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not Path(args.source_path).exists():
        raise FileNotFoundError(f"Source path not found: {args.source_path}")
    
    # Train model
    train_gaussian_splatting(
        args.source_path,
        args.model_path,
        iterations=args.iterations,
        resolution=args.resolution
    )
    
    # Export PLY if requested
    if args.export_ply:
        export_ply(args.model_path, args.export_ply)


if __name__ == "__main__":
    main()
