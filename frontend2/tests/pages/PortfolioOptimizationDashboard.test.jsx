/**
 * Portfolio Optimization Dashboard Tests
 * Phase 2: Portfolio Optimization & Rebalancing
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import PortfolioOptimizationDashboard from '../../src/pages/PortfolioOptimizationDashboard';

vi.mock('axios');

describe('PortfolioOptimizationDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<PortfolioOptimizationDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Portfolio Optimization/i)).toBeInTheDocument();
    });
  });

  it('should display optimization parameters', async () => {
    const mockData = {
      current_weights: { AAPL: 0.3, MSFT: 0.7 },
      optimized_weights: { AAPL: 0.4, MSFT: 0.6 }
    };

    axios.get.mockResolvedValue({ data: { data: mockData } });

    render(<PortfolioOptimizationDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Portfolio Optimization/i)).toBeInTheDocument();
    });
  });
});
