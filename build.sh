#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit  # Exit on error

echo "Starting build process..."

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Handle migration inconsistency
echo "Checking for migration inconsistencies..."

# Try to run migrations normally first
if python manage.py migrate --noinput 2>&1; then
    echo "[SUCCESS] Migrations applied successfully!"
else
    echo "[WARNING] Migration error detected. Attempting to fix..."
    
    # If there's an inconsistency error, we need to fake the sites migration
    # This is safe because the tables are likely already created
    echo "Faking sites.0001_initial migration..."
    python manage.py migrate sites 0001 --fake-initial || true
    
    echo "Faking sites.0002_alter_domain_unique migration..."
    python manage.py migrate sites --fake-initial || true
    
    echo "Now running all migrations..."
    python manage.py migrate --noinput
    
    echo "[SUCCESS] Migrations fixed and applied!"
fi

echo "Build completed successfully!"
