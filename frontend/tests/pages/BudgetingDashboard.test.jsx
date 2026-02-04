/**
 * Budgeting Dashboard Tests
 * Phase 10: Budgeting & Expense Tracking
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import BudgetingDashboard from '../../src/pages/BudgetingDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('BudgetingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<BudgetingDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Budgeting/i, level: 1 })).toBeInTheDocument();
  });
});
