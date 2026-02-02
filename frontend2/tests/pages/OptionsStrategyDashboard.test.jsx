/**
 * Options Strategy Builder Dashboard Tests
 * Phase 6: Options Strategy Builder & Analytics
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import OptionsStrategyDashboard from '../../src/pages/OptionsStrategyDashboard';

vi.mock('../../src/services/apiClient');

describe('OptionsStrategyDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: {} } });
    
    render(<OptionsStrategyDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Options Strategy/i)).toBeInTheDocument();
    });
  });
});
