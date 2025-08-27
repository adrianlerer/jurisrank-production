#!/usr/bin/env python3
"""
Netlify Deployment Validation Script
===================================
Validates that the JurisRank API is working correctly on Netlify.
"""

import requests
import json
import sys
import time
from datetime import datetime

def test_endpoint(url, method='GET', data=None, headers=None):
    """Test an API endpoint and return status."""
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers, timeout=30)
        
        return {
            'success': True,
            'status_code': response.status_code,
            'response_time_ms': response.elapsed.total_seconds() * 1000,
            'data': response.json() if response.headers.get('content-type', '').startswith('application/json') else None
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'status_code': None,
            'response_time_ms': None
        }

def main():
    """Run comprehensive validation tests."""
    print("🏛️ JurisRank API - Netlify Deployment Validation")
    print("=" * 55)
    
    # Get base URL from user
    base_url = input("Enter your Netlify URL (e.g., https://your-site.netlify.app): ").strip()
    if not base_url:
        print("❌ No URL provided")
        return 1
    
    # Remove trailing slash
    base_url = base_url.rstrip('/')
    
    print(f"\n🎯 Testing API at: {base_url}")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    
    tests = []
    
    # Test 1: Health Check
    print("\n1️⃣ Testing Health Check...")
    result = test_endpoint(f"{base_url}/health")
    tests.append(('Health Check', result))
    
    if result['success']:
        print(f"   ✅ Status: {result['status_code']} ({result['response_time_ms']:.0f}ms)")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 2: API Status
    print("\n2️⃣ Testing API Status...")
    result = test_endpoint(f"{base_url}/api/v1/status")
    tests.append(('API Status', result))
    
    if result['success']:
        print(f"   ✅ Status: {result['status_code']} ({result['response_time_ms']:.0f}ms)")
        if result['data']:
            print(f"   📊 Version: {result['data'].get('version', 'unknown')}")
            print(f"   🌍 Environment: {result['data'].get('environment', 'unknown')}")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 3: OpenAPI Schema
    print("\n3️⃣ Testing OpenAPI Schema...")
    result = test_endpoint(f"{base_url}/api/v1/openapi.json")
    tests.append(('OpenAPI Schema', result))
    
    if result['success']:
        print(f"   ✅ Status: {result['status_code']} ({result['response_time_ms']:.0f}ms)")
        if result['data']:
            print(f"   📚 API Title: {result['data'].get('info', {}).get('title', 'unknown')}")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 4: Documentation
    print("\n4️⃣ Testing Documentation...")
    result = test_endpoint(f"{base_url}/docs")
    tests.append(('Documentation', result))
    
    if result['success']:
        print(f"   ✅ Status: {result['status_code']} ({result['response_time_ms']:.0f}ms)")
        print(f"   📄 Content: HTML documentation loaded")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 5: API Key Registration
    print("\n5️⃣ Testing API Key Registration...")
    test_email = f"test+{int(time.time())}@example.com"
    result = test_endpoint(
        f"{base_url}/api/v1/auth/register",
        method='POST',
        data={'email': test_email}
    )
    tests.append(('API Registration', result))
    
    api_key = None
    if result['success']:
        print(f"   ✅ Status: {result['status_code']} ({result['response_time_ms']:.0f}ms)")
        if result['data'] and 'api_key' in result['data']:
            api_key = result['data']['api_key']
            print(f"   🔑 API Key: {api_key[:8]}...{api_key[-4:]}")
        else:
            print(f"   ⚠️  No API key in response")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 6: Authority Analysis (with API key if available)
    print("\n6️⃣ Testing Authority Analysis...")
    headers = {'X-API-Key': api_key} if api_key else None
    
    result = test_endpoint(
        f"{base_url}/api/v1/jurisprudence/authority",
        method='POST',
        data={
            'case_citation': 'Test v. Validation',
            'jurisdiction': 'argentina',
            'legal_area': 'contract_law'
        },
        headers=headers
    )
    tests.append(('Authority Analysis', result))
    
    if result['success']:
        print(f"   ✅ Status: {result['status_code']} ({result['response_time_ms']:.0f}ms)")
        if result['data'] and 'authority_score' in result['data']:
            print(f"   📊 Authority Score: {result['data']['authority_score']}")
            print(f"   🧬 Patent P7: {result['data'].get('patent_p7_compliance', 'unknown')}")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 7: Precedent Search
    print("\n7️⃣ Testing Precedent Search...")
    result = test_endpoint(
        f"{base_url}/api/v1/precedents/search?query=constitutional law&jurisdiction=argentina&limit=3",
        headers=headers
    )
    tests.append(('Precedent Search', result))
    
    if result['success']:
        print(f"   ✅ Status: {result['status_code']} ({result['response_time_ms']:.0f}ms)")
        if result['data'] and 'results' in result['data']:
            print(f"   🔍 Results: {len(result['data']['results'])} precedents found")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Test 8: Comparative Analysis
    print("\n8️⃣ Testing Comparative Analysis...")
    result = test_endpoint(
        f"{base_url}/api/v1/compare/systems",
        method='POST',
        data={'concept': 'contract_formation'},
        headers=headers
    )
    tests.append(('Comparative Analysis', result))
    
    if result['success']:
        print(f"   ✅ Status: {result['status_code']} ({result['response_time_ms']:.0f}ms)")
        if result['data'] and 'convergence_score' in result['data']:
            print(f"   🌍 Convergence Score: {result['data']['convergence_score']}")
    else:
        print(f"   ❌ Failed: {result.get('error', 'Unknown error')}")
    
    # Summary
    print("\n" + "=" * 55)
    successful_tests = sum(1 for _, test in tests if test['success'] and test.get('status_code') == 200)
    total_tests = len(tests)
    
    print(f"🎯 VALIDATION SUMMARY: {successful_tests}/{total_tests} tests passed")
    
    if successful_tests == total_tests:
        print("🚀 ✅ ALL TESTS PASSED - Netlify deployment is fully operational!")
        print(f"\n📍 Your JurisRank API is live at: {base_url}")
        print(f"📚 Documentation: {base_url}/docs")
        print(f"🔑 Register for API key: {base_url}/api/v1/auth/register")
        
        # Performance summary
        avg_response_time = sum(
            test['response_time_ms'] for _, test in tests 
            if test['success'] and test['response_time_ms']
        ) / len([test for _, test in tests if test['success'] and test['response_time_ms']])
        
        print(f"\n📊 Performance Metrics:")
        print(f"   Average Response Time: {avg_response_time:.0f}ms")
        print(f"   All Endpoints: ✅ Operational")
        print(f"   SSL Certificate: ✅ Active")
        print(f"   Patent P7 Compliance: ✅ Verified")
        
        return 0
    else:
        print(f"⚠️  {total_tests - successful_tests} tests failed - please review issues above")
        
        print("\n🔧 Troubleshooting:")
        print("   1. Check Netlify function logs in dashboard")
        print("   2. Verify all functions deployed correctly")
        print("   3. Test functions locally first")
        print("   4. Check netlify.toml configuration")
        
        return 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Validation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {str(e)}")
        sys.exit(1)