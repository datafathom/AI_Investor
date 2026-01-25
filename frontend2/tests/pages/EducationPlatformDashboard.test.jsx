/**
 * Education Platform Dashboard Tests
 * Phase 21: Education Platform & Learning Management
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import EducationPlatformDashboard from '../../src/pages/EducationPlatformDashboard';

vi.mock('axios');

describe('EducationPlatformDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<EducationPlatformDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Education Platform/i)).toBeInTheDocument();
    });
  });
});
