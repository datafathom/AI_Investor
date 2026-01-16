/**
 * AuthGuard Component Tests
 */

import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import AuthGuard from '../../src/components/AuthGuard';
import { authService } from '../../src/utils/authService';

// Mock authService
vi.mock('../../src/utils/authService', () => ({
  authService: {
    isAuthenticated: vi.fn(),
  },
}));

describe('AuthGuard', () => {
  const mockOnShowLogin = vi.fn();
  const TestChild = () => <div>Protected Content</div>;

  beforeEach(() => {
    vi.clearAllMocks();
    // Clear any existing intervals
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should render children when authenticated', () => {
    authService.isAuthenticated.mockReturnValue(true);

    render(
      <AuthGuard onShowLogin={mockOnShowLogin}>
        <TestChild />
      </AuthGuard>
    );

    expect(screen.getByText('Protected Content')).toBeInTheDocument();
    expect(mockOnShowLogin).not.toHaveBeenCalled();
  });

  it('should not render children when not authenticated', () => {
    authService.isAuthenticated.mockReturnValue(false);

    render(
      <AuthGuard onShowLogin={mockOnShowLogin}>
        <TestChild />
      </AuthGuard>
    );

    expect(screen.queryByText('Protected Content')).not.toBeInTheDocument();
  });

  it('should call onShowLogin when not authenticated', () => {
    authService.isAuthenticated.mockReturnValue(false);

    render(
      <AuthGuard onShowLogin={mockOnShowLogin}>
        <TestChild />
      </AuthGuard>
    );

    expect(mockOnShowLogin).toHaveBeenCalled();
  });

  it('should check authentication status periodically', () => {
    authService.isAuthenticated.mockReturnValue(false);

    render(
      <AuthGuard onShowLogin={mockOnShowLogin}>
        <TestChild />
      </AuthGuard>
    );

    const initialCallCount = authService.isAuthenticated.mock.calls.length;

    // Fast-forward time
    vi.advanceTimersByTime(500);

    expect(authService.isAuthenticated.mock.calls.length).toBeGreaterThan(initialCallCount);
  });

  it('should listen to storage events for auth changes', () => {
    authService.isAuthenticated.mockReturnValue(false);

    render(
      <AuthGuard onShowLogin={mockOnShowLogin}>
        <TestChild />
      </AuthGuard>
    );

    // Simulate storage event
    const storageEvent = new StorageEvent('storage', {
      key: 'widget_os_token',
      newValue: 'test-token',
    });

    authService.isAuthenticated.mockReturnValue(true);
    window.dispatchEvent(storageEvent);

    // Should check auth again
    expect(authService.isAuthenticated).toHaveBeenCalled();
  });

  it('should clean up intervals and event listeners on unmount', () => {
    authService.isAuthenticated.mockReturnValue(false);
    const removeEventListenerSpy = vi.spyOn(window, 'removeEventListener');

    const { unmount } = render(
      <AuthGuard onShowLogin={mockOnShowLogin}>
        <TestChild />
      </AuthGuard>
    );

    unmount();

    expect(removeEventListenerSpy).toHaveBeenCalledWith('storage', expect.any(Function));
  });
});

