/**
 * Sidebar Component Tests
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Sidebar from '../../src/components/Layout/Sidebar';

// Mock react-router-dom
vi.mock('react-router-dom', () => ({
  NavLink: ({ to, children, style, title }) => {
    // Handle style as function (receives { isActive })
    const computedStyle = typeof style === 'function' ? style({ isActive: false }) : style;
    
    // Handle render prop pattern (children as function)
    if (typeof children === 'function') {
      const renderResult = children({ isActive: false });
      return <a href={to} style={computedStyle} title={title}>{renderResult}</a>;
    }
    return <a href={to} style={computedStyle} title={title}>{children}</a>;
  },
}));

describe('Sidebar', () => {
  const defaultProps = {
    collapsed: false,
    onToggle: vi.fn(),
  };

  it('should render sidebar', () => {
    render(<Sidebar {...defaultProps} />);
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
  });

  it('should render navigation items', () => {
    render(<Sidebar {...defaultProps} />);
    expect(screen.getByText(/dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/chat/i)).toBeInTheDocument();
    expect(screen.getByText(/telemetry/i)).toBeInTheDocument();
  });

  it('should call onToggle when toggle button is clicked', async () => {
    const user = userEvent.setup();
    render(<Sidebar {...defaultProps} />);

    const toggleButton = screen.getByRole('button', { name: /collapse sidebar/i });
    await user.click(toggleButton);

    expect(defaultProps.onToggle).toHaveBeenCalled();
  });

  it('should show collapsed state when collapsed', () => {
    const { container } = render(<Sidebar {...defaultProps} collapsed={true} />);
    const sidebar = container.querySelector('.sidebar');
    expect(sidebar).toBeInTheDocument();
    // Check that collapsed button label is shown
    expect(screen.getByRole('button', { name: /expand sidebar/i })).toBeInTheDocument();
  });
});

