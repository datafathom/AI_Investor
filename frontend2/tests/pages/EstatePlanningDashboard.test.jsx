/**
 * Estate Planning Dashboard Tests
 * Phase 9: Estate Planning & Inheritance Simulation
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import EstatePlanningDashboard from '../../src/pages/EstatePlanningDashboard';

vi.mock('../../src/services/apiClient');

describe('EstatePlanningDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: {} } });
    
    render(<EstatePlanningDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Estate Planning/i)).toBeInTheDocument();
    });
  });
});
