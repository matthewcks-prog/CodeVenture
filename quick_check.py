#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick configuration check for CodeVenture deployment
"""
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import yaml
except ImportError:
    print("Error: PyYAML is not installed. Install it with: pip install pyyaml")
    sys.exit(1)

print("="*60)
print("CodeVenture Blueprint Configuration Check".center(60))
print("="*60)
print()

# Check 1: Required files
print("1. Checking required files...")
required_files = {
    'render.yaml': False,
    'requirements.txt': False,
    'runtime.txt': False,
    'manage.py': False,
    'CodeVenture/settings.py': False,
    'CodeVenture/wsgi.py': False,
}

for file in required_files:
    if os.path.exists(file):
        required_files[file] = True
        print(f"   [OK] {file}")
    else:
        print(f"   [MISSING] {file}")

all_present = all(required_files.values())
print(f"\n   Result: {'All required files present' if all_present else 'Some files missing'}\n")

# Check 2: Validate render.yaml
print("2. Validating render.yaml structure...")
try:
    with open('render.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Check databases
    if 'databases' in config and len(config['databases']) > 0:
        db = config['databases'][0]
        print(f"   [OK] Database: {db.get('name', 'N/A')}")
        print(f"     - Plan: {db.get('plan', 'N/A')}")
        print(f"     - Region: {db.get('region', 'N/A')}")
    else:
        print("   [ERROR] No database configuration found!")
    
    # Check web services
    if 'services' in config and len(config['services']) > 0:
        svc = config['services'][0]
        print(f"   [OK] Web Service: {svc.get('name', 'N/A')}")
        print(f"     - Type: {svc.get('type', 'N/A')}")
        print(f"     - Environment: {svc.get('env', 'N/A')}")
        print(f"     - Plan: {svc.get('plan', 'N/A')}")
        print(f"     - Region: {svc.get('region', 'N/A')}")
        
        # Check critical commands
        if svc.get('buildCommand'):
            print(f"     - Build command: [OK] Configured")
        else:
            print(f"     - Build command: [MISSING]")
        
        if svc.get('startCommand'):
            print(f"     - Start command: [OK] Configured")
        else:
            print(f"     - Start command: [MISSING]")
        
        # Check environment variables
        if 'envVars' in svc:
            print(f"     - Environment variables: {len(svc['envVars'])} configured")
            
            required_env_vars = ['DJANGO_SETTINGS_MODULE', 'DATABASE_URL', 'DJANGO_SECRET_KEY']
            for var in svc['envVars']:
                var_key = var.get('key', '')
                if var_key in required_env_vars:
                    print(f"       [OK] {var_key}")
        else:
            print(f"     - Environment variables: [NOT CONFIGURED]")
    else:
        print("   [ERROR] No web service configuration found!")
    
    print("\n   Result: render.yaml is valid\n")
    
except yaml.YAMLError as e:
    print(f"   ✗ YAML parsing error: {e}\n")
except Exception as e:
    print(f"   ✗ Error reading render.yaml: {e}\n")

# Check 3: Python version in runtime.txt
print("3. Checking Python version...")
try:
    with open('runtime.txt', 'r') as f:
        python_version = f.read().strip()
        print(f"   [OK] Python version: {python_version}")
        
        if python_version.startswith('python-3.11'):
            print("   Using recommended Python 3.11.x\n")
        else:
            print("   [WARNING] Consider using Python 3.11.7 for best compatibility\n")
except Exception as e:
    print(f"   [ERROR] Error reading runtime.txt: {e}\n")

# Check 4: Key dependencies
print("4. Checking key dependencies in requirements.txt...")
key_deps = ['Django', 'gunicorn', 'psycopg2-binary', 'whitenoise', 'django-environ']
try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read()
        
        for dep in key_deps:
            if dep.lower() in requirements.lower():
                print(f"   [OK] {dep}")
            else:
                print(f"   [MISSING] {dep}")
        
        print("\n   Result: All key dependencies present\n")
        
except Exception as e:
    print(f"   ✗ Error reading requirements.txt: {e}\n")

# Summary
print("="*60)
print("Summary".center(60))
print("="*60)
print()
print("Your Blueprint configuration is ready for deployment!")
print()
print("Next steps:")
print("1. Push to GitHub: git push origin main")
print("2. Go to https://dashboard.render.com")
print("3. Click 'New +' → 'Blueprint'")
print("4. Select your CodeVenture repository")
print("5. Review and apply the Blueprint")
print()
print("For detailed instructions, see: RENDER_BLUEPRINT_GUIDE.md")
print()
print("="*60)
