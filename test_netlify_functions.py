#!/usr/bin/env python3
"""
Netlify Functions Local Testing Script
=====================================
Test all JurisRank API serverless functions before deployment.
"""

import json
import sys
import os
from pathlib import Path

def test_function(function_name, event_data):
    """Test a Netlify function locally by importing and executing it."""
    try:
        # Add api directory to path
        api_dir = Path(__file__).parent / 'api'
        sys.path.insert(0, str(api_dir))
        
        # Import the function
        module = __import__(function_name)
        handler = getattr(module, 'handler')
        
        # Mock context object
        context = {
            'function_name': function_name,
            'memory_limit': '128',
            'timeout': '10'
        }
        
        # Call the handler
        result = handler(event_data, context)
        
        print(f"✅ {function_name}: SUCCESS")
        print(f"   Status: {result.get('statusCode', 'unknown')}")
        
        # Parse body if it's JSON
        if result.get('body'):
            try:
                body = json.loads(result['body'])
                if 'error' in body:
                    print(f"   Error: {body['error'].get('message', 'Unknown error')}")
                else:
                    print(f"   Response: {type(body).__name__} with {len(body)} fields")
            except json.JSONDecodeError:
                print(f"   Body: HTML content ({len(result['body'])} chars)")
        
        return True
        
    except Exception as e:
        print(f"❌ {function_name}: ERROR - {str(e)}")
        return False

def main():
    """Run all function tests."""
    print("🧪 Testing JurisRank Netlify Serverless Functions")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 0
    
    # Test health endpoint
    total_tests += 1
    if test_function('health', {'httpMethod': 'GET'}):
        tests_passed += 1
    
    # Test status endpoint  
    total_tests += 1
    if test_function('status', {'httpMethod': 'GET'}):
        tests_passed += 1
    
    # Test register endpoint
    total_tests += 1
    if test_function('register', {
        'httpMethod': 'POST',
        'body': json.dumps({'email': 'test@example.com'})
    }):
        tests_passed += 1
    
    # Test authority endpoint
    total_tests += 1
    if test_function('authority', {
        'httpMethod': 'POST',
        'body': json.dumps({
            'case_citation': 'Test v. Case',
            'jurisdiction': 'argentina',
            'legal_area': 'contract_law'
        })
    }):
        tests_passed += 1
    
    # Test search endpoint
    total_tests += 1
    if test_function('search', {
        'httpMethod': 'GET',
        'queryStringParameters': {
            'query': 'contract law',
            'jurisdiction': 'argentina',
            'limit': '5'
        }
    }):
        tests_passed += 1
    
    # Test compare endpoint
    total_tests += 1
    if test_function('compare', {
        'httpMethod': 'POST',
        'body': json.dumps({'concept': 'contract_formation'})
    }):
        tests_passed += 1
    
    # Test openapi endpoint
    total_tests += 1
    if test_function('openapi', {'httpMethod': 'GET'}):
        tests_passed += 1
    
    # Test docs endpoint
    total_tests += 1
    if test_function('docs', {
        'httpMethod': 'GET',
        'headers': {'host': 'localhost:8888'}
    }):
        tests_passed += 1
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {tests_passed}/{total_tests} functions passed")
    
    if tests_passed == total_tests:
        print("🚀 All functions ready for Netlify deployment!")
        return 0
    else:
        print(f"⚠️  {total_tests - tests_passed} functions need attention")
        return 1

if __name__ == '__main__':
    sys.exit(main())