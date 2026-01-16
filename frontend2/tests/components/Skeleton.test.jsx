/**
 * Skeleton Component Tests
 */

import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Skeleton from '../../src/components/Skeleton';

describe('Skeleton', () => {
  it('should render skeleton component', () => {
    const { container } = render(<Skeleton />);
    expect(container.querySelector('.skeleton')).toBeInTheDocument();
  });

  it('should render with custom width', () => {
    const { container } = render(<Skeleton width="200px" />);
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveStyle({ width: '200px' });
  });

  it('should render with custom height', () => {
    const { container } = render(<Skeleton height="50px" />);
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveStyle({ height: '50px' });
  });

  it('should render with default classes', () => {
    const { container } = render(<Skeleton />);
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveClass('skeleton');
    expect(skeleton).toHaveClass('shimmer');
  });

  it('should render circular skeleton', () => {
    const { container } = render(<Skeleton width="50px" height="50px" borderRadius="50%" />);
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveStyle({ borderRadius: '50%' });
  });

  it('should render rectangular skeleton', () => {
    const { container } = render(<Skeleton width="100px" height="20px" borderRadius="4px" />);
    const skeleton = container.querySelector('.skeleton');
    expect(skeleton).toHaveStyle({ borderRadius: '4px' });
  });
});

