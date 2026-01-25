/**
 * Compliance Dashboard Tests
 * Phase 25: Compliance & Regulatory Reporting
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import ComplianceDashboard from '../../src/pages/ComplianceDashboard';

vi.mock('axios');

describe('ComplianceDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<ComplianceDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Compliance/i)).toBeInTheDocument();
    });
  });
});
