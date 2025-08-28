#!/usr/bin/env python3
"""
Test specific legal URL parsing
"""

import sys
sys.path.append('.')

from enhanced_url_parser import AcademicURLParser

def test_specific_legal_url():
    """Test the specific URL that failed"""
    
    parser = AcademicURLParser()
    
    # The URL that failed
    test_url = "https://abogados.com.ar/el-ombudsman-corporativo-de-ia-la-nueva-funcion-estrategica-en-grandes-estudios-juridicos/37414"
    
    print(f"🧪 Testing Legal URL: {test_url}")
    print("=" * 80)
    
    # Test URL detection
    is_legal = parser._is_legal_website(test_url)
    print(f"🔍 Is Legal Website: {is_legal}")
    
    # Test parsing
    try:
        result = parser.parse_academic_url(test_url)
        
        if result:
            print("\n✅ Parsing Success!")
            print(f"📄 Title: {result.get('title')}")
            print(f"👥 Authors: {result.get('authors')}")
            print(f"📅 Year: {result.get('year')}")
            print(f"📰 Publication: {result.get('publication')}")
            print(f"🔗 URL: {result.get('url')}")
            print(f"📝 Abstract: {result.get('abstract', 'None')}")
            print(f"📂 Type: {result.get('reference_type')}")
            print(f"🏷️  Source: {result.get('source')}")
            
            return result
        else:
            print("\n❌ Parsing failed - returned None")
            return None
            
    except Exception as e:
        print(f"\n❌ Error during parsing: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_bibliography_integration():
    """Test integration with bibliography manager"""
    
    print("\n\n🔗 Testing Bibliography Manager Integration")
    print("=" * 80)
    
    try:
        sys.path.append('src')
        from bibliography_manager import BibliographyParser, BibliographyAnalyzer
        
        parser = BibliographyParser()
        analyzer = BibliographyAnalyzer()
        
        test_url = "https://abogados.com.ar/el-ombudsman-corporativo-de-ia-la-nueva-funcion-estrategica-en-grandes-estudios-juridicos/37414"
        
        # Parse with bibliography parser
        reference = parser.parse_reference(test_url)
        
        if reference:
            print("✅ Bibliography Parser Success!")
            print(f"📄 Title: {reference.title}")
            print(f"👥 Authors: {reference.authors}")
            print(f"📅 Year: {reference.year}")
            print(f"📰 Publication: {reference.publication}")
            print(f"⚖️  Jurisprudential Relevance: {reference.jurisprudential_relevance}")
            
            # Test relevance calculation
            if reference.jurisprudential_relevance == 0.0:
                print("\n🔄 Recalculating relevance...")
                new_relevance = analyzer.calculate_jurisprudential_relevance(reference)
                print(f"⚖️  New Relevance: {new_relevance}")
            
        else:
            print("❌ Bibliography Parser failed")
            
    except Exception as e:
        print(f"❌ Error in bibliography integration: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🧪 Testing Legal URL Parsing")
    print("🎯 Target: abogados.com.ar ombudsman IA article")
    
    # Test URL parser
    result = test_specific_legal_url()
    
    # Test bibliography integration
    test_bibliography_integration()
    
    if result:
        print("\n🎉 Test completed successfully!")
    else:
        print("\n⚠️  Test needs improvement")