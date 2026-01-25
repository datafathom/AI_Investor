/**
 * Bill Payment Dashboard Tests
 * Phase 11: Bill Payment Automation
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import BillPaymentDashboard from '../../src/pages/BillPaymentDashboard';

vi.mock('axios');

describe('BillPaymentDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<BillPaymentDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Bill Payment/i)).toBeInTheDocument();
    });
  });
});
