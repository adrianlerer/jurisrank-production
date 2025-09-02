# @jurisrank/sdk

Official JavaScript/TypeScript SDK for JurisRank AI Constitutional Analysis API

[![npm version](https://badge.fury.io/js/@jurisrank%2Fsdk.svg)](https://www.npmjs.com/package/@jurisrank/sdk)
[![TypeScript](https://img.shields.io/badge/TypeScript-Ready-blue.svg)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### Installation

```bash
npm install @jurisrank/sdk
# or
yarn add @jurisrank/sdk
# or
pnpm add @jurisrank/sdk
```

### Basic Usage

```typescript
import JurisRank from '@jurisrank/sdk';

// Initialize client
const client = JurisRank({
  apiKey: 'your-api-key' // Optional for public endpoints
});

// Analyze constitutional case
const analysis = await client.analyzeConstitutional({
  case_facts: "Un menor fue separado de su familia por decisión judicial sin garantías del debido proceso.",
  legal_question: "¿Es constitucional la medida de separación adoptada sin audiencia previa?"
});

console.log(analysis.constitutional_assessment);
```

## 📖 API Reference

### Constitutional Analysis

Analyze legal cases for constitutional compliance:

```typescript
const analysis = await client.analyzeConstitutional({
  case_facts: "Descripción detallada de los hechos del caso",
  legal_question: "Pregunta jurídica específica",
  jurisdiction: "argentina", // Optional
  case_type: "constitutional", // Optional
  urgency_level: "high", // Optional: 'low' | 'medium' | 'high'
  analysis_depth: "comprehensive" // Optional: 'basic' | 'comprehensive' | 'expert'
});

// Response includes:
// - constitutional_assessment: Boolean result with confidence score
// - legal_reasoning: Arguments and counter-arguments
// - recommendations: Legal strategy and risk assessment
// - metadata: Processing information and confidence metrics
```

### Precedent Search

Search for relevant legal precedents:

```typescript
const precedents = await client.searchPrecedents({
  query: "tenencia de menores debido proceso",
  jurisdiction: ["argentina", "caba"],
  date_range: {
    start_date: "2020-01-01",
    end_date: "2024-12-31"
  },
  court_level: ["supreme_court", "appeals_court"],
  limit: 10,
  sort_by: "relevance",
  include_summary: true
});

// Access results
precedents.results.forEach(precedent => {
  console.log(`${precedent.case_name}: ${precedent.relevance_score}`);
});
```

### Document Enhancement

Enhance legal documents with citations and improvements:

```typescript
const enhancement = await client.enhanceDocument({
  document_text: "Su extenso documento legal...",
  enhancement_type: "full_enhancement",
  target_audience: "court",
  jurisdiction: "argentina",
  legal_area: "constitutional_law"
});

// Access enhanced version
console.log(enhancement.enhanced_document.enhanced_text);
console.log(enhancement.enhanced_document.suggested_citations);
```

### Bibliography Management

Manage legal citations and references:

```typescript
// Create bibliography entry
const entry = await client.createBibliographyEntry({
  title: "Caso Bazterrica - Análisis Constitucional",
  author: "Juan Pérez",
  year: 2023,
  url: "https://example.com/article",
  citation_format: "legal",
  tags: ["constitutional", "criminal_law"]
});

// Search bibliography
const results = await client.searchBibliography({
  query: "Bazterrica",
  tags: ["constitutional"],
  limit: 20
});
```

## 🔧 Configuration Options

```typescript
const client = JurisRank({
  apiKey: 'your-api-key',           // Optional API key
  baseURL: 'https://custom.api.com', // Custom base URL
  timeout: 30000,                    // Request timeout (ms)
  retries: 3,                       // Retry attempts
  retryDelay: 1000                  // Delay between retries (ms)
});
```

## 🚨 Error Handling

The SDK provides comprehensive error handling:

```typescript
import { JurisRankError } from '@jurisrank/sdk';

try {
  const analysis = await client.analyzeConstitutional({
    case_facts: "...",
    legal_question: "..."
  });
} catch (error) {
  if (error instanceof JurisRankError) {
    console.log(`Error ${error.code}: ${error.message}`);
    console.log(`Status: ${error.statusCode}`);
    console.log(`Details:`, error.details);
  }
}
```

## 📊 Rate Limiting

Monitor your API usage:

```typescript
// Check rate limit info after any request
const rateLimitInfo = client.getRateLimitInfo();

if (rateLimitInfo) {
  console.log(`Remaining requests: ${rateLimitInfo.remaining}`);
  console.log(`Resets at: ${rateLimitInfo.reset}`);
}
```

## ⚡ Quick Methods

For simple one-off requests without client setup:

```typescript
import { QuickStart } from '@jurisrank/sdk';

// Quick analysis
const analysis = await QuickStart.analyzeConstitutional({
  case_facts: "Hechos del caso",
  legal_question: "Pregunta legal"
}, 'optional-api-key');
```

## 🔍 Health Monitoring

Check API status and health:

```typescript
// Check API health
const health = await client.getHealth();
console.log(`Status: ${health.status}`);
console.log(`Response time: ${health.performance.response_time_ms}ms`);

// Get API status
const status = await client.getStatus();
```

## 📚 TypeScript Support

Full TypeScript support with comprehensive type definitions:

```typescript
import type { 
  ConstitutionalAnalysisRequest,
  ConstitutionalAnalysisResponse,
  JurisRankConfig 
} from '@jurisrank/sdk';

// Strongly typed requests and responses
const request: ConstitutionalAnalysisRequest = {
  case_facts: "Caso detallado...",
  legal_question: "¿Es constitucional?",
  analysis_depth: "comprehensive" // Autocomplete available
};
```

## 🌐 Environment Support

- **Node.js**: >=16.0.0
- **Browser**: Modern browsers with ES2020 support
- **TypeScript**: Full support with declarations
- **CommonJS**: ✅ Supported
- **ES Modules**: ✅ Supported

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/adrianlerer/jurisrank-production/issues)
- **Documentation**: [Complete API documentation](https://github.com/adrianlerer/jurisrank-production/blob/main/API_DOCUMENTATION.md)
- **Email**: iadrianlerer@gmail.com

## 🏛️ About JurisRank

JurisRank AI revolutionizes constitutional law analysis through advanced AI ensemble methods. Developed by constitutional law expert Ignacio Adrian Lerer, it provides world-class legal analysis capabilities to legal professionals, researchers, and institutions.

**Features:**
- 🧠 Multi-model AI ensemble (Darwin ASI + GPT-4o + Claude-3.5 + Gemini)
- ⚖️ Constitutional precedent analysis
- 📚 Comprehensive citation verification
- 🔍 Advanced jurisprudential search
- 📊 Risk assessment and legal strategy recommendations

---

*Made with ⚖️ by the JurisRank team*