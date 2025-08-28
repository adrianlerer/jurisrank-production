#!/usr/bin/env python3
"""
Test script for URL parsing integration
Tests SSRN URL parsing and jurisprudential relevance calculation
"""

import sys
import os
sys.path.append('src')

from bibliography_manager import BibliographyParser

def test_ssrn_url_parsing():
    """Test SSRN URL parsing"""
    
    # Create parser
    parser = BibliographyParser()
    
    # Test SSRN URL
    ssrn_url = "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3956067"
    
    print("Testing SSRN URL parsing...")
    print(f"URL: {ssrn_url}")
    
    try:
        # Parse the URL
        reference = parser.parse_reference(ssrn_url)
        
        if reference:
            print("\n✅ URL parsed successfully!")
            print(f"Title: {reference.title}")
            print(f"Authors: {reference.authors}")
            print(f"Year: {reference.year}")
            print(f"Publication: {reference.publication}")
            print(f"URL: {reference.url}")
            print(f"Abstract: {reference.abstract[:200] if reference.abstract else 'None'}...")
            print(f"Reference Type: {reference.reference_type}")
            print(f"Jurisprudential Relevance: {reference.jurisprudential_relevance}")
            
            return True
        else:
            print("❌ Failed to parse URL")
            return False
            
    except Exception as e:
        print(f"❌ Error parsing URL: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_generic_parsing():
    """Test the original generic parsing for comparison"""
    
    parser = BibliographyParser()
    
    # Test with a regular citation
    citation = 'Smith, J. (2023) "Legal Technology and AI" Journal of Law and Technology, 15(2), 123-145'
    
    print("\nTesting regular citation parsing...")
    print(f"Citation: {citation}")
    
    try:
        reference = parser.parse_reference(citation)
        
        if reference:
            print("\n✅ Citation parsed successfully!")
            print(f"Title: {reference.title}")
            print(f"Authors: {reference.authors}")
            print(f"Year: {reference.year}")
            print(f"Publication: {reference.publication}")
            print(f"Jurisprudential Relevance: {reference.jurisprudential_relevance}")
            
            return True
        else:
            print("❌ Failed to parse citation")
            return False
            
    except Exception as e:
        print(f"❌ Error parsing citation: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing URL Parsing Integration")
    print("=" * 50)
    
    # Test SSRN URL parsing
    ssrn_test = test_ssrn_url_parsing()
    
    # Test regular citation parsing
    generic_test = test_generic_parsing()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"SSRN URL Parsing: {'✅ PASS' if ssrn_test else '❌ FAIL'}")
    print(f"Generic Citation Parsing: {'✅ PASS' if generic_test else '❌ FAIL'}")
    
    if ssrn_test and generic_test:
        print("\n🎉 All tests passed! URL parsing integration is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")