/**
 * WindowHeader Component Tests
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import WindowHeader from '../../src/components/WindowHeader';

describe('WindowHeader', () => {
  const defaultProps = {
    title: 'Test Widget',
    widgetId: 'test-widget',
    onClose: vi.fn(),
    onMinimize: vi.fn(),
    onMaximize: vi.fn(),
    onLock: vi.fn(),
    onViewSource: vi.fn(),
    minimized: false,
    maximized: false,
    locked: false,
  };

  it('should render window header with title', () => {
    render(<WindowHeader {...defaultProps} />);
    expect(screen.getByText('Test Widget')).toBeInTheDocument();
  });

  it('should call onClose when close button is clicked', async () => {
    const user = userEvent.setup();
    render(<WindowHeader {...defaultProps} />);

    const closeButton = screen.getByRole('button', { name: /close window/i });
    await user.click(closeButton);

    expect(defaultProps.onClose).toHaveBeenCalled();
  });

  it('should call onMinimize when minimize button is clicked', async () => {
    const user = userEvent.setup();
    render(<WindowHeader {...defaultProps} />);

    const minimizeButton = screen.getByRole('button', { name: /minimize window/i });
    await user.click(minimizeButton);

    expect(defaultProps.onMinimize).toHaveBeenCalled();
  });

  it('should call onMaximize when maximize button is clicked', async () => {
    const user = userEvent.setup();
    render(<WindowHeader {...defaultProps} />);

    const maximizeButton = screen.getByRole('button', { name: /maximize window/i });
    await user.click(maximizeButton);

    expect(defaultProps.onMaximize).toHaveBeenCalled();
  });

  it('should call onLock when lock button is clicked', async () => {
    const user = userEvent.setup();
    render(<WindowHeader {...defaultProps} />);

    const lockButton = screen.getByRole('button', { name: /lock widget/i });
    await user.click(lockButton);

    expect(defaultProps.onLock).toHaveBeenCalled();
  });

  it('should call onViewSource when view source button is clicked', async () => {
    const user = userEvent.setup();
    render(<WindowHeader {...defaultProps} />);

    const viewSourceButton = screen.getByRole('button', { name: /view source code/i });
    await user.click(viewSourceButton);

    expect(defaultProps.onViewSource).toHaveBeenCalled();
  });

  it('should show locked state when locked', () => {
    render(<WindowHeader {...defaultProps} isLocked={true} />);
    const lockButton = screen.getByRole('button', { name: /unlock widget/i });
    expect(lockButton).toBeInTheDocument();
  });

  it('should show maximized state when maximized', () => {
    render(<WindowHeader {...defaultProps} isMaximized={true} />);
    const maximizeButton = screen.getByRole('button', { name: /restore window/i });
    expect(maximizeButton).toBeInTheDocument();
  });
});

