/**
 * News Sentiment Dashboard Tests
 * Phase 16: News & Sentiment Analysis
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import NewsSentimentDashboard from '../../src/pages/NewsSentimentDashboard';

vi.mock('../../src/services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('NewsSentimentDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ data: { data: [] } });
    
    render(<NewsSentimentDashboard />);
    
    expect(await screen.findByRole('heading', { name: /News & Sentiment Analysis/i, level: 1 })).toBeInTheDocument();
  });
});
