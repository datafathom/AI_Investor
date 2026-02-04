/**
 * WindowGroup Component Tests
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import WindowGroup from '../../src/components/WindowManager/WindowGroup';
import { useWindowManager } from '../../src/hooks/useWindowManager';

// Mock useWindowManager
vi.mock('../../src/hooks/useWindowManager', () => ({
  useWindowManager: vi.fn(),
}));

describe('WindowGroup', () => {
  const mockWindows = [
    { id: 'win1', title: 'Window 1', state: 'normal' },
    { id: 'win2', title: 'Window 2', state: 'normal' },
  ];

  let mockWindowManager;

  beforeEach(() => {
    vi.clearAllMocks();
    mockWindowManager = {
      getGroupWindows: vi.fn((groupId) => {
        // Return windows for group1
        if (groupId === 'group1') {
          return mockWindows;
        }
        return [];
      }),
      bringToFront: vi.fn(),
      unregisterWindow: vi.fn(),
    };
    useWindowManager.mockReturnValue(mockWindowManager);
  });

  it('should not render when group has no windows', () => {
    mockWindowManager.getGroupWindows.mockReturnValue([]);
    const { container } = render(<WindowGroup groupId="group1" />);
    expect(container.firstChild).toBeNull();
  });

  it('should render windows as tabs', async () => {
    render(<WindowGroup groupId="group1" />);
    // Wait for useEffect to set active tab
    await waitFor(() => {
      expect(screen.getByText('Window 1')).toBeInTheDocument();
    });
    expect(screen.getByText('Window 2')).toBeInTheDocument();
  });

  it('should switch active tab when clicked', async () => {
    const user = userEvent.setup();
    render(<WindowGroup groupId="group1" />);

    await waitFor(() => {
      expect(screen.getByText('Window 2')).toBeInTheDocument();
    });

    // Click on the tab container (div with window-group-tab class)
    const tabs = screen.getAllByText('Window 2');
    const tabContainer = tabs[0].closest('.window-group-tab');
    if (tabContainer) {
      await user.click(tabContainer);
      expect(mockWindowManager.bringToFront).toHaveBeenCalledWith('win2');
    }
  });

  it('should close window when close button is clicked', async () => {
    const user = userEvent.setup();
    render(<WindowGroup groupId="group1" />);

    await waitFor(() => {
      expect(screen.getByText('Window 1')).toBeInTheDocument();
    });

    // Find close button (×) for a tab - it's a button with title "Close tab"
    const closeButtons = screen.getAllByTitle('Close tab');
    if (closeButtons.length > 0) {
      await user.click(closeButtons[0]);
      expect(mockWindowManager.unregisterWindow).toHaveBeenCalled();
    }
  });
});

