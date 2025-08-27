"""
JurisRank Documentation Validation
=================================
Validates documentation examples and usage patterns.
"""

import sys
sys.path.insert(0, 'src')

import re
import json
from jurisrank import JurisRankAPI, get_version, get_api_info

def test_readme_examples():
    """Test code examples from README.md."""
    print("📖 Testing README Examples...")
    
    # Test basic usage example from README
    print("  🔍 Testing basic usage example...")
    
    try:
        # Example from README.md
        import jurisrank

        # Initialize free API client
        client = jurisrank.JurisRankAPI(api_key="test_api_key")

        # Analyze jurisprudential authority
        authority_score = client.analyze_document("example_case.pdf")
        print(f"    ✅ analyze_document returned: {authority_score.authority_score}")

        # Search relevant precedents
        precedents = client.search_jurisprudence("constitutional law", limit=10)
        print(f"    ✅ search_jurisprudence returned: {len(precedents)} precedents")
        
        # Test individual precedent structure
        for precedent in precedents:
            assert hasattr(precedent, 'id')
            assert hasattr(precedent, 'title')
            assert hasattr(precedent, 'authority_score')
            print(f"    ✅ Precedent structure valid: {precedent.title}")
            break  # Just test the first one
            
    except Exception as e:
        print(f"    ❌ README example failed: {e}")
        raise

def test_api_documentation_examples():
    """Test examples from API documentation."""
    print("📚 Testing API Documentation Examples...")
    
    # Test model creation examples
    print("  🏗️  Testing model examples...")
    
    from jurisrank.models import LegalDocument, AnalysisResult, AuthorityScore
    from datetime import datetime
    
    # Test LegalDocument from docs
    try:
        doc = LegalDocument(
            id="unique_identifier",
            title="Caso Ejemplo vs Estado",
            court="Corte Suprema de Justicia",
            date="2023-05-15",
            authority_score=92.0,
            jurisdiction="argentina",
            summary="Resumen automático del fallo..."
        )
        print(f"    ✅ LegalDocument example: {doc.title}")
    except Exception as e:
        print(f"    ❌ LegalDocument example failed: {e}")
    
    # Test AnalysisResult from docs
    try:
        result = AnalysisResult(
            document_id="doc_123",
            authority_score=85.5,
            confidence=0.92,
            analysis_summary="High authority precedent with strong legal basis",
            insights=["Strong precedential value", "Clear legal reasoning"]
        )
        print(f"    ✅ AnalysisResult example: {result.document_id}")
    except Exception as e:
        print(f"    ❌ AnalysisResult example failed: {e}")

def test_client_configuration():
    """Test client configuration options."""
    print("🔧 Testing Client Configuration...")
    
    # Test default configuration
    client = JurisRankAPI()
    assert client.base_url == "https://api.jurisrank.io"
    print("    ✅ Default configuration works")
    
    # Test custom configuration
    client = JurisRankAPI(
        api_key="test_key",
        base_url="https://custom.api.example.com"
    )
    assert client.api_key == "test_key"
    assert client.base_url == "https://custom.api.example.com"
    print("    ✅ Custom configuration works")
    
    # Test session headers
    assert "User-Agent" in client.session.headers
    assert "jurisrank-python" in client.session.headers["User-Agent"]
    print("    ✅ Session headers configured")

def test_api_info_consistency():
    """Test API info consistency with documentation."""
    print("ℹ️  Testing API Info Consistency...")
    
    info = get_api_info()
    
    # Check documented keys exist
    expected_keys = {
        'version', 'api_base_url', 'documentation', 
        'free_tier', 'supported_languages', 'supported_jurisdictions'
    }
    
    for key in expected_keys:
        assert key in info, f"Missing API info key: {key}"
        print(f"    ✅ {key}: {info[key]}")
    
    # Validate specific values match documentation
    assert info['free_tier'] == 'unlimited'
    assert 'en' in info['supported_languages']
    assert 'es' in info['supported_languages']
    assert 'argentina' in info['supported_jurisdictions']

def test_version_consistency():
    """Test version consistency across files."""
    print("🏷️  Testing Version Consistency...")
    
    version = get_version()
    print(f"    ✅ Package version: {version}")
    
    # Version should be a valid semantic version
    version_pattern = r'^\d+\.\d+\.\d+$'
    assert re.match(version_pattern, version), f"Invalid version format: {version}"
    print(f"    ✅ Version format valid: {version}")

def test_docstring_completeness():
    """Test docstring completeness for public API."""
    print("📝 Testing Docstring Completeness...")
    
    # Test main API class docstrings
    api_class = JurisRankAPI
    assert api_class.__doc__ is not None, "JurisRankAPI missing docstring"
    print("    ✅ JurisRankAPI has docstring")
    
    # Test public methods have docstrings
    public_methods = [
        'analyze_document', 'search_jurisprudence', 
        'get_authority_score', 'analyze_document_async'
    ]
    
    for method_name in public_methods:
        method = getattr(api_class, method_name)
        assert method.__doc__ is not None, f"Method {method_name} missing docstring"
        print(f"    ✅ {method_name} has docstring")

def validate_example_patterns():
    """Validate common usage patterns work correctly."""
    print("🎯 Testing Usage Patterns...")
    
    # Pattern 1: Quick analysis
    client = JurisRankAPI(api_key="test_key")
    result = client.analyze_document("document.pdf")
    assert hasattr(result, 'authority_score')
    assert hasattr(result, 'confidence')
    print("    ✅ Quick analysis pattern works")
    
    # Pattern 2: Batch search
    queries = ["constitutional law", "contract formation", "human rights"]
    results = []
    for query in queries:
        docs = client.search_jurisprudence(query)
        results.extend(docs)
    
    assert len(results) > 0
    print(f"    ✅ Batch search pattern: {len(results)} total results")
    
    # Pattern 3: Authority scoring
    courts = ["Supreme Court", "Appeals Court"]
    scores = []
    for court in courts:
        score = client.get_authority_score(court)
        scores.append(score)
    
    assert all(isinstance(s, (int, float)) for s in scores)
    print(f"    ✅ Authority scoring pattern: {len(scores)} scores")

def test_error_documentation():
    """Test that documented error cases work as described."""
    print("🚨 Testing Error Documentation...")
    
    from jurisrank.models import LegalDocument
    
    # Test documented validation error
    try:
        # This should raise ValueError according to docs
        doc = LegalDocument(
            id="test",
            title="Test",
            court="Test Court",
            date="2024-01-01",
            authority_score=150  # Invalid: > 100
        )
        assert False, "Should have raised ValueError for invalid authority score"
    except ValueError:
        print("    ✅ Authority score validation error works as documented")

def main():
    """Run all documentation validation tests."""
    print("🚀 JurisRank Documentation Validation Suite")
    print("=" * 55)
    
    try:
        test_readme_examples()
        test_api_documentation_examples()
        test_client_configuration()
        test_api_info_consistency()
        test_version_consistency()
        test_docstring_completeness()
        validate_example_patterns()
        test_error_documentation()
        
        print("\n" + "=" * 55)
        print("✅ All documentation validation tests passed!")
        
    except Exception as e:
        print(f"\n❌ Documentation test failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
