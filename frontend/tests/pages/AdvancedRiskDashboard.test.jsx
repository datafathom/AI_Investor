/**
 * Advanced Risk Management Dashboard Tests
 * Phase 3: Advanced Risk Metrics & Stress Testing
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import AdvancedRiskDashboard from '../../src/pages/AdvancedRiskDashboard';

// Mock apiClient with factory
vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn(),
  },
}));

describe('AdvancedRiskDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({});
    
    render(<AdvancedRiskDashboard />);
    
    // Use role and name for specificity
    expect(await screen.findByRole('heading', { name: /ADVANCED RISK/i, level: 1 })).toBeInTheDocument();
  });

  it('should display risk metrics', async () => {
    const mockData = {
      var: 0.05,
      cvar: 0.07,
      max_drawdown: 0.12,
      sharpe_ratio: 1.5,
      sortino_ratio: 1.8,
      calmar_ratio: 1.2
    };

    apiClient.get.mockResolvedValue(mockData);

    render(<AdvancedRiskDashboard />);

    // Wait for the value to appear
    expect(await screen.findByText(/\$0\.05/)).toBeInTheDocument();
    expect(await screen.findByText(/0\.07/)).toBeInTheDocument();
  });
});
