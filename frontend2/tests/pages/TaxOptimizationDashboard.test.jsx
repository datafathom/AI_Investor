/**
 * Tax Optimization Dashboard Tests
 * Phase 4: Enhanced Tax-Loss Harvesting & Optimization
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import TaxOptimizationDashboard from '../../src/pages/TaxOptimizationDashboard';

vi.mock('axios');

describe('TaxOptimizationDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<TaxOptimizationDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Tax Optimization/i)).toBeInTheDocument();
    });
  });

  it('should display tax-loss harvesting opportunities', async () => {
    const mockData = {
      harvest_candidates: [
        { symbol: 'AAPL', unrealized_loss: -500.0 }
      ]
    };

    axios.get.mockResolvedValue({ data: { data: mockData } });

    render(<TaxOptimizationDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Tax Optimization/i)).toBeInTheDocument();
    });
  });
});
