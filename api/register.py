import json
from datetime import datetime
import hashlib
import time

def handler(event, context):
    """Netlify function for API registration endpoint."""
    
    # Generate a unique API key
    timestamp = str(int(time.time()))
    unique_data = f"jr_netlify_{timestamp}"
    api_key = f"jr_free_{hashlib.md5(unique_data.encode()).hexdigest()[:16]}"
    
    response_data = {
        "api_key": api_key,
        "status": "active", 
        "tier": "free_forever",
        "timestamp": datetime.now().isoformat(),
        "rate_limit": {
            "requests_per_hour": 1000,
            "daily_limit": 10000
        },
        "features": [
            "jurisprudence_analysis",
            "precedent_search", 
            "comparative_systems",
            "authority_scoring"
        ],
        "documentation": "https://docs.jurisrank.com",
        "support": "https://github.com/adrianlerer/jurisrank-core"
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block'
        },
        'body': json.dumps(response_data)
    }