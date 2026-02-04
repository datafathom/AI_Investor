/**
 * Marketplace Dashboard Tests
 * Phase 30: Extension Marketplace & Custom Tools
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import MarketplaceDashboard from '../../src/pages/MarketplaceDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('MarketplaceDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    // Marketplace store expects response.data?.data or response.data
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<MarketplaceDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Extension Marketplace/i, level: 1 })).toBeInTheDocument();
  });
});
