/**
 * Budgeting Dashboard Tests
 * Phase 10: Budgeting & Expense Tracking
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import BudgetingDashboard from '../../src/pages/BudgetingDashboard';

vi.mock('axios');

describe('BudgetingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<BudgetingDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Budgeting/i)).toBeInTheDocument();
    });
  });
});
