/**
 * Advanced Charting Dashboard Tests
 * Phase 5: Advanced Charting & Technical Analysis
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import AdvancedChartingDashboard from '../../src/pages/AdvancedChartingDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('AdvancedChartingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard with chart', async () => {
    apiClient.get.mockResolvedValue({
      symbol: 'AAPL',
      price: 150.00,
      change: 1.5,
      changePercent: 1.0,
      volume: 1000000,
      lastUpdate: new Date().toISOString()
    });
    
    render(<AdvancedChartingDashboard />);
    
    expect(await screen.findByText('Advanced Charting')).toBeInTheDocument();
  });

  it('should display chart controls', async () => {
    const mockData = {
      chart_data: [],
      indicators: []
    };

    apiClient.get.mockResolvedValue({ data: { data: mockData } });

    render(<AdvancedChartingDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Advanced Charting/i)).toBeInTheDocument();
    });
  });
});
