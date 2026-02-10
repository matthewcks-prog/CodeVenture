#!/usr/bin/env python
"""
Render Deployment Verification Script
This script checks if your CodeVenture deployment is properly configured.
"""

import sys
import os
import requests
from urllib.parse import urlparse

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

def check_url(url):
    """Check if a URL is accessible"""
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        return response.status_code, response.elapsed.total_seconds()
    except requests.RequestException as e:
        return None, str(e)

def check_static_files(base_url):
    """Check if static files are being served"""
    static_urls = [
        f"{base_url}/static/admin/css/base.css",  # Django admin CSS
    ]
    
    results = []
    for url in static_urls:
        try:
            response = requests.head(url, timeout=5)
            results.append((url, response.status_code))
        except:
            results.append((url, None))
    
    return results

def verify_deployment():
    """Main verification function"""
    
    print_header("CodeVenture Deployment Verification")
    
    # Get the URL to check
    default_url = "https://codeventure-l7dc.onrender.com"
    url = input(f"Enter your Render URL [{default_url}]: ").strip() or default_url
    
    # Ensure URL has scheme
    if not url.startswith('http'):
        url = f"https://{url}"
    
    print(f"\n{Colors.BOLD}Checking: {url}{Colors.END}\n")
    
    # Check 1: Main URL accessibility
    print_info("Checking main URL accessibility...")
    status_code, response_time = check_url(url)
    
    if status_code:
        if status_code == 200:
            print_success(f"Site is accessible (Status: {status_code}, Response time: {response_time:.2f}s)")
        elif status_code in [301, 302]:
            print_success(f"Site is accessible with redirect (Status: {status_code})")
        else:
            print_warning(f"Site returned status code: {status_code}")
    else:
        print_error(f"Site is not accessible: {response_time}")
        return False
    
    # Check 2: HTTPS redirect
    print_info("Checking HTTPS redirect...")
    http_url = url.replace('https://', 'http://')
    try:
        response = requests.get(http_url, timeout=5, allow_redirects=False)
        if response.status_code in [301, 302, 308] and 'https' in response.headers.get('Location', ''):
            print_success("HTTPS redirect is properly configured")
        else:
            print_warning("HTTPS redirect might not be configured")
    except:
        print_warning("Could not verify HTTPS redirect")
    
    # Check 3: Static files
    print_info("Checking static files...")
    static_results = check_static_files(url)
    
    static_ok = False
    for static_url, status in static_results:
        if status == 200:
            print_success(f"Static files are being served")
            static_ok = True
            break
    
    if not static_ok:
        print_warning("Could not verify static file serving (might be normal if admin isn't set up)")
    
    # Check 4: Database connectivity (indirect check)
    print_info("Checking database connectivity (indirect)...")
    try:
        admin_url = f"{url}/admin/"
        response = requests.get(admin_url, timeout=5)
        if response.status_code == 200 or response.status_code == 302:
            print_success("Admin page accessible (database likely connected)")
        else:
            print_warning(f"Admin page returned status: {response.status_code}")
    except:
        print_warning("Could not access admin page")
    
    # Check 5: Security headers
    print_info("Checking security headers...")
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        
        security_checks = {
            'X-Frame-Options': 'DENY',
            'Strict-Transport-Security': None,  # Should exist
            'X-Content-Type-Options': 'nosniff',
        }
        
        for header, expected in security_checks.items():
            if header in headers:
                if expected is None or headers[header] == expected:
                    print_success(f"Security header '{header}' is set")
                else:
                    print_warning(f"Security header '{header}' value: {headers[header]}")
            else:
                print_warning(f"Security header '{header}' is missing")
    except:
        print_warning("Could not check security headers")
    
    # Summary
    print_header("Verification Summary")
    print_info(f"Deployment URL: {url}")
    print_info("Next steps:")
    print("  1. Visit your site in a browser")
    print("  2. Test login/signup functionality")
    print("  3. Check Render logs for any errors")
    print("  4. Create a superuser if needed:")
    print("     → Dashboard → Service → Shell → 'python manage.py createsuperuser'")
    print("\n")
    
    return True

def check_local_config():
    """Check local configuration files"""
    
    print_header("Local Configuration Check")
    
    required_files = {
        'render.yaml': 'Render Blueprint configuration',
        'requirements.txt': 'Python dependencies',
        'runtime.txt': 'Python version specification',
        'Procfile': 'Process file (backup)',
        '.env.example': 'Environment variables template',
    }
    
    all_present = True
    for filename, description in required_files.items():
        if os.path.exists(filename):
            print_success(f"{filename} - {description}")
        else:
            print_error(f"{filename} is missing - {description}")
            all_present = False
    
    print("\n")
    
    # Check render.yaml content
    if os.path.exists('render.yaml'):
        print_info("Checking render.yaml configuration...")
        with open('render.yaml', 'r') as f:
            content = f.read()
            
            checks = {
                'databases:': 'Database configuration',
                'type: web': 'Web service definition',
                'buildCommand:': 'Build command',
                'startCommand:': 'Start command',
                'DATABASE_URL': 'Database URL reference',
            }
            
            for check, description in checks.items():
                if check in content:
                    print_success(f"Contains {description}")
                else:
                    print_warning(f"Missing {description}")
    
    return all_present

if __name__ == "__main__":
    print(f"\n{Colors.BOLD}CodeVenture Deployment Verification Tool{Colors.END}")
    print(f"{Colors.BOLD}Version 1.0{Colors.END}\n")
    
    choice = input("Check (1) Local Configuration or (2) Deployed Site? [1/2]: ").strip()
    
    if choice == "1":
        check_local_config()
    elif choice == "2":
        verify_deployment()
    else:
        print("Checking both...\n")
        check_local_config()
        verify_deployment()
    
    print_info("For detailed deployment guide, see: RENDER_BLUEPRINT_GUIDE.md")
    print()
