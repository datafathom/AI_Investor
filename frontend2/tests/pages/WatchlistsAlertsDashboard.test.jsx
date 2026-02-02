/**
 * Watchlists & Alerts Dashboard Tests
 * Phase 17: Watchlists & Price Alerts
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import WatchlistsAlertsDashboard from '../../src/pages/WatchlistsAlertsDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('WatchlistsAlertsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard with watchlists', async () => {
    apiClient.get.mockResolvedValue([
      { id: 1, name: 'Tech Giants', symbols: ['AAPL', 'MSFT', 'GOOGL'] },
      { id: 2, name: 'Growth', symbols: ['TSLA', 'NVDA'] }
    ]);
    
    render(<WatchlistsAlertsDashboard />);
    
    // Use role for specificity
    expect(await screen.findByRole('heading', { name: /Watchlists & Price Alerts/i, level: 1 })).toBeInTheDocument();
  });
});
