#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit  # Exit on error

echo "===> Starting build process..."

# Upgrade pip
echo "===> Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "===> Installing dependencies..."
pip install -r requirements.txt

# Collect static files
echo "===> Collecting static files..."
python manage.py collectstatic --noinput

# Fix any migration history inconsistencies (sites / socialaccount ordering)
echo "===> Checking migration history..."
python manage.py fix_migration_history --execute

# Apply database migrations
echo "===> Running migrations..."
python manage.py migrate --noinput

# Ensure the Sites framework record exists (required by allauth)
echo "===> Configuring site record..."
python manage.py setup_site

# Seed curriculum (learning modules, submodules, CPE assessments). Idempotent; safe on every deploy.
echo "===> Seeding curriculum data..."
python manage.py seed_data

echo "===> Build completed successfully!"
