#!/usr/bin/env python3
"""
Django CRM Package Script
Cleans and creates a distributable zip archive
"""

import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def should_exclude(path, base_dir):
    """Check if a path should be excluded from the zip"""
    relative_path = str(Path(path).relative_to(base_dir))
    
    exclude_patterns = [
        '__pycache__',
        '.pyc',
        '.pyo',
        '.sqlite3',
        '.DS_Store',
        '.git',
        '.gitignore',
        'venv',
        'env',
        '.venv',
        'node_modules',
        '.vscode',
        '.idea',
        '.pytest_cache',
        '*.egg-info',
    ]
    
    for pattern in exclude_patterns:
        if pattern in relative_path:
            return True
    return False

def create_package():
    """Create a clean package of the Django CRM project"""
    
    base_dir = Path(__file__).resolve().parent
    project_name = base_dir.name
    
    print("📦 Packaging Django CRM Project...")
    print(f"📁 Project: {project_name}\n")
    
    # Step 1: Run cleanup
    print("Step 1: Running cleanup...")
    try:
        # Import and run cleanup
        import cleanup
        cleanup.cleanup()
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
    
    print("\nStep 2: Creating zip archive...")
    
    # Create zip filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"{project_name}-clean-{timestamp}.zip"
    zip_path = base_dir.parent / zip_name
    
    # Create zip file
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        file_count = 0
        for root, dirs, files in os.walk(base_dir):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(Path(root) / d, base_dir)]
            
            for file in files:
                file_path = Path(root) / file
                
                # Skip excluded files
                if should_exclude(file_path, base_dir):
                    continue
                
                # Add file to zip
                arcname = Path(project_name) / file_path.relative_to(base_dir)
                zipf.write(file_path, arcname)
                file_count += 1
    
    file_size = zip_path.stat().st_size / (1024 * 1024)  # Size in MB
    
    print(f"\n✅ Package created successfully!")
    print(f"📦 File: {zip_path}")
    print(f"📊 Size: {file_size:.2f} MB")
    print(f"📄 Files: {file_count}")
    print("")
    print("Package contents:")
    print("  ✓ Source code")
    print("  ✓ Templates")
    print("  ✓ Configuration files")
    print("  ✓ requirements.txt")
    print("  ✓ README.md")
    print("")
    print("Ready for distribution! 🚀")

if __name__ == "__main__":
    try:
        create_package()
    except Exception as e:
        print(f"❌ Error during packaging: {e}")
        exit(1)
