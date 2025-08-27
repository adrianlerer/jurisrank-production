import json

def handler(event, context):
    """Netlify function for OpenAPI schema endpoint."""
    
    # Get the base URL from the event
    headers = event.get('headers', {})
    host = headers.get('host', 'jurisrank-api.netlify.app')
    protocol = 'https'
    base_url = f"{protocol}://{host}"
    
    openapi_schema = {
        "openapi": "3.0.1",
        "info": {
            "title": "JurisRank API",
            "version": "1.0.0",
            "description": "Revolutionary jurisprudential analysis platform with evolutionary methodologies for multi-jurisdictional legal research. Deployed on Netlify for 99.99% uptime.",
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
                "url": base_url,
                "description": "Production server (Netlify)"
            }
        ],
        "security": [{"ApiKeyAuth": []}],
        "components": {
            "securitySchemes": {
                "ApiKeyAuth": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-API-Key",
                    "description": "Free API key obtained from /api/v1/auth/register"
                }
            },
            "schemas": {
                "HealthResponse": {
                    "type": "object",
                    "required": ["status", "timestamp", "version"],
                    "properties": {
                        "status": {"type": "string", "enum": ["healthy"]},
                        "timestamp": {"type": "string", "format": "date-time"},
                        "version": {"type": "string"},
                        "environment": {"type": "string"}
                    }
                },
                "AuthorityAnalysisRequest": {
                    "type": "object",
                    "required": ["case_identifier"],
                    "properties": {
                        "case_identifier": {"type": "string", "example": "arg_case_001"},
                        "jurisdiction": {"type": "string", "enum": ["argentina", "usa", "canada", "france", "germany"]}
                    }
                },
                "AuthorityAnalysisResponse": {
                    "type": "object",
                    "properties": {
                        "authority_score": {"type": "number", "minimum": 0, "maximum": 100},
                        "influence_rank": {"type": "integer"},
                        "citation_count": {"type": "integer"},
                        "temporal_trend": {"type": "string", "enum": ["increasing", "stable", "decreasing"]},
                        "confidence_interval": {"type": "array", "items": {"type": "number"}, "minItems": 2, "maxItems": 2},
                        "case_id": {"type": "string"},
                        "analysis_timestamp": {"type": "string", "format": "date-time"},
                        "methodology": {"type": "string"},
                        "patent_p7_compliant": {"type": "boolean"}
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
                                    "schema": {"$ref": "#/components/schemas/HealthResponse"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/v1/auth/register": {
                "get": {"tags": ["Authentication"], "summary": "Get free API key", "responses": {"200": {"description": "API key generated"}}},
                "post": {"tags": ["Authentication"], "summary": "Register with user info", "responses": {"200": {"description": "API key generated"}}}
            },
            "/api/v1/jurisprudence/authority": {
                "post": {
                    "tags": ["Jurisprudence"],
                    "summary": "Analyze case authority",
                    "description": "Perform evolutionary authority analysis using Patent P7 methodologies",
                    "security": [{"ApiKeyAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/AuthorityAnalysisRequest"}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Authority analysis completed",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/AuthorityAnalysisResponse"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "tags": [
            {"name": "Health", "description": "Service health monitoring"},
            {"name": "Authentication", "description": "Free API key management"},
            {"name": "Jurisprudence", "description": "Legal case analysis"}
        ],
        "externalDocs": {
            "description": "JurisRank GitHub Repository",
            "url": "https://github.com/adrianlerer/jurisrank-core"
        }
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Cache-Control': 'public, max-age=3600'
        },
        'body': json.dumps(openapi_schema)
    }