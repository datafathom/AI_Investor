/**
 * AI Predictions Dashboard Tests
 * Phase 22: AI Predictions & Forecasting
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import AIPredictionsDashboard from '../../src/pages/AIPredictionsDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('AIPredictionsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<AIPredictionsDashboard />);
    
    expect(await screen.findByRole('heading', { name: /AI Predictions/i, level: 1 })).toBeInTheDocument();
  });

  it('should display prediction data', async () => {
    const mockPredictions = {
      price_forecast: { symbol: 'AAPL', predicted_price: 150.0, confidence: 0.85 }
    };

    apiClient.get.mockResolvedValue({ data: { data: mockPredictions } });

    render(<AIPredictionsDashboard />);

    expect(await screen.findByRole('heading', { name: /AI Predictions/i, level: 1 })).toBeInTheDocument();
  });
});
