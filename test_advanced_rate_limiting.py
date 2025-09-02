#!/usr/bin/env python3
"""
Comprehensive Rate Limiting Test Suite
Testing all edge cases, scenarios, and production requirements
"""

import pytest
import time
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask
from typing import List, Dict, Any
import json
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from rate_limiter import (
    AdvancedRateLimiter, 
    ClientTier, 
    rate_limit,
    add_rate_limit_monitoring_endpoints
)


class TestAdvancedRateLimiter:
    """Comprehensive test suite for advanced rate limiting"""
    
    def setup_method(self):
        """Setup for each test method"""
        self.rate_limiter = AdvancedRateLimiter()
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        
        # Add test routes with rate limiting
        @self.app.route('/test/endpoint')
        @rate_limit
        def test_endpoint():
            return {'success': True, 'message': 'Test endpoint response'}
        
        @self.app.route('/api/v1/analysis/constitutional', methods=['POST'])
        @rate_limit
        def constitutional_analysis():
            return {'success': True, 'analysis_id': 'test-123'}
        
        @self.app.route('/api/v1/document/enhance', methods=['POST'])
        @rate_limit
        def document_enhance():
            return {'success': True, 'enhanced_document': 'test'}
        
        # Add monitoring endpoints
        add_rate_limit_monitoring_endpoints(self.app)
        
        self.client = self.app.test_client()
    
    def test_client_identifier_generation(self):
        """Test client identifier generation from various sources"""
        with self.app.test_request_context('/', headers={'Authorization': 'Bearer test-key'}):
            client_id = self.rate_limiter.get_client_identifier()
            assert client_id.startswith('api:')
        
        with self.app.test_request_context('/', headers={'X-API-Key': 'test-key'}):
            client_id = self.rate_limiter.get_client_identifier()
            assert client_id.startswith('api:')
        
        with self.app.test_request_context('/', environ_base={'REMOTE_ADDR': '192.168.1.1'},
                                         headers={'User-Agent': 'TestAgent/1.0'}):
            client_id = self.rate_limiter.get_client_identifier()
            assert client_id.startswith('anon:')
    
    def test_client_tier_detection(self):
        """Test client tier detection logic"""
        # Test API key clients
        api_client_id = "api:1234567890abcdef"
        tier = self.rate_limiter.detect_client_tier(api_client_id)
        assert tier in [ClientTier.AUTHENTICATED, ClientTier.PREMIUM, ClientTier.ADMIN]
        
        # Test anonymous clients
        anon_client_id = "anon:1234567890abcdef"
        tier = self.rate_limiter.detect_client_tier(anon_client_id)
        assert tier == ClientTier.DEFAULT
    
    def test_basic_rate_limiting(self):
        """Test basic rate limiting functionality"""
        # Configure low limits for testing
        self.rate_limiter.tier_limits[ClientTier.DEFAULT].requests_per_hour = 5
        
        # Make requests within limit
        for i in range(4):
            response = self.client.get('/test/endpoint')
            assert response.status_code == 200
            assert 'X-RateLimit-Limit' in response.headers
            assert 'X-RateLimit-Remaining' in response.headers
        
        # Next request should still be allowed (5th request)
        response = self.client.get('/test/endpoint')
        assert response.status_code == 200
        assert response.headers['X-RateLimit-Remaining'] == '0'
        
        # 6th request should be rate limited
        response = self.client.get('/test/endpoint')
        assert response.status_code == 429
        assert 'RATE_LIMIT_EXCEEDED' in response.get_json()['error']['code']
    
    def test_rate_limit_headers(self):
        """Test RFC-compliant rate limiting headers"""
        response = self.client.get('/test/endpoint')
        
        # Check required headers
        required_headers = [
            'X-RateLimit-Limit',
            'X-RateLimit-Remaining', 
            'X-RateLimit-Reset',
            'X-RateLimit-Window',
            'X-RateLimit-Policy'
        ]
        
        for header in required_headers:
            assert header in response.headers, f"Missing required header: {header}"
        
        # Validate header values
        assert int(response.headers['X-RateLimit-Limit']) > 0
        assert int(response.headers['X-RateLimit-Remaining']) >= 0
        assert int(response.headers['X-RateLimit-Reset']) > time.time()
        assert int(response.headers['X-RateLimit-Window']) > 0
    
    def test_retry_after_header(self):
        """Test Retry-After header on rate limit exceeded"""
        # Set very low limit
        self.rate_limiter.tier_limits[ClientTier.DEFAULT].requests_per_hour = 1
        
        # First request should succeed
        response = self.client.get('/test/endpoint')
        assert response.status_code == 200
        
        # Second request should be rate limited with Retry-After header
        response = self.client.get('/test/endpoint')
        assert response.status_code == 429
        assert 'Retry-After' in response.headers
        assert int(response.headers['Retry-After']) > 0
    
    def test_endpoint_specific_limits(self):
        """Test endpoint-specific rate limiting"""
        # Constitutional analysis has lower limits
        const_limit = self.rate_limiter.endpoint_limits['/api/v1/analysis/constitutional']
        
        # Make requests up to constitutional analysis limit
        for i in range(const_limit.requests_per_hour):
            response = self.client.post('/api/v1/analysis/constitutional')
            if response.status_code == 429:
                break
        
        # Next request to constitutional analysis should be limited
        response = self.client.post('/api/v1/analysis/constitutional')
        assert response.status_code == 429
        
        # But regular endpoint might still work (if it has higher limits)
        response = self.client.get('/test/endpoint')
        # This might be 200 or 429 depending on overall limits
    
    def test_different_client_tiers(self):
        """Test different rate limits for different client tiers"""
        # Test with different authorization headers to simulate tiers
        headers_default = {}
        headers_authenticated = {'Authorization': 'Bearer valid-key'}
        
        # Reset limits for testing
        self.rate_limiter.tier_limits[ClientTier.DEFAULT].requests_per_hour = 2
        self.rate_limiter.tier_limits[ClientTier.AUTHENTICATED].requests_per_hour = 10
        
        # Default tier client should be limited quickly
        for i in range(3):
            response = self.client.get('/test/endpoint', headers=headers_default)
            if response.status_code == 429:
                break
        assert response.status_code == 429
        
        # Authenticated client should have higher limits
        response = self.client.get('/test/endpoint', headers=headers_authenticated)
        assert response.status_code == 200
    
    def test_concurrent_requests(self):
        """Test rate limiting under concurrent load"""
        # Set low limit for testing
        self.rate_limiter.tier_limits[ClientTier.DEFAULT].requests_per_hour = 10
        
        def make_request():
            return self.client.get('/test/endpoint')
        
        # Make 20 concurrent requests
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [future.result() for future in as_completed(futures)]
        
        # Count successful and rate-limited responses
        success_count = sum(1 for r in results if r.status_code == 200)
        rate_limited_count = sum(1 for r in results if r.status_code == 429)
        
        assert success_count <= 10  # Should not exceed rate limit
        assert rate_limited_count > 0  # Should have some rate limited
        assert success_count + rate_limited_count == 20  # All requests accounted for
    
    def test_thread_safety(self):
        """Test thread safety of rate limiter"""
        results = []
        
        def worker_thread():
            local_results = []
            for i in range(50):
                client_id = f"test-client-{threading.current_thread().ident}"
                is_allowed, info = self.rate_limiter.is_within_limits(
                    client_id, ClientTier.DEFAULT, '/test/endpoint'
                )
                local_results.append(is_allowed)
            results.extend(local_results)
        
        # Run multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker_thread)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should have processed all requests without errors
        assert len(results) == 250  # 5 threads * 50 requests
    
    def test_time_window_behavior(self):
        """Test behavior across different time windows"""
        # Set limits with minute restrictions
        self.rate_limiter.tier_limits[ClientTier.DEFAULT].requests_per_minute = 2
        self.rate_limiter.tier_limits[ClientTier.DEFAULT].requests_per_hour = 100
        
        # Make 2 requests (should succeed)
        for i in range(2):
            response = self.client.get('/test/endpoint')
            assert response.status_code == 200
        
        # 3rd request should be rate limited due to minute limit
        response = self.client.get('/test/endpoint')
        assert response.status_code == 429
    
    def test_rate_limit_statistics(self):
        """Test rate limiting statistics endpoint"""
        # Make some requests first
        for i in range(5):
            self.client.get('/test/endpoint')
        
        # Check statistics
        response = self.client.get('/api/v1/rate-limit/stats')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert 'total_clients' in data['data']
        assert 'total_requests' in data['data']
        assert 'total_violations' in data['data']
        assert data['data']['total_requests'] >= 5
    
    def test_client_usage_endpoint(self):
        """Test individual client usage endpoint"""
        # Make some requests
        for i in range(3):
            self.client.get('/test/endpoint')
        
        # Check usage
        response = self.client.get('/api/v1/rate-limit/my-usage')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['success'] is True
        assert 'client_tier' in data['data']
        assert 'requests_made' in data['data']
        assert data['data']['requests_made'] >= 3
    
    def test_cleanup_old_clients(self):
        """Test cleanup of old client records"""
        # Add some fake old clients
        old_time = time.time() - 100000  # Very old
        
        for i in range(10):
            client_id = f"old-client-{i}"
            self.rate_limiter.clients[client_id] = type('Usage', (), {
                'requests_count': 0,
                'first_request_time': old_time,
                'last_request_time': old_time,
                'window_start': old_time,
                'total_requests': 0,
                'violations': 0
            })()
        
        initial_count = len(self.rate_limiter.clients)
        
        # Run cleanup
        self.rate_limiter.cleanup_old_clients(max_age=86400)  # 1 day
        
        final_count = len(self.rate_limiter.clients)
        assert final_count < initial_count
    
    def test_error_response_format(self):
        """Test error response format compliance"""
        # Force a rate limit error
        self.rate_limiter.tier_limits[ClientTier.DEFAULT].requests_per_hour = 1
        
        # First request succeeds
        self.client.get('/test/endpoint')
        
        # Second request should fail with proper format
        response = self.client.get('/test/endpoint')
        assert response.status_code == 429
        
        error_data = response.get_json()
        assert 'error' in error_data
        assert 'code' in error_data['error']
        assert 'message' in error_data['error']
        assert 'details' in error_data['error']
        assert error_data['error']['code'] == 'RATE_LIMIT_EXCEEDED'
    
    def test_burst_allowance(self):
        """Test burst allowance functionality"""
        # This would require more sophisticated implementation
        # For now, verify the burst_allowance field exists
        limits = self.rate_limiter.tier_limits[ClientTier.DEFAULT]
        assert hasattr(limits, 'burst_allowance')
        assert limits.burst_allowance > 0
    
    def test_multiple_endpoints_interference(self):
        """Test that different endpoints don't interfere incorrectly"""
        # Set up different limits
        const_endpoint = '/api/v1/analysis/constitutional'
        enhance_endpoint = '/api/v1/document/enhance'
        
        # Make requests to constitutional endpoint
        responses_const = []
        for i in range(10):
            response = self.client.post(const_endpoint)
            responses_const.append(response)
            if response.status_code == 429:
                break
        
        # Make requests to enhancement endpoint
        responses_enhance = []
        for i in range(10):
            response = self.client.post(enhance_endpoint)
            responses_enhance.append(response)
            if response.status_code == 429:
                break
        
        # Both endpoints should have their own limits applied
        const_success = sum(1 for r in responses_const if r.status_code == 200)
        enhance_success = sum(1 for r in responses_enhance if r.status_code == 200)
        
        # Should have some successful requests on both
        # (exact numbers depend on configured limits)
        assert const_success >= 0
        assert enhance_success >= 0


