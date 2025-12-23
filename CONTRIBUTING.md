# Contributing to Gaussian Splatting Pipeline

Thank you for considering contributing to this project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, GPU, CUDA version)
- Error messages or logs

### Suggesting Enhancements

Feature requests are welcome! Please include:
- Clear description of the feature
- Use case and benefits
- Any implementation ideas

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/gaussian-splats.git
   cd gaussian-splats
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   - Run through the full pipeline
   - Verify Docker builds work
   - Check documentation renders correctly

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of changes"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

## Code Style

### Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

Example:
```python
def extract_frames(video_path, output_dir, fps=None):
    """
    Extract frames from video file.
    
    Args:
        video_path: Path to input video
        output_dir: Directory for output frames
        fps: Target frames per second (None = original)
    
    Returns:
        Number of frames extracted
    """
    # Implementation here
    pass
```

### Documentation
- Use clear, concise language
- Include code examples where helpful
- Update README.md if adding features
- Add comments for TODO items

## Project Structure

Please maintain the existing structure:
```
gaussian_splats/
├── data/           # Data directories (not committed)
├── scripts/        # Python scripts and automation
├── docs/           # Documentation and guides
├── docker/         # Docker-related files
└── example/        # Example projects and results
```

## Testing

Before submitting:
- Test on at least one complete dataset
- Verify Docker build succeeds
- Check all scripts run without errors
- Validate documentation accuracy

## Review Process

1. Maintainer will review PR within 1 week
2. May request changes or clarifications
3. Once approved, changes will be merged
4. You'll be added to contributors list!

## Community Guidelines

- Be respectful and constructive
- Help others in discussions and issues
- Share your results and learnings
- Credit others' work appropriately

## Questions?

Feel free to:
- Open a discussion on GitHub
- Comment on related issues
- Reach out directly (see README for contact)

Thank you for contributing! 🎉
