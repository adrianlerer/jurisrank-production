#!/usr/bin/env python3
"""
Enhanced API Integration with Advanced Rate Limiting
Integration layer that adds rate limiting to existing JurisRank API endpoints
"""

import sys
import os
from flask import Flask, request, jsonify, g
from functools import wraps

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import our rate limiter
from rate_limiter import rate_limit, add_rate_limit_monitoring_endpoints


def create_enhanced_api():
    """
    Create Flask app with enhanced rate limiting for JurisRank API
    """
    app = Flask(__name__)
    app.config['TESTING'] = False
    
    # Add rate limiting monitoring endpoints
    add_rate_limit_monitoring_endpoints(app)
    
    # Enhanced Constitutional Analysis endpoint
    @app.route('/api/v1/analysis/constitutional', methods=['POST'])
    @rate_limit
    def enhanced_constitutional_analysis():
        """Enhanced constitutional analysis with rate limiting"""
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'INVALID_REQUEST',
                        'message': 'No JSON data provided'
                    }
                }), 400
            
            required_fields = ['case_facts', 'legal_question']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'MISSING_REQUIRED_FIELDS',
                        'message': f'Missing required fields: {", ".join(missing_fields)}',
                        'details': {'missing_fields': missing_fields}
                    }
                }), 400
            
            # Simulate constitutional analysis
            analysis_result = {
                'analysis_id': f'const_analysis_{hash(data["case_facts"][:50]) % 100000}',
                'constitutional_assessment': {
                    'is_constitutional': True,
                    'confidence_score': 0.85,
                    'constitutional_basis': ['Artículo 18 CN', 'Artículo 19 CN'],
                    'potential_violations': [],
                    'precedent_support': ['Caso Bazterrica', 'Caso Arriola']
                },
                'legal_reasoning': {
                    'primary_arguments': [
                        'Principio de legalidad constitucional',
                        'Garantías del debido proceso'
                    ],
                    'counter_arguments': [],
                    'supporting_precedents': [
                        {
                            'case_name': 'Bazterrica, Gustavo c/ Estado Nacional',
                            'citation': 'Fallos 308:1392',
                            'relevance_score': 0.92,
                            'key_principle': 'Principio de reserva'
                        }
                    ]
                },
                'metadata': {
                    'analysis_timestamp': '2024-09-02T11:45:00Z',
                    'processing_time_ms': 1250,
                    'model_version': 'JurisRank-v0.3.0',
                    'rate_limit_tier': getattr(g, 'client_tier', 'default').value if hasattr(g, 'client_tier') else 'default'
                }
            }
            
            return jsonify({
                'success': True,
                'data': analysis_result
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': str(e)
                }
            }), 500
    
    # Enhanced Precedent Search endpoint
    @app.route('/api/v1/search/precedents', methods=['POST'])
    @rate_limit
    def enhanced_precedent_search():
        """Enhanced precedent search with rate limiting"""
        try:
            data = request.get_json()
            
            if not data or 'query' not in data:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'INVALID_REQUEST',
                        'message': 'Query parameter is required'
                    }
                }), 400
            
            query = data['query']
            limit = data.get('limit', 10)
            
            # Simulate precedent search
            search_results = {
                'results': [
                    {
                        'case_id': 'case_001',
                        'case_name': 'Bazterrica, Gustavo c/ Estado Nacional',
                        'citation': 'Fallos 308:1392',
                        'court': 'Corte Suprema de Justicia',
                        'date_decided': '1986-08-29',
                        'jurisdiction': 'Nacional',
                        'relevance_score': 0.95,
                        'authority_score': 0.98,
                        'summary': 'Leading case sobre principio de reserva y tenencia personal',
                        'key_holdings': ['Principio de reserva', 'Autonomía personal'],
                        'legal_principles': ['Art. 19 CN', 'Principio de legalidad']
                    },
                    {
                        'case_id': 'case_002', 
                        'case_name': 'Arriola, Sebastián c/ Estado Nacional',
                        'citation': 'Fallos 332:1963',
                        'court': 'Corte Suprema de Justicia',
                        'date_decided': '2009-08-25',
                        'jurisdiction': 'Nacional',
                        'relevance_score': 0.88,
                        'authority_score': 0.95,
                        'summary': 'Evolución jurisprudencial del principio de reserva'
                    }
                ][:limit],
                'metadata': {
                    'total_results': 2,
                    'search_time_ms': 890,
                    'query_interpretation': f'Constitutional precedents for: {query}',
                    'filters_applied': {}
                }
            }
            
            return jsonify({
                'success': True,
                'data': search_results
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': str(e)
                }
            }), 500
    
    # Enhanced Document Enhancement endpoint
    @app.route('/api/v1/document/enhance', methods=['POST'])
    @rate_limit
    def enhanced_document_enhancement():
        """Enhanced document enhancement with rate limiting"""
        try:
            data = request.get_json()
            
            if not data or 'document_text' not in data:
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'INVALID_REQUEST',
                        'message': 'document_text parameter is required'
                    }
                }), 400
            
            document_text = data['document_text']
            enhancement_type = data.get('enhancement_type', 'basic_enhancement')
            
            # Simulate document enhancement
            enhancement_result = {
                'enhanced_document': {
                    'enhanced_text': f'{document_text}\\n\\n[Enhanced with legal citations and improvements]',
                    'suggested_citations': [
                        {
                            'position': 150,
                            'original_text': 'principio constitucional',
                            'suggested_citation': 'Ver Fallos 308:1392, "Bazterrica"',
                            'authority_level': 0.95,
                            'verification_status': 'verified'
                        }
                    ],
                    'legal_improvements': [
                        {
                            'section': 'Introduction',
                            'improvement_type': 'citation',
                            'suggestion': 'Add reference to constitutional precedent',
                            'priority': 'high'
                        }
                    ]
                },
                'analysis': {
                    'document_score': 0.82,
                    'legal_strength': 0.78,
                    'citation_quality': 0.85,
                    'areas_for_improvement': ['Citations needed', 'Legal argumentation'],
                    'strengths': ['Clear structure', 'Relevant case facts']
                },
                'metadata': {
                    'enhancement_timestamp': '2024-09-02T11:50:00Z',
                    'processing_time_ms': 2100,
                    'model_version': 'JurisRank-Enhance-v0.3.0'
                }
            }
            
            return jsonify({
                'success': True,
                'data': enhancement_result
            })
            
        except Exception as e:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INTERNAL_ERROR',
                    'message': str(e)
                }
            }), 500
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        """Health check endpoint (no rate limiting for monitoring)"""
        return jsonify({
            'status': 'healthy',
            'timestamp': '2024-09-02T11:45:00Z',
            'version': '0.3.0',
            'services': {
                'rate_limiter': 'operational',
                'api_endpoints': 'operational'
            }
        })
    
    # API Status endpoint
    @app.route('/api/v1/status')
    @rate_limit
    def api_status():
        """API status with rate limiting"""
        from rate_limiter import rate_limiter as rl
        stats = rl.get_stats()
        
        return jsonify({
            'success': True,
            'data': {
                'status': 'operational',
                'version': '0.3.0',
                'rate_limiting': {
                    'enabled': True,
                    'total_clients': stats['total_clients'],
                    'total_requests': stats['total_requests'],
                    'violation_rate': f"{stats['violation_rate']*100:.2f}%"
                },
                'endpoints': {
                    'constitutional_analysis': '/api/v1/analysis/constitutional',
                    'precedent_search': '/api/v1/search/precedents',
                    'document_enhancement': '/api/v1/document/enhance'
                }
            }
        })
    
    return app


def run_enhanced_api():
    """Run the enhanced API server"""
    app = create_enhanced_api()
    
    print("🏛️ JurisRank Enhanced API with Advanced Rate Limiting")
    print("🚀 Starting server on http://localhost:5000")
    print("📊 Rate limiting monitoring: /api/v1/rate-limit/stats")
    print("🔍 Health check: /health")
    print("📋 API status: /api/v1/status")
    
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    run_enhanced_api()