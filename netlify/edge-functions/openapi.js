export default async (request, context) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
    'Cache-Control': 'public, max-age=300'
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 200, headers });
  }

  if (request.method !== 'GET') {
    return new Response(
      JSON.stringify({
        error: { code: 405, message: 'Method not allowed' }
      }),
      { status: 405, headers }
    );
  }

  // Get the base URL from request
  const url = new URL(request.url);
  const baseUrl = `${url.protocol}//${url.host}`;

  const openApiSchema = {
    openapi: '3.0.1',
    info: {
      title: 'JurisRank API - Evolutionary Jurisprudential Analysis',
      description: `
Revolutionary API for jurisprudential analysis powered by Patent P7 methodology.

## 🏛️ About JurisRank

JurisRank applies evolutionary methodologies to measure legal authority and influence across diverse jurisdictional systems. Our Patent P7 approach provides unprecedented insights into jurisprudential dynamics.

## 🚀 Features

- **Multi-jurisdictional Analysis**: Argentina, USA, Canada, and expanding
- **Evolutionary Scoring**: Patent P7 methodology for authority measurement  
- **Free Forever**: Complete API access without restrictions
- **Developer Friendly**: Full REST API with comprehensive documentation

## 🔑 Getting Started

1. Register for your free API key: \`POST /api/v1/auth/register\`
2. Include API key in requests: \`X-API-Key: your_key_here\`  
3. Start analyzing jurisprudence with evolutionary precision

## 📚 Patent P7 Methodology

Our proprietary methodology analyzes:
- Jurisdictional hierarchy and authority patterns
- Cross-citation networks and influence propagation
- Temporal evolution of legal precedents
- Multi-system comparative jurisprudence
      `,
      version: '1.0.0',
      contact: {
        name: 'JurisRank API Support',
        url: 'https://github.com/adrianlerer/jurisrank-production'
      },
      license: {
        name: 'MIT License',
        url: 'https://opensource.org/licenses/MIT'
      },
      'x-patent': {
        methodology: 'Patent P7 - Evolutionary Jurisprudential Analysis',
        inventor: 'Ignacio Adrian Lerer',
        status: 'Patent Applied - INPI Argentina'
      }
    },
    servers: [
      {
        url: baseUrl,
        description: 'JurisRank Production API - Maintenance Free'
      }
    ],
    paths: {
      '/health': {
        get: {
          tags: ['System'],
          summary: 'Health Check',
          description: 'Check API operational status and uptime metrics',
          responses: {
            200: {
              description: 'API is healthy and operational',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/HealthResponse' }
                }
              }
            }
          }
        }
      },
      '/api/v1/status': {
        get: {
          tags: ['System'],
          summary: 'API Status',
          description: 'Comprehensive API status including endpoints and metadata',
          responses: {
            200: {
              description: 'Complete API status information',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/StatusResponse' }
                }
              }
            }
          }
        }
      },
      '/api/v1/auth/register': {
        get: {
          tags: ['Authentication'],
          summary: 'Generate Free API Key',
          description: 'Register for immediate free API access - no restrictions',
          responses: {
            200: {
              description: 'API key generated successfully',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/RegisterResponse' }
                }
              }
            }
          }
        },
        post: {
          tags: ['Authentication'],
          summary: 'Generate Free API Key (POST)',
          description: 'Alternative POST method for API key generation',
          responses: {
            200: {
              description: 'API key generated successfully',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/RegisterResponse' }
                }
              }
            }
          }
        }
      },
      '/api/v1/jurisprudence/authority': {
        post: {
          tags: ['JurisRank Analysis'],
          summary: 'Jurisprudential Authority Analysis',
          description: 'Patent P7 evolutionary analysis of legal case authority and precedential strength',
          security: [{ ApiKeyAuth: [] }],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/AuthorityRequest' }
              }
            }
          },
          responses: {
            200: {
              description: 'Authority analysis completed',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/AuthorityResponse' }
                }
              }
            },
            400: {
              description: 'Invalid request parameters',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/ErrorResponse' }
                }
              }
            }
          }
        }
      },
      '/api/v1/precedents/search': {
        get: {
          tags: ['JurisRank Analysis'],
          summary: 'Precedent Search',
          description: 'Search jurisprudential precedents with Patent P7 relevance ranking',
          security: [{ ApiKeyAuth: [] }],
          parameters: [
            {
              name: 'query',
              in: 'query',
              required: true,
              description: 'Search query for legal concepts or case content',
              schema: { type: 'string', example: 'constitutional law' }
            },
            {
              name: 'jurisdiction',
              in: 'query',
              description: 'Legal jurisdiction to search',
              schema: { type: 'string', enum: ['argentina', 'usa', 'canada'], default: 'argentina' }
            },
            {
              name: 'limit',
              in: 'query', 
              description: 'Maximum number of results (1-50)',
              schema: { type: 'integer', minimum: 1, maximum: 50, default: 10 }
            },
            {
              name: 'offset',
              in: 'query',
              description: 'Results offset for pagination',
              schema: { type: 'integer', minimum: 0, default: 0 }
            }
          ],
          responses: {
            200: {
              description: 'Search results with Patent P7 ranking',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/SearchResponse' }
                }
              }
            }
          }
        }
      },
      '/api/v1/compare/systems': {
        post: {
          tags: ['JurisRank Analysis'],
          summary: 'Comparative Systems Analysis', 
          description: 'Cross-jurisdictional legal system comparison with evolutionary convergence analysis',
          security: [{ ApiKeyAuth: [] }],
          requestBody: {
            required: true,
            content: {
              'application/json': {
                schema: { $ref: '#/components/schemas/CompareRequest' }
              }
            }
          },
          responses: {
            200: {
              description: 'Comparative analysis completed',
              content: {
                'application/json': {
                  schema: { $ref: '#/components/schemas/CompareResponse' }
                }
              }
            }
          }
        }
      }
    },
    components: {
      securitySchemes: {
        ApiKeyAuth: {
          type: 'apiKey',
          in: 'header',
          name: 'X-API-Key',
          description: 'Free API key from /api/v1/auth/register'
        }
      },
      schemas: {
        HealthResponse: {
          type: 'object',
          properties: {
            status: { type: 'string', example: 'healthy' },
            timestamp: { type: 'string', format: 'date-time' },
            version: { type: 'string', example: '1.0.0-netlify' },
            environment: { type: 'string', example: 'production' },
            uptime: { type: 'string', example: '99.9%' },
            maintenance_free: { type: 'boolean', example: true }
          }
        },
        AuthorityRequest: {
          type: 'object',
          required: ['case_citation'],
          properties: {
            case_citation: { type: 'string', example: 'CSJN Fallos 340:1304' },
            jurisdiction: { type: 'string', enum: ['argentina', 'usa', 'canada'], default: 'argentina' },
            legal_area: { type: 'string', example: 'constitutional_law' }
          }
        },
        AuthorityResponse: {
          type: 'object',
          properties: {
            authority_score: { type: 'number', example: 95.2 },
            case_citation: { type: 'string' },
            jurisdiction: { type: 'string' },
            patent_p7_methodology: { type: 'object' }
          }
        },
        CompareRequest: {
          type: 'object',
          properties: {
            concept: { type: 'string', example: 'contract_formation' },
            jurisdictions: { 
              type: 'array', 
              items: { type: 'string' }, 
              example: ['argentina', 'usa', 'canada'] 
            }
          }
        },
        ErrorResponse: {
          type: 'object',
          properties: {
            error: {
              type: 'object',
              properties: {
                code: { type: 'integer' },
                message: { type: 'string' },
                details: { type: 'string' }
              }
            }
          }
        }
      }
    },
    tags: [
      {
        name: 'System',
        description: 'API health and status endpoints'
      },
      {
        name: 'Authentication', 
        description: 'Free API key registration'
      },
      {
        name: 'JurisRank Analysis',
        description: 'Patent P7 jurisprudential analysis endpoints'
      }
    ],
    'x-tagGroups': [
      {
        name: 'API Management',
        tags: ['System', 'Authentication']
      },
      {
        name: 'Jurisprudential Analysis',
        tags: ['JurisRank Analysis']
      }
    ]
  };

  return new Response(JSON.stringify(openApiSchema), {
    status: 200,
    headers
  });
};