#!/usr/bin/env python3
"""
JurisRank API Contract Validation Suite
======================================
Comprehensive validation of API contracts, security headers, and OpenAPI compliance.
Based on user requirements for "open-source release" checklist.
"""

import json
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
import time
import sys
from dataclasses import dataclass
import re

# Configuration
BASE_URL = "https://5000-i09td971cyg7b4ytmaaxl.e2b.dev"
LOCAL_URL = "http://localhost:5000"

@dataclass
class ValidationResult:
    """Structure for validation test results."""
    test_name: str
    status: str  # PASS, FAIL, WARNING
    message: str
    details: Optional[Dict[str, Any]] = None
    execution_time: Optional[float] = None

class APIContractValidator:
    """Comprehensive API contract and security validation."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.timeout = 10
        self.results: List[ValidationResult] = []
        
    def log_result(self, result: ValidationResult):
        """Log a validation result."""
        self.results.append(result)
        status_symbol = {
            'PASS': '✅',
            'FAIL': '❌', 
            'WARNING': '⚠️'
        }.get(result.status, '❓')
        
        exec_time = f" ({result.execution_time:.3f}s)" if result.execution_time else ""
        print(f"{status_symbol} {result.test_name}{exec_time}")
        print(f"   {result.message}")
        if result.details:
            print(f"   Details: {json.dumps(result.details, indent=2)}")
        print()

    def validate_dns_tls_connectivity(self) -> ValidationResult:
        """Test 1: DNS/TLS Reachability"""
        start_time = time.time()
        try:
            response = self.session.get(f"{self.base_url}/health")
            execution_time = time.time() - start_time
            
            if response.status_code == 200:
                return ValidationResult(
                    test_name="DNS/TLS Connectivity",
                    status="PASS",
                    message=f"Successfully connected to {self.base_url}",
                    details={
                        "status_code": response.status_code,
                        "response_time": f"{execution_time:.3f}s",
                        "headers": dict(response.headers)
                    },
                    execution_time=execution_time
                )
            else:
                return ValidationResult(
                    test_name="DNS/TLS Connectivity", 
                    status="FAIL",
                    message=f"HTTP {response.status_code} received",
                    execution_time=execution_time
                )
        except Exception as e:
            execution_time = time.time() - start_time
            return ValidationResult(
                test_name="DNS/TLS Connectivity",
                status="FAIL", 
                message=f"Connection failed: {str(e)}",
                execution_time=execution_time
            )

    def validate_security_headers(self) -> List[ValidationResult]:
        """Test 2: Security Headers Audit"""
        results = []
        required_headers = {
            'Content-Security-Policy': 'CSP header missing',
            'X-Content-Type-Options': 'Should be "nosniff"',
            'X-Frame-Options': 'Should be "DENY" or "SAMEORIGIN"', 
            'X-XSS-Protection': 'Should be "1; mode=block"',
            'Strict-Transport-Security': 'HSTS header missing',
            'Referrer-Policy': 'Referrer policy missing'
        }
        
        try:
            response = self.session.get(f"{self.base_url}/health")
            headers = response.headers
            
            for header, description in required_headers.items():
                if header in headers:
                    results.append(ValidationResult(
                        test_name=f"Security Header: {header}",
                        status="PASS",
                        message=f"Present: {headers[header]}",
                        details={"header_value": headers[header]}
                    ))
                else:
                    results.append(ValidationResult(
                        test_name=f"Security Header: {header}",
                        status="WARNING",
                        message=description,
                        details={"recommendation": "Add security header for production"}
                    ))
                    
        except Exception as e:
            results.append(ValidationResult(
                test_name="Security Headers Audit",
                status="FAIL",
                message=f"Failed to retrieve headers: {str(e)}"
            ))
            
        return results

    def validate_api_endpoints(self) -> List[ValidationResult]:
        """Test 3: API Endpoint Contract Validation"""
        results = []
        
        # Test API Status endpoint
        try:
            response = self.session.get(f"{self.base_url}/api/v1/status")
            if response.status_code == 200:
                data = response.json()
                required_fields = ['status', 'version', 'environment', 'endpoints']
                
                missing_fields = [field for field in required_fields if field not in data]
                if not missing_fields:
                    results.append(ValidationResult(
                        test_name="API Status Endpoint Contract",
                        status="PASS",
                        message="All required fields present",
                        details=data
                    ))
                else:
                    results.append(ValidationResult(
                        test_name="API Status Endpoint Contract",
                        status="FAIL",
                        message=f"Missing fields: {missing_fields}",
                        details=data
                    ))
            else:
                results.append(ValidationResult(
                    test_name="API Status Endpoint Contract",
                    status="FAIL",
                    message=f"HTTP {response.status_code}: {response.text}"
                ))
        except Exception as e:
            results.append(ValidationResult(
                test_name="API Status Endpoint Contract",
                status="FAIL",
                message=f"Request failed: {str(e)}"
            ))
            
        # Test Registration endpoint
        try:
            response = self.session.post(f"{self.base_url}/api/v1/auth/register")
            if response.status_code == 200:
                data = response.json()
                required_fields = ['api_key', 'status', 'tier']
                
                missing_fields = [field for field in required_fields if field not in data]
                if not missing_fields:
                    results.append(ValidationResult(
                        test_name="Registration Endpoint Contract",
                        status="PASS",
                        message="API key generation successful",
                        details={"api_key_format": data.get('api_key', '')[:10] + "..."}
                    ))
                else:
                    results.append(ValidationResult(
                        test_name="Registration Endpoint Contract", 
                        status="FAIL",
                        message=f"Missing fields: {missing_fields}"
                    ))
        except Exception as e:
            results.append(ValidationResult(
                test_name="Registration Endpoint Contract",
                status="FAIL",
                message=f"Registration failed: {str(e)}"
            ))
            
        return results

    def validate_error_handling(self) -> List[ValidationResult]:
        """Test 4: Error Contract Validation"""
        results = []
        
        # Test 404 error structure
        try:
            response = self.session.get(f"{self.base_url}/nonexistent")
            if response.status_code == 404:
                # Check if response is JSON structured error
                try:
                    error_data = response.json()
                    if 'error' in error_data or 'message' in error_data:
                        results.append(ValidationResult(
                            test_name="404 Error Structure",
                            status="PASS",
                            message="Structured error response",
                            details=error_data
                        ))
                    else:
                        results.append(ValidationResult(
                            test_name="404 Error Structure",
                            status="WARNING",
                            message="HTML error response (should be JSON)",
                            details={"content_type": response.headers.get('content-type')}
                        ))
                except:
                    results.append(ValidationResult(
                        test_name="404 Error Structure",
                        status="WARNING",
                        message="Non-JSON error response",
                        details={"content_type": response.headers.get('content-type')}
                    ))
        except Exception as e:
            results.append(ValidationResult(
                test_name="404 Error Structure",
                status="FAIL",
                message=f"Error testing failed: {str(e)}"
            ))
            
        # Test method not allowed
        try:
            response = self.session.delete(f"{self.base_url}/health")
            if response.status_code == 405:
                results.append(ValidationResult(
                    test_name="405 Method Not Allowed",
                    status="PASS",
                    message="Proper method validation",
                    details={"allowed_methods": response.headers.get('allow', 'Not specified')}
                ))
        except Exception as e:
            results.append(ValidationResult(
                test_name="405 Method Not Allowed",
                status="WARNING",
                message=f"Method validation unclear: {str(e)}"
            ))
            
        return results

    def validate_performance_requirements(self) -> List[ValidationResult]:
        """Test 5: Performance Contract Validation"""
        results = []
        
        # Health endpoint performance
        times = []
        for i in range(5):
            start_time = time.time()
            try:
                response = self.session.get(f"{self.base_url}/health")
                execution_time = time.time() - start_time
                if response.status_code == 200:
                    times.append(execution_time)
            except:
                pass
            time.sleep(0.1)
        
        if times:
            avg_time = sum(times) / len(times)
            max_time = max(times)
            
            if avg_time < 1.0:  # Under 1 second average
                results.append(ValidationResult(
                    test_name="Health Endpoint Performance",
                    status="PASS",
                    message=f"Average response time: {avg_time:.3f}s",
                    details={
                        "average_ms": f"{avg_time*1000:.1f}",
                        "max_ms": f"{max_time*1000:.1f}",
                        "samples": len(times)
                    }
                ))
            else:
                results.append(ValidationResult(
                    test_name="Health Endpoint Performance",
                    status="WARNING",
                    message=f"Slow response time: {avg_time:.3f}s",
                    details={
                        "average_ms": f"{avg_time*1000:.1f}",
                        "max_ms": f"{max_time*1000:.1f}",
                        "recommendation": "Optimize for < 1s response"
                    }
                ))
        else:
            results.append(ValidationResult(
                test_name="Health Endpoint Performance",
                status="FAIL",
                message="Could not measure performance"
            ))
            
        return results

    def validate_content_types(self) -> List[ValidationResult]:
        """Test 6: Content Type Validation"""
        results = []
        
        endpoints_to_test = [
            ("/health", "application/json"),
            ("/api/v1/status", "application/json")
        ]
        
        for endpoint, expected_type in endpoints_to_test:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                content_type = response.headers.get('content-type', '').lower()
                
                if expected_type.lower() in content_type:
                    results.append(ValidationResult(
                        test_name=f"Content-Type: {endpoint}",
                        status="PASS",
                        message=f"Correct content type: {content_type}",
                        details={"content_type": content_type}
                    ))
                else:
                    results.append(ValidationResult(
                        test_name=f"Content-Type: {endpoint}",
                        status="FAIL",
                        message=f"Expected {expected_type}, got {content_type}",
                        details={"expected": expected_type, "actual": content_type}
                    ))
            except Exception as e:
                results.append(ValidationResult(
                    test_name=f"Content-Type: {endpoint}",
                    status="FAIL",
                    message=f"Request failed: {str(e)}"
                ))
                
        return results

    def generate_openapi_schema(self) -> ValidationResult:
        """Test 7: Generate OpenAPI Schema Documentation"""
        try:
            # Get API status to understand endpoints
            response = self.session.get(f"{self.base_url}/api/v1/status")
            if response.status_code == 200:
                api_data = response.json()
                endpoints = api_data.get('endpoints', {})
                
                # Generate basic OpenAPI 3.0 schema
                openapi_schema = {
                    "openapi": "3.0.0",
                    "info": {
                        "title": "JurisRank API",
                        "version": api_data.get('version', '1.0.0'),
                        "description": "Revolutionary jurisprudential analysis platform",
                        "contact": {
                            "name": "JurisRank Support"
                        },
                        "license": {
                            "name": "MIT"
                        }
                    },
                    "servers": [
                        {
                            "url": self.base_url,
                            "description": "Production server"
                        }
                    ],
                    "paths": {
                        "/health": {
                            "get": {
                                "summary": "Health check endpoint",
                                "responses": {
                                    "200": {
                                        "description": "Service is healthy",
                                        "content": {
                                            "application/json": {
                                                "schema": {
                                                    "type": "object",
                                                    "properties": {
                                                        "status": {"type": "string"},
                                                        "timestamp": {"type": "string"},
                                                        "version": {"type": "string"}
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
                
                # Add discovered endpoints
                for endpoint_key, endpoint_path in endpoints.items():
                    if endpoint_path not in openapi_schema["paths"]:
                        openapi_schema["paths"][endpoint_path] = {
                            "get": {
                                "summary": f"{endpoint_key.title()} endpoint",
                                "responses": {
                                    "200": {
                                        "description": "Success",
                                        "content": {
                                            "application/json": {
                                                "schema": {"type": "object"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                
                # Save schema to file
                with open('openapi_schema.json', 'w') as f:
                    json.dump(openapi_schema, f, indent=2)
                
                return ValidationResult(
                    test_name="OpenAPI Schema Generation",
                    status="PASS",
                    message="OpenAPI 3.0 schema generated successfully",
                    details={
                        "schema_file": "openapi_schema.json",
                        "endpoints_documented": len(openapi_schema["paths"]),
                        "api_version": openapi_schema["info"]["version"]
                    }
                )
        except Exception as e:
            return ValidationResult(
                test_name="OpenAPI Schema Generation",
                status="FAIL",
                message=f"Schema generation failed: {str(e)}"
            )

    def run_comprehensive_validation(self) -> Dict[str, Any]:
        """Run all validation tests and generate report."""
        print("🔍 JurisRank API Contract Validation Suite")
        print("=" * 50)
        print(f"📍 Target URL: {self.base_url}")
        print(f"🕐 Started: {datetime.now().isoformat()}")
        print()
        
        # Run all validation tests
        validation_tests = [
            ("DNS/TLS Connectivity", lambda: [self.validate_dns_tls_connectivity()]),
            ("Security Headers", self.validate_security_headers),
            ("API Endpoints", self.validate_api_endpoints), 
            ("Error Handling", self.validate_error_handling),
            ("Performance", self.validate_performance_requirements),
            ("Content Types", self.validate_content_types),
            ("OpenAPI Schema", lambda: [self.generate_openapi_schema()])
        ]
        
        for test_category, test_function in validation_tests:
            print(f"🧪 {test_category}")
            print("-" * 30)
            
            try:
                test_results = test_function()
                for result in test_results:
                    self.log_result(result)
            except Exception as e:
                error_result = ValidationResult(
                    test_name=test_category,
                    status="FAIL",
                    message=f"Test execution failed: {str(e)}"
                )
                self.log_result(error_result)
        
        # Generate summary
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == "PASS"])
        failed_tests = len([r for r in self.results if r.status == "FAIL"])
        warning_tests = len([r for r in self.results if r.status == "WARNING"])
        
        summary = {
            "validation_timestamp": datetime.now().isoformat(),
            "target_url": self.base_url,
            "total_tests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "warnings": warning_tests,
            "success_rate": f"{(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "0%",
            "results": [
                {
                    "test": r.test_name,
                    "status": r.status,
                    "message": r.message,
                    "details": r.details,
                    "execution_time": r.execution_time
                }
                for r in self.results
            ]
        }
        
        print("📊 VALIDATION SUMMARY")
        print("=" * 50)
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {warning_tests}")
        print(f"📈 Success Rate: {summary['success_rate']}")
        print()
        
        # Save detailed report
        with open('api_contract_validation_report.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📄 Detailed report saved: api_contract_validation_report.json")
        
        return summary

def main():
    """Main validation execution."""
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = BASE_URL
    
    print(f"🚀 JurisRank API Contract Validation")
    print(f"🎯 Target: {base_url}")
    print()
    
    validator = APIContractValidator(base_url)
    summary = validator.run_comprehensive_validation()
    
    # Exit with error code if there are failures
    if summary['failed'] > 0:
        print(f"❌ Validation completed with {summary['failed']} failures")
        sys.exit(1)
    else:
        print(f"✅ All validations passed successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()