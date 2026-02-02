/**
 * DockerWidget Component Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import DockerWidget from '../../src/components/DockerWidget';
import apiClient from '../../src/services/apiClient';

// Mock apiClient
vi.mock('../../src/services/apiClient');

describe('DockerWidget', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render docker widget', async () => {
  it('should render docker widget', async () => {
    apiClient.get.mockResolvedValueOnce({
      data: [],
    });
    render(<DockerWidget />);
    await waitFor(() => {
      // When empty, shows "No containers found" or "0 containers"
      expect(screen.getAllByText(/no containers found|0 container/i).length).toBeGreaterThan(0);
    });
  });

  it('should show loading state initially', () => {
    apiClient.get.mockImplementation(() => new Promise(() => {})); // Never resolves
    render(<DockerWidget />);
    expect(screen.getByText(/connecting to docker/i)).toBeInTheDocument();
  });

  it('should display containers when fetch succeeds', async () => {
    const mockContainers = [
      { id: '1', name: 'container1', status: 'Up 2 hours', state: 'running', image: 'nginx' },
      { id: '2', name: 'container2', status: 'Exited (0)', state: 'exited', image: 'redis' },
    ];

    apiClient.get.mockResolvedValueOnce({
      data: mockContainers,
    });

    render(<DockerWidget />);

    await waitFor(() => {
      expect(screen.getByText('container1')).toBeInTheDocument();
      expect(screen.getByText('container2')).toBeInTheDocument();
    });
  });

  it('should show error message when fetch fails', async () => {
    apiClient.get.mockRejectedValueOnce(new Error('Failed to fetch'));

    render(<DockerWidget />);

    await waitFor(() => {
      expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument();
    });
  });

  it('should show retry button on error', async () => {
    apiClient.get.mockRejectedValueOnce(new Error('Failed to fetch'));

    render(<DockerWidget />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
    });
  });

  it('should retry fetch when retry button is clicked', async () => {
    const user = userEvent.setup();
    apiClient.get.mockRejectedValueOnce(new Error('Failed to fetch'));

    render(<DockerWidget />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
    });

    const mockContainers = [{ Id: '1', Names: ['container1'], Status: 'Running' }];
    apiClient.get.mockResolvedValueOnce({
      data: mockContainers,
    });

    const retryButton = screen.getByRole('button', { name: /retry/i });
    await user.click(retryButton);

    await waitFor(() => {
      expect(apiClient.get).toHaveBeenCalledTimes(2);
    });
  });
});

