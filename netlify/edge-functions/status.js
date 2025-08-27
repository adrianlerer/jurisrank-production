export default async (request, context) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff'
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

  const statusData = {
    status: 'operational',
    version: '1.0.0-netlify',
    environment: 'production', 
    timestamp: new Date().toISOString(),
    uptime_guarantee: '99.9%',
    maintenance_free: true,
    endpoints: {
      health: '/health',
      status: '/api/v1/status',
      register: '/api/v1/auth/register',
      authority: '/api/v1/jurisprudence/authority',
      search: '/api/v1/precedents/search',
      compare: '/api/v1/compare/systems',
      openapi: '/api/v1/openapi.json',
      docs: '/docs'
    },
    patent_p7: {
      methodology: 'evolutionary_jurisprudential_analysis',
      compliance: true,
      version: '7.0'
    }
  };

  return new Response(JSON.stringify(statusData), {
    status: 200,
    headers
  });
};