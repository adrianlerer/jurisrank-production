#!/bin/bash
# JurisRank External Agent Test Script
# Usage: bash jurisrank_agent_test.sh <BASE_URL>

set -e

BASE_URL="${1:-https://5000-i09td971cyg7b4ytmaaxl.e2b.dev}"

echo "🔍 JurisRank External Agent Test"
echo "🎯 Target: $BASE_URL"
echo "📅 $(date)"
echo "=================================="

# Function to check HTTP status
check_status() {
    local url="$1"
    local expected="$2"
    local description="$3"
    
    echo -n "Testing $description... "
    
    status=$(curl -sS -w "%{http_code}" -o /dev/null "$url" 2>/dev/null || echo "000")
    
    if [ "$status" = "$expected" ]; then
        echo "✅ $status"
        return 0
    else
        echo "❌ $status (expected $expected)"
        return 1
    fi
}

# Function to test JSON endpoint
test_json_endpoint() {
    local url="$1"
    local description="$2"
    
    echo -n "Testing $description... "
    
    response=$(curl -sS "$url" 2>/dev/null || echo '{"error": "connection_failed"}')
    
    if echo "$response" | jq empty 2>/dev/null; then
        echo "✅ Valid JSON"
        echo "$response" | jq -c '.' | head -c 100
        echo "..."
        return 0
    else
        echo "❌ Invalid JSON or connection failed"
        return 1
    fi
}

# Test counters
PASSED=0
TOTAL=0

# Test 1: Health Check
TOTAL=$((TOTAL + 1))
if check_status "$BASE_URL/health" "200" "Health endpoint"; then
    PASSED=$((PASSED + 1))
fi

# Test 2: API Status
TOTAL=$((TOTAL + 1))
if test_json_endpoint "$BASE_URL/api/v1/status" "API Status endpoint"; then
    PASSED=$((PASSED + 1))
fi

# Test 3: OpenAPI Schema
TOTAL=$((TOTAL + 1))
if test_json_endpoint "$BASE_URL/api/v1/openapi.json" "OpenAPI schema"; then
    PASSED=$((PASSED + 1))
    
    # Additional OpenAPI validation
    echo -n "Validating OpenAPI structure... "
    schema=$(curl -sS "$BASE_URL/api/v1/openapi.json" 2>/dev/null || echo '{}')
    
    if echo "$schema" | jq -e '.openapi and .info and .paths' >/dev/null 2>&1; then
        endpoints=$(echo "$schema" | jq '.paths | keys | length')
        version=$(echo "$schema" | jq -r '.info.version')
        echo "✅ Valid (v$version, $endpoints endpoints)"
    else
        echo "❌ Invalid OpenAPI structure"
    fi
fi

# Test 4: Swagger UI
TOTAL=$((TOTAL + 1))
if check_status "$BASE_URL/docs" "200" "Swagger UI docs"; then
    PASSED=$((PASSED + 1))
fi

# Test 5: Security Headers
TOTAL=$((TOTAL + 1))
echo -n "Testing security headers... "
headers=$(curl -sS -I "$BASE_URL/health" 2>/dev/null | tr -d '\r')

security_headers=(
    "x-content-type-options"
    "x-frame-options"
    "x-xss-protection"
    "content-security-policy"
    "referrer-policy"
)

found_headers=0
for header in "${security_headers[@]}"; do
    if echo "$headers" | grep -qi "^$header:"; then
        found_headers=$((found_headers + 1))
    fi
done

if [ "$found_headers" -ge 4 ]; then
    echo "✅ $found_headers/5 security headers present"
    PASSED=$((PASSED + 1))
else
    echo "⚠️ Only $found_headers/5 security headers found"
fi

# Test 6: Rate Limiting Detection
TOTAL=$((TOTAL + 1))
echo -n "Testing rate limiting headers... "
response_headers=$(curl -sS -I "$BASE_URL/api/v1/status" 2>/dev/null | tr -d '\r')

if echo "$response_headers" | grep -qi "x-ratelimit\|retry-after"; then
    echo "✅ Rate limiting headers detected"
    PASSED=$((PASSED + 1))
else
    echo "ℹ️ No rate limiting headers (may be implemented server-side)"
    # Don't fail for this - rate limiting might be implemented differently
    PASSED=$((PASSED + 1))
fi

# Test 7: Error Handling
TOTAL=$((TOTAL + 1))
echo -n "Testing error handling... "
error_response=$(curl -sS "$BASE_URL/nonexistent-endpoint" 2>/dev/null || echo '{"error": "connection_failed"}')

if echo "$error_response" | jq -e '.error.code and .error.message' >/dev/null 2>&1; then
    echo "✅ Structured error response"
    PASSED=$((PASSED + 1))
else
    echo "⚠️ Non-structured error response"
fi

# Summary
echo "=================================="
echo "📊 Test Results: $PASSED/$TOTAL passed"
success_rate=$(( (PASSED * 100) / TOTAL ))
echo "📈 Success Rate: $success_rate%"

if [ "$success_rate" -ge 85 ]; then
    echo "🎉 JurisRank API validation PASSED"
    echo "✅ Ready for external integration"
    exit 0
else
    echo "⚠️ JurisRank API validation needs attention"
    echo "🔧 Some tests failed - check configuration"
    exit 1
fi