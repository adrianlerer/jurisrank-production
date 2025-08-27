"""
JurisRank Precedent Search API - Netlify Serverless Function
===========================================================
Handles jurisprudential precedent search with multi-jurisdictional support.
"""

import json
from datetime import datetime

def handler(event, context):
    """
    Netlify serverless function for precedent search.
    Supports GET requests with query parameters.
    """
    
    # Set CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type, Authorization, X-API-Key",
        "Access-Control-Allow-Methods": "GET, OPTIONS",
        "Content-Type": "application/json",
        "X-Frame-Options": "DENY",
        "X-Content-Type-Options": "nosniff",
        "X-XSS-Protection": "1; mode=block",
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
    }
    
    # Handle OPTIONS preflight requests
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    # Only allow GET requests
    if event.get('httpMethod') != 'GET':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({
                'error': {
                    'code': 405,
                    'message': 'Method not allowed',
                    'allowed_methods': ['GET', 'OPTIONS'],
                    'timestamp': datetime.now().isoformat()
                }
            })
        }
    
    # Parse query parameters
    query_params = event.get('queryStringParameters', {}) or {}
    query = query_params.get('query', '')
    jurisdiction = query_params.get('jurisdiction', 'argentina')
    try:
        limit = int(query_params.get('limit', 10))
    except (ValueError, TypeError):
        limit = 10
    
    # Mock jurisprudential cases data
    mock_cases = [
        {
            "case_id": "arg_case_001", 
            "title": "Recurso de Amparo - Derecho a la Salud",
            "court": "Corte Suprema de Justicia de la Nación",
            "date": "2023-05-15",
            "authority_score": 95.2,
            "relevance_score": 0.98,
            "summary": "Fallo sobre acceso a medicación de alto costo con aplicación del principio de proporcionalidad...",
            "key_concepts": ["derecho a la salud", "amparo", "medicamentos", "proporcionalidad"],
            "jurisdiction": "argentina",
            "patent_p7_compliance": True
        },
        {
            "case_id": "arg_case_002",
            "title": "Contrato de Adhesión - Cláusulas Abusivas", 
            "court": "Cámara Nacional de Apelaciones",
            "date": "2023-03-20",
            "authority_score": 82.7,
            "relevance_score": 0.85,
            "summary": "Análisis evolutivo de cláusulas abusivas en contratos bancarios bajo metodología P7...",
            "key_concepts": ["contrato", "cláusulas abusivas", "derecho del consumidor"],
            "jurisdiction": "argentina",
            "patent_p7_compliance": True
        },
        {
            "case_id": "usa_case_001",
            "title": "Brown v. Board of Education Revisited",
            "court": "Supreme Court of the United States",
            "date": "2023-06-10",
            "authority_score": 98.5,
            "relevance_score": 0.95,
            "summary": "Contemporary application of Equal Protection Clause in educational contexts...",
            "key_concepts": ["equal protection", "education", "constitutional law"],
            "jurisdiction": "usa",
            "patent_p7_compliance": True
        }
    ]
    
    # Filter by jurisdiction if specified
    if jurisdiction != 'all':
        filtered_cases = [case for case in mock_cases if case['jurisdiction'] == jurisdiction]
    else:
        filtered_cases = mock_cases
    
    # Apply limit
    results = filtered_cases[:limit]
    
    # Prepare response
    response_data = {
        "results": results,
        "total_results": len(filtered_cases),
        "query_time_ms": 145,
        "query": query,
        "jurisdiction": jurisdiction,
        "limit": limit,
        "patent_p7_methodology": "evolutionary_precedent_analysis",
        "timestamp": datetime.now().isoformat(),
        "api_version": "1.0.0-netlify"
    }
    
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(response_data)
    }