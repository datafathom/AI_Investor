/**
 * Window Manager Component Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import WindowManagerWidget from '../../src/components/WindowManager/WindowManagerWidget';
import { useWindowManager } from '../../src/hooks/useWindowManager';

// Mock the useWindowManager hook
vi.mock('../../src/hooks/useWindowManager', () => ({
  useWindowManager: vi.fn(),
}));

describe('WindowManagerWidget', () => {
  const mockUseWindowManager = {
    windows: [],
    registerWindow: vi.fn(),
    saveLayout: vi.fn(),
    loadLayout: vi.fn(),
    getSavedLayouts: vi.fn(() => []),
    deleteLayout: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    useWindowManager.mockReturnValue(mockUseWindowManager);
  });

  it('should render window manager widget', () => {
    render(<WindowManagerWidget />);
    expect(screen.getByText(/window manager/i)).toBeInTheDocument();
  });

  it('should display list of windows', () => {
    const mockWindows = [
      { id: 'w1', title: 'Window 1', state: 'normal' },
      { id: 'w2', title: 'Window 2', state: 'minimized' },
    ];
    useWindowManager.mockReturnValue({
      ...mockUseWindowManager,
      windows: mockWindows,
    });

    render(<WindowManagerWidget />);
    // WindowManagerWidget shows window count in header stats
    expect(screen.getByText(/2 window/i)).toBeInTheDocument();
    
    // If registry is shown, windows would be listed there
    // But by default registry is hidden, so we just check the count
  });

  it('should handle creating test window', () => {
    const registerWindow = vi.fn();
    useWindowManager.mockReturnValue({
      ...mockUseWindowManager,
      registerWindow,
    });

    render(<WindowManagerWidget />);
    const createButton = screen.getByText(/create test window/i);
    fireEvent.click(createButton);

    expect(registerWindow).toHaveBeenCalled();
  });

  it('should handle saving layout', () => {
    const saveLayout = vi.fn();
    useWindowManager.mockReturnValue({
      ...mockUseWindowManager,
      saveLayout,
    });

    render(<WindowManagerWidget />);
    const layoutInput = screen.getByPlaceholderText(/layout name/i);
    const saveButton = screen.getByText(/save layout/i);
    
    fireEvent.change(layoutInput, { target: { value: 'Test Layout' } });
    fireEvent.click(saveButton);

    expect(saveLayout).toHaveBeenCalledWith('Test Layout');
  });
});

