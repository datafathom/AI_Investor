/**
 * Integrations Dashboard Tests
 * Phase 28: Third-Party Integrations & API Connections
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import IntegrationsDashboard from '../../src/pages/IntegrationsDashboard';

vi.mock('axios');

describe('IntegrationsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<IntegrationsDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Integrations/i)).toBeInTheDocument();
    });
  });
});
