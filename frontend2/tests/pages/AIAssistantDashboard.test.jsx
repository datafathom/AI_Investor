/**
 * AI Assistant Dashboard Tests
 * Phase 23: AI Assistant & Conversational Interface
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import AIAssistantDashboard from '../../src/pages/AIAssistantDashboard';

vi.mock('axios');

describe('AIAssistantDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<AIAssistantDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/AI Assistant/i)).toBeInTheDocument();
    });
  });
});
