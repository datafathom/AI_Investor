/**
 * Watchlists & Alerts Dashboard Tests
 * Phase 17: Watchlists & Price Alerts
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import WatchlistsAlertsDashboard from '../../src/pages/WatchlistsAlertsDashboard';

vi.mock('axios');

describe('WatchlistsAlertsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<WatchlistsAlertsDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Watchlists/i)).toBeInTheDocument();
    });
  });
});
