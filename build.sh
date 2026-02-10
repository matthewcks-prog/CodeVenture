#!/usr/bin/env bash
# Build script for Render deployment
set -o errexit  # Exit on error

echo "===> Starting build process..."

# Upgrade pip
echo "===> Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "===> Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Collect static files
echo "===> Collecting static files..."
python manage.py collectstatic --noinput

# Fix any migration inconsistencies BEFORE running migrate.
# This handles the socialaccount/sites ordering issue by directly
# inserting missing migration records via raw SQL, which bypasses
# Django's consistency check that blocks normal migrate commands.
echo "===> Checking and fixing migration history..."
python manage.py fix_migration_history --execute

# Now run migrations normally
echo "===> Running migrations..."
python manage.py migrate --noinput

echo "===> Build completed successfully!"
