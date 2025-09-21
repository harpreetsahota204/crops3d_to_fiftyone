#!/usr/bin/env python3
"""
Script to parse Crops3D PLY files into a FiftyOne dataset.
Each PLY file will be added as a sample with classification based on the crop type.
The resulting FO3D files will have the same name as the original PLY files.
"""

import os
from pathlib import Path
import fiftyone as fo
from tqdm import tqdm

def get_crop_type_from_filename(filename):
    """
    Extract the crop type from the filename.
    Files are named like: Cabbage-mvs_1005_01.ply, Cotton-1.ply, Maize-1-1.ply, etc.
    """
    # Remove .ply extension
    name_without_ext = filename.replace('.ply', '')
    
    # The crop type is the prefix before the first hyphen
    if '-' in name_without_ext:
        crop_type = name_without_ext.split('-')[0]
        return crop_type
    
    return "Unknown"

def process_point_cloud(point_cloud_path, output_path):
    """
    Process a PLY point cloud file and create a FiftyOne 3D scene.
    """
    # Use relative path for the PLY file
    
    # Create a new FiftyOne 3D scene
    scene = fo.Scene()
    # Set camera to use Y-up coordinate system which is standard for 3D
    scene.camera = fo.PerspectiveCamera(up="-Y")

    # Create a mesh from the point cloud with RGB coloring
    mesh = fo.PlyMesh(
        name="mesh",  # Name of the mesh in the scene
        ply_path=point_cloud_path,  # Use relative path
        is_point_cloud=True,  # Treat as point cloud rather than mesh
        center_geometry=True,
    )

    # Add the mesh to our scene
    scene.add(mesh)
    
    # Save the scene as a .fo3d file
    scene.write(output_path)
    print(f"Processed: {os.path.basename(point_cloud_path)} -> {os.path.basename(output_path)}")

def create_fiftyone_dataset(data_dir=".", dataset_name="crops3d"):
    """
    Create a FiftyOne dataset from PLY files in the specified directory.
    """
    data_path = Path(data_dir)

    # Create new dataset
    print(f"Creating FiftyOne dataset: {dataset_name}")
    dataset = fo.Dataset(name=dataset_name, persistent=True, overwrite=True)
    
    # Get all PLY files
    ply_files = sorted(list(data_path.glob("*.ply")))
    print(f"Found {len(ply_files)} PLY files")
    
    if not ply_files:
        print("No PLY files found in the specified directory!")
        return None
    
    # Create samples for each PLY file
    samples = []
    
    print("Processing PLY files and creating FO3D scenes...")
    for ply_path in tqdm(ply_files, desc="Processing"):
        # Get the filename
        filename = ply_path.name
        
        # Extract crop type from filename
        crop_type = get_crop_type_from_filename(filename)
        
        # Create the FO3D output path with same name as PLY
        fo3d_filename = filename.replace('.ply', '.fo3d')
        fo3d_path = str(data_path / fo3d_filename)
        
        # Process the point cloud and create FO3D file
        process_point_cloud(str(ply_path), fo3d_path)
        
        # Create a sample for this PLY file
        # Use the FO3D file as the filepath for 3D visualization
        sample = fo.Sample(filepath=fo3d_path)
        
        # Add classification label
        sample["crop_type"] = fo.Classification(label=crop_type)
        
        samples.append(sample)
    
    # Add all samples to dataset
    print(f"\nAdding {len(samples)} samples to dataset...")
    dataset.add_samples(samples)
    
    # Save the dataset
    dataset.save()
    print(f"Dataset '{dataset_name}' created successfully with {len(dataset)} samples!")
    
    return dataset

if __name__ == "__main__":
    # Create the dataset
    dataset = create_fiftyone_dataset(data_dir=".", dataset_name="crops3d")
