/**
 * MetricCard Component Tests
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import MetricCard from '../../src/components/MetricCard';

describe('MetricCard', () => {
  it('should render metric card with label and value', () => {
    render(<MetricCard label="CPU Usage" value="45%" />);
    expect(screen.getByText('CPU Usage')).toBeInTheDocument();
    expect(screen.getByText('45%')).toBeInTheDocument();
  });

  it('should render with icon when provided', () => {
    render(<MetricCard label="Memory" value="8GB" icon="💾" />);
    expect(screen.getByText('💾')).toBeInTheDocument();
  });

  it('should render with custom color', () => {
    const { container } = render(
      <MetricCard label="Test" value="100" color="#ff0000" />
    );
    const valueElement = container.querySelector('.metric-card-value');
    expect(valueElement).toHaveStyle({ color: '#ff0000' });
  });

  it('should render with default className', () => {
    const { container } = render(
      <MetricCard label="Test" value="100" />
    );
    expect(container.querySelector('.metric-card')).toBeInTheDocument();
    expect(container.querySelector('.metric-card')).toHaveClass('metric-card');
  });
});

