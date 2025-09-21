#!/usr/bin/env python3
"""
Script to flatten the Crops3D directory structure.
Prepends directory names to filenames and moves all PLY files to the current directory.

Usage:
    python flatten_crops3d.py
    
    Or with custom paths:
    python flatten_crops3d.py --source Crops3D/Crops3D --target ./flattened_data
"""

import os
import shutil
import argparse
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
        print("\nExpected directory structure:")
        print("  Crops3D/")
        print("  └── Crops3D/")
        print("      ├── Cabbage/")
        print("      ├── Cotton/")
        print("      ├── Maize/")
        print("      └── ...")
        return False
    
    # Create target directory if it doesn't exist
    target_path.mkdir(parents=True, exist_ok=True)
    
    # Get all crop subdirectories
    crop_dirs = [d for d in source_path.iterdir() if d.is_dir()]
    
    if not crop_dirs:
        print(f"No subdirectories found in {source_dir}")
        return False
    
    total_files = 0
    moved_files = 0
    skipped_files = []
    
    print(f"Found {len(crop_dirs)} crop directories:")
    for crop_dir in sorted(crop_dirs):
        ply_count = len(list(crop_dir.glob("*.ply")))
        print(f"  - {crop_dir.name}: {ply_count} PLY files")
    
    print("\nStarting to flatten directory structure...")
    print("="*50)
    
    for crop_dir in sorted(crop_dirs):
        crop_name = crop_dir.name
        ply_files = sorted(list(crop_dir.glob("*.ply")))
        
        if ply_files:
            print(f"\nProcessing {crop_name}: {len(ply_files)} files")
            
            for ply_file in ply_files:
                # Create new filename with crop name prepended
                new_filename = f"{crop_name}-{ply_file.name}"
                target_file = target_path / new_filename
                
                # Copy or move the file
                if target_file.exists():
                    skipped_files.append(new_filename)
                    print(f"  ⏩ Skipping {new_filename} (already exists)")
                else:
                    shutil.copy2(ply_file, target_file)
                    moved_files += 1
                    if moved_files <= 5 or moved_files % 50 == 0:  # Show first 5 and every 50th
                        print(f"  ✓ Copied: {ply_file.name} -> {new_filename}")
                
                total_files += 1
    
    print(f"\n{'='*50}")
    print(f"✅ Flattening complete!")
    print(f"Total files processed: {total_files}")
    print(f"Files copied: {moved_files}")
    print(f"Files skipped (already exist): {len(skipped_files)}")
    
    if skipped_files and len(skipped_files) <= 10:
        print("\nSkipped files:")
        for f in skipped_files[:10]:
            print(f"  - {f}")
    
    # Verify the result
    ply_count = len(list(target_path.glob("*.ply")))
    print(f"\nTotal PLY files in {target_dir}: {ply_count}")
    
    # Show count per crop type
    print("\nFinal file count per crop type:")
    crop_counts = {}
    for crop_dir in sorted(crop_dirs):
        crop_name = crop_dir.name
        crop_files = list(target_path.glob(f"{crop_name}-*.ply"))
        if crop_files:
            crop_counts[crop_name] = len(crop_files)
            print(f"  {crop_name:12} : {len(crop_files):4} files")
    
    # Expected totals based on the README
    expected = {
        'Maize': 225, 'Cabbage': 196, 'Cotton': 176, 'Rapeseed': 150,
        'Wheat': 148, 'Potato': 118, 'Rice': 84, 'Tomato': 83
    }
    
    print("\nVerification against expected counts:")
    all_match = True
    for crop, expected_count in expected.items():
        actual_count = crop_counts.get(crop, 0)
        if actual_count == expected_count:
            print(f"  ✓ {crop}: {actual_count} (matches expected)")
        else:
            print(f"  ✗ {crop}: {actual_count} (expected {expected_count})")
            all_match = False
    
    if all_match:
        print("\n🎉 All crop counts match expected values!")
    
    return True

def main():
    parser = argparse.ArgumentParser(
        description='Flatten the Crops3D directory structure for processing with FiftyOne'
    )
    parser.add_argument(
        '--source', 
        default='Crops3D/Crops3D',
        help='Source directory containing crop subdirectories (default: Crops3D/Crops3D)'
    )
    parser.add_argument(
        '--target', 
        default='.',
        help='Target directory for flattened files (default: current directory)'
    )
    
    args = parser.parse_args()
    
    success = flatten_crops3d_directory(args.source, args.target)
    
    if success:
        print("\n📝 Next steps:")
        print("1. Run: python parse_crops3d_to_fiftyone.py")
        print("2. Launch FiftyOne to visualize the dataset")
        return 0
    else:
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
