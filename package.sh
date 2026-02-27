#!/bin/bash

echo "📦 Packaging Django CRM Project..."
echo ""

# Run cleanup first
echo "Step 1: Running cleanup..."
if [ -f "cleanup.sh" ]; then
    bash cleanup.sh
else
    python3 cleanup.py
fi

echo ""
echo "Step 2: Creating zip archive..."

# Get the parent directory name
PROJECT_NAME="Django-CRM"
ZIP_NAME="${PROJECT_NAME}-clean-$(date +%Y%m%d-%H%M%S).zip"

# Create zip file (exclude unnecessary files)
cd ..
zip -r "$ZIP_NAME" "$PROJECT_NAME" \
    -x "*.git*" \
    -x "*__pycache__*" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "*.sqlite3" \
    -x "*/.DS_Store" \
    -x "*/node_modules/*" \
    -x "*/venv/*" \
    -x "*/env/*" \
    -x "*/.vscode/*" \
    -x "*/.idea/*"

cd "$PROJECT_NAME"

echo ""
echo "✅ Package created successfully!"
echo "📦 File: ../$ZIP_NAME"
echo ""
echo "Package contents:"
echo "  ✓ Source code"
echo "  ✓ Templates"
echo "  ✓ Configuration files"
echo "  ✓ requirements.txt"
echo "  ✓ README.md"
echo ""
echo "Ready for distribution! 🚀"
