export default async (request, context) => {
  // CORS headers
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'Cache-Control': 'no-cache'
  };

  // Handle OPTIONS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 200, headers });
  }

  // Only allow GET
  if (request.method !== 'GET') {
    return new Response(
      JSON.stringify({
        error: {
          code: 405,
          message: 'Method not allowed',
          allowed_methods: ['GET', 'OPTIONS']
        }
      }),
      { status: 405, headers }
    );
  }

  // Health response
  const healthData = {
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0-netlify',
    environment: 'production',
    uptime: '99.9%',
    maintenance_free: true
  };

  return new Response(JSON.stringify(healthData), {
    status: 200,
    headers
  });
};