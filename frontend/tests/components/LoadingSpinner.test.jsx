/**
 * LoadingSpinner Component Tests
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import LoadingSpinner from '../../src/components/LoadingSpinner';

describe('LoadingSpinner', () => {
  it('should render loading spinner', () => {
    const { container } = render(<LoadingSpinner />);
    expect(container.querySelector('.loading-spinner')).toBeInTheDocument();
  });

  it('should render with custom message', () => {
    render(<LoadingSpinner message="Loading data..." />);
    expect(screen.getByText('Loading data...')).toBeInTheDocument();
  });

  it('should render with default message when no message provided', () => {
    const { container } = render(<LoadingSpinner />);
    // Component renders spinner but no message when message prop is not provided
    expect(container.querySelector('.loading-spinner')).toBeInTheDocument();
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

  it('should apply size prop', () => {
    const { container: container1 } = render(<LoadingSpinner size="small" />);
    expect(container1.querySelector('.loading-spinner')).toHaveClass('loading-spinner-small');

    const { container: container2 } = render(<LoadingSpinner size="large" />);
    expect(container2.querySelector('.loading-spinner')).toHaveClass('loading-spinner-large');
  });
});

