/**
 * Credit Monitoring Dashboard Tests
 * Phase 12: Credit Score Monitoring & Improvement
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import CreditMonitoringDashboard from '../../src/pages/CreditMonitoringDashboard';

vi.mock('axios');

describe('CreditMonitoringDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<CreditMonitoringDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Credit Monitoring/i)).toBeInTheDocument();
    });
  });
});
