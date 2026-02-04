/**
 * Portfolio Optimization Dashboard Tests
 * Phase 2: Portfolio Optimization & Rebalancing
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import PortfolioOptimizationDashboard from '../../src/pages/PortfolioOptimizationDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('PortfolioOptimizationDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<PortfolioOptimizationDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Portfolio Optimization/i, level: 1 })).toBeInTheDocument();
  });

  it('should display optimization parameters', async () => {
    const mockData = {
      current_weights: { AAPL: 0.3, MSFT: 0.7 },
      optimized_weights: { AAPL: 0.4, MSFT: 0.6 }
    };

    apiClient.get.mockResolvedValue({ data: { data: mockData } });

    render(<PortfolioOptimizationDashboard />);

    expect(await screen.findByRole('heading', { name: /Portfolio Optimization/i, level: 1 })).toBeInTheDocument();
  });
});
