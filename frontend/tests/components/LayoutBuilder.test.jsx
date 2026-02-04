/**
 * LayoutBuilder Component Tests
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LayoutBuilder from '../../src/components/LayoutBuilder/LayoutBuilder';
import { useWidgetLayout } from '../../src/hooks/useWidgetLayout';

// Mock useWidgetLayout
vi.mock('../../src/hooks/useWidgetLayout', () => ({
  useWidgetLayout: vi.fn(),
}));

describe('LayoutBuilder', () => {
  const mockLayout = [
    { i: 'widget1', x: 0, y: 0, w: 4, h: 3 },
    { i: 'widget2', x: 4, y: 0, w: 4, h: 3 },
  ];

  const mockWidgetLayout = {
    layout: mockLayout,
    setLayout: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    useWidgetLayout.mockReturnValue(mockWidgetLayout);
    // Mock window methods
    window.alert = vi.fn();
    window.confirm = vi.fn(() => true);
  });

  it('should render layout builder', () => {
    render(<LayoutBuilder />);
    expect(screen.getByText(/layout builder/i)).toBeInTheDocument();
  });

  it('should display layout types', () => {
    render(<LayoutBuilder />);
    // Layout types are rendered as buttons, check for their names
    const gridButtons = screen.getAllByText(/grid layout/i);
    expect(gridButtons.length).toBeGreaterThan(0);
    expect(screen.getByText(/split panes/i)).toBeInTheDocument();
    expect(screen.getByText(/tabbed/i)).toBeInTheDocument();
  });

  it('should save layout with name', async () => {
    const user = userEvent.setup();
    const onSave = vi.fn();
    render(<LayoutBuilder onSave={onSave} />);

    const nameInput = screen.getByPlaceholderText(/layout name/i);
    await user.type(nameInput, 'My Layout');

    const saveButton = screen.getByRole('button', { name: /save layout/i });
    await user.click(saveButton);

    expect(onSave).toHaveBeenCalled();
    expect(onSave.mock.calls[0][0]).toMatchObject({
      name: 'My Layout',
      type: 'grid',
    });
  });

  it('should not save layout without name', async () => {
    const user = userEvent.setup();
    const onSave = vi.fn();
    render(<LayoutBuilder onSave={onSave} />);

    const saveButton = screen.getByRole('button', { name: /save layout/i });
    await user.click(saveButton);

    expect(window.alert).toHaveBeenCalledWith('Please enter a layout name');
    expect(onSave).not.toHaveBeenCalled();
  });

  it('should reset layout when reset button is clicked', async () => {
    const user = userEvent.setup();
    render(<LayoutBuilder />);

    const resetButton = screen.getByRole('button', { name: /reset/i });
    await user.click(resetButton);

    expect(mockWidgetLayout.setLayout).toHaveBeenCalledWith([]);
  });
});

