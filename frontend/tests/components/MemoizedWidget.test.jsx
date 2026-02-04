/**
 * MemoizedWidget Component Tests
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoizedWidget } from '../../src/components/MemoizedWidget';

describe('MemoizedWidget', () => {
  it('should render wrapped component', () => {
    render(
      <MemoizedWidget widgetId="test">
        <div>Test Content</div>
      </MemoizedWidget>
    );
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('should memoize component to prevent unnecessary re-renders', () => {
    const renderCount = vi.fn();
    const TestContent = () => {
      renderCount();
      return <div>Test</div>;
    };

    const { rerender } = render(
      <MemoizedWidget widgetId="test">
        <TestContent />
      </MemoizedWidget>
    );

    expect(renderCount).toHaveBeenCalledTimes(1);
    expect(screen.getByText('Test')).toBeInTheDocument();

    // Re-render with same widgetId but different children (should still render)
    rerender(
      <MemoizedWidget widgetId="test">
        <div>Different Content</div>
      </MemoizedWidget>
    );

    // TestContent should not re-render since it's been replaced
    expect(renderCount).toHaveBeenCalledTimes(1);
    expect(screen.getByText('Different Content')).toBeInTheDocument();
  });
});

