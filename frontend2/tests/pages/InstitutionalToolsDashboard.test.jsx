/**
 * Institutional Tools Dashboard Tests
 * Phase 26: Institutional Tools & Professional Features
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import InstitutionalToolsDashboard from '../../src/pages/InstitutionalToolsDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('InstitutionalToolsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<InstitutionalToolsDashboard />);
    
    expect(await screen.findByRole('heading', { name: /Institutional Tools/i, level: 1 })).toBeInTheDocument();
  });
});
