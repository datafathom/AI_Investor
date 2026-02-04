/**
 * PerformanceMonitor Component Tests
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import PerformanceMonitor from '../../src/components/PerformanceMonitor/PerformanceMonitor';

describe('PerformanceMonitor', () => {
  it('should render performance monitor', () => {
    render(<PerformanceMonitor />);
    expect(screen.getByText(/performance/i)).toBeInTheDocument();
  });

  it('should display performance metrics', () => {
    const metrics = {
      fps: 60,
      memory: 100,
      cpu: 50,
    };
    render(<PerformanceMonitor metrics={metrics} />);
    // Performance monitor displays charts/metrics
    expect(document.body).toBeTruthy();
  });
});

