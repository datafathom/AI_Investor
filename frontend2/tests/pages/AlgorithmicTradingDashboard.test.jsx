/**
 * Algorithmic Trading Dashboard Tests
 * Phase 15: Algorithmic Trading & Strategy Builder
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import AlgorithmicTradingDashboard from '../../src/pages/AlgorithmicTradingDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('AlgorithmicTradingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<AlgorithmicTradingDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Algorithmic Trading/i, level: 1 })).toBeInTheDocument();
  });
});
