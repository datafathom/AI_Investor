/**
 * Paper Trading Dashboard Tests
 * Phase 14: Paper Trading & Simulation
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import PaperTradingDashboard from '../../src/pages/PaperTradingDashboard';

vi.mock('axios');

describe('PaperTradingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<PaperTradingDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Paper Trading/i)).toBeInTheDocument();
    });
  });
});
