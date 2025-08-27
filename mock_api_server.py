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

# Rate limiting storage (simple in-memory for mock)
from collections import defaultdict
import time

rate_limit_storage = defaultdict(list)

def check_rate_limit(ip_address, limit_per_minute=60):
    """Simple rate limiting implementation."""
    current_time = time.time()
    minute_ago = current_time - 60
    
    # Clean old requests
    rate_limit_storage[ip_address] = [
        req_time for req_time in rate_limit_storage[ip_address] 
        if req_time > minute_ago
    ]
    
    # Check if limit exceeded
    if len(rate_limit_storage[ip_address]) >= limit_per_minute:
        return False
    
    # Add current request
    rate_limit_storage[ip_address].append(current_time)
    return True

@app.before_request
def apply_rate_limiting():
    """Apply rate limiting to API endpoints."""
    if request.path.startswith('/api/'):
        client_ip = request.remote_addr or 'unknown'
        
        # Different limits for different endpoints
        if request.path.startswith('/api/v1/auth/'):
            limit = 10  # 10 requests per minute for auth
        else:
            limit = 60  # 60 requests per minute for other APIs
            
        if not check_rate_limit(client_ip, limit):
            return jsonify({
                "error": {
                    "code": 429,
                    "message": "Rate limit exceeded",
                    "details": f"Maximum {limit} requests per minute allowed",
                    "timestamp": datetime.now().isoformat(),
                    "retry_after": 60
                }
            }), 429, {'Retry-After': '60'}

# Security headers middleware
@app.after_request
def add_security_headers(response):
    """Add security headers to all responses."""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'"
    
    # Add HSTS for HTTPS environments (production)
    if request.is_secure or request.headers.get('X-Forwarded-Proto') == 'https':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
    
    # Add rate limit headers
    if hasattr(request, 'rate_limit_remaining'):
        response.headers['X-RateLimit-Limit'] = str(request.rate_limit_limit)
        response.headers['X-RateLimit-Remaining'] = str(request.rate_limit_remaining)
        response.headers['X-RateLimit-Reset'] = str(int(time.time()) + 60)
    
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
            "compare": "/api/v1/compare/systems",
            "openapi": "/api/v1/openapi.json"
        }
    })

