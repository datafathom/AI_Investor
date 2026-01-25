/**
 * Enterprise Dashboard Tests
 * Phase 24: Enterprise Features & Multi-User Management
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import EnterpriseDashboard from '../../src/pages/EnterpriseDashboard';

vi.mock('axios');

describe('EnterpriseDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<EnterpriseDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Enterprise/i)).toBeInTheDocument();
    });
  });
});
