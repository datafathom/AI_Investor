/**
 * NotificationCenter Component Tests
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import NotificationCenter from '../../src/components/NotificationCenter/NotificationCenter';

// Mock zustand store
const mockUseStore = vi.fn();
vi.mock('../../src/store/store', () => ({
  useStore: () => mockUseStore(),
}));

describe('NotificationCenter', () => {
  const defaultProps = {
    onClose: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('should render notification center', () => {
    mockUseStore.mockReturnValue({
      notifications: [],
      removeNotification: vi.fn(),
      clearNotifications: vi.fn(),
    });
    render(<NotificationCenter {...defaultProps} />);
    // "Notifications" appears in the header, use getAllByText and check it exists
    expect(screen.getAllByText(/notifications/i).length).toBeGreaterThan(0);
  });

  it('should display notifications', () => {
    const removeNotification = vi.fn();
    const clearNotifications = vi.fn();
    mockUseStore.mockReturnValue({
      notifications: [
        { id: 1, title: 'Test Notification', message: 'Test message', type: 'info', read: false },
        { id: 2, title: 'Error Notification', message: 'Error message', type: 'error', read: false },
      ],
      removeNotification,
      clearNotifications,
    });

    render(<NotificationCenter {...defaultProps} />);

    expect(screen.getByText('Test Notification')).toBeInTheDocument();
    expect(screen.getByText('Error Notification')).toBeInTheDocument();
  });

  it('should call removeNotification when notification is dismissed', async () => {
    const user = userEvent.setup();
    const removeNotification = vi.fn();
    mockUseStore.mockReturnValue({
      notifications: [
        { id: 1, title: 'Test', message: 'Test', type: 'info', read: false },
      ],
      removeNotification,
      clearNotifications: vi.fn(),
    });

    render(<NotificationCenter {...defaultProps} />);

    const dismissButton = screen.getByTitle(/dismiss/i) || screen.getByText(/×/);
    await user.click(dismissButton);

    expect(removeNotification).toHaveBeenCalledWith(1);
  });

  it('should call clearNotifications when clear all is clicked', async () => {
    const user = userEvent.setup();
    const clearNotifications = vi.fn();
    mockUseStore.mockReturnValue({
      notifications: [
        { id: 1, title: 'Test', message: 'Test', type: 'info', read: false },
      ],
      removeNotification: vi.fn(),
      clearNotifications,
    });

    render(<NotificationCenter {...defaultProps} />);

    const clearButton = screen.getByText(/clear all/i);
    await user.click(clearButton);

    expect(clearNotifications).toHaveBeenCalled();
  });
});