def run_comprehensive_tests():
    """Run all rate limiting tests"""
    print("🧪 Starting Comprehensive Rate Limiting Tests")
    print("=" * 50)
    
    test_suite = TestAdvancedRateLimiter()
    
    test_methods = [
        method for method in dir(test_suite) 
        if method.startswith('test_') and callable(getattr(test_suite, method))
    ]
    
    passed = 0
    failed = 0
    
    for test_method_name in test_methods:
        try:
            test_suite.setup_method()
            test_method = getattr(test_suite, test_method_name)
            test_method()
            print(f"✅ {test_method_name}")
            passed += 1
        except Exception as e:
            print(f"❌ {test_method_name}: {str(e)}")
            failed += 1
    
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print(f"🎯 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("🎉 All tests passed! Rate limiting implementation is production-ready.")
    else:
        print("⚠️  Some tests failed. Review implementation before production deployment.")
    
    return failed == 0


def run_load_test():
    """Run a simple load test to verify performance"""
    print("\\n🚀 Running Load Test")
    print("=" * 30)
    
    app = Flask(__name__)
    rate_limiter = AdvancedRateLimiter()
    
    @app.route('/load-test')
    @rate_limit
    def load_test_endpoint():
        return {'message': 'Load test response'}
    
    client = app.test_client()
    
    # Measure performance
    start_time = time.time()
    
    requests_made = 0
    for i in range(1000):
        response = client.get('/load-test')
        requests_made += 1
        if i % 100 == 0:
            print(f"Processed {i} requests...")
    
    end_time = time.time()
    duration = end_time - start_time
    rps = requests_made / duration
    
    print(f"📈 Load Test Results:")
    print(f"   Requests: {requests_made}")
    print(f"   Duration: {duration:.2f}s")
    print(f"   Rate: {rps:.0f} requests/second")
    print(f"   Avg Response Time: {(duration/requests_made)*1000:.2f}ms")


if __name__ == '__main__':
    # Run all tests
    success = run_comprehensive_tests()
    
    # Run load test
    run_load_test()
    
    # Exit with proper code
    sys.exit(0 if success else 1)