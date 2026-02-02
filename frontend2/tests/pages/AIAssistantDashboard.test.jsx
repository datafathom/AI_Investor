/**
 * AI Assistant Dashboard Tests
 * Phase 23: AI Assistant & Conversational Interface
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import AIAssistantDashboard from '../../src/pages/AIAssistantDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('AIAssistantDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<AIAssistantDashboard />);
    
    expect(await screen.findByRole('heading', { name: /AI Assistant/i, level: 1 })).toBeInTheDocument();
  });
});
