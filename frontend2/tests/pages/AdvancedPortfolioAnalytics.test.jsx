/**
 * Advanced Portfolio Analytics Dashboard Tests
 * Phase 1: Portfolio Performance Attribution & Risk Decomposition
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import AdvancedPortfolioAnalytics from '../../src/pages/AdvancedPortfolioAnalytics';

// Mock axios
vi.mock('axios');

describe('AdvancedPortfolioAnalytics', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render loading state initially', () => {
    axios.get.mockResolvedValue({ data: { data: null } });
    
    render(<AdvancedPortfolioAnalytics />);
    
    expect(screen.getByText('Loading analytics...')).toBeInTheDocument();
  });

  it('should render dashboard with analytics data', async () => {
    const mockAttribution = {
      total_return: 15.5,
      benchmark_return: 12.0,
      active_return: 3.5,
      breakdown: [
        { factor: 'Sector', contribution: 2.0 },
        { factor: 'Stock Selection', contribution: 1.5 }
      ]
    };

    const mockRiskDecomp = {
      total_risk: 0.18,
      factor_risks: [
        { factor: 'Market', risk: 0.12 },
        { factor: 'Sector', risk: 0.06 }
      ]
    };

    axios.get
      .mockResolvedValueOnce({ data: { data: mockAttribution } })
      .mockResolvedValueOnce({ data: { data: mockRiskDecomp } });

    render(<AdvancedPortfolioAnalytics />);

    await waitFor(() => {
      expect(screen.getByText('Advanced Portfolio Analytics')).toBeInTheDocument();
      expect(screen.getByText(/Performance Attribution/i)).toBeInTheDocument();
      expect(screen.getByText(/Risk Decomposition/i)).toBeInTheDocument();
    });
  });

  it('should handle API errors gracefully', async () => {
    axios.get.mockRejectedValue(new Error('API Error'));

    render(<AdvancedPortfolioAnalytics />);

    await waitFor(() => {
      expect(screen.queryByText('Loading analytics...')).not.toBeInTheDocument();
    });
  });
});
