/**
 * @jurisrank/sdk - Official JavaScript/TypeScript SDK
 * 
 * Complete SDK for JurisRank AI Constitutional Analysis API
 * Provides TypeScript support, error handling, and retry mechanisms
 * 
 * @version 0.3.0
 * @author Ignacio Adrian Lerer
 * @license MIT
 */

// Main exports
export { JurisRankClient } from './client';

// Type exports
export type {
  JurisRankConfig,
  ConstitutionalAnalysisRequest,
  ConstitutionalAnalysisResponse,
  PrecedentSearchRequest,
  PrecedentSearchResponse,
  DocumentEnhancementRequest,
  DocumentEnhancementResponse,
  BibliographyEntry,
  BibliographySearchRequest,
  BibliographySearchResponse,
  JurisRankApiResponse,
  RateLimitInfo,
  HealthCheckResponse
} from './types';

// Error exports
export { JurisRankError } from './types';

// Default export and convenience function
import { JurisRankClient } from './client';
import { JurisRankConfig } from './types';

/**
 * Create a new JurisRank client instance
 * 
 * @param config Configuration options
 * @returns JurisRank client instance
 * 
 * @example
 * ```typescript
 * import JurisRank from '@jurisrank/sdk';
 * 
 * const client = JurisRank({
 *   apiKey: 'your-api-key'
 * });
 * 
 * const analysis = await client.analyzeConstitutional({
 *   case_facts: "Caso de tenencia personal de menores...",
 *   legal_question: "¿Es constitucional la medida adoptada?"
 * });
 * ```
 */
export default function JurisRank(config?: JurisRankConfig): JurisRankClient {
  return new JurisRankClient(config);
}

// Named export for those who prefer it
export const createClient = JurisRank;

/**
 * SDK Version
 */
export const VERSION = '0.3.0';

/**
 * Convenience methods for quick usage
 */
export const QuickStart = {
  /**
   * Quick constitutional analysis without client setup
   */
  async analyzeConstitutional(
    request: import('./types').ConstitutionalAnalysisRequest,
    apiKey?: string
  ) {
    const client = new JurisRankClient({ apiKey });
    return client.analyzeConstitutional(request);
  },

  /**
   * Quick precedent search without client setup
   */
  async searchPrecedents(
    request: import('./types').PrecedentSearchRequest,
    apiKey?: string
  ) {
    const client = new JurisRankClient({ apiKey });
    return client.searchPrecedents(request);
  },

  /**
   * Quick document enhancement without client setup
   */
  async enhanceDocument(
    request: import('./types').DocumentEnhancementRequest,
    apiKey?: string
  ) {
    const client = new JurisRankClient({ apiKey });
    return client.enhanceDocument(request);
  }
};