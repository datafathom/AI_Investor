/**
 * Institutional Tools Dashboard Tests
 * Phase 26: Institutional Tools & Professional Features
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import InstitutionalToolsDashboard from '../../src/pages/InstitutionalToolsDashboard';

vi.mock('axios');

describe('InstitutionalToolsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<InstitutionalToolsDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Institutional Tools/i)).toBeInTheDocument();
    });
  });
});
