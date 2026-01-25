/**
 * Developer Platform Dashboard Tests
 * Phase 29: Developer Platform & Public API
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import DeveloperPlatformDashboard from '../../src/pages/DeveloperPlatformDashboard';

vi.mock('axios');

describe('DeveloperPlatformDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<DeveloperPlatformDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Developer Platform/i)).toBeInTheDocument();
    });
  });
});
