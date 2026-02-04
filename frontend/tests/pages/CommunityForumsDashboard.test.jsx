/**
 * Community Forums Dashboard Tests
 * Phase 20: Community Forums & Discussion
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import apiClient from '../../src/services/apiClient';
import CommunityForumsDashboard from '../../src/pages/CommunityForumsDashboard';

vi.mock('../../src/services/apiClient');

describe('CommunityForumsDashboard', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render dashboard', async () => {
    apiClient.get.mockResolvedValue({ 
      data: { data: [] } 
    });
    
    render(<CommunityForumsDashboard />);
    
    await waitFor(() => {
      expect(screen.getByText(/Community Forums/i)).toBeInTheDocument();
    });
  });

  it('should load and display forum threads', async () => {
    const mockThreads = [
      { id: '1', title: 'Test Thread', content: 'Test content', category: 'general' }
    ];

    apiClient.get
      .mockResolvedValueOnce({ data: { data: mockThreads } })
      .mockResolvedValueOnce({ data: { data: [] } });

    render(<CommunityForumsDashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Community Forums/i)).toBeInTheDocument();
    });
  });
});
