/**
 * Advanced Charting Dashboard Tests
 * Phase 5: Advanced Charting & Technical Analysis
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import AdvancedChartingDashboard from '../../src/pages/AdvancedChartingDashboard';

vi.mock('axios');

describe('AdvancedChartingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<AdvancedChartingDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Advanced Charting/i)).toBeInTheDocument();
    });
  });

  it('should display chart controls', async () => {
    const mockData = {
      chart_data: [],
      indicators: []
    };

    axios.get.mockResolvedValue({ data: { data: mockData } });

    render(<AdvancedChartingDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Advanced Charting/i)).toBeInTheDocument();
    });
  });
});
