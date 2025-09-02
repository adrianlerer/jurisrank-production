/**
 * JurisRank SDK TypeScript Type Definitions
 * Complete type coverage for all API endpoints and data structures
 */

// Configuration Types
export interface JurisRankConfig {
  apiKey?: string;
  baseURL?: string;
  timeout?: number;
  retries?: number;
  retryDelay?: number;
}

// Constitutional Analysis Types
export interface ConstitutionalAnalysisRequest {
  case_facts: string;
  legal_question: string;
  jurisdiction?: string;
  case_type?: string;
  urgency_level?: 'low' | 'medium' | 'high';
  analysis_depth?: 'basic' | 'comprehensive' | 'expert';
}

export interface ConstitutionalAnalysisResponse {
  analysis_id: string;
  constitutional_assessment: {
    is_constitutional: boolean;
    confidence_score: number;
    constitutional_basis: string[];
    potential_violations: string[];
    precedent_support: string[];
  };
  legal_reasoning: {
    primary_arguments: string[];
    counter_arguments: string[];
    supporting_precedents: Array<{
      case_name: string;
      citation: string;
      relevance_score: number;
      key_principle: string;
    }>;
  };
  recommendations: {
    legal_strategy: string[];
    additional_research: string[];
    risk_assessment: {
      litigation_risk: 'low' | 'medium' | 'high';
      success_probability: number;
      key_challenges: string[];
    };
  };
  metadata: {
    analysis_timestamp: string;
    processing_time_ms: number;
    model_version: string;
    confidence_metrics: {
      overall_confidence: number;
      precedent_confidence: number;
      constitutional_confidence: number;
    };
  };
}

// Precedent Search Types
export interface PrecedentSearchRequest {
  query: string;
  jurisdiction?: string[];
  date_range?: {
    start_date?: string;
    end_date?: string;
  };
  court_level?: string[];
  legal_area?: string[];
  limit?: number;
  sort_by?: 'relevance' | 'date' | 'authority';
  include_summary?: boolean;
}

export interface PrecedentSearchResponse {
  results: Array<{
    case_id: string;
    case_name: string;
    citation: string;
    court: string;
    date_decided: string;
    jurisdiction: string;
    relevance_score: number;
    authority_score: number;
    summary?: string;
    key_holdings: string[];
    legal_principles: string[];
    cited_authorities: string[];
    url?: string;
    doi?: string;
  }>;
  metadata: {
    total_results: number;
    search_time_ms: number;
    query_interpretation: string;
    filters_applied: Record<string, any>;
  };
}

// Document Enhancement Types
export interface DocumentEnhancementRequest {
  document_text: string;
  enhancement_type: 'citation_verification' | 'legal_review' | 'precedent_analysis' | 'full_enhancement';
  target_audience?: 'court' | 'client' | 'academic' | 'general';
  jurisdiction?: string;
  legal_area?: string;
}

export interface DocumentEnhancementResponse {
  enhanced_document: {
    enhanced_text: string;
    suggested_citations: Array<{
      position: number;
      original_text: string;
      suggested_citation: string;
      authority_level: number;
      verification_status: 'verified' | 'suggested' | 'needs_review';
    }>;
    legal_improvements: Array<{
      section: string;
      improvement_type: 'clarity' | 'legal_accuracy' | 'citation' | 'argument_strength';
      suggestion: string;
      priority: 'low' | 'medium' | 'high';
    }>;
  };
  analysis: {
    document_score: number;
    legal_strength: number;
    citation_quality: number;
    areas_for_improvement: string[];
    strengths: string[];
  };
  metadata: {
    enhancement_timestamp: string;
    processing_time_ms: number;
    model_version: string;
    enhancement_statistics: {
      citations_added: number;
      improvements_suggested: number;
      legal_issues_identified: number;
    };
  };
}

// Bibliography Management Types
export interface BibliographyEntry {
  id?: number;
  title: string;
  author?: string;
  year?: number;
  url?: string;
  doi?: string;
  citation_format?: 'apa' | 'mla' | 'chicago' | 'legal';
  tags?: string[];
  notes?: string;
  created_at?: string;
  updated_at?: string;
}

export interface BibliographySearchRequest {
  query?: string;
  author?: string;
  year?: number;
  tags?: string[];
  limit?: number;
  offset?: number;
  sort_by?: 'title' | 'author' | 'year' | 'created_at';
  sort_order?: 'asc' | 'desc';
}

export interface BibliographySearchResponse {
  entries: BibliographyEntry[];
  metadata: {
    total_count: number;
    page_count: number;
    current_page: number;
    per_page: number;
  };
}

// API Response Wrapper
export interface JurisRankApiResponse<T = any> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
  metadata: {
    request_id: string;
    timestamp: string;
    version: string;
    rate_limit?: {
      limit: number;
      remaining: number;
      reset_time: string;
    };
  };
}

// Error Types
export class JurisRankError extends Error {
  public code: string;
  public statusCode?: number;
  public details?: Record<string, any>;

  constructor(message: string, code: string, statusCode?: number, details?: Record<string, any>) {
    super(message);
    this.name = 'JurisRankError';
    this.code = code;
    this.statusCode = statusCode;
    this.details = details;
  }
}

// Rate Limiting Types
export interface RateLimitInfo {
  limit: number;
  remaining: number;
  reset: Date;
  retryAfter?: number;
}

// Health Check Types
export interface HealthCheckResponse {
  status: 'healthy' | 'unhealthy' | 'degraded';
  timestamp: string;
  version: string;
  services: {
    database: 'up' | 'down';
    ai_models: 'up' | 'down' | 'partial';
    external_apis: 'up' | 'down' | 'partial';
  };
  performance: {
    response_time_ms: number;
    memory_usage_mb: number;
    cpu_usage_percent: number;
  };
}