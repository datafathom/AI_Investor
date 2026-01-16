/**
 * DockerWidget Component Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import DockerWidget from '../../src/components/DockerWidget';

// Mock fetch
global.fetch = vi.fn();

describe('DockerWidget', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render docker widget', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });
    render(<DockerWidget />);
    await waitFor(() => {
      // When empty, shows "No containers found" or "0 containers"
      expect(screen.getAllByText(/no containers found|0 container/i).length).toBeGreaterThan(0);
    });
  });

  it('should show loading state initially', () => {
    fetch.mockImplementation(() => new Promise(() => {})); // Never resolves
    render(<DockerWidget />);
    expect(screen.getByText(/connecting to docker/i)).toBeInTheDocument();
  });

  it('should display containers when fetch succeeds', async () => {
    const mockContainers = [
      { id: '1', name: 'container1', status: 'Up 2 hours', state: 'running', image: 'nginx' },
      { id: '2', name: 'container2', status: 'Exited (0)', state: 'exited', image: 'redis' },
    ];

    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockContainers,
    });

    render(<DockerWidget />);

    await waitFor(() => {
      expect(screen.getByText('container1')).toBeInTheDocument();
      expect(screen.getByText('container2')).toBeInTheDocument();
    });
  });

  it('should show error message when fetch fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Failed to fetch'));

    render(<DockerWidget />);

    await waitFor(() => {
      expect(screen.getByText(/failed to fetch/i)).toBeInTheDocument();
    });
  });

  it('should show retry button on error', async () => {
    fetch.mockRejectedValueOnce(new Error('Failed to fetch'));

    render(<DockerWidget />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
    });
  });

  it('should retry fetch when retry button is clicked', async () => {
    const user = userEvent.setup();
    fetch.mockRejectedValueOnce(new Error('Failed to fetch'));

    render(<DockerWidget />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /retry/i })).toBeInTheDocument();
    });

    const mockContainers = [{ Id: '1', Names: ['container1'], Status: 'Running' }];
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockContainers,
    });

    const retryButton = screen.getByRole('button', { name: /retry/i });
    await user.click(retryButton);

    await waitFor(() => {
      expect(fetch).toHaveBeenCalledTimes(2);
    });
  });
});

