/**
 * Social Trading Dashboard Tests
 * Phase 19: Social Trading & Copy Trading
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import SocialTradingDashboard from '../../src/pages/SocialTradingDashboard';

vi.mock('axios');

describe('SocialTradingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<SocialTradingDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Social Trading/i)).toBeInTheDocument();
    });
  });
});
