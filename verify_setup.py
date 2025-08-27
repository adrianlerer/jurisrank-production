#!/usr/bin/env python3
"""
JurisRank Setup Verification Script
==================================
Simple script to verify that JurisRank is properly set up and accessible.
Can be run from any machine with Python and internet access.
"""

import json
import sys
from pathlib import Path
try:
    import requests
except ImportError:
    print("❌ requests library not found. Install with: pip install requests")
    sys.exit(1)

def check_file(filename, description):
    """Check if a file exists locally."""
    if Path(filename).exists():
        lines = len(Path(filename).read_text().splitlines())
        print(f"✅ {description}: {filename} ({lines} lines)")
        return True
    else:
        print(f"❌ {description}: {filename} not found")
        return False

def check_url(url, description):
    """Check if a URL is accessible."""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ {description}: {url} (HTTP {response.status_code})")
            return True
        else:
            print(f"⚠️ {description}: {url} (HTTP {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ {description}: {url} - {str(e)}")
        return False

def main():
    print("🔍 JurisRank Setup Verification")
    print("=" * 40)
    
    base_url = "https://5000-ihpc0zttjgtqrprr5t3vr.e2b.dev"
    
    # Check local files
    print("\n📁 Local Files Check:")
    local_checks = [
        ("README.md", "Main documentation"),
        ("EXTERNAL_AUDIT_REPORT.md", "External audit report"),
        ("SECURITY_CHECKLIST.md", "Security checklist"),
        ("scripts/generate_audit_report.py", "Audit generator"),
        ("examples/jurisrank_agent_test.sh", "External test script"),
        ("openapi_schema.json", "OpenAPI specification"),
    ]
    
    local_passed = 0
    for filename, description in local_checks:
        if check_file(filename, description):
            local_passed += 1
    
    # Check external URLs
    print("\n🌐 External API Check:")
    url_checks = [
        (f"{base_url}/health", "Health endpoint"),
        (f"{base_url}/api/v1/status", "API status"),
        (f"{base_url}/api/v1/openapi.json", "OpenAPI schema"),
        (f"{base_url}/docs", "Swagger UI"),
    ]
    
    url_passed = 0
    for url, description in url_checks:
        if check_url(url, description):
            url_passed += 1
    
    # Test API functionality
    print("\n🧪 API Functionality Check:")
    try:
        # Test API registration
        reg_response = requests.post(f"{base_url}/api/v1/auth/register", timeout=10)
        if reg_response.status_code == 200:
            data = reg_response.json()
            if 'api_key' in data:
                print("✅ API Registration: Working (API key generated)")
            else:
                print("⚠️ API Registration: Response missing api_key")
        else:
            print(f"⚠️ API Registration: HTTP {reg_response.status_code}")
    except Exception as e:
        print(f"❌ API Registration: {str(e)}")
    
    # Summary
    total_local = len(local_checks)
    total_urls = len(url_checks)
    
    print("\n📊 Summary:")
    print(f"📁 Local Files: {local_passed}/{total_local} ({local_passed/total_local*100:.1f}%)")
    print(f"🌐 External URLs: {url_passed}/{total_urls} ({url_passed/total_urls*100:.1f}%)")
    
    overall_score = (local_passed + url_passed) / (total_local + total_urls) * 100
    print(f"🎯 Overall Score: {overall_score:.1f}%")
    
    if overall_score >= 90:
        print("\n🎉 JurisRank Setup: EXCELLENT")
        print("✅ Ready for development and external use")
        return 0
    elif overall_score >= 75:
        print("\n👍 JurisRank Setup: GOOD")
        print("⚠️ Some components missing but functional")
        return 0
    else:
        print("\n🔧 JurisRank Setup: NEEDS ATTENTION")
        print("❌ Multiple issues found - check setup")
        return 1

if __name__ == "__main__":
    sys.exit(main())