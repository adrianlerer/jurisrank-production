"""
JurisRank Integration Tests
==========================
End-to-end testing against mock API server.
"""

import sys
sys.path.insert(0, 'src')

import requests
import json
import time
from jurisrank import JurisRankAPI

# Mock server configuration
BASE_URL = "http://localhost:5000"
API_KEY = "jr_free_mock_api_key_12345"

def test_api_registration():
    """Test API registration endpoint."""
    print("🔐 Testing API Registration...")
    
    response = requests.get(f"{BASE_URL}/api/v1/auth/register")
    assert response.status_code == 200
    
    data = response.json()
    assert "api_key" in data
    assert data["status"] == "active"
    assert data["tier"] == "free_forever"
    
    print(f"  ✅ Registration successful: {data['api_key'][:20]}...")

def test_authority_analysis():
    """Test authority analysis endpoint."""
    print("📊 Testing Authority Analysis...")
    
    payload = {
        "case_identifier": "test_case_123",
        "jurisdiction": "argentina",
        "legal_area": "constitutional"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/jurisprudence/authority",
        json=payload,
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "authority_score" in data
    assert 0 <= data["authority_score"] <= 100
    assert "citation_count" in data
    assert "temporal_trend" in data
    
    print(f"  ✅ Authority Score: {data['authority_score']}")
    print(f"  ✅ Citation Count: {data['citation_count']}")

def test_precedent_search():
    """Test precedent search endpoint."""
    print("🔍 Testing Precedent Search...")
    
    params = {
        "query": "derecho constitucional",
        "jurisdiction": "argentina", 
        "limit": 5
    }
    
    response = requests.get(
        f"{BASE_URL}/api/v1/precedents/search",
        params=params,
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "results" in data
    assert "total_results" in data
    assert len(data["results"]) > 0
    
    # Validate result structure
    result = data["results"][0]
    assert "case_id" in result
    assert "title" in result
    assert "court" in result
    assert "authority_score" in result
    
    print(f"  ✅ Found {len(data['results'])} cases")
    print(f"  ✅ Query time: {data['query_time_ms']}ms")

def test_comparative_analysis():
    """Test comparative analysis endpoint."""
    print("⚖️ Testing Comparative Analysis...")
    
    payload = {
        "concept": "contract_formation",
        "jurisdictions": ["argentina", "usa_common"],
        "time_period": "2020-2025"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/compare/systems",
        json=payload,
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "comparative_analysis" in data
    assert "convergence_score" in data
    assert "argentina" in data["comparative_analysis"]
    
    print(f"  ✅ Convergence Score: {data['convergence_score']}")
    print(f"  ✅ Systems compared: {list(data['comparative_analysis'].keys())}")

def test_api_client_integration():
    """Test JurisRank client against mock API."""
    print("🔌 Testing API Client Integration...")
    
    # Create client with mock base URL
    client = JurisRankAPI(api_key=API_KEY, base_url=BASE_URL)
    
    # Test basic functionality 
    result = client.analyze_document("test_document.pdf")
    assert result.authority_score > 0
    print(f"  ✅ Client analyze_document: {result.authority_score}")
    
    docs = client.search_jurisprudence("constitutional law")
    assert len(docs) > 0
    print(f"  ✅ Client search: {len(docs)} documents")
    
    score = client.get_authority_score("Supreme Court")
    assert score > 0
    print(f"  ✅ Client authority score: {score}")

def test_error_handling():
    """Test error handling and edge cases."""
    print("🚨 Testing Error Handling...")
    
    # Test invalid endpoint
    response = requests.get(f"{BASE_URL}/api/v1/invalid_endpoint")
    assert response.status_code == 404
    print("  ✅ 404 error handled correctly")
    
    # Test malformed JSON
    response = requests.post(
        f"{BASE_URL}/api/v1/jurisprudence/authority",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code != 200
    print("  ✅ Malformed JSON handled")

def test_performance_metrics():
    """Test basic performance metrics."""
    print("⚡ Testing Performance Metrics...")
    
    # Measure response times
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/health")
    health_time = (time.time() - start_time) * 1000
    
    start_time = time.time()
    response = requests.get(f"{BASE_URL}/api/v1/precedents/search?query=test&limit=5")
    search_time = (time.time() - start_time) * 1000
    
    print(f"  ✅ Health check: {health_time:.2f}ms")
    print(f"  ✅ Search query: {search_time:.2f}ms")
    
    # Basic performance assertions
    assert health_time < 500  # Should be under 500ms
    assert search_time < 2000  # Should be under 2 seconds

def main():
    """Run all integration tests."""
    print("🚀 JurisRank Integration Test Suite")
    print("=" * 45)
    
    try:
        test_api_registration()
        test_authority_analysis()
        test_precedent_search()
        test_comparative_analysis()
        test_api_client_integration()
        test_error_handling()
        test_performance_metrics()
        
        print("\n" + "=" * 45)
        print("✅ All integration tests passed successfully!")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
