#!/usr/bin/env python
"""
Fix Django Migration Inconsistencies
This script helps resolve migration order issues in the database
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeVenture.settings')

try:
    django.setup()
except Exception as e:
    print(f"[ERROR] Error setting up Django: {e}")
    sys.exit(1)

from django.core.management import call_command
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder


def check_migration_issues():
    """Check for migration inconsistencies"""
    print("[INFO] Checking for migration issues...\n")
    
    recorder = MigrationRecorder(connection)
    applied_migrations = recorder.applied_migrations()
    
    # Check for the specific issue: socialaccount before sites
    socialaccount_applied = any(
        app == 'socialaccount' and name == '0001_initial' 
        for app, name in applied_migrations
    )
    sites_applied = any(
        app == 'sites' and name == '0001_initial' 
        for app, name in applied_migrations
    )
    
    print(f"[OK] Sites 0001_initial applied: {sites_applied}")
    print(f"[OK] Socialaccount 0001_initial applied: {socialaccount_applied}")
    
    if socialaccount_applied and not sites_applied:
        print("\n[WARNING] Issue detected: socialaccount.0001_initial is applied but sites.0001_initial is not!")
        print("   This will cause migration errors.\n")
        return True
    elif not socialaccount_applied and not sites_applied:
        print("\n[OK] No migrations applied yet. Database is clean.\n")
        return False
    else:
        print("\n[OK] No migration order issues detected.\n")
        return False


def fix_migration_order():
    """Fix migration order by faking the sites migrations"""
    print("[FIX] Attempting to fix migration order...\n")
    
    try:
        # Fake the sites migrations
        print("1. Faking sites migrations...")
        call_command('migrate', 'sites', '--fake-initial', verbosity=2)
        print("   [OK] Sites migrations faked\n")
        
        # Now run all migrations normally
        print("2. Running all migrations...")
        call_command('migrate', verbosity=2)
        print("   [OK] All migrations applied\n")
        
        print("[SUCCESS] Migration fix completed successfully!")
        return True
    except Exception as e:
        print(f"[ERROR] Error fixing migrations: {e}")
        return False


def show_migration_status():
    """Show current migration status"""
    print("\n[INFO] Current Migration Status:\n")
    try:
        call_command('showmigrations', verbosity=1)
    except Exception as e:
        print(f"[ERROR] Error showing migrations: {e}")


def main():
    """Main function"""
    print("=" * 60)
    print("Django Migration Fix Tool")
    print("=" * 60)
    print()
    
    # Check for issues
    has_issues = check_migration_issues()
    
    if has_issues:
        response = input("Would you like to fix the migration order? (y/n): ")
        if response.lower() == 'y':
            success = fix_migration_order()
            if success:
                show_migration_status()
        else:
            print("\nNo changes made. You can fix this manually by running:")
            print("  python manage.py migrate sites --fake-initial")
            print("  python manage.py migrate")
    else:
        show_migration_status()
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    main()
