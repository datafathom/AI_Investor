/**
 * Education Platform Dashboard Tests
 * Phase 21: Education Platform & Learning Management
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import EducationPlatformDashboard from '../../src/pages/EducationPlatformDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('EducationPlatformDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<EducationPlatformDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Education Platform/i, level: 1 })).toBeInTheDocument();
  });
});
