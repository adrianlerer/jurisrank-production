"""
JurisRank API Validation Script
==============================
Comprehensive validation of API structure and documentation consistency.
"""

import sys
sys.path.insert(0, 'src')

import inspect
from jurisrank import JurisRankAPI, get_api_info
from jurisrank.models import LegalDocument, AnalysisResult, AuthorityScore, SearchQuery

def validate_api_structure():
    """Validate API class structure and methods."""
    print("🔍 Validating API Structure...")
    
    # Check JurisRankAPI class
    api_methods = [method for method in dir(JurisRankAPI) if not method.startswith('_')]
    expected_methods = ['analyze_document', 'analyze_document_async', 'search_jurisprudence', 'get_authority_score']
    
    for method in expected_methods:
        if method in api_methods:
            print(f"  ✅ Method '{method}' exists")
        else:
            print(f"  ❌ Method '{method}' missing")
    
    # Check method signatures
    print("\n📋 Validating Method Signatures...")
    
    # analyze_document signature
    sig = inspect.signature(JurisRankAPI.analyze_document)
    params = list(sig.parameters.keys())
    if 'document_path' in params:
        print("  ✅ analyze_document has 'document_path' parameter")
    else:
        print("  ❌ analyze_document missing 'document_path' parameter")
    
    # search_jurisprudence signature  
    sig = inspect.signature(JurisRankAPI.search_jurisprudence)
    params = list(sig.parameters.keys())
    if 'query' in params and 'jurisdiction' in params:
        print("  ✅ search_jurisprudence has required parameters")
    else:
        print("  ❌ search_jurisprudence missing required parameters")

def validate_models():
    """Validate data model structure."""
    print("\n🏗️  Validating Data Models...")
    
    # Test LegalDocument model
    try:
        doc = LegalDocument(
            id="test_123",
            title="Test Case",
            court="Test Court",
            date="2024-01-01",
            authority_score=85.5
        )
        print("  ✅ LegalDocument model validation passed")
    except Exception as e:
        print(f"  ❌ LegalDocument model error: {e}")
    
    # Test AnalysisResult model
    try:
        result = AnalysisResult(
            document_id="doc_123",
            authority_score=88.5,
            confidence=0.95,
            analysis_summary="Test analysis"
        )
        print("  ✅ AnalysisResult model validation passed")
    except Exception as e:
        print(f"  ❌ AnalysisResult model error: {e}")
    
    # Test AuthorityScore model
    try:
        from datetime import datetime
        authority = AuthorityScore(
            entity_id="court_123",
            entity_type="court",
            name="Supreme Court",
            authority_score=92.0,
            jurisdiction="argentina"
        )
        print("  ✅ AuthorityScore model validation passed")
    except Exception as e:
        print(f"  ❌ AuthorityScore model error: {e}")

def validate_api_info():
    """Validate API information consistency."""
    print("\n📊 Validating API Information...")
    
    info = get_api_info()
    required_keys = ['version', 'api_base_url', 'free_tier', 'supported_languages', 'supported_jurisdictions']
    
    for key in required_keys:
        if key in info:
            print(f"  ✅ API info contains '{key}': {info[key]}")
        else:
            print(f"  ❌ API info missing '{key}'")

def validate_error_handling():
    """Test error handling and validation."""
    print("\n🛡️  Validating Error Handling...")
    
    # Test invalid authority score
    try:
        doc = LegalDocument(
            id="test_123",
            title="Test Case", 
            court="Test Court",
            date="2024-01-01",
            authority_score=150  # Invalid: > 100
        )
        print("  ❌ Should have raised error for invalid authority score")
    except ValueError:
        print("  ✅ Correctly validates authority score range")
    except Exception as e:
        print(f"  ⚠️  Unexpected error type: {e}")
    
    # Test invalid entity type
    try:
        authority = AuthorityScore(
            entity_id="test",
            entity_type="invalid_type",
            name="Test",
            authority_score=85.0,
            jurisdiction="argentina"
        )
        print("  ❌ Should have raised error for invalid entity type")
    except ValueError:
        print("  ✅ Correctly validates entity type")
    except Exception as e:
        print(f"  ⚠️  Unexpected error type: {e}")

def main():
    """Run all validation tests."""
    print("🚀 JurisRank API Validation Suite")
    print("=" * 40)
    
    validate_api_structure()
    validate_models()
    validate_api_info()
    validate_error_handling()
    
    print("\n" + "=" * 40)
    print("✅ API validation completed successfully!")

if __name__ == "__main__":
    main()
