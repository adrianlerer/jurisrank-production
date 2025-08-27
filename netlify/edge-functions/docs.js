export default async (request, context) => {
  const headers = {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'public, max-age=300',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block'
  };

  // Get the base URL for OpenAPI schema
  const url = new URL(request.url);
  const baseUrl = `${url.protocol}//${url.host}`;

  const swaggerHtml = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏛️ JurisRank API Documentation</title>
    <meta name="description" content="Interactive documentation for JurisRank jurisprudential analysis API powered by Patent P7 methodology">
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
    <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@4.15.5/favicon-32x32.png" sizes="32x32" />
    <style>
        html {
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }
        *, *:before, *:after {
            box-sizing: inherit;
        }
        body {
            margin: 0;
            background: #fafafa;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* JurisRank Custom Styling */
        .swagger-ui .topbar {
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            border-bottom: 3px solid #f59e0b;
            padding: 10px 0;
        }
        
        .swagger-ui .topbar .download-url-wrapper .select-label {
            color: white;
            font-weight: 600;
        }
        
        .swagger-ui .topbar-wrapper .link {
            color: white;
            font-size: 1.3em;
            font-weight: bold;
        }
        
        .swagger-ui .topbar-wrapper .link:after {
            content: ' - Patent P7 Methodology';
            font-size: 0.7em;
            font-weight: normal;
            opacity: 0.9;
            margin-left: 8px;
        }
        
        .swagger-ui .info .title {
            color: #1e3a8a;
        }
        
        .swagger-ui .scheme-container {
            background: #f3f4f6;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
            margin: 20px 0;
        }
        
        /* Patent P7 Badge */
        .patent-badge {
            display: inline-block;
            background: linear-gradient(45deg, #f59e0b, #d97706);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: bold;
            margin-left: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        .info-banner {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-left: 4px solid #3b82f6;
            padding: 20px;
            margin: 20px 0;
            border-radius: 0 8px 8px 0;
        }
        
        .info-banner h3 {
            color: #1e40af;
            margin-top: 0;
            font-size: 1.2em;
        }
        
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .feature-card {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }
        
        .feature-card .emoji {
            font-size: 2em;
            margin-bottom: 10px;
            display: block;
        }
        
        .api-key-notice {
            background: #fef3c7;
            border: 1px solid #f59e0b;
            padding: 15px;
            border-radius: 6px;
            margin: 20px 0;
        }
        
        .api-key-notice strong {
            color: #92400e;
        }
    </style>
</head>
<body>
    <div class="info-banner">
        <h3>🏛️ JurisRank API <span class="patent-badge">Patent P7</span></h3>
        <p><strong>Revolutionary Jurisprudential Analysis Platform</strong></p>
        <p>Explore cutting-edge legal analysis powered by evolutionary methodologies and multi-jurisdictional intelligence. This interactive documentation provides complete API access for developers.</p>
        
        <div class="feature-grid">
            <div class="feature-card">
                <span class="emoji">🌍</span>
                <strong>Multi-jurisdictional</strong><br>
                <small>Argentina, USA, Canada</small>
            </div>
            <div class="feature-card">
                <span class="emoji">🧬</span>
                <strong>Evolutionary</strong><br>
                <small>Patent P7 Methodology</small>
            </div>
            <div class="feature-card">
                <span class="emoji">⚡</span>
                <strong>Serverless</strong><br>
                <small>99.9% Uptime</small>
            </div>
            <div class="feature-card">
                <span class="emoji">🔓</span>
                <strong>Free Forever</strong><br>
                <small>No Restrictions</small>
            </div>
        </div>
        
        <div class="api-key-notice">
            <strong>🔑 Get Started:</strong> Generate your free API key using the 
            <strong>POST /api/v1/auth/register</strong> endpoint below. Include it in requests as 
            <code>X-API-Key: your_key_here</code>
        </div>
    </div>
    
    <div id="swagger-ui"></div>
    
    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
    <script>
    window.onload = function() {
        const ui = SwaggerUIBundle({
            url: '${baseUrl}/api/v1/openapi.json',
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
            defaultModelExpandDepth: 2,
            tryItOutEnabled: true,
            displayRequestDuration: true,
            supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
            
            // Custom request interceptor for API key handling
            requestInterceptor: function(request) {
                // Add API key if available in localStorage
                const apiKey = localStorage.getItem('jurisrank-api-key');
                if (apiKey) {
                    request.headers['X-API-Key'] = apiKey;
                }
                
                // Add custom user agent
                request.headers['User-Agent'] = 'JurisRank-Swagger-UI/1.0.0';
                
                return request;
            },
            
            // Response interceptor for helpful messages
            responseInterceptor: function(response) {
                if (response.status === 401) {
                    console.warn('🔑 JurisRank API: Get your free API key from /api/v1/auth/register');
                }
                
                return response;
            }
        });
        
        // Add JurisRank branding
        setTimeout(() => {
            const topbar = document.querySelector('.swagger-ui .topbar');
            if (topbar) {
                const brandingDiv = document.createElement('div');
                brandingDiv.innerHTML = \`
                    <div style="position: absolute; top: 50%; right: 20px; transform: translateY(-50%); 
                               color: white; font-size: 0.9em; opacity: 0.9;">
                        <strong>🏛️ Free Forever API</strong> • No Restrictions
                    </div>
                \`;
                topbar.style.position = 'relative';
                topbar.appendChild(brandingDiv);
            }
        }, 500);
        
        // Global API key helper function
        window.saveApiKey = function(key) {
            localStorage.setItem('jurisrank-api-key', key);
            alert('✅ API key saved! It will be automatically included in requests.');
        };
    };
    
    // Console branding and help
    console.log('%c🏛️ JurisRank API Documentation', 'color: #1e3a8a; font-size: 18px; font-weight: bold;');
    console.log('%cPatent P7 Methodology - Revolutionary Jurisprudential Analysis', 'color: #374151; font-style: italic;');
    console.log('%c\\n💡 Tip: Save your API key for automatic inclusion:', 'color: #374151;');
    console.log('%csaveApiKey("your-api-key-here")', 'color: #059669; font-family: monospace; font-weight: bold;');
    </script>
</body>
</html>`;

  return new Response(swaggerHtml, {
    status: 200,
    headers
  });
};