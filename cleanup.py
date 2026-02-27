#!/usr/bin/env python3
"""
Django CRM Cleanup Script
Removes all generated files and caches for a clean distribution
"""

import os
import shutil
from pathlib import Path

def cleanup():
    """Remove all generated files and caches"""
    
    base_dir = Path(__file__).resolve().parent
    print("🧹 Starting Django CRM Cleanup...")
    print(f"📁 Base directory: {base_dir}\n")
    
    removed_count = 0
    
    # Remove SQLite database
    db_file = base_dir / "db.sqlite3"
    if db_file.exists():
        db_file.unlink()
        print(f"✓ Removed {db_file.name}")
        removed_count += 1
    
    # Remove all __pycache__ directories
    for pycache in base_dir.rglob("__pycache__"):
        if pycache.is_dir():
            shutil.rmtree(pycache)
            print(f"✓ Removed {pycache.relative_to(base_dir)}")
            removed_count += 1
    
    # Remove all .pyc and .pyo files
    for pyc_file in list(base_dir.rglob("*.pyc")) + list(base_dir.rglob("*.pyo")):
        if pyc_file.is_file():
            pyc_file.unlink()
            removed_count += 1
    
    print(f"✓ Removed .pyc/.pyo files")
    
    # Remove migration files (keep __init__.py)
    for migration_dir in base_dir.rglob("migrations"):
        if migration_dir.is_dir():
            for migration_file in migration_dir.glob("*.py"):
                if migration_file.name != "__init__.py":
                    migration_file.unlink()
                    print(f"✓ Removed {migration_file.relative_to(base_dir)}")
                    removed_count += 1
    
    # Remove .DS_Store files (Mac)
    for ds_store in base_dir.rglob(".DS_Store"):
        if ds_store.is_file():
            ds_store.unlink()
            removed_count += 1
    
    # Remove any .sqlite3 files
    for sqlite_file in base_dir.rglob("*.sqlite3"):
        if sqlite_file.is_file():
            sqlite_file.unlink()
            print(f"✓ Removed {sqlite_file.name}")
            removed_count += 1
    
    print(f"\n✅ Cleanup completed! Removed {removed_count} items\n")
    print("To reset the database, run:")
    print("  python manage.py migrate")
    print("  python manage.py createsuperuser")

if __name__ == "__main__":
    try:
        cleanup()
    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        exit(1)
