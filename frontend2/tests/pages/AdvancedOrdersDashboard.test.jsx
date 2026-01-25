/**
 * Advanced Orders Dashboard Tests
 * Phase 13: Advanced Order Types & Smart Execution
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import AdvancedOrdersDashboard from '../../src/pages/AdvancedOrdersDashboard';

vi.mock('axios');

describe('AdvancedOrdersDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<AdvancedOrdersDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Advanced Orders/i)).toBeInTheDocument();
    });
  });
});
