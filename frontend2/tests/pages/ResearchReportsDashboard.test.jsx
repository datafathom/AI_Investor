/**
 * Research Reports Dashboard Tests
 * Phase 18: Research Reports & Generation
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import ResearchReportsDashboard from '../../src/pages/ResearchReportsDashboard';

vi.mock('axios');

describe('ResearchReportsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<ResearchReportsDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Research Reports/i)).toBeInTheDocument();
    });
  });
});
