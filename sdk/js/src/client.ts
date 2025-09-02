/**
 * JurisRank SDK Main Client Implementation
 * Provides comprehensive access to all JurisRank API endpoints
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import {
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
  JurisRankError,
  RateLimitInfo,
  HealthCheckResponse
} from './types';

export class JurisRankClient {
  private client: AxiosInstance;
  private config: Required<JurisRankConfig>;
  private rateLimitInfo: RateLimitInfo | null = null;

  constructor(config: JurisRankConfig = {}) {
    // Default configuration
    this.config = {
      apiKey: config.apiKey || '',
      baseURL: config.baseURL || 'https://api.jurisrank.com/v1',
      timeout: config.timeout || 30000,
      retries: config.retries || 3,
      retryDelay: config.retryDelay || 1000
    };

    // Initialize axios client
    this.client = axios.create({
      baseURL: this.config.baseURL,
      timeout: this.config.timeout,
      headers: {
        'Content-Type': 'application/json',
        'User-Agent': '@jurisrank/sdk@0.3.0',
        ...(this.config.apiKey && { 'Authorization': `Bearer ${this.config.apiKey}` })
      }
    });

    // Setup interceptors
    this.setupInterceptors();
  }

  /**
   * Setup request/response interceptors for error handling and rate limiting
   */
  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        config.headers = config.headers || {};
        config.headers['X-Request-Timestamp'] = new Date().toISOString();
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => {
        this.updateRateLimitInfo(response);
        return response;
      },
      async (error) => {
        if (error.response?.status === 429) {
          // Rate limit exceeded
          this.updateRateLimitInfo(error.response);
          
          if (this.rateLimitInfo?.retryAfter) {
            await this.delay(this.rateLimitInfo.retryAfter * 1000);
            return this.client.request(error.config);
          }
        }

        // Convert to JurisRankError
        throw this.createError(error);
      }
    );
  }

  /**
   * Update rate limit information from response headers
   */
  private updateRateLimitInfo(response: AxiosResponse): void {
    const headers = response.headers;
    
    if (headers['x-ratelimit-limit']) {
      this.rateLimitInfo = {
        limit: parseInt(headers['x-ratelimit-limit']),
        remaining: parseInt(headers['x-ratelimit-remaining'] || '0'),
        reset: new Date(parseInt(headers['x-ratelimit-reset']) * 1000),
        retryAfter: headers['retry-after'] ? parseInt(headers['retry-after']) : undefined
      };
    }
  }

  /**
   * Create standardized error from axios error
   */
  private createError(error: any): JurisRankError {
    if (error.response) {
      const { status, data } = error.response;
      const message = data?.error?.message || data?.message || `HTTP ${status} Error`;
      const code = data?.error?.code || `HTTP_${status}`;
      
      return new JurisRankError(message, code, status, data?.error?.details);
    } else if (error.request) {
      return new JurisRankError('Network error', 'NETWORK_ERROR');
    } else {
      return new JurisRankError(error.message, 'UNKNOWN_ERROR');
    }
  }

  /**
   * Delay utility for retry logic
   */
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Generic API request method with retry logic
   */
  private async request<T>(config: AxiosRequestConfig): Promise<T> {
    let lastError: any;
    
    for (let attempt = 0; attempt <= this.config.retries; attempt++) {
      try {
        const response = await this.client.request<JurisRankApiResponse<T>>(config);
        
        if (response.data.success) {
          return response.data.data!;
        } else {
          throw new JurisRankError(
            response.data.error?.message || 'API Error',
            response.data.error?.code || 'API_ERROR',
            response.status,
            response.data.error?.details
          );
        }
      } catch (error) {
        lastError = error;
        
        // Don't retry on client errors (4xx except 429)
        if (error instanceof JurisRankError && 
            error.statusCode && 
            error.statusCode >= 400 && 
            error.statusCode < 500 && 
            error.statusCode !== 429) {
          throw error;
        }
        
        // Wait before retry
        if (attempt < this.config.retries) {
          await this.delay(this.config.retryDelay * Math.pow(2, attempt));
        }
      }
    }
    
    throw lastError;
  }

  // API Methods

  /**
   * Perform constitutional analysis on a legal case
   */
  async analyzeConstitutional(request: ConstitutionalAnalysisRequest): Promise<ConstitutionalAnalysisResponse> {
    return this.request<ConstitutionalAnalysisResponse>({
      method: 'POST',
      url: '/analysis/constitutional',
      data: request
    });
  }

  /**
   * Search for legal precedents
   */
  async searchPrecedents(request: PrecedentSearchRequest): Promise<PrecedentSearchResponse> {
    return this.request<PrecedentSearchResponse>({
      method: 'POST',
      url: '/search/precedents',
      data: request
    });
  }

  /**
   * Enhance legal document with citations and improvements
   */
  async enhanceDocument(request: DocumentEnhancementRequest): Promise<DocumentEnhancementResponse> {
    return this.request<DocumentEnhancementResponse>({
      method: 'POST',
      url: '/document/enhance',
      data: request
    });
  }

  // Bibliography Management Methods

  /**
   * Create a new bibliography entry
   */
  async createBibliographyEntry(entry: Omit<BibliographyEntry, 'id' | 'created_at' | 'updated_at'>): Promise<BibliographyEntry> {
    return this.request<BibliographyEntry>({
      method: 'POST',
      url: '/bibliography/entries',
      data: entry
    });
  }

  /**
   * Get bibliography entry by ID
   */
  async getBibliographyEntry(id: number): Promise<BibliographyEntry> {
    return this.request<BibliographyEntry>({
      method: 'GET',
      url: `/bibliography/entries/${id}`
    });
  }

  /**
   * Update bibliography entry
   */
  async updateBibliographyEntry(id: number, entry: Partial<BibliographyEntry>): Promise<BibliographyEntry> {
    return this.request<BibliographyEntry>({
      method: 'PUT',
      url: `/bibliography/entries/${id}`,
      data: entry
    });
  }

  /**
   * Delete bibliography entry
   */
  async deleteBibliographyEntry(id: number): Promise<void> {
    await this.request<void>({
      method: 'DELETE',
      url: `/bibliography/entries/${id}`
    });
  }

  /**
   * Search bibliography entries
   */
  async searchBibliography(request: BibliographySearchRequest = {}): Promise<BibliographySearchResponse> {
    return this.request<BibliographySearchResponse>({
      method: 'GET',
      url: '/bibliography/search',
      params: request
    });
  }

  // Utility Methods

  /**
   * Check API health status
   */
  async getHealth(): Promise<HealthCheckResponse> {
    return this.request<HealthCheckResponse>({
      method: 'GET',
      url: '/health'
    });
  }

  /**
   * Get API status and information
   */
  async getStatus(): Promise<any> {
    return this.request<any>({
      method: 'GET',
      url: '/status'
    });
  }

  /**
   * Get current rate limit information
   */
  getRateLimitInfo(): RateLimitInfo | null {
    return this.rateLimitInfo;
  }

  /**
   * Update API configuration
   */
  updateConfig(newConfig: Partial<JurisRankConfig>): void {
    Object.assign(this.config, newConfig);
    
    // Update axios instance if needed
    if (newConfig.baseURL) {
      this.client.defaults.baseURL = newConfig.baseURL;
    }
    
    if (newConfig.timeout) {
      this.client.defaults.timeout = newConfig.timeout;
    }
    
    if (newConfig.apiKey !== undefined) {
      if (newConfig.apiKey) {
        this.client.defaults.headers['Authorization'] = `Bearer ${newConfig.apiKey}`;
      } else {
        delete this.client.defaults.headers['Authorization'];
      }
    }
  }
}