"""
JurisRank API Documentation - Netlify Serverless Function
=========================================================
Serves Swagger UI interface for interactive API documentation.
"""

import json

def handler(event, context):
    """
    Netlify serverless function for API documentation interface.
    Serves Swagger UI with dynamic OpenAPI schema integration.
    """
    
    # Get the request origin for proper API URL construction
    headers = event.get('headers', {})
    host = headers.get('host', 'jurisrank-api.netlify.app')
    protocol = 'https' if 'netlify' in host or 'vercel' in host else 'http'
    
    # Construct base URL for API calls
    base_url = f"{protocol}://{host}"
    
    # Swagger UI HTML with JurisRank branding
    swagger_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>JurisRank API Documentation</title>
        <meta name="description" content="Interactive documentation for JurisRank jurisprudential analysis API">
        <meta name="keywords" content="JurisRank, API, jurisprudence, legal analysis, Patent P7">
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui.css" />
        <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@4.15.5/favicon-32x32.png" sizes="32x32" />
        <style>
            html {{
                box-sizing: border-box;
                overflow: -moz-scrollbars-vertical;
                overflow-y: scroll;
            }}
            *, *:before, *:after {{
                box-sizing: inherit;
            }}
            body {{
                margin: 0;
                background: #fafafa;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }}
            
            /* JurisRank Branding */
            .swagger-ui .topbar {{
                background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                border-bottom: 3px solid #f59e0b;
            }}
            
            .swagger-ui .topbar .download-url-wrapper .select-label {{
                color: white;
                font-weight: 600;
            }}
            
            .swagger-ui .topbar-wrapper .link {{
                color: white;
                font-size: 1.2em;
                font-weight: bold;
            }}
            
            .swagger-ui .topbar-wrapper .link:after {{
                content: ' - Revolutionary Jurisprudential Analysis';
                font-size: 0.8em;
                font-weight: normal;
                opacity: 0.9;
            }}
            
            /* Custom styling for JurisRank */
            .swagger-ui .info .title {{
                color: #1e3a8a;
            }}
            
            .swagger-ui .scheme-container {{
                background: #f3f4f6;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
            }}
            
            /* Patent P7 Badge */
            .patent-badge {{
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
            }}
            
            .info-section {{
                background: #eff6ff;
                border-left: 4px solid #3b82f6;
                padding: 15px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
            }}
            
            .info-section h3 {{
                color: #1e40af;
                margin-top: 0;
            }}
            
            /* Security notice */
            .security-notice {{
                background: #fef3c7;
                border: 1px solid #f59e0b;
                padding: 12px;
                border-radius: 6px;
                margin: 15px 0;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="info-section">
            <h3>🏛️ JurisRank API <span class="patent-badge">Patent P7</span></h3>
            <p><strong>Revolutionary Jurisprudential Analysis Platform</strong></p>
            <p>Access cutting-edge legal analysis powered by evolutionary methodologies and multi-jurisdictional intelligence.</p>
            
            <div class="security-notice">
                <strong>🔐 Free Forever API:</strong> Register for your free API key below. No credit card required.
                Rate limits apply for fair usage across all users.
            </div>
        </div>
        
        <div id="swagger-ui"></div>
        
        <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@4.15.5/swagger-ui-standalone-preset.js"></script>
        <script>
        window.onload = function() {{
            // JurisRank Swagger UI Configuration
            const ui = SwaggerUIBundle({{
                url: '{base_url}/api/openapi',
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
                
                // JurisRank customization
                tryItOutEnabled: true,
                displayRequestDuration: true,
                supportedSubmitMethods: ['get', 'post', 'put', 'delete', 'patch'],
                
                // OAuth2 configuration for future authentication
                initOAuth: {{
                    clientId: "jurisrank-swagger-ui",
                    realm: "jurisrank-api",
                    appName: "JurisRank API Explorer",
                    scopeSeparator: " ",
                    additionalQueryStringParams: {{}},
                    useBasicAuthenticationWithAccessCodeGrant: false,
                    usePkceWithAuthorizationCodeGrant: false
                }},
                
                // Custom request interceptor for API key handling
                requestInterceptor: function(request) {{
                    // Add API key header if available
                    const apiKey = localStorage.getItem('jurisrank-api-key');
                    if (apiKey) {{
                        request.headers['X-API-Key'] = apiKey;
                    }}
                    
                    // Add user agent for analytics
                    request.headers['User-Agent'] = 'JurisRank-Swagger-UI/1.0.0';
                    
                    return request;
                }},
                
                // Response interceptor for error handling
                responseInterceptor: function(response) {{
                    // Log API usage for analytics
                    if (response.status === 401) {{
                        console.warn('JurisRank API: Authentication required. Please register for a free API key.');
                    }}
                    
                    return response;
                }}
            }});
            
            // Add JurisRank branding to topbar
            setTimeout(() => {{
                const topbar = document.querySelector('.swagger-ui .topbar');
                if (topbar) {{
                    const brandingDiv = document.createElement('div');
                    brandingDiv.innerHTML = `
                        <div style="position: absolute; top: 50%; right: 20px; transform: translateY(-50%); 
                                   color: white; font-size: 0.9em; opacity: 0.9;">
                            <strong>Patent P7</strong> • Multi-Jurisdictional Analysis
                        </div>
                    `;
                    topbar.style.position = 'relative';
                    topbar.appendChild(brandingDiv);
                }}
            }}, 500);
            
            // Save API key functionality
            window.saveApiKey = function(key) {{
                localStorage.setItem('jurisrank-api-key', key);
                alert('API key saved! It will be automatically included in requests.');
            }};
        }};
        
        // Add global API key helper
        console.log('%c🏛️ JurisRank API Explorer', 'color: #1e3a8a; font-size: 16px; font-weight: bold;');
        console.log('%cTo save your API key for automatic inclusion in requests:', 'color: #374151;');
        console.log('%csaveApiKey("your-api-key-here")', 'color: #059669; font-family: monospace;');
        </script>
    </body>
    </html>
    """
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html; charset=utf-8',
            'Cache-Control': 'public, max-age=300',  # 5 minutes cache
            'X-Frame-Options': 'SAMEORIGIN',  # Allow framing from same origin
            'X-Content-Type-Options': 'nosniff',
            'X-XSS-Protection': '1; mode=block'
        },
        'body': swagger_html
    }