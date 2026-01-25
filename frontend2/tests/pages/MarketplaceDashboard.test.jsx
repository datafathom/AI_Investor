/**
 * Marketplace Dashboard Tests
 * Phase 30: Extension Marketplace & Custom Tools
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import MarketplaceDashboard from '../../src/pages/MarketplaceDashboard';

vi.mock('axios');

describe('MarketplaceDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<MarketplaceDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Marketplace/i)).toBeInTheDocument();
    });
  });
});
