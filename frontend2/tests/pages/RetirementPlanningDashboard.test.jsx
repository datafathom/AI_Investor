/**
 * Retirement Planning Dashboard Tests
 * Phase 8: Retirement Planning & Withdrawal Strategies
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import RetirementPlanningDashboard from '../../src/pages/RetirementPlanningDashboard';

vi.mock('axios');

describe('RetirementPlanningDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<RetirementPlanningDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Retirement Planning/i)).toBeInTheDocument();
    });
  });
});
