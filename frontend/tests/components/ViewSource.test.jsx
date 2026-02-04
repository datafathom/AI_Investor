/**
 * ViewSource Component Tests
 */

import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ViewSource from '../../src/components/ViewSource';

describe('ViewSource', () => {
  const defaultProps = {
    source: 'const Test = () => <div>Test</div>;',
    onClose: vi.fn(),
  };

  it('should render view source modal', () => {
    render(<ViewSource {...defaultProps} />);
    expect(screen.getByText(/source code/i)).toBeInTheDocument();
  });

  it('should display source code', () => {
    render(<ViewSource {...defaultProps} />);
    // SyntaxHighlighter renders code in <pre><code> tags
    const codeElement = document.querySelector('code, pre');
    expect(codeElement).toBeInTheDocument();
    expect(codeElement?.textContent).toContain('const Test');
  });

  it('should call onClose when close button is clicked', async () => {
    const user = userEvent.setup();
    render(<ViewSource {...defaultProps} />);

    const closeButton = screen.getByRole('button', { name: /close/i });
    await user.click(closeButton);

    expect(defaultProps.onClose).toHaveBeenCalled();
  });

  it('should not render when source is not provided', () => {
    render(<ViewSource source={null} onClose={vi.fn()} />);
    expect(screen.queryByText(/source code/i)).not.toBeInTheDocument();
  });
});

