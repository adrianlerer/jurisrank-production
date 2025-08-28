#!/usr/bin/env python3
"""
Complete system test for Bibliography Management
Tests both API endpoints and parsing functionality
"""

import requests
import json
import time

# Service URL
SERVICE_URL = "https://5001-igepuerlq6q43vehrz8hr.e2b.dev"

def test_import_legal_references():
    """Test importing legal references with relevance calculation"""
    
    # Test references with various formats
    test_references = [
        'Smith, J. (2023) "Artificial Intelligence in Legal Practice: A Comparative Analysis" Harvard Law Review, 136(4), 1123-1145',
        'https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3956067',  # SSRN URL
        'Johnson, M. & Brown, L. (2022) "Constitutional Law and Machine Learning" Yale Law Journal, 131(8), 2234-2267',
        'Taylor, R. (2024) "Jurisprudential Frameworks for AI Governance" Stanford Law Review, 76(2), 456-489'
    ]
    
    print("🧪 Testing Legal Reference Import")
    print("=" * 50)
    
    for i, ref_text in enumerate(test_references, 1):
        print(f"\n📝 Test {i}: {ref_text[:60]}...")
        
        try:
            # Import through API
            response = requests.post(
                f"{SERVICE_URL}/api/v1/bibliography/import",
                headers={'Content-Type': 'application/json'},
                json={'text': ref_text},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success'] and result['imported'] > 0:
                    print(f"   ✅ Imported successfully")
                    print(f"   📊 Imported: {result['imported']} references")
                    if result['references']:
                        ref = result['references'][0]
                        print(f"   📄 Title: {ref.get('title', 'Unknown')}")
                        print(f"   👥 Authors: {ref.get('authors', 'Unknown')}")
                        print(f"   ⚖️ Relevance: {ref.get('relevance', 0):.2f}")
                else:
                    print(f"   ⚠️ No references imported: {result.get('message', 'Unknown error')}")
            else:
                print(f"   ❌ API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")
        
        time.sleep(0.5)  # Small delay between requests

def test_search_functionality():
    """Test search functionality"""
    
    print("\n\n🔍 Testing Search Functionality")
    print("=" * 50)
    
    search_terms = [
        "legal",
        "artificial intelligence", 
        "law",
        "constitutional"
    ]
    
    for term in search_terms:
        print(f"\n🔎 Searching for: '{term}'")
        
        try:
            response = requests.get(
                f"{SERVICE_URL}/api/v1/bibliography/search",
                params={'query': term},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print(f"   ✅ Found {len(result.get('references', []))} results")
                    
                    for i, ref in enumerate(result.get('references', [])[:3], 1):  # Show top 3
                        print(f"   {i}. {ref.get('title', 'Unknown Title')}")
                        print(f"      Relevance: {ref.get('jurisprudential_relevance', 0):.2f}")
                else:
                    print(f"   ⚠️ Search failed: {result.get('message', 'Unknown error')}")
            else:
                print(f"   ❌ API Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")

def test_export_functionality():
    """Test export functionality"""
    
    print("\n\n📤 Testing Export Functionality")
    print("=" * 50)
    
    formats = ['json', 'bibtex', 'apa']
    
    for format_name in formats:
        print(f"\n📋 Exporting as {format_name.upper()}...")
        
        try:
            response = requests.get(
                f"{SERVICE_URL}/api/v1/bibliography/export",
                params={'format': format_name},
                timeout=10
            )
            
            if response.status_code == 200:
                if format_name == 'json':
                    try:
                        data = response.json()
                        print(f"   ✅ JSON export successful - {len(data.get('references', []))} references")
                    except:
                        print(f"   ⚠️ JSON response but invalid format")
                else:
                    print(f"   ✅ {format_name.upper()} export successful - {len(response.text)} characters")
                    # Show first few lines
                    lines = response.text.split('\n')[:3]
                    for line in lines:
                        if line.strip():
                            print(f"   📝 {line[:60]}...")
            else:
                print(f"   ❌ Export failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {str(e)}")

def main():
    """Run complete system test"""
    
    print("🚀 JurisRank Bibliography Management System Test")
    print("🌐 Service URL:", SERVICE_URL)
    print("📅 Testing comprehensive functionality...")
    
    # Test import
    test_import_legal_references()
    
    # Test search  
    test_search_functionality()
    
    # Test export
    test_export_functionality()
    
    print("\n" + "=" * 50)
    print("✅ Complete system test finished!")
    print(f"🌐 Web Interface: {SERVICE_URL}")
    print("📊 Check the web interface to see imported references")

if __name__ == "__main__":
    main()