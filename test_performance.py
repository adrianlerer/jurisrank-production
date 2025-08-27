"""
JurisRank Performance & Stress Tests
==================================
Performance testing and load analysis.
"""

import sys
sys.path.insert(0, 'src')

import requests
import time
import threading
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from jurisrank import JurisRankAPI

# Configuration
BASE_URL = "http://localhost:5000"
API_KEY = "jr_free_mock_api_key_12345"

class PerformanceTester:
    def __init__(self):
        self.results = []
        self.errors = []

    def time_request(self, url, method='GET', **kwargs):
        """Time a single request."""
        start_time = time.time()
        try:
            if method == 'GET':
                response = requests.get(url, **kwargs)
            elif method == 'POST':
                response = requests.post(url, **kwargs)
            
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to ms
            
            return {
                'duration': duration,
                'status_code': response.status_code,
                'success': response.status_code == 200
            }
        except Exception as e:
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            self.errors.append(str(e))
            return {
                'duration': duration,
                'status_code': None,
                'success': False,
                'error': str(e)
            }

    def run_concurrent_requests(self, url, num_requests=10, num_threads=5, method='GET', **kwargs):
        """Run concurrent requests and measure performance."""
        results = []
        
        def make_request():
            return self.time_request(url, method, **kwargs)
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
        
        return results

def test_response_times():
    """Test individual endpoint response times."""
    print("⏱️  Testing Response Times...")
    
    tester = PerformanceTester()
    
    # Test health endpoint
    result = tester.time_request(f"{BASE_URL}/health")
    print(f"  ✅ Health check: {result['duration']:.2f}ms")
    
    # Test API status
    result = tester.time_request(f"{BASE_URL}/api/v1/status")
    print(f"  ✅ API status: {result['duration']:.2f}ms")
    
    # Test search endpoint
    result = tester.time_request(
        f"{BASE_URL}/api/v1/precedents/search",
        params={"query": "test", "limit": 5}
    )
    print(f"  ✅ Search query: {result['duration']:.2f}ms")
    
    # Test authority analysis
    result = tester.time_request(
        f"{BASE_URL}/api/v1/jurisprudence/authority",
        method='POST',
        json={"case_identifier": "test_case", "jurisdiction": "argentina"},
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    print(f"  ✅ Authority analysis: {result['duration']:.2f}ms")

def test_concurrent_load():
    """Test concurrent request handling."""
    print("🚀 Testing Concurrent Load...")
    
    tester = PerformanceTester()
    
    # Test concurrent health checks
    results = tester.run_concurrent_requests(
        f"{BASE_URL}/health",
        num_requests=20,
        num_threads=5
    )
    
    durations = [r['duration'] for r in results if r['success']]
    success_rate = len([r for r in results if r['success']]) / len(results)
    
    print(f"  ✅ Concurrent requests: {len(results)}")
    print(f"  ✅ Success rate: {success_rate:.2%}")
    print(f"  ✅ Avg response time: {statistics.mean(durations):.2f}ms")
    print(f"  ✅ Min/Max: {min(durations):.2f}ms / {max(durations):.2f}ms")

def test_search_performance():
    """Test search endpoint under load."""
    print("🔍 Testing Search Performance...")
    
    tester = PerformanceTester()
    
    search_queries = [
        "constitutional law",
        "contract formation",
        "human rights",
        "administrative law",
        "criminal procedure"
    ]
    
    results = []
    for query in search_queries:
        result = tester.time_request(
            f"{BASE_URL}/api/v1/precedents/search",
            params={"query": query, "limit": 10}
        )
        results.append(result)
    
    durations = [r['duration'] for r in results if r['success']]
    success_rate = len([r for r in results if r['success']]) / len(results)
    
    print(f"  ✅ Search queries tested: {len(search_queries)}")
    print(f"  ✅ Success rate: {success_rate:.2%}")
    print(f"  ✅ Avg search time: {statistics.mean(durations):.2f}ms")

def test_stress_testing():
    """Stress test with high load."""
    print("💪 Stress Testing (High Load)...")
    
    tester = PerformanceTester()
    
    # High-load concurrent test
    results = tester.run_concurrent_requests(
        f"{BASE_URL}/api/v1/precedents/search",
        num_requests=50,
        num_threads=10,
        params={"query": "stress test", "limit": 5}
    )
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    if successful:
        durations = [r['duration'] for r in successful]
        avg_time = statistics.mean(durations)
        max_time = max(durations)
        min_time = min(durations)
    else:
        avg_time = max_time = min_time = 0
    
    print(f"  ✅ Total requests: {len(results)}")
    print(f"  ✅ Successful: {len(successful)} ({len(successful)/len(results):.2%})")
    print(f"  ✅ Failed: {len(failed)}")
    print(f"  ✅ Avg response time: {avg_time:.2f}ms")
    print(f"  ✅ Response time range: {min_time:.2f}ms - {max_time:.2f}ms")
    
    # Performance assertions
    success_rate = len(successful) / len(results)
    assert success_rate >= 0.95, f"Success rate too low: {success_rate:.2%}"
    
    if successful:
        assert avg_time < 1000, f"Average response time too high: {avg_time:.2f}ms"

def test_memory_usage():
    """Basic memory usage testing."""
    print("💾 Testing Memory Usage...")
    
    # Test client creation and destruction
    clients = []
    for i in range(100):
        client = JurisRankAPI(api_key=API_KEY, base_url=BASE_URL)
        clients.append(client)
    
    print(f"  ✅ Created {len(clients)} client instances")
    
    # Test large result processing
    tester = PerformanceTester()
    result = tester.time_request(
        f"{BASE_URL}/api/v1/precedents/search",
        params={"query": "test", "limit": 100}
    )
    
    print(f"  ✅ Large result query: {result['duration']:.2f}ms")

def test_api_client_performance():
    """Test JurisRank client performance."""
    print("🔌 Testing API Client Performance...")
    
    client = JurisRankAPI(api_key=API_KEY, base_url=BASE_URL)
    
    # Test multiple operations
    operations = []
    
    start_time = time.time()
    result = client.analyze_document("test.pdf")
    operations.append(('analyze_document', time.time() - start_time))
    
    start_time = time.time()
    docs = client.search_jurisprudence("test query")
    operations.append(('search_jurisprudence', time.time() - start_time))
    
    start_time = time.time()
    score = client.get_authority_score("Test Court")
    operations.append(('get_authority_score', time.time() - start_time))
    
    for op_name, duration in operations:
        print(f"  ✅ {op_name}: {duration*1000:.2f}ms")

def main():
    """Run all performance tests."""
    print("🚀 JurisRank Performance Test Suite")
    print("=" * 50)
    
    try:
        test_response_times()
        test_concurrent_load()
        test_search_performance()
        test_stress_testing()
        test_memory_usage()
        test_api_client_performance()
        
        print("\n" + "=" * 50)
        print("✅ All performance tests completed successfully!")
        
    except AssertionError as e:
        print(f"\n❌ Performance test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)
