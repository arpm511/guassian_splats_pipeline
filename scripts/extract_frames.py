"""
Video to Frames Extraction Script

Extracts frames from video input for Gaussian Splatting processing.
"""

import cv2
import os
import argparse
from pathlib import Path
from tqdm import tqdm


def extract_frames(video_path, output_dir, fps=None, max_frames=None, quality=95):
    """
    Extract frames from video file.
    
    Args:
        video_path: Path to input video file
        output_dir: Directory to save extracted frames
        fps: Target frames per second (None = use original fps)
        max_frames: Maximum number of frames to extract (None = all frames)
        quality: JPEG quality for saved frames (0-100)
    """
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Open video
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")
    
    # Get video properties
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Video FPS: {original_fps}")
    print(f"Total frames in video: {total_frames}")
    
    # Calculate frame skip if fps is specified
    frame_skip = 1
    if fps is not None and fps < original_fps:
        frame_skip = int(original_fps / fps)
        print(f"Extracting every {frame_skip} frame(s) to achieve ~{fps} FPS")
    
    # Extract frames
    frame_count = 0
    saved_count = 0
    
    with tqdm(total=min(total_frames, max_frames) if max_frames else total_frames, 
              desc="Extracting frames") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Check if we should save this frame
            if frame_count % frame_skip == 0:
                # Save frame
                frame_filename = output_dir / f"frame_{saved_count:06d}.jpg"
                cv2.imwrite(
                    str(frame_filename), 
                    frame,
                    [cv2.IMWRITE_JPEG_QUALITY, quality]
                )
                saved_count += 1
                pbar.update(1)
                
                if max_frames and saved_count >= max_frames:
                    break
            
            frame_count += 1
    
    cap.release()
    print(f"\nExtracted {saved_count} frames to {output_dir}")
    return saved_count


def main():
    parser = argparse.ArgumentParser(
        description="Extract frames from video for Gaussian Splatting"
    )
    parser.add_argument(
        "video_path",
        type=str,
        help="Path to input video file"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="data/processed/frames",
        help="Output directory for frames (default: data/processed/frames)"
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=None,
        help="Target frames per second (default: use video fps)"
    )
    parser.add_argument(
        "--max_frames",
        type=int,
        default=None,
        help="Maximum number of frames to extract (default: all)"
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=95,
        help="JPEG quality 0-100 (default: 95)"
    )
    
    args = parser.parse_args()
    
    # Validate input
    if not os.path.exists(args.video_path):
        raise FileNotFoundError(f"Video file not found: {args.video_path}")
    
    # Extract frames
    extract_frames(
        args.video_path,
        args.output_dir,
        fps=args.fps,
        max_frames=args.max_frames,
        quality=args.quality
    )


if __name__ == "__main__":
    main()
