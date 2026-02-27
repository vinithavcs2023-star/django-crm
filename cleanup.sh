#!/bin/bash

echo "🧹 Starting Django CRM Cleanup..."

# Remove SQLite database
if [ -f "db.sqlite3" ]; then
    rm db.sqlite3
    echo "✓ Removed db.sqlite3"
fi

# Remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "✓ Removed __pycache__ directories"

# Remove all .pyc files
find . -type f -name "*.pyc" -delete
echo "✓ Removed .pyc files"

# Remove all .pyo files
find . -type f -name "*.pyo" -delete
echo "✓ Removed .pyo files"

# Remove migration files (keep __init__.py)
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
echo "✓ Removed migration files"

find . -path "*/migrations/*.pyc" -delete
echo "✓ Removed migration .pyc files"

# Remove .DS_Store files (Mac)
find . -name ".DS_Store" -delete 2>/dev/null
echo "✓ Removed .DS_Store files"

# Remove any .sqlite3 files
find . -type f -name "*.sqlite3" -delete
echo "✓ Removed all .sqlite3 files"

echo ""
echo "✅ Cleanup completed successfully!"
echo ""
echo "To reset the database, run:"
echo "  python manage.py migrate"
echo "  python manage.py createsuperuser"
