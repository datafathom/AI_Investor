/**
 * Credit Monitoring Dashboard Tests
 * Phase 12: Credit Score Monitoring & Improvement
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import CreditMonitoringDashboard from '../../src/pages/CreditMonitoringDashboard';

vi.mock('../../src/services/apiClient');

describe('CreditMonitoringDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: {} } });
    
    render(<CreditMonitoringDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Credit Monitoring/i)).toBeInTheDocument();
    });
  });
});
