/**
 * OfflineIndicator Component Tests
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import OfflineIndicator from '../../src/components/OfflineIndicator/OfflineIndicator';
import syncService from '../../src/services/syncService';

// Mock syncService
vi.mock('../../src/services/syncService', () => ({
  default: {
    getQueueStatus: vi.fn(() => []),
    on: vi.fn(),
    off: vi.fn(),
  },
}));

describe('OfflineIndicator', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Reset navigator.onLine
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      configurable: true,
      value: true,
    });
  });

  it('should render offline indicator when offline', () => {
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      configurable: true,
      value: false,
    });

    syncService.getQueueStatus.mockReturnValue([]);

    render(<OfflineIndicator />);
    expect(screen.getByText(/offline/i)).toBeInTheDocument();
  });

  it('should not render when online and no queue', () => {
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      configurable: true,
      value: true,
    });

    syncService.getQueueStatus.mockReturnValue([]);

    render(<OfflineIndicator />);
    expect(screen.queryByText(/offline/i)).not.toBeInTheDocument();
  });

  it('should show syncing message when queue has items', () => {
    Object.defineProperty(navigator, 'onLine', {
      writable: true,
      configurable: true,
      value: true,
    });

    syncService.getQueueStatus.mockReturnValue([{ id: 1 }, { id: 2 }]);

    render(<OfflineIndicator />);
    expect(screen.getByText(/syncing/i)).toBeInTheDocument();
  });
});

