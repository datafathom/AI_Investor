/**
 * Market Store Tests
 * Phase 17: Market Data State Management
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import useMarketStore from '../marketStore';
import apiClient from '../../services/apiClient';

// Mock apiClient
vi.mock('../../services/apiClient', () => ({
  default: {
    get: vi.fn(),
  },
}));

describe('marketStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    useMarketStore.getState().clearAll();
  });

  it('should fetch quote successfully', async () => {
    const mockQuote = { symbol: 'AAPL', price: 150.0 };
    // Standard Wrapped Pattern: apiClient returns body, body has .data
    apiClient.get.mockResolvedValueOnce({ data: { data: mockQuote } });

    await useMarketStore.getState().fetchQuote('AAPL');

    expect(apiClient.get).toHaveBeenCalledWith('/market/quote/AAPL');
    expect(useMarketStore.getState().quotes['AAPL']).toEqual(mockQuote);
  });

  it('should fetch history successfully', async () => {
    const mockBars = [{ time: '2023-01-01', close: 145 }];
    const mockHistoryResponse = { bars: mockBars, count: 1 };
    
    apiClient.get.mockResolvedValueOnce({ data: { data: mockHistoryResponse } });

    await useMarketStore.getState().fetchHistory('AAPL', 'compact');

    expect(apiClient.get).toHaveBeenCalledWith('/market/history/AAPL', expect.any(Object));
    expect(useMarketStore.getState().history['AAPL'].bars).toEqual(mockBars);
  });

  it('should fetch health status', async () => {
    const mockHealth = { status: 'ok', latency: '40ms' };
    apiClient.get.mockResolvedValueOnce({ data: { data: mockHealth } });

    await useMarketStore.getState().fetchHealth();

    expect(apiClient.get).toHaveBeenCalledWith('/market/health');
    expect(useMarketStore.getState().health).toEqual(mockHealth);
  });
});
