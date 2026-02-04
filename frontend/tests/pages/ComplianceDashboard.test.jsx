/**
 * Compliance Dashboard Tests
 * Phase 25: Compliance & Regulatory Reporting
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import ComplianceDashboard from '../../src/pages/ComplianceDashboard';

vi.mock('../../src/services/apiClient');

describe('ComplianceDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: {} } });
    
    render(<ComplianceDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Compliance/i)).toBeInTheDocument();
    });
  });
});
