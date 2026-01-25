/**
 * Options Strategy Builder Dashboard Tests
 * Phase 6: Options Strategy Builder & Analytics
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import OptionsStrategyDashboard from '../../src/pages/OptionsStrategyDashboard';

vi.mock('axios');

describe('OptionsStrategyDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<OptionsStrategyDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Options Strategy/i)).toBeInTheDocument();
    });
  });
});
