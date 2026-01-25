/**
 * Algorithmic Trading Dashboard Tests
 * Phase 15: Algorithmic Trading & Strategy Builder
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import AlgorithmicTradingDashboard from '../../src/pages/AlgorithmicTradingDashboard';

vi.mock('axios');

describe('AlgorithmicTradingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<AlgorithmicTradingDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Algorithmic Trading/i)).toBeInTheDocument();
    });
  });
});
