/**
 * Retirement Planning Dashboard Tests
 * Phase 8: Retirement Planning & Withdrawal Strategies
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import RetirementPlanningDashboard from '../../src/pages/RetirementPlanningDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('RetirementPlanningDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<RetirementPlanningDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Retirement Planning/i, level: 1 })).toBeInTheDocument();
  });
});
