/**
 * Toaster Component Tests
 */

import { describe, it, expect } from 'vitest';
import { render } from '@testing-library/react';
import Toaster from '../../src/components/Toaster';

// Mock sonner
vi.mock('sonner', () => ({
  Toaster: ({ position, toastOptions, theme }) => (
    <div data-testid="sonner-toaster" data-position={position} data-theme={theme}>
      <div data-testid="toast-options">{JSON.stringify(toastOptions)}</div>
    </div>
  ),
}));

describe('Toaster', () => {
  it('should render toaster component', () => {
    const { container } = render(<Toaster />);
    expect(container.querySelector('[data-testid="sonner-toaster"]')).toBeInTheDocument();
  });

  it('should pass correct props to Sonner', () => {
    const { container } = render(<Toaster />);
    const toaster = container.querySelector('[data-testid="sonner-toaster"]');
    expect(toaster).toHaveAttribute('data-position', 'bottom-right');
    expect(toaster).toHaveAttribute('data-theme', 'light');
  });

  it('should configure toast options with palette colors', () => {
    const { container } = render(<Toaster />);
    const toastOptions = container.querySelector('[data-testid="toast-options"]');
    expect(toastOptions).toBeInTheDocument();
    const options = JSON.parse(toastOptions.textContent);
    expect(options).toHaveProperty('style');
    expect(options).toHaveProperty('classNames');
  });
});


