/**
 * Research Reports Dashboard Tests
 * Phase 18: Research Reports & Generation
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import ResearchReportsDashboard from '../../src/pages/ResearchReportsDashboard';

vi.mock('../../src/services/apiClient');

describe('ResearchReportsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: {} } });
    
    render(<ResearchReportsDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Research Reports/i)).toBeInTheDocument();
    });
  });
});
