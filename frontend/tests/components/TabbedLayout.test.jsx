/**
 * Tabbed Layout Component Tests
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import TabbedLayout from '../../src/components/TabbedLayout/TabbedLayout';

describe('TabbedLayout', () => {
  const mockTabs = [
    { id: 'tab1', label: 'Tab 1', content: <div>Content 1</div> },
    { id: 'tab2', label: 'Tab 2', content: <div>Content 2</div> },
    { id: 'tab3', label: 'Tab 3', content: <div>Content 3</div> },
  ];

  it('should render tabs', () => {
    render(<TabbedLayout tabs={mockTabs} />);
    expect(screen.getByText('Tab 1')).toBeInTheDocument();
    expect(screen.getByText('Tab 2')).toBeInTheDocument();
    expect(screen.getByText('Tab 3')).toBeInTheDocument();
  });

  it('should display first tab content by default', () => {
    render(<TabbedLayout tabs={mockTabs} />);
    expect(screen.getByText('Content 1')).toBeInTheDocument();
    expect(screen.queryByText('Content 2')).not.toBeInTheDocument();
  });

  it('should switch tabs on click', () => {
    render(<TabbedLayout tabs={mockTabs} />);
    fireEvent.click(screen.getByText('Tab 2'));

    expect(screen.getByText('Content 2')).toBeInTheDocument();
    expect(screen.queryByText('Content 1')).not.toBeInTheDocument();
  });

  it('should handle tab close', () => {
    const onTabClose = vi.fn();
    render(<TabbedLayout tabs={mockTabs} onTabClose={onTabClose} />);

    const closeButton = screen.getAllByTitle(/close tab/i)[0];
    fireEvent.click(closeButton);

    expect(onTabClose).toHaveBeenCalledWith('tab1');
  });
});

