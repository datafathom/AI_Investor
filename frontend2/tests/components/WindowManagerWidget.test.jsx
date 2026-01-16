/**
 * WindowManagerWidget Component Tests
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import WindowManagerWidget from '../../src/components/WindowManager/WindowManagerWidget';
import { useWindowManager } from '../../src/hooks/useWindowManager';

// Mock useWindowManager
vi.mock('../../src/hooks/useWindowManager', () => ({
  useWindowManager: vi.fn(),
}));

describe('WindowManagerWidget', () => {
  const mockWindows = [
    { id: 'win1', title: 'Window 1', state: 'normal' },
  ];

  const mockWindowManager = {
    windows: mockWindows,
    registerWindow: vi.fn(),
    saveLayout: vi.fn(),
    loadLayout: vi.fn(),
    getSavedLayouts: vi.fn(() => ({
      'Layout 1': { windows: [{ id: 'win1' }] },
      'Layout 2': { windows: [{ id: 'win2' }] },
    })),
    deleteLayout: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    useWindowManager.mockReturnValue(mockWindowManager);
    // Mock window methods
    window.alert = vi.fn();
    window.confirm = vi.fn(() => true);
  });

  it('should render window manager widget', () => {
    render(<WindowManagerWidget />);
    expect(screen.getByText(/window manager/i)).toBeInTheDocument();
  });

  it('should create test window when button is clicked', async () => {
    const user = userEvent.setup();
    render(<WindowManagerWidget />);

    const createButton = screen.getByRole('button', { name: /create test window/i });
    await user.click(createButton);

    expect(mockWindowManager.registerWindow).toHaveBeenCalled();
  });

  it('should save layout with name', async () => {
    const user = userEvent.setup();
    render(<WindowManagerWidget />);

    const nameInput = screen.getByPlaceholderText(/layout name/i);
    await user.type(nameInput, 'My Layout');

    const saveButton = screen.getByRole('button', { name: /save layout/i });
    await user.click(saveButton);

    expect(mockWindowManager.saveLayout).toHaveBeenCalledWith('My Layout');
  });

  it('should not save layout without name', async () => {
    const user = userEvent.setup();
    render(<WindowManagerWidget />);

    const saveButton = screen.getByRole('button', { name: /save layout/i });
    await user.click(saveButton);

    expect(window.alert).toHaveBeenCalledWith('Please enter a layout name');
    expect(mockWindowManager.saveLayout).not.toHaveBeenCalled();
  });

  it('should display saved layouts', () => {
    render(<WindowManagerWidget />);
    expect(screen.getByText('Layout 1')).toBeInTheDocument();
    expect(screen.getByText('Layout 2')).toBeInTheDocument();
  });

  it('should load layout when clicked', async () => {
    const user = userEvent.setup();
    render(<WindowManagerWidget />);

    // Find all load buttons and click the first one
    const loadButtons = screen.getAllByTitle('Load layout');
    await user.click(loadButtons[0]);

    expect(mockWindowManager.loadLayout).toHaveBeenCalledWith('Layout 1');
  });

  it('should delete layout when delete button is clicked', async () => {
    const user = userEvent.setup();
    render(<WindowManagerWidget />);

    // Find all delete buttons and click the first one
    const deleteButtons = screen.getAllByTitle('Delete layout');
    await user.click(deleteButtons[0]);

    expect(mockWindowManager.deleteLayout).toHaveBeenCalledWith('Layout 1');
  });
});

