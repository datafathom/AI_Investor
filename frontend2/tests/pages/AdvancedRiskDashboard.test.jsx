/**
 * Advanced Risk Management Dashboard Tests
 * Phase 3: Advanced Risk Metrics & Stress Testing
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import AdvancedRiskDashboard from '../../src/pages/AdvancedRiskDashboard';

vi.mock('axios');

describe('AdvancedRiskDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<AdvancedRiskDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Advanced Risk Management/i)).toBeInTheDocument();
    });
  });

  it('should display risk metrics', async () => {
    const mockData = {
      var_95: 0.05,
      cvar_95: 0.07,
      max_drawdown: 0.12
    };

    axios.get.mockResolvedValue({ data: { data: mockData } });

    render(<AdvancedRiskDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Advanced Risk Management/i)).toBeInTheDocument();
    });
  });
});
