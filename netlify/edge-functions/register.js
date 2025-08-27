export default async (request, context) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-API-Key',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff'
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 200, headers });
  }

  if (!['GET', 'POST'].includes(request.method)) {
    return new Response(
      JSON.stringify({
        error: { code: 405, message: 'Method not allowed' }
      }),
      { status: 405, headers }
    );
  }

  // Generate API key
  const generateApiKey = () => {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = 'jr_';
    for (let i = 0; i < 32; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  };

  const registrationData = {
    api_key: generateApiKey(),
    tier: 'free_forever',
    rate_limits: {
      requests_per_minute: 60,
      requests_per_day: 10000,
      concurrent_requests: 10
    },
    features: [
      'jurisprudence_authority_analysis',
      'precedent_search',
      'comparative_systems_analysis',
      'evolutionary_methodology',
      'multi_jurisdictional_support'
    ],
    status: 'active',
    created_at: new Date().toISOString(),
    expires_at: null,
    cost: '$0.00 USD',
    upgrade_available: false,
    message: 'Welcome to JurisRank API - Free Forever!'
  };

  return new Response(JSON.stringify(registrationData), {
    status: 200,
    headers
  });
};