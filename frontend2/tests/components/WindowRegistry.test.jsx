/**
 * WindowRegistry Component Tests
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import WindowRegistry from '../../src/components/WindowManager/WindowRegistry';
import { useWindowManager } from '../../src/hooks/useWindowManager';

// Mock useWindowManager
vi.mock('../../src/hooks/useWindowManager', () => ({
  useWindowManager: vi.fn(),
}));

describe('WindowRegistry', () => {
  const mockWindows = [
    { id: 'win1', title: 'Window 1', state: 'normal', zIndex: 100, createdAt: new Date() },
    { id: 'win2', title: 'Window 2', state: 'minimized', zIndex: 50, createdAt: new Date() },
  ];

  const mockWindowManager = {
    windows: mockWindows,
    windowStack: mockWindows,
    bringToFront: vi.fn(),
    minimizeWindow: vi.fn(),
    maximizeWindow: vi.fn(),
    restoreWindow: vi.fn(),
    toggleLock: vi.fn(),
    unregisterWindow: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    useWindowManager.mockReturnValue(mockWindowManager);
  });

  it('should render window registry', () => {
    render(<WindowRegistry />);
    expect(screen.getByText(/window registry/i)).toBeInTheDocument();
  });

  it('should display all windows', () => {
    render(<WindowRegistry />);
    expect(screen.getByText('Window 1')).toBeInTheDocument();
    expect(screen.getByText('Window 2')).toBeInTheDocument();
  });

  it('should filter windows by search', async () => {
    const user = userEvent.setup();
    render(<WindowRegistry />);

    const searchInput = screen.getByPlaceholderText(/filter windows/i);
    await user.type(searchInput, 'Window 1');

    expect(screen.getByText('Window 1')).toBeInTheDocument();
    expect(screen.queryByText('Window 2')).not.toBeInTheDocument();
  });

  it('should call bringToFront when window is clicked', async () => {
    const user = userEvent.setup();
    const onSelectWindow = vi.fn();
    render(<WindowRegistry onSelectWindow={onSelectWindow} />);

    const windowItem = screen.getByText('Window 1').closest('[role="button"]');
    if (windowItem) {
      await user.click(windowItem);
      expect(mockWindowManager.bringToFront).toHaveBeenCalledWith('win1');
      expect(onSelectWindow).toHaveBeenCalledWith('win1');
    }
  });

  it('should call minimizeWindow when minimize button is clicked', async () => {
    const user = userEvent.setup();
    render(<WindowRegistry />);

    // Find minimize button for Window 1
    const minimizeButtons = screen.getAllByTitle(/minimize/i);
    if (minimizeButtons.length > 0) {
      await user.click(minimizeButtons[0]);
      expect(mockWindowManager.minimizeWindow).toHaveBeenCalled();
    }
  });
});

