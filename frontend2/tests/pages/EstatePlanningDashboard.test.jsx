/**
 * Estate Planning Dashboard Tests
 * Phase 9: Estate Planning & Inheritance Simulation
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import EstatePlanningDashboard from '../../src/pages/EstatePlanningDashboard';

vi.mock('axios');

describe('EstatePlanningDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<EstatePlanningDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Estate Planning/i)).toBeInTheDocument();
    });
  });
});
