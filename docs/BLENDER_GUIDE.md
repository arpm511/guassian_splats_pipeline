# Blender Gaussian Splatting Visualization Guide

This guide covers importing and visualizing Gaussian Splats in Blender.

## Installation

### Required Software
- Blender 4.5 or later (Blender 4.2+ works, but 4.5 is recommended)
- Kiri 3DGS Render Add-on

### Installing the Add-on

1. **Download the Add-on**
   - Visit [Kiri 3DGS Render Add-on](https://github.com/KIRI-Innovation/kiri-3dgs-blender-addon)
   - Go to the [Releases section](https://github.com/KIRI-Innovation/kiri-3dgs-blender-addon/releases)
   - For Blender 4.5: Download the latest version
   - For Blender 4.2-4.4: Download version 4.0 from the releases
   - Save the ZIP file (do NOT extract it)

2. **Install in Blender**
   - Open Blender 4.5
   - Drag and drop the downloaded ZIP file directly into Blender
   - Click `OK` to install the add-on
   - Alternatively: Go to `Edit` → `Preferences` → `Add-ons` → `Install...` and select the ZIP

3. **Verify Installation**
   - Go to `Edit` → `Preferences` → `Add-ons`
   - Search for "3DGS" or "Kiri"
   - Ensure the checkbox is enabled next to "3D View: Kiri 3DGS Render"
   - You should see a 3DGS panel in the N-panel of the 3D viewport

## Importing Your Gaussian Splat

### Step 1: Import PLY File

1. **Open Blender**
   - Start with a new project or open existing scene
   - Delete the default cube, light, and camera (optional, but cleaner)

2. **Open the 3DGS Panel**
   - Press `N` to open the properties panel on the right side of the 3D viewport
   - Click on the `3DGS Render` tab
   - You should see the Kiri 3DGS Render controls

3. **Import Gaussian Splat**
   - In the 3DGS Render panel, click `Import PLY`
   - Navigate to your PLY file:
     ```
     data/output/splats/<project_name>/point_cloud.ply
     ```
   - Select the PLY file and click `Import PLY`
   - The splat will be imported as a point cloud object

### Step 2: Initial Setup

After importing, you should see a point cloud in the viewport:

1. **View the Gaussian Splat**
   - Change viewport shading to `Rendered` mode (press `Z` and select `Rendered`)
   - Or click the sphere icon in the top-right of the viewport
   - You should now see your Gaussian Splat rendered in real-time

2. **Navigation**
   - Middle mouse button: Rotate view
   - Scroll wheel: Zoom in/out
   - Shift + middle mouse: Pan

2. **Adjust Viewport Display**
   - Press `Z` and select display mode
   - `Solid` or `Material Preview` works best initially

## Scene Setup

### Lighting

Gaussian Splats are pre-lit from the training data, but you may want to add additional lighting:

```
1. Add lights for artistic effect:
   - Key light (main light source)
   - Fill light (soften shadows)
   - Rim light (highlight edges)

2. Use environment lighting:
   - Switch to Shader Editor
   - Add Environment Texture
   - Load an HDRI image
```

### Camera Setup

1. **Position Camera**
   - Select the camera (`Camera` in outliner)
   - Press `G` to move, `R` to rotate
   - Press `Numpad 0` to view through camera

2. **Camera Settings**
   - Focal length: 35-50mm for natural perspective
   - Depth of Field: Optional, but can add cinematic effect

### Render Settings

#### For Quick Previews (EEVEE)

```
Render Engine: Eevee
Sampling: 32-64 samples
Viewport Samples: 16
```

#### For High Quality (Cycles)

```
Render Engine: Cycles
Sampling: 512-2048 samples
Device: GPU Compute (if available)
```

## Advanced Techniques

### Creating a Turntable Animation

1. **Add an Empty Object**
   - `Add` → `Empty` → `Plain Axes`
   - Position at center of your Gaussian Splat

2. **Parent Camera to Empty**
   - Select camera, then shift-select empty
   - Press `Ctrl+P` → `Object`

3. **Animate Rotation**
   - Select the empty
   - Frame 1: Press `I` → `Rotation`
   - Frame 240: Rotate 360° on Z axis, press `I` → `Rotation`
   - Set frame range to 1-240

4. **Render Animation**
   - Set output location and format
   - `Render` → `Render Animation`

### Compositing

Add post-processing effects:

1. **Enable Compositing**
   - Switch to Compositing workspace
   - Check "Use Nodes"

2. **Common Effects**
   - Color correction
   - Glare/bloom
   - Vignette
   - Chromatic aberration

### Mixing with 3D Geometry

You can combine Gaussian Splats with traditional 3D models:

1. **Add 3D Objects**
   - Import or create 3D meshes
   - Position them in your scene

2. **Lighting Considerations**
   - Match lighting to your Gaussian Splat's baked lighting
   - Use similar color temperature

## Troubleshooting

### Import Issues

**Problem: Add-on not appearing**
- Ensure you have Blender 3.6+
- Check add-on is enabled in Preferences
- Restart Blender

**Problem: PLY file doesn't import**
- Verify PLY file exists and isn't corrupted
- Check file path doesn't contain special characters
- Try re-exporting from training script

### Display Issues

**Problem: Splat looks wrong or distorted**
- Check camera settings match training data
- Verify correct import settings
- Try adjusting splat size/opacity in add-on settings

**Problem: Performance is slow**
- Reduce viewport samples
- Use smaller splat point size
- Cull invisible splats

### Rendering Issues

**Problem: Render is too dark/bright**
- Adjust exposure in render settings
- Check lighting setup
- Modify splat opacity settings

**Problem: Artifacts in render**
- Increase sample count
- Check for overlapping geometry
- Adjust denoising settings

## Tips for Best Results

1. **Lighting**
   - Keep it simple; splats are pre-lit
   - Add subtle environment lighting for reflections
   - Avoid harsh additional lights

2. **Camera**
   - Stay within the bounds of training viewpoints
   - Extreme angles may show artifacts
   - Use cameras similar to training data

3. **Performance**
   - Large splats can be heavy
   - Consider decimating for viewport work
   - Render on GPU for better performance

4. **Output**
   - Use PNG format for final renders (lossless)
   - Set resolution to at least 1080p
   - Enable transparent background if needed

## Resources

- [Blender Manual](https://docs.blender.org/)
- [Gaussian Splatting Blender Add-on Docs](https://github.com/ReshotAI/gaussian-splatting-blender-addon)
- [Blender Artists Forum](https://blenderartists.org/)

## Example Renders

<!-- TODO: Add example renders showing different techniques -->

### Basic Render
![Basic Render](../docs/images/blender_basic.png)

### Turntable Animation
![Turntable](../docs/images/blender_turntable.gif)

### Mixed with 3D Geometry
![Mixed Scene](../docs/images/blender_mixed.png)

---

For more help, check the main [README](../README.md) or open an issue on GitHub.
