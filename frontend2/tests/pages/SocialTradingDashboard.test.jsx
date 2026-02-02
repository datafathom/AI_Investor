/**
 * Social Trading Dashboard Tests
 * Phase 19: Social Trading & Copy Trading
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import SocialTradingDashboard from '../../src/pages/SocialTradingDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('SocialTradingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    // socialTradingStore expects response.data?.data or response.data
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<SocialTradingDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Social Trading/i, level: 1 })).toBeInTheDocument();
  });
});
