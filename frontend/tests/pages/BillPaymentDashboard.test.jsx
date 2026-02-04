/**
 * Bill Payment Dashboard Tests
 * Phase 11: Bill Payment Automation
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import BillPaymentDashboard from '../../src/pages/BillPaymentDashboard';

vi.mock('../../src/services/apiClient');

describe('BillPaymentDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: {} } });
    
    render(<BillPaymentDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Bill Payment/i)).toBeInTheDocument();
    });
  });
});
