/**
 * Enterprise Dashboard Tests
 * Phase 24: Enterprise Features & Multi-User Management
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import EnterpriseDashboard from '../../src/pages/EnterpriseDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('EnterpriseDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<EnterpriseDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Enterprise/i, level: 1 })).toBeInTheDocument();
  });
});
