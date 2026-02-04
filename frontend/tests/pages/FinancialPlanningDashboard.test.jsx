/**
 * Financial Planning Dashboard Tests
 * Phase 7: Financial Planning & Goal Tracking
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import FinancialPlanningDashboard from '../../src/pages/FinancialPlanningDashboard';

vi.mock('../../src/services/apiClient');

describe('FinancialPlanningDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: {} } });
    
    render(<FinancialPlanningDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Financial Planning/i)).toBeInTheDocument();
    });
  });
});
