/**
 * JurisRank Client Tests
 */

import { JurisRankClient } from '../src/client';
import { JurisRankError } from '../src/types';
import axios from 'axios';

// Mock axios
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('JurisRankClient', () => {
  let client: JurisRankClient;
  let mockAxiosInstance: any;

  beforeEach(() => {
    mockAxiosInstance = {
      request: jest.fn(),
      interceptors: {
        request: { use: jest.fn() },
        response: { use: jest.fn() }
      },
      defaults: { headers: {} }
    };
    
    mockedAxios.create.mockReturnValue(mockAxiosInstance);
    
    client = new JurisRankClient({
      apiKey: 'test-api-key',
      baseURL: 'https://test.api.com'
    });
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('Initialization', () => {
    it('should create client with default config', () => {
      const defaultClient = new JurisRankClient();
      expect(mockedAxios.create).toHaveBeenCalledWith(
        expect.objectContaining({
          baseURL: 'https://api.jurisrank.com/v1',
          timeout: 30000
        })
      );
    });

    it('should create client with custom config', () => {
      expect(mockedAxios.create).toHaveBeenCalledWith(
        expect.objectContaining({
          baseURL: 'https://test.api.com',
          timeout: 30000
        })
      );
    });
  });

  describe('Constitutional Analysis', () => {
    it('should perform constitutional analysis successfully', async () => {
      const mockResponse = {
        data: {
          success: true,
          data: {
            analysis_id: 'test-123',
            constitutional_assessment: {
              is_constitutional: true,
              confidence_score: 0.85,
              constitutional_basis: ['Article 18'],
              potential_violations: [],
              precedent_support: ['Case A', 'Case B']
            }
          }
        }
      };

      mockAxiosInstance.request.mockResolvedValue(mockResponse);

      const result = await client.analyzeConstitutional({
        case_facts: 'Test case facts',
        legal_question: 'Is this constitutional?'
      });

      expect(mockAxiosInstance.request).toHaveBeenCalledWith({
        method: 'POST',
        url: '/analysis/constitutional',
        data: {
          case_facts: 'Test case facts',
          legal_question: 'Is this constitutional?'
        }
      });

      expect(result.analysis_id).toBe('test-123');
      expect(result.constitutional_assessment.is_constitutional).toBe(true);
    });

    it('should handle API errors', async () => {
      const mockError = {
        response: {
          status: 400,
          data: {
            success: false,
            error: {
              code: 'INVALID_REQUEST',
              message: 'Invalid request parameters'
            }
          }
        }
      };

      mockAxiosInstance.request.mockRejectedValue(mockError);

      await expect(
        client.analyzeConstitutional({
          case_facts: '',
          legal_question: ''
        })
      ).rejects.toThrow(JurisRankError);
    });
  });

  describe('Precedent Search', () => {
    it('should search precedents successfully', async () => {
      const mockResponse = {
        data: {
          success: true,
          data: {
            results: [
              {
                case_id: 'case-1',
                case_name: 'Test Case v. State',
                citation: '123 Test 456',
                relevance_score: 0.9
              }
            ],
            metadata: {
              total_results: 1,
              search_time_ms: 150
            }
          }
        }
      };

      mockAxiosInstance.request.mockResolvedValue(mockResponse);

      const result = await client.searchPrecedents({
        query: 'constitutional rights'
      });

      expect(result.results).toHaveLength(1);
      expect(result.results[0].case_name).toBe('Test Case v. State');
    });
  });

  describe('Document Enhancement', () => {
    it('should enhance document successfully', async () => {
      const mockResponse = {
        data: {
          success: true,
          data: {
            enhanced_document: {
              enhanced_text: 'Enhanced legal document...',
              suggested_citations: [],
              legal_improvements: []
            },
            analysis: {
              document_score: 0.8,
              legal_strength: 0.75,
              citation_quality: 0.85
            }
          }
        }
      };

      mockAxiosInstance.request.mockResolvedValue(mockResponse);

      const result = await client.enhanceDocument({
        document_text: 'Original document',
        enhancement_type: 'full_enhancement'
      });

      expect(result.enhanced_document.enhanced_text).toBe('Enhanced legal document...');
      expect(result.analysis.document_score).toBe(0.8);
    });
  });

  describe('Bibliography Management', () => {
    it('should create bibliography entry', async () => {
      const mockResponse = {
        data: {
          success: true,
          data: {
            id: 1,
            title: 'Test Article',
            author: 'Test Author',
            year: 2023
          }
        }
      };

      mockAxiosInstance.request.mockResolvedValue(mockResponse);

      const result = await client.createBibliographyEntry({
        title: 'Test Article',
        author: 'Test Author',
        year: 2023
      });

      expect(result.id).toBe(1);
      expect(result.title).toBe('Test Article');
    });

    it('should search bibliography', async () => {
      const mockResponse = {
        data: {
          success: true,
          data: {
            entries: [
              { id: 1, title: 'Article 1' },
              { id: 2, title: 'Article 2' }
            ],
            metadata: {
              total_count: 2,
              page_count: 1,
              current_page: 1,
              per_page: 10
            }
          }
        }
      };

      mockAxiosInstance.request.mockResolvedValue(mockResponse);

      const result = await client.searchBibliography({ query: 'test' });

      expect(result.entries).toHaveLength(2);
      expect(result.metadata.total_count).toBe(2);
    });
  });

  describe('Utility Methods', () => {
    it('should get health status', async () => {
      const mockResponse = {
        data: {
          success: true,
          data: {
            status: 'healthy',
            timestamp: '2023-01-01T00:00:00Z',
            version: '1.0.0'
          }
        }
      };

      mockAxiosInstance.request.mockResolvedValue(mockResponse);

      const result = await client.getHealth();

      expect(result.status).toBe('healthy');
      expect(result.version).toBe('1.0.0');
    });

    it('should update configuration', () => {
      client.updateConfig({
        timeout: 60000,
        retries: 5
      });

      expect(mockAxiosInstance.defaults.timeout).toBe(60000);
    });
  });

  describe('Error Handling', () => {
    it('should handle network errors', async () => {
      const networkError = new Error('Network Error');
      mockAxiosInstance.request.mockRejectedValue(networkError);

      await expect(
        client.getHealth()
      ).rejects.toThrow(JurisRankError);
    });

    it('should handle rate limiting', async () => {
      const rateLimitError = {
        response: {
          status: 429,
          headers: {
            'x-ratelimit-limit': '100',
            'x-ratelimit-remaining': '0',
            'x-ratelimit-reset': '1234567890',
            'retry-after': '60'
          },
          data: {
            success: false,
            error: {
              code: 'RATE_LIMIT_EXCEEDED',
              message: 'Rate limit exceeded'
            }
          }
        }
      };

      mockAxiosInstance.request.mockRejectedValue(rateLimitError);

      await expect(
        client.getHealth()
      ).rejects.toThrow(JurisRankError);
    });
  });
});