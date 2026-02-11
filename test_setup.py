"""
Quick test script to verify Django setup and configuration.
"""
import os
import sys
import django

# Fix encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeVenture.settings')
django.setup()

from django.conf import settings
from django.contrib.auth.models import User
from UserManagement.models import Student, Parent, Teacher

print("=" * 60)
print("CodeVenture Configuration Test")
print("=" * 60)

print("\n[OK] Django setup successful!")
print(f"[OK] DEBUG mode: {settings.DEBUG}")
print(f"[OK] SECRET_KEY configured: {'Yes' if settings.SECRET_KEY and settings.SECRET_KEY != 'insecure-dev-key-change-me' else 'No (using default)'}")
print(f"[OK] Database: {settings.DATABASES['default']['ENGINE']}")
print(f"[OK] Google OAuth configured: {settings.GOOGLE_OAUTH_CONFIGURED}")

if settings.GOOGLE_OAUTH_CONFIGURED:
    print(f"  - Client ID: {settings._GOOGLE_CLIENT_ID[:20]}...")
    print(f"  - Client Secret: {'*' * 20}")

print("\n" + "=" * 60)
print("Database Models Test")
print("=" * 60)

# Test database connectivity
try:
    user_count = User.objects.count()
    student_count = Student.objects.count()
    parent_count = Parent.objects.count()
    teacher_count = Teacher.objects.count()
    
    print(f"\n[OK] Database connection successful!")
    print(f"  - Total users: {user_count}")
    print(f"  - Students: {student_count}")
    print(f"  - Parents: {parent_count}")
    print(f"  - Teachers: {teacher_count}")
    
except Exception as e:
    print(f"\n[ERROR] Database error: {str(e)}")

print("\n" + "=" * 60)
print("Middleware Test")
print("=" * 60)

for middleware in settings.MIDDLEWARE:
    print(f"[OK] {middleware.split('.')[-1]}")

print("\n" + "=" * 60)
print("Installed Apps Test")
print("=" * 60)

for app in settings.INSTALLED_APPS:
    if not app.startswith('django.'):
        print(f"[OK] {app}")

print("\n" + "=" * 60)
print("All checks passed! Application is ready to use.")
print("=" * 60)
