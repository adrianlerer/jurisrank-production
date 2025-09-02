/**
 * Jest Test Setup
 * Global test configuration and mocks
 */

// Mock axios for tests
jest.mock('axios', () => ({
  create: jest.fn(() => ({
    request: jest.fn(),
    interceptors: {
      request: { use: jest.fn() },
      response: { use: jest.fn() }
    },
    defaults: { headers: {} }
  })),
  defaults: { headers: {} }
}));

// Global test timeout
jest.setTimeout(10000);

// Console suppression for cleaner test output
global.console = {
  ...console,
  log: jest.fn(),
  debug: jest.fn(),
  info: jest.fn(),
  warn: jest.fn(),
  error: jest.fn()
};