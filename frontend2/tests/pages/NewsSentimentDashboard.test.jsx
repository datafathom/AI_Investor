/**
 * News Sentiment Dashboard Tests
 * Phase 16: News & Sentiment Analysis
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import NewsSentimentDashboard from '../../src/pages/NewsSentimentDashboard';

vi.mock('axios');

describe('NewsSentimentDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    axios.get.mockResolvedValue({ data: { data: {} } });
    
    render(<NewsSentimentDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/News Sentiment/i)).toBeInTheDocument();
    });
  });
});
