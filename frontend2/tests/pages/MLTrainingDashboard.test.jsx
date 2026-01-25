/**
 * ML Training Dashboard Tests
 * Phase 27: ML Training & Model Management
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import MLTrainingDashboard from '../../src/pages/MLTrainingDashboard';

vi.mock('axios');

describe('MLTrainingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<MLTrainingDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/ML Training/i)).toBeInTheDocument();
    });
  });
});
