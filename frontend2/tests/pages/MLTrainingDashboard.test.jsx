/**
 * ML Training Dashboard Tests
 * Phase 27: ML Training & Model Management
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import MLTrainingDashboard from '../../src/pages/MLTrainingDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('MLTrainingDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<MLTrainingDashboard />);
    
    expect(await screen.findByRole('heading', { name: /ML Training/i, level: 1 })).toBeInTheDocument();
  });
});
