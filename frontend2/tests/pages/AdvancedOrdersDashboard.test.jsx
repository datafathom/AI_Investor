/**
 * Advanced Orders Dashboard Tests
 * Phase 13: Advanced Order Types & Smart Execution
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import AdvancedOrdersDashboard from '../../src/pages/AdvancedOrdersDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('AdvancedOrdersDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<AdvancedOrdersDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Advanced Orders/i, level: 1 })).toBeInTheDocument();
  });
});
