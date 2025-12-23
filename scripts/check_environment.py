#!/usr/bin/env python3
"""
Utility script to validate project setup and environment.
Run this to check if everything is configured correctly.
"""

import sys
import subprocess
from pathlib import Path


def check_command(command, name):
    """Check if a command is available."""
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"✓ {name} is installed")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print(f"✗ {name} is NOT installed")
    return False


def check_python_package(package_name, import_name=None):
    """Check if a Python package is installed."""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✓ Python package '{package_name}' is installed")
        return True
    except ImportError:
        print(f"✗ Python package '{package_name}' is NOT installed")
        return False


def check_directory(path, name):
    """Check if a directory exists."""
    if Path(path).exists():
        print(f"✓ Directory '{name}' exists")
        return True
    else:
        print(f"✗ Directory '{name}' does NOT exist")
        return False


def check_gpu():
    """Check NVIDIA GPU availability."""
    try:
        result = subprocess.run(
            ["nvidia-smi"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ NVIDIA GPU detected")
            print(f"  {result.stdout.split('NVIDIA')[1].split('|')[0].strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("✗ NVIDIA GPU not detected (nvidia-smi failed)")
    return False


def check_cuda():
    """Check CUDA availability in PyTorch."""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"✓ CUDA is available in PyTorch")
            print(f"  CUDA version: {torch.version.cuda}")
            print(f"  GPU count: {torch.cuda.device_count()}")
            if torch.cuda.device_count() > 0:
                print(f"  GPU 0: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print("✗ CUDA is NOT available in PyTorch")
            return False
    except ImportError:
        print("✗ PyTorch not installed, cannot check CUDA")
        return False


def main():
    print("=" * 60)
    print("Gaussian Splatting Pipeline - Environment Check")
    print("=" * 60)
    print()
    
    # Track overall status
    all_checks_passed = True
    
    print("Checking system commands...")
    print("-" * 60)
    checks = [
        check_command("python", "Python"),
        check_command("python3", "Python3"),
        check_command("git", "Git"),
        check_command("colmap", "COLMAP"),
        check_command("docker", "Docker"),
    ]
    all_checks_passed &= any(checks[:2])  # Either python or python3
    print()
    
    print("Checking GPU & CUDA...")
    print("-" * 60)
    check_gpu()
    check_cuda()
    print()
    
    print("Checking Python packages...")
    print("-" * 60)
    packages = [
        ("numpy", "numpy"),
        ("opencv-python", "cv2"),
        ("torch", "torch"),
        ("torchvision", "torchvision"),
        ("pillow", "PIL"),
        ("tqdm", "tqdm"),
        ("plyfile", "plyfile"),
    ]
    for package, import_name in packages:
        check_python_package(package, import_name)
    print()
    
    print("Checking project structure...")
    print("-" * 60)
    directories = [
        ("data/input/videos", "Input videos"),
        ("data/processed/frames", "Processed frames"),
        ("data/processed/colmap", "COLMAP output"),
        ("data/output/splats", "Output splats"),
        ("scripts", "Scripts"),
        ("docs", "Documentation"),
        ("example", "Example"),
    ]
    for path, name in directories:
        check_directory(path, name)
    print()
    
    print("Checking key files...")
    print("-" * 60)
    files = [
        "README.md",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml",
        "scripts/extract_frames.py",
        "scripts/run_colmap.py",
        "scripts/train_gaussian_splat.py",
    ]
    for filepath in files:
        if Path(filepath).exists():
            print(f"✓ {filepath} exists")
        else:
            print(f"✗ {filepath} is missing")
    print()
    
    print("=" * 60)
    print("Environment Check Complete")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Install any missing dependencies")
    print("2. Review IMPLEMENTATION_GUIDE.md for detailed setup")
    print("3. Run your first pipeline: ./scripts/pipeline.sh <video> <project>")
    print()


if __name__ == "__main__":
    main()
