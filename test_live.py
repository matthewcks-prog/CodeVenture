#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test to check if deployment is live
"""
import requests
import sys
import io

# Ensure UTF-8 output on Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

url = "https://codeventure-l7dc.onrender.com"

print(f"Testing deployment at: {url}")
print("Please wait... (this may take up to 60 seconds if the service is sleeping)\n")

try:
    response = requests.get(url, timeout=70)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Time: {response.elapsed.total_seconds():.2f} seconds")
    
    if response.status_code == 200:
        print("\n[SUCCESS] Deployment is LIVE and working!")
        print(f"\nYou can access your app at: {url}")
    elif response.status_code in [301, 302, 308]:
        print(f"\n[SUCCESS] Deployment is LIVE (redirecting to: {response.headers.get('Location', 'unknown')})")
    elif response.status_code == 404:
        print("\n[NOT FOUND] Deployment returned 404")
        print("This means:")
        print("  1. The service was deleted (as you mentioned)")
        print("  2. OR the service exists but the app isn't routing correctly")
        print("\n--> You need to deploy using Blueprint via Render Dashboard")
        print("    Follow the steps in TEST_DEPLOYMENT.md")
    else:
        print(f"\n[WARNING] Deployment returned status code: {response.status_code}")
        print("This might indicate an issue. Check Render logs.")
        
except requests.exceptions.Timeout:
    print("\n[TIMEOUT] Request timed out after 70 seconds")
    print("This might mean:")
    print("  1. The service is sleeping and taking longer than usual to wake up")
    print("  2. There's an issue with the deployment")
    print("\n--> Check Render Dashboard for service status")
    
except requests.exceptions.ConnectionError:
    print("\n[ERROR] Could not connect to the deployment")
    print("This might mean:")
    print("  1. No deployment exists yet (you need to deploy via Render Dashboard)")
    print("  2. Network connectivity issues")
    print("\n--> Follow the deployment steps in TEST_DEPLOYMENT.md")
    
except Exception as e:
    print(f"\n[ERROR] Error: {e}")
    
print("\n" + "="*60)
