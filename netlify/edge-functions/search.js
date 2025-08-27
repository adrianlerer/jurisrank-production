export default async (request, context) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-API-Key, Authorization',
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff'
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 200, headers });
  }

  if (request.method !== 'GET') {
    return new Response(
      JSON.stringify({
        error: {
          code: 405,
          message: 'Method not allowed. Use GET for precedent search.',
          allowed_methods: ['GET', 'OPTIONS']
        }
      }),
      { status: 405, headers }
    );
  }

  const url = new URL(request.url);
  const query = url.searchParams.get('query') || '';
  const jurisdiction = url.searchParams.get('jurisdiction') || 'argentina';
  const limit = Math.min(parseInt(url.searchParams.get('limit')) || 10, 50);
  const offset = parseInt(url.searchParams.get('offset')) || 0;

  if (!query.trim()) {
    return new Response(
      JSON.stringify({
        error: {
          code: 400,
          message: 'Missing required parameter: query',
          example: '/api/v1/precedents/search?query=constitutional law&jurisdiction=argentina&limit=10'
        }
      }),
      { status: 400, headers }
    );
  }

  // Mock jurisprudential database with Patent P7 scoring
  const generatePrecedents = (searchQuery, jurisdiction, limit) => {
    const precedentsDb = {
      argentina: [
        {
          case_id: 'arg_csjn_2023_001',
          title: 'Recurso de Amparo - Derecho a la Salud vs. Obra Social',
          court: 'Corte Suprema de Justicia de la Nación',
          date: '2023-05-15',
          citation: 'CSJN, Fallos 345:789',
          summary: 'Análisis evolutivo del derecho a la salud en el contexto de prestaciones médicas de alto costo. Aplicación de principios constitucionales con metodología P7.',
          key_concepts: ['derecho a la salud', 'amparo', 'prestaciones médicas', 'proporcionalidad'],
          authority_score: 95.2,
          relevance_score: 0.94,
          patent_p7_compliance: true
        },
        {
          case_id: 'arg_csjn_2023_002', 
          title: 'Contrato de Adhesión - Cláusulas Abusivas en Servicios Financieros',
          court: 'Cámara Nacional de Apelaciones en lo Comercial',
          date: '2023-03-20',
          citation: 'CNCom, Sala A, 15/03/2023',
          summary: 'Evaluación de cláusulas contractuales bajo criterios evolutivos. Análisis de poder negociador asimétrico con enfoque P7.',
          key_concepts: ['contrato de adhesión', 'cláusulas abusivas', 'derecho del consumidor', 'servicios financieros'],
          authority_score: 82.7,
          relevance_score: 0.87,
          patent_p7_compliance: true
        },
        {
          case_id: 'arg_federal_2023_003',
          title: 'Responsabilidad Civil - Daño Ambiental Colectivo', 
          court: 'Tribunal Federal de Primera Instancia',
          date: '2023-07-08',
          citation: 'TF1I, Expte. 4521/2022',
          summary: 'Determinación de responsabilidad civil por daños ambientales aplicando metodologías evolutivas de causalidad.',
          key_concepts: ['responsabilidad civil', 'daño ambiental', 'acción colectiva', 'causalidad evolutiva'],
          authority_score: 78.4,
          relevance_score: 0.82,
          patent_p7_compliance: true
        }
      ],
      usa: [
        {
          case_id: 'usa_scotus_2023_001',
          title: 'Constitutional Analysis - Equal Protection in Digital Age',
          court: 'Supreme Court of the United States',
          date: '2023-06-12',
          citation: '598 U.S. ___ (2023)',
          summary: 'Evolution of Equal Protection Clause interpretation in digital privacy contexts using adaptive constitutional methodology.',
          key_concepts: ['equal protection', 'digital rights', 'constitutional evolution', 'privacy'],
          authority_score: 98.1,
          relevance_score: 0.91,
          patent_p7_compliance: true
        }
      ],
      canada: [
        {
          case_id: 'can_scc_2023_001',
          title: 'Charter Rights - Indigenous Land Claims Evolution',
          court: 'Supreme Court of Canada', 
          date: '2023-04-25',
          citation: '2023 SCC 15',
          summary: 'Evolutionary interpretation of Charter rights in indigenous contexts with adaptive legal framework analysis.',
          key_concepts: ['charter rights', 'indigenous law', 'land claims', 'constitutional evolution'],
          authority_score: 93.8,
          relevance_score: 0.89,
          patent_p7_compliance: true
        }
      ]
    };

    const cases = precedentsDb[jurisdiction] || precedentsDb['argentina'];
    
    // Filter cases based on query relevance
    const queryWords = searchQuery.toLowerCase().split(/\s+/);
    const filteredCases = cases.filter(case_ => {
      const searchableText = (
        case_.title + ' ' + 
        case_.summary + ' ' + 
        case_.key_concepts.join(' ')
      ).toLowerCase();
      
      return queryWords.some(word => searchableText.includes(word));
    });

    // Sort by relevance score (Patent P7 ranking)
    filteredCases.sort((a, b) => b.relevance_score - a.relevance_score);
    
    return filteredCases.slice(offset, offset + limit);
  };

  const results = generatePrecedents(query, jurisdiction, limit);
  const totalResults = jurisdiction === 'argentina' ? 847 : jurisdiction === 'usa' ? 1205 : 623;

  const searchResponse = {
    results: results,
    search_metadata: {
      query: query,
      jurisdiction: jurisdiction,
      total_results: totalResults,
      returned_results: results.length,
      limit: limit,
      offset: offset,
      has_more: offset + results.length < totalResults,
      query_time_ms: Math.floor(Math.random() * 150) + 45
    },
    evolutionary_analysis: {
      methodology: 'evolutionary_precedent_ranking',
      ranking_factors: [
        'jurisdictional_authority',
        'temporal_relevance', 
        'cross_citation_density',
        'conceptual_similarity',
        'precedential_strength'
      ],
      confidence_score: 0.92,
      algorithm_version: 'JurisRank-Search-2025.1'
    },
    pagination: {
      current_page: Math.floor(offset / limit) + 1,
      total_pages: Math.ceil(totalResults / limit),
      next_page_url: offset + limit < totalResults ? 
        `/api/v1/precedents/search?query=${encodeURIComponent(query)}&jurisdiction=${jurisdiction}&limit=${limit}&offset=${offset + limit}` : null,
      prev_page_url: offset > 0 ?
        `/api/v1/precedents/search?query=${encodeURIComponent(query)}&jurisdiction=${jurisdiction}&limit=${limit}&offset=${Math.max(0, offset - limit)}` : null
    },
    timestamp: new Date().toISOString()
  };

  return new Response(JSON.stringify(searchResponse), {
    status: 200,
    headers
  });
};