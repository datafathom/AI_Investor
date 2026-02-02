/**
 * Developer Platform Dashboard Tests
 * Phase 29: Developer Platform & Public API
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import DeveloperPlatformDashboard from '../../src/pages/DeveloperPlatformDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('DeveloperPlatformDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    // publicApiStore expects response.data?.data or response.data
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<DeveloperPlatformDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Developer Platform/i, level: 1 })).toBeInTheDocument();
  });
});
