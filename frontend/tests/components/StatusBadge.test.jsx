/**
 * StatusBadge Component Tests
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import StatusBadge from '../../src/components/StatusBadge';

describe('StatusBadge', () => {
  it('should render status badge with text', () => {
    render(<StatusBadge status="Connected" type="success" />);
    expect(screen.getByText('Connected')).toBeInTheDocument();
  });

  it('should apply correct status class', () => {
    const { container } = render(<StatusBadge status="Connected" type="success" />);
    const badge = container.querySelector('.status-badge');
    expect(badge).toBeInTheDocument();
  });

  it('should handle different status types', () => {
    const { container: container1 } = render(<StatusBadge status="OK" type="success" />);
    expect(container1.querySelector('.status-badge')).toBeInTheDocument();

    const { container: container2 } = render(<StatusBadge status="Error" type="error" />);
    expect(container2.querySelector('.status-badge')).toBeInTheDocument();

    const { container: container3 } = render(<StatusBadge status="Warning" type="warning" />);
    expect(container3.querySelector('.status-badge')).toBeInTheDocument();

    const { container: container4 } = render(<StatusBadge status="Loading" type="info" />);
    expect(container4.querySelector('.status-badge')).toBeInTheDocument();
  });

  it('should handle different sizes', () => {
    const { container: container1 } = render(<StatusBadge status="Test" size="small" />);
    expect(container1.querySelector('.status-badge-small')).toBeInTheDocument();

    const { container: container2 } = render(<StatusBadge status="Test" size="large" />);
    expect(container2.querySelector('.status-badge-large')).toBeInTheDocument();

    const { container: container3 } = render(<StatusBadge status="Test" size="medium" />);
    expect(container3.querySelector('.status-badge-medium')).toBeInTheDocument();
  });
});

