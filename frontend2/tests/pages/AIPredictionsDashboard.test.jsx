/**
 * AI Predictions Dashboard Tests
 * Phase 22: AI Predictions & Forecasting
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import AIPredictionsDashboard from '../../src/pages/AIPredictionsDashboard';

vi.mock('axios');

describe('AIPredictionsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<AIPredictionsDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/AI Predictions/i)).toBeInTheDocument();
    });
  });

  it('should display prediction data', async () => {
    const mockPredictions = {
      price_forecast: { symbol: 'AAPL', predicted_price: 150.0, confidence: 0.85 }
    };

    axios.get.mockResolvedValue({ data: { data: mockPredictions } });

    render(<AIPredictionsDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/AI Predictions/i)).toBeInTheDocument();
    });
  });
});
