/**
 * Split Pane Component Tests
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import SplitPane from '../../src/components/SplitPane/SplitPane';

describe('SplitPane', () => {
  it('should render split pane with children', () => {
    render(
      <SplitPane>
        <div>Pane 1</div>
        <div>Pane 2</div>
      </SplitPane>
    );

    expect(screen.getByText('Pane 1')).toBeInTheDocument();
    expect(screen.getByText('Pane 2')).toBeInTheDocument();
  });

  it('should render horizontal split by default', () => {
    const { container } = render(
      <SplitPane>
        <div>Pane 1</div>
        <div>Pane 2</div>
      </SplitPane>
    );

    const splitPane = container.querySelector('.split-pane');
    expect(splitPane).toHaveClass('split-pane-horizontal');
  });

  it('should render vertical split when direction is vertical', () => {
    const { container } = render(
      <SplitPane direction="vertical">
        <div>Pane 1</div>
        <div>Pane 2</div>
      </SplitPane>
    );

    const splitPane = container.querySelector('.split-pane');
    expect(splitPane).toHaveClass('split-pane-vertical');
  });
});

