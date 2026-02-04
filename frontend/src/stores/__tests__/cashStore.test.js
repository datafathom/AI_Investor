/**
 * Cash Store Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import useCashStore from '../cashStore';
import apiClient from '../../services/apiClient';

// Mock apiClient
vi.mock('../../services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('cashStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    useCashStore.getState().reset();
  });

  it('should initialize with default state', () => {
    const state = useCashStore.getState();
    expect(state.baseCurrency).toBe('USD');
    expect(state.balances).toEqual([]);
    expect(state.isLoading).toBe(false);
  });

  it('should set base currency', () => {
    useCashStore.getState().setBaseCurrency('EUR');
    expect(useCashStore.getState().baseCurrency).toBe('EUR');
  });

  it('should update balance and calculate total USD', () => {
    useCashStore.getState().updateBalance('USD', 1000);
    expect(useCashStore.getState().balances).toHaveLength(1);
    expect(useCashStore.getState().totalValueUSD).toBe(1000);

    // Update with FX rate
    useCashStore.getState().setFxRates([{ pair: 'EUR/USD', rate: 1.1 }]);
    useCashStore.getState().updateBalance('EUR', 100);
    
    // 1000 USD + (100 EUR * 1.1) = 1110 USD
    expect(useCashStore.getState().totalValueUSD).toBe(1110);
  });

  it('should fetch cash data successfully', async () => {
    const mockData = {
      balances: [{ currency: 'USD', amount: 500, amountUSD: 500, interestRate: 0.1 }],
      fx_rates: [{ pair: 'GBP/USD', rate: 1.25 }],
    };
    apiClient.get.mockResolvedValueOnce({ data: { data: mockData } });

    await useCashStore.getState().fetchCashData();

    expect(apiClient.get).toHaveBeenCalledWith('/cash/dashboard');
    expect(useCashStore.getState().balances).toEqual(mockData.balances);
    expect(useCashStore.getState().fxRates['GBP/USD'].rate).toBe(1.25);
  });

  it('should handle FX conversion', async () => {
    const mockResult = { txId: 'tx123', status: 'completed' };
    apiClient.post.mockResolvedValueOnce({ data: { data: mockResult } });
    apiClient.get.mockResolvedValueOnce({ data: { data: {} } }); // fetchCashData refresh

    const result = await useCashStore.getState().executeFxConversion('USD', 'EUR', 100);

    expect(apiClient.post).toHaveBeenCalledWith('/cash/fx/convert', expect.any(Object));
    expect(result).toEqual(mockResult);
  });
});
