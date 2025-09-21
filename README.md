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

# 2. Reorganize files (flatten directory structure with renamed files)
# Move all PLY files to top level with directory name prepended

# 3. Run the parsing script
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
