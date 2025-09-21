# Crops3D Dataset

## Overview

Crops3D is a comprehensive 3D agricultural dataset designed for realistic perception and segmentation tasks in precision agriculture. The dataset features high-quality 3D point cloud data from diverse real-world agricultural scenarios, providing a valuable resource for researchers and practitioners working on agricultural computer vision applications.

## Dataset Information

- **Paper**: [Crops3D: a diverse 3D crop dataset for realistic perception and segmentation toward agricultural applications](https://doi.org/10.1038/s41597-024-04290-0)

- **Authors**: Jianzhong Zhu, Ruifang Zhai, He Ren, Kai Xie, Aobo Du, Xinwei He, Chenxi Cui, Yinghua Wang, Junli Ye, Jiashi Wang, Xue Jiang, Yulong Wang, Chenglong Huang, Wanneng Yang

- **Publication**: Scientific Data, 2024

## Download

The complete dataset can be downloaded from:
**[https://springernature.figshare.com/ndownloader/files/50027964](https://springernature.figshare.com/ndownloader/files/50027964)**

- **File Size**: ~9GB (compressed ZIP file)

- **Format**: PLY point cloud files with RGB color information

## Dataset Statistics

The dataset contains **1,180 high-quality 3D point cloud samples** across 8 different crop types:

| Crop Type | Number of Samples |
|-----------|------------------|
| Maize     | 225              |
| Cabbage   | 196              |
| Cotton    | 176              |
| Rapeseed  | 150              |
| Wheat     | 148              |
| Potato    | 118              |
| Rice      | 84               |
| Tomato    | 83               |
| **Total** | **1,180**        |

## Key Features

- **Diversity**: Multiple point cloud acquisition methods and eight distinct crop types

- **Authenticity**: Real-world agricultural settings with natural variations

- **Complexity**: Intricate crop structures with substantial self-occlusion and varying growth stages

- **High Quality**: RGB-colored point clouds with detailed geometric information

## Supported Tasks

The dataset is designed to support three critical tasks in 3D crop phenotyping:

1. **Instance Segmentation**: Precise segmentation of individual plants in agricultural plots

2. **Plant Type Classification**: Accurate identification and classification of different crop types

3. **Plant Organ Segmentation**: Detailed segmentation of plant organs for fine-grained analysis

## Directory Structure

### Original Dataset Structure
The original Crops3D.zip contains several directories:

```
Crops3D/
├── Crops3D/           # Raw annotated point cloud data
│   ├── Cabbage/       # PLY files for each crop type
│   ├── Cotton/
│   ├── Maize/
│   ├── Potato/
│   ├── Rapeseed/
│   ├── Rice/
│   ├── Tomato/
│   └── Wheat/
├── Crops3D_10k/       # Subsampled to 10,000 points using FPS
├── Crops3D_10k-C/     # Corruption robustness test data
└── Crops3D_IS/        # Instance segmentation data
```

### Current Working Directory Structure
For ease of processing with the included parsing script, the files have been reorganized:

- Directory names are prepended to filenames (e.g., `Cabbage-mvs_1005_01.ply`)

- All PLY files are consolidated at the top level

- This flat structure is expected by `parse_crops3d_to_fiftyone.py`

### Flattening Script

Use this Python script to automatically flatten the directory structure after extracting the dataset:

```python
#!/usr/bin/env python3
"""
Script to flatten the Crops3D directory structure.
Prepends directory names to filenames and moves all PLY files to the current directory.
"""

import os
import shutil
from pathlib import Path

def flatten_crops3d_directory(source_dir="Crops3D/Crops3D", target_dir="."):
    """
    Flatten the Crops3D directory structure by prepending crop names to filenames.
    
    Args:
        source_dir: Path to the Crops3D/Crops3D directory containing crop subdirectories
        target_dir: Directory where flattened files will be placed (default: current directory)
    """
    source_path = Path(source_dir)
    target_path = Path(target_dir)
    
    if not source_path.exists():
        print(f"Error: Source directory '{source_dir}' not found!")
        print("Make sure you've extracted the Crops3D.zip file first.")
        return
    
    # Get all crop subdirectories
    crop_dirs = [d for d in source_path.iterdir() if d.is_dir()]
    
    if not crop_dirs:
        print(f"No subdirectories found in {source_dir}")
        return
    
    total_files = 0
    moved_files = 0
    
    print(f"Found {len(crop_dirs)} crop directories")
    print("Starting to flatten directory structure...")
    
    for crop_dir in crop_dirs:
        crop_name = crop_dir.name
        ply_files = list(crop_dir.glob("*.ply"))
        
        print(f"\nProcessing {crop_name}: {len(ply_files)} files")
        
        for ply_file in ply_files:
            # Create new filename with crop name prepended
            new_filename = f"{crop_name}-{ply_file.name}"
            target_file = target_path / new_filename
            
            # Copy or move the file
            if target_file.exists():
                print(f"  Skipping {new_filename} (already exists)")
            else:
                shutil.copy2(ply_file, target_file)
                moved_files += 1
                print(f"  Copied: {ply_file.name} -> {new_filename}")
            
            total_files += 1
    
    print(f"\n{'='*50}")
    print(f"Flattening complete!")
    print(f"Total files processed: {total_files}")
    print(f"Files copied: {moved_files}")
    print(f"Files skipped (already exist): {total_files - moved_files}")
    
    # Verify the result
    ply_count = len(list(target_path.glob("*.ply")))
    print(f"\nTotal PLY files in {target_dir}: {ply_count}")
    
    # Show sample of files for each crop type
    print("\nSample files per crop type:")
    for crop_dir in crop_dirs:
        crop_name = crop_dir.name
        crop_files = list(target_path.glob(f"{crop_name}-*.ply"))
        if crop_files:
            print(f"  {crop_name}: {len(crop_files)} files")

if __name__ == "__main__":
    # Run the flattening process
    flatten_crops3d_directory()
```

## Usage with FiftyOne

The repository includes a parsing script `parse_crops3d_to_fiftyone.py` that:

1. Loads all PLY files from the current directory

2. Extracts crop type from filenames

3. Creates FiftyOne 3D scenes (.fo3d files) for visualization

4. Builds a FiftyOne dataset with classification labels

### Quick Start

```bash
# 1. Download and extract the dataset
wget https://springernature.figshare.com/ndownloader/files/50027964 -O Crops3D.zip
unzip Crops3D.zip

# 2. Flatten the directory structure
# Save the flattening script from above as flatten_crops3d.py, then run:
python flatten_crops3d.py

# Alternative: Run the flattening code directly
python -c "
from pathlib import Path
import shutil

source = Path('Crops3D/Crops3D')
if source.exists():
    for crop_dir in source.iterdir():
        if crop_dir.is_dir():
            for ply in crop_dir.glob('*.ply'):
                new_name = f'{crop_dir.name}-{ply.name}'
                shutil.copy2(ply, new_name)
                print(f'Copied: {new_name}')
    print('Flattening complete!')
else:
    print('Crops3D/Crops3D directory not found!')
"

# 3. Run the parsing script to create FiftyOne dataset
python parse_crops3d_to_fiftyone.py

# 4. Launch FiftyOne to visualize
python -c "import fiftyone as fo; session = fo.launch_app(fo.load_dataset('crops3d'))"
```

## File Format

Each PLY file contains:
- **3D Point Coordinates**: X, Y, Z positions

- **RGB Color Information**: Red, Green, Blue values for each point

- **Point Cloud Density**: Varies by acquisition method and crop type

Example filename patterns:

- `Cabbage-mvs_1005_01.ply` (Multi-view stereo acquisition)

- `Cabbage-sl_901_02.ply` (Structured light acquisition)

- `Cotton-1.ply` (Simple numbered format)

- `Maize-1-1.ply` (Multi-part numbering)

## Citation

If you use this dataset in your research, please cite:

```bibtex
@article{zhu2024crops3d,
  title={Crops3D: a diverse 3D crop dataset for realistic perception and segmentation toward agricultural applications},
  author={Zhu, Jianzhong and Zhai, Ruifang and Ren, He and Xie, Kai and Du, Aobo and He, Xinwei and Cui, Chenxi and Wang, Yinghua and Ye, Junli and Wang, Jiashi and Jiang, Xue and Wang, Yulong and Huang, Chenglong and Yang, Wanneng},
  journal={Scientific Data},
  volume={11},
  number={1438},
  year={2024},
  doi={10.1038/s41597-024-04290-0},
  publisher={Nature Publishing Group}
}
```

## License

The Crops3D dataset is released under the **Creative Commons Attribution 4.0 International License (CC BY 4.0)**. This license allows for sharing and adaptation of the dataset, provided appropriate credit is given.

## Additional Resources

- **GitHub Repository**: [https://github.com/clawCa/Crops3D](https://github.com/clawCa/Crops3D)

- **Figshare Page**: [https://figshare.com/articles/dataset/Crops3D_a_diverse_3D_crop_dataset_for_realistic_perception_and_segmentation_toward_agricultural_applications/27313272](https://figshare.com/articles/dataset/Crops3D_a_diverse_3D_crop_dataset_for_realistic_perception_and_segmentation_toward_agricultural_applications/27313272)

- **Paper DOI**: [10.1038/s41597-024-04290-0](https://doi.org/10.1038/s41597-024-04290-0)


## Notes

- The dataset has been uploaded to Hugging Face for easier access

- Point clouds can be visualized directly in FiftyOne's 3D viewer

- Each crop type exhibits unique structural characteristics and growth patterns

- The dataset includes samples from different acquisition methods (multi-view stereo and structured light)

## Contact

For questions about this specific repository setup, please open an issue. For questions about the original dataset, please refer to the paper authors.
