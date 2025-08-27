"""
JurisRank Mock API Server
========================
Local server simulation for integration testing.
Enhanced with security headers and structured error responses.
"""

from flask import Flask, jsonify, request, make_response
from datetime import datetime
import json
from functools import wraps

app = Flask(__name__)

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    # Note: HSTS header omitted in development environment
    return response

# Error handlers for structured responses
@app.errorhandler(404)
def not_found(error):
    """Structured 404 error response."""
    return jsonify({
        "error": {
            "code": 404,
            "message": "Resource not found",
            "details": "The requested endpoint does not exist",
            "timestamp": datetime.now().isoformat(),
            "path": request.path
        }
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Structured 405 error response."""
    return jsonify({
        "error": {
            "code": 405,
            "message": "Method not allowed",
            "details": f"The {request.method} method is not allowed for this endpoint",
            "timestamp": datetime.now().isoformat(),
            "path": request.path,
            "allowed_methods": ["GET", "POST"]  # Simplified for mock
        }
    }), 405

@app.errorhandler(400)
def bad_request(error):
    """Structured 400 error response."""
    return jsonify({
        "error": {
            "code": 400,
            "message": "Bad request",
            "details": "Invalid request format or missing required parameters",
            "timestamp": datetime.now().isoformat(),
            "path": request.path
        }
    }), 400

@app.errorhandler(500)
def internal_error(error):
    """Structured 500 error response."""
    return jsonify({
        "error": {
            "code": 500,
            "message": "Internal server error",
            "details": "An unexpected error occurred while processing the request",
            "timestamp": datetime.now().isoformat(),
            "path": request.path
        }
    }), 500

def validate_json_input(f):
    """Decorator to validate JSON input for POST endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            if not request.is_json:
                return jsonify({
                    "error": {
                        "code": 400,
                        "message": "Invalid content type",
                        "details": "Request must be application/json",
                        "timestamp": datetime.now().isoformat()
                    }
                }), 400
        return f(*args, **kwargs)
    return decorated_function

# Mock data
MOCK_CASES = [
    {
        "case_id": "arg_case_001", 
        "title": "Recurso de Amparo - Derecho a la Salud",
        "court": "Corte Suprema de Justicia de la Nación",
        "date": "2023-05-15",
        "authority_score": 95.2,
        "relevance_score": 0.98,
        "summary": "Fallo sobre acceso a medicación de alto costo...",
        "key_concepts": ["derecho a la salud", "amparo", "medicamentos"]
    },
    {
        "case_id": "arg_case_002",
        "title": "Contrato de Adhesión - Cláusulas Abusivas", 
        "court": "Cámara Nacional de Apelaciones",
        "date": "2023-03-20",
        "authority_score": 82.7,
        "relevance_score": 0.85,
        "summary": "Análisis de cláusulas abusivas en contratos bancarios...",
        "key_concepts": ["contrato", "cláusulas abusivas", "derecho del consumidor"]
    }
]

@app.route('/api/v1/auth/register', methods=['GET', 'POST'])
@validate_json_input
def register_api():
    """Mock API registration endpoint."""
    return jsonify({
        "api_key": "jr_free_mock_api_key_12345",
        "status": "active", 
        "tier": "free_forever",
        "timestamp": datetime.now().isoformat(),
        "rate_limit": {
            "requests_per_hour": 1000,
            "daily_limit": 10000
        }
    })

@app.route('/api/v1/jurisprudence/authority', methods=['POST'])
@validate_json_input
def analyze_authority():
    """Mock authority analysis endpoint."""
    data = request.get_json()
    if not data:
        return jsonify({
            "error": {
                "code": 400,
                "message": "Missing request body",
                "details": "Request body with case_identifier is required",
                "timestamp": datetime.now().isoformat()
            }
        }), 400
    
    case_id = data.get('case_identifier', 'unknown')
    
    return jsonify({
        "authority_score": 87.5,
        "influence_rank": 25,
        "citation_count": 156,
        "temporal_trend": "increasing",
        "confidence_interval": [0.82, 0.93],
        "case_id": case_id,
        "analysis_timestamp": datetime.now().isoformat(),
        "methodology": "evolutionary_authority_ranking"
    })

@app.route('/api/v1/precedents/search', methods=['GET'])
def search_precedents():
    """Mock precedent search endpoint."""
    query = request.args.get('query', '')
    jurisdiction = request.args.get('jurisdiction', 'argentina')
    limit = int(request.args.get('limit', 10))
    
    # Filter and return mock cases
    results = MOCK_CASES[:limit]
    
    return jsonify({
        "results": results,
        "total_results": len(MOCK_CASES),
        "query_time_ms": 145,
        "query": query,
        "jurisdiction": jurisdiction
    })

@app.route('/api/v1/compare/systems', methods=['POST'])
@validate_json_input
def compare_systems():
    """Mock comparative analysis endpoint.""" 
    data = request.get_json()
    if not data:
        return jsonify({
            "error": {
                "code": 400,
                "message": "Missing request body",
                "details": "Request body with concept field is required",
                "timestamp": datetime.now().isoformat()
            }
        }), 400
    
    concept = data.get('concept', 'contract_formation')
    
    return jsonify({
        "comparative_analysis": {
            "argentina": {
                "approach": "civil_law",
                "key_principles": ["forma escrita", "causa lícita", "objeto determinado"],
                "authority_cases": ["caso_001", "caso_002"]
            },
            "usa_common": {
                "approach": "common_law",
                "key_principles": ["consideration", "offer_acceptance", "mutual_assent"], 
                "authority_cases": ["case_001", "case_002"]
            }
        },
        "convergence_score": 0.73,
        "concept": concept,
        "analysis_timestamp": datetime.now().isoformat(),
        "cross_jurisdiction_compatibility": 0.78
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-mock"
    })

@app.route('/api/v1/status', methods=['GET'])
def api_status():
    """API status endpoint."""
    return jsonify({
        "status": "operational",
        "version": "1.0.0",
        "environment": "mock_testing",
        "endpoints": {
            "register": "/api/v1/auth/register",
            "authority": "/api/v1/jurisprudence/authority", 
            "search": "/api/v1/precedents/search",
            "compare": "/api/v1/compare/systems"
        }
    })

if __name__ == '__main__':
    print("🚀 Starting JurisRank Mock API Server...")
    print("📍 Available at: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/health")
    print("📊 API status: http://localhost:5000/api/v1/status")
    app.run(host='0.0.0.0', port=5000, debug=True)
