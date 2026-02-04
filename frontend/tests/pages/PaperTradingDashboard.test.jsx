/**
 * Paper Trading Dashboard Tests
 * Phase 14: Paper Trading & Simulation
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import PaperTradingDashboard from '../../src/pages/PaperTradingDashboard';

vi.mock('../../src/services/apiClient');

describe('PaperTradingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: {} } });
    
    render(<PaperTradingDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Paper Trading/i)).toBeInTheDocument();
    });
  });
});