@app.route('/api/v1/openapi.json', methods=['GET'])
def get_openapi_schema():
    """OpenAPI 3.0.1 specification endpoint."""
    openapi_schema = {
        "openapi": "3.0.1",
        "info": {
            "title": "JurisRank API",
            "version": "1.0.0",
            "description": "Revolutionary jurisprudential analysis platform with evolutionary methodologies for multi-jurisdictional legal research.",
            "termsOfService": "https://jurisrank.com/terms",
            "contact": {
                "name": "JurisRank Support",
                "email": "api-support@jurisrank.com",
                "url": "https://jurisrank.com/support"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "servers": [
            {
                "url": "https://api.jurisrank.com",
                "description": "Production server"
            },
            {
                "url": f"{request.url_root}api/v1",
                "description": "Development server"
            }
        ],
        "security": [
            {
                "ApiKeyAuth": []
            }
        ],
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key",
                    "description": "Free API key obtained from /auth/register"
                }
            },
            "schemas": {
                "ErrorResponse": {
                    "type": "object",
                    "required": ["error"],
                    "properties": {
                        "error": {
                            "type": "object",
                            "required": ["code", "message", "timestamp"],
                            "properties": {
                                "code": {
                                    "type": "integer",
                                    "description": "HTTP status code"
                                },
                                "message": {
                                    "type": "string",
                                    "description": "Error message"
                                },
                                "details": {
                                    "type": "string",
                                    "description": "Additional error details"
                                },
                                "timestamp": {
                                    "type": "string",
                                    "format": "date-time",
                                    "description": "Error timestamp in ISO 8601 format"
                                },
                                "path": {
                                    "type": "string",
                                    "description": "Request path that generated the error"
                                }
                            }
                        }
                    },
                    "example": {
                        "error": {
                            "code": 404,
                            "message": "Resource not found",
                            "details": "The requested endpoint does not exist",
                            "timestamp": "2025-08-27T17:45:52.887806Z",
                            "path": "/api/v1/nonexistent"
                        }
                    }
                },
                "HealthResponse": {
                    "type": "object",
                    "required": ["status", "timestamp", "version"],
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["healthy", "degraded", "unhealthy"],
                            "description": "Service health status"
                        },
                        "timestamp": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Health check timestamp"
                        },
                        "version": {
                            "type": "string",
                            "description": "API version"
                        }
                    },
                    "example": {
                        "status": "healthy",
                        "timestamp": "2025-08-27T17:45:52.887806Z",
                        "version": "1.0.0-mock"
                    }
                },
                "ApiRegistrationResponse": {
                    "type": "object",
                    "required": ["api_key", "status", "tier"],
                    "properties": {
                        "api_key": {
                            "type": "string",
                            "description": "Generated API key for authentication",
                            "example": "jr_free_mock_api_key_12345"
                        },
                        "status": {
                            "type": "string",
                            "enum": ["active", "pending", "suspended"],
                            "description": "API key status"
                        },
                        "tier": {
                            "type": "string",
                            "enum": ["free_forever", "professional", "enterprise"],
                            "description": "API tier and features available"
                        },
                        "timestamp": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Registration timestamp"
                        },
                        "rate_limit": {
                            "type": "object",
                            "properties": {
                                "requests_per_hour": {
                                    "type": "integer",
                                    "description": "Hourly request limit"
                                },
                                "daily_limit": {
                                    "type": "integer", 
                                    "description": "Daily request limit"
                                }
                            }
                        }
                    }
                },
                "AuthorityAnalysisRequest": {
                    "type": "object",
                    "required": ["case_identifier"],
                    "properties": {
                        "case_identifier": {
                            "type": "string",
                            "description": "Unique case identifier for analysis",
                            "example": "arg_case_001"
                        },
                        "jurisdiction": {
                            "type": "string",
                            "enum": ["argentina", "usa", "canada", "france", "germany"],
                            "description": "Legal jurisdiction for analysis"
                        },
                        "methodology": {
                            "type": "string",
                            "enum": ["evolutionary", "traditional", "comparative"],
                            "default": "evolutionary",
                            "description": "Analysis methodology to apply"
                        }
                    }
                },
                "AuthorityAnalysisResponse": {
                    "type": "object",
                    "required": ["authority_score", "case_id"],
                    "properties": {
                        "authority_score": {
                            "type": "number",
                            "minimum": 0,
                            "maximum": 100,
                            "description": "Evolutionary authority score (0-100)"
                        },
                        "influence_rank": {
                            "type": "integer",
                            "description": "Relative influence ranking"
                        },
                        "citation_count": {
                            "type": "integer",
                            "description": "Number of citations found"
                        },
                        "temporal_trend": {
                            "type": "string",
                            "enum": ["increasing", "stable", "decreasing"],
                            "description": "Authority trend over time"
                        },
                        "confidence_interval": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            },
                            "minItems": 2,
                            "maxItems": 2,
                            "description": "Statistical confidence interval [lower, upper]"
                        },
                        "case_id": {
                            "type": "string",
                            "description": "Analyzed case identifier"
                        },
                        "analysis_timestamp": {
                            "type": "string",
                            "format": "date-time"
                        },
                        "methodology": {
                            "type": "string",
                            "description": "Analysis methodology used"
                        }
                    }
                }
            }
        },
        "paths": {
            "/health": {
                "get": {
                    "tags": ["Health"],
                    "summary": "Health check endpoint",
                    "description": "Returns the current health status of the JurisRank API service",
                    "operationId": "healthCheck",
                    "responses": {
                        "200": {
                            "description": "Service is healthy",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HealthResponse"
                                    }
                                }
                            }
                        },
                        "503": {
                            "description": "Service unavailable",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ErrorResponse"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/auth/register": {
                "get": {
                    "tags": ["Authentication"],
                    "summary": "Register for free API access",
                    "description": "Get a free API key for JurisRank services. No registration required - instant access following 'Intel Inside' model.",
                    "operationId": "registerApi",
                    "responses": {
                        "200": {
                            "description": "API key generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ApiRegistrationResponse"
                                    }
                                }
                            }
                        },
                        "429": {
                            "description": "Rate limit exceeded",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ErrorResponse"
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "tags": ["Authentication"],
                    "summary": "Register with user information",
                    "description": "Register for API access with optional user information for better service",
                    "operationId": "registerApiWithInfo",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "email": {
                                            "type": "string",
                                            "format": "email",
                                            "description": "Email for notifications (optional)"
                                        },
                                        "organization": {
                                            "type": "string",
                                            "description": "Organization name (optional)"
                                        },
                                        "use_case": {
                                            "type": "string",
                                            "description": "Intended use case (optional)"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "API key generated successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ApiRegistrationResponse"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/jurisprudence/authority": {
                "post": {
                    "tags": ["Jurisprudence"],
                    "summary": "Analyze case authority",
                    "description": "Perform evolutionary authority analysis on a specific legal case using Patent P7 methodologies",
                    "operationId": "analyzeAuthority",
                    "security": [{"ApiKeyAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/AuthorityAnalysisRequest"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Authority analysis completed successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/AuthorityAnalysisResponse"
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Invalid request format",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ErrorResponse"
                                    }
                                }
                            }
                        },
                        "401": {
                            "description": "Invalid or missing API key",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/ErrorResponse"
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/precedents/search": {
                "get": {
                    "tags": ["Precedents"],
                    "summary": "Search legal precedents",
                    "description": "Search for relevant legal precedents across multiple jurisdictions",
                    "operationId": "searchPrecedents",
                    "security": [{"ApiKeyAuth": []}],
                    "parameters": [
                        {
                            "name": "query",
                            "in": "query",
                            "required": True,
                            "schema": {
                                "type": "string",
                                "minLength": 3,
                                "maxLength": 500
                            },
                            "description": "Search query for legal precedents"
                        },
                        {
                            "name": "jurisdiction",
                            "in": "query",
                            "schema": {
                                "type": "string",
                                "enum": ["argentina", "usa", "canada", "france", "germany", "all"],
                                "default": "argentina"
                            },
                            "description": "Target jurisdiction for search"
                        },
                        {
                            "name": "limit",
                            "in": "query",
                            "schema": {
                                "type": "integer",
                                "minimum": 1,
                                "maximum": 100,
                                "default": 10
                            },
                            "description": "Maximum number of results to return"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Search completed successfully",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "results": {
                                                "type": "array",
                                                "items": {
                                                    "type": "object",
                                                    "properties": {
                                                        "case_id": {"type": "string"},
                                                        "title": {"type": "string"},
                                                        "court": {"type": "string"},
                                                        "date": {"type": "string", "format": "date"},
                                                        "authority_score": {"type": "number"},
                                                        "relevance_score": {"type": "number"},
                                                        "summary": {"type": "string"},
                                                        "key_concepts": {
                                                            "type": "array",
                                                            "items": {"type": "string"}
                                                        }
                                                    }
                                                }
                                            },
                                            "total_results": {"type": "integer"},
                                            "query_time_ms": {"type": "integer"},
                                            "query": {"type": "string"},
                                            "jurisdiction": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/compare/systems": {
                "post": {
                    "tags": ["Comparative Analysis"],
                    "summary": "Compare legal systems",
                    "description": "Perform cross-jurisdictional comparative analysis between different legal systems (Common Law vs Civil Law)",
                    "operationId": "compareSystems", 
                    "security": [{"ApiKeyAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["concept"],
                                    "properties": {
                                        "concept": {
                                            "type": "string",
                                            "description": "Legal concept to compare across jurisdictions",
                                            "example": "contract_formation"
                                        },
                                        "jurisdictions": {
                                            "type": "array",
                                            "items": {
                                                "type": "string",
                                                "enum": ["argentina", "usa", "canada", "france", "germany"]
                                            },
                                            "description": "Jurisdictions to include in comparison"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Comparative analysis completed",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "comparative_analysis": {
                                                "type": "object",
                                                "description": "Analysis results by jurisdiction"
                                            },
                                            "convergence_score": {
                                                "type": "number",
                                                "minimum": 0,
                                                "maximum": 1,
                                                "description": "Legal convergence score between systems"
                                            },
                                            "concept": {"type": "string"},
                                            "analysis_timestamp": {"type": "string", "format": "date-time"},
                                            "cross_jurisdiction_compatibility": {"type": "number"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "tags": [
            {
                "name": "Health",
                "description": "Service health and monitoring endpoints"
            },
            {
                "name": "Authentication", 
                "description": "API key management and registration"
            },
            {
                "name": "Jurisprudence",
                "description": "Legal case analysis and authority scoring"
            },
            {
                "name": "Precedents",
                "description": "Legal precedent search and discovery"
            },
            {
                "name": "Comparative Analysis",
                "description": "Cross-jurisdictional legal system comparison"
            }
        ],
        "externalDocs": {
            "description": "JurisRank API Documentation",
            "url": "https://docs.jurisrank.com"
        }
    }
    
    return jsonify(openapi_schema)

@app.route('/docs', methods=['GET'])
def swagger_ui():
    """Swagger UI documentation interface."""
    swagger_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>JurisRank API Documentation</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
        <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@4.15.5/favicon-32x32.png" sizes="32x32" />
        <style>
            html {{
                box-sizing: border-box;
                overflow: -moz-scrollbars-vertical;
                overflow-y: scroll;
            }}
            *, *:before, *:after {{
                box-sizing: inherit;
            }}
            body {{
                margin:0;
                background: #fafafa;
            }}
            .swagger-ui .topbar {{
                background-color: #1e3a8a;
            }}
            .swagger-ui .topbar .download-url-wrapper .select-label {{
                color: white;
            }}
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
        <script>
        window.onload = function() {{
            const ui = SwaggerUIBundle({{
                url: '{request.url_root}api/v1/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                apisSorter: "alpha",
                operationsSorter: "alpha",
                docExpansion: "list",
                filter: true,
                showExtensions: true,
                showCommonExtensions: true,
                defaultModelsExpandDepth: 2,
                defaultModelExpandDepth: 2
            }});
        }};
        </script>
    </body>
    </html>
    """
    return swagger_html

if __name__ == '__main__':
    print("🚀 Starting JurisRank Mock API Server...")
    print("📍 Available at: http://localhost:5000")
    print("🔍 Health check: http://localhost:5000/health")
    print("📊 API status: http://localhost:5000/api/v1/status")
    app.run(host='0.0.0.0', port=5000, debug=True)
