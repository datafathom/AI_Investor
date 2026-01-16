/**
 * LoginModal Component Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import LoginModal from '../../src/components/LoginModal';
import { authService } from '../../src/utils/authService';

// Mock authService
vi.mock('../../src/utils/authService', () => ({
  authService: {
    login: vi.fn(),
    register: vi.fn(),
    isAuthenticated: vi.fn(),
    getCurrentUser: vi.fn(),
  },
}));

describe('LoginModal', () => {
  const mockOnClose = vi.fn();
  const mockOnLoginSuccess = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    authService.isAuthenticated.mockReturnValue(false);
    authService.getCurrentUser.mockReturnValue(null);
  });

  it('should render login form when open', () => {
    render(
      <LoginModal
        isOpen={true}
        onClose={mockOnClose}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );

    expect(screen.getByPlaceholderText(/enter username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/••••••••/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
  });

  it('should not render when closed', () => {
    render(
      <LoginModal
        isOpen={false}
        onClose={mockOnClose}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );

    expect(screen.queryByPlaceholderText(/enter username/i)).not.toBeInTheDocument();
  });

  it('should show error when username and password are empty', async () => {
    const user = userEvent.setup();
    render(
      <LoginModal
        isOpen={true}
        onClose={mockOnClose}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );

    const submitButton = screen.getByRole('button', { name: /sign in/i });
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/username and password required/i)).toBeInTheDocument();
    });
  });

  it('should call login on successful form submission', async () => {
    const user = userEvent.setup();
    authService.login.mockResolvedValue({
      token: 'test-token',
      user: { id: 1, username: 'testuser' },
    });

    render(
      <LoginModal
        isOpen={true}
        onClose={mockOnClose}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );

    const usernameInput = screen.getByPlaceholderText(/enter username/i);
    const passwordInput = screen.getByPlaceholderText(/••••••••/);
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'testpass123');
    await user.click(submitButton);

    await waitFor(() => {
      expect(authService.login).toHaveBeenCalledWith('testuser', 'testpass123');
      expect(mockOnLoginSuccess).toHaveBeenCalled();
      expect(mockOnClose).toHaveBeenCalled();
    });
  });

  it('should show error message on login failure', async () => {
    const user = userEvent.setup();
    authService.login.mockRejectedValue(new Error('Invalid credentials'));

    render(
      <LoginModal
        isOpen={true}
        onClose={mockOnClose}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );

    const usernameInput = screen.getByPlaceholderText(/enter username/i);
    const passwordInput = screen.getByPlaceholderText(/••••••••/);
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'wrongpass');
    await user.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });

    expect(mockOnLoginSuccess).not.toHaveBeenCalled();
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it('should toggle between login and register modes', async () => {
    const user = userEvent.setup();
    render(
      <LoginModal
        isOpen={true}
        onClose={mockOnClose}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );

    // Initially in login mode
    expect(screen.getByRole('button', { name: /sign in/i })).toBeInTheDocument();
    expect(screen.getByText(/don't have an account/i)).toBeInTheDocument();

    // Find the toggle button - text is "Don't have an account? Sign Up"
    const toggleButton = screen.getByText(/don't have an account/i);
    await user.click(toggleButton);
    
    // After toggle, should show "Sign Up" button and toggle button text changes
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
      // The main submit button should be "Sign Up", not "Sign In"
      const submitButtons = screen.getAllByRole('button');
      const signInSubmitButton = submitButtons.find(btn => 
        btn.textContent === 'Sign In' && btn.type === 'submit'
      );
      expect(signInSubmitButton).toBeUndefined();
      // Toggle button is still visible but with different text - this is expected behavior
      // The button switches between "Don't have an account? Sign Up" and "Already have an account? Sign In"
      expect(screen.getByText(/already have an account/i)).toBeInTheDocument();
    });
  });

  it('should call register and then login when in register mode', async () => {
    const user = userEvent.setup();
    authService.register.mockResolvedValue({});
    authService.login.mockResolvedValue({
      token: 'test-token',
      user: { id: 1, username: 'newuser' },
    });

    render(
      <LoginModal
        isOpen={true}
        onClose={mockOnClose}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );

    // Switch to register mode
    const toggleButton = screen.getByText(/don't have an account/i);
    await user.click(toggleButton);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /sign up/i })).toBeInTheDocument();
    });

    const usernameInput = screen.getByPlaceholderText(/enter username/i);
    const passwordInput = screen.getByPlaceholderText(/••••••••/);
    const submitButton = screen.getByRole('button', { name: /sign up/i });

    await user.type(usernameInput, 'newuser');
    await user.type(passwordInput, 'newpass123');
    await user.click(submitButton);

    await waitFor(() => {
      expect(authService.register).toHaveBeenCalledWith('newuser', 'newpass123');
      expect(authService.login).toHaveBeenCalledWith('newuser', 'newpass123');
      expect(mockOnLoginSuccess).toHaveBeenCalled();
    });
  });

  it('should close modal when close button is clicked', async () => {
    const user = userEvent.setup();
    render(
      <LoginModal
        isOpen={true}
        onClose={mockOnClose}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );

    // LoginModal closes when clicking overlay (modal-overlay has onClick={onClose})
    const overlay = document.querySelector('.modal-overlay');
    expect(overlay).toBeInTheDocument();
    
    // Click on overlay (but not on the modal itself)
    await user.click(overlay);
    
    expect(mockOnClose).toHaveBeenCalled();
  });

  it('should clear form on successful login', async () => {
    const user = userEvent.setup();
    authService.login.mockResolvedValue({
      token: 'test-token',
      user: { id: 1, username: 'testuser' },
    });

    render(
      <LoginModal
        isOpen={true}
        onClose={mockOnClose}
        onLoginSuccess={mockOnLoginSuccess}
      />
    );

    const usernameInput = screen.getByPlaceholderText(/enter username/i);
    const passwordInput = screen.getByPlaceholderText(/••••••••/);
    const submitButton = screen.getByRole('button', { name: /sign in/i });

    await user.type(usernameInput, 'testuser');
    await user.type(passwordInput, 'testpass123');
    await user.click(submitButton);

    await waitFor(() => {
      expect(mockOnLoginSuccess).toHaveBeenCalled();
    });

    // Form should be cleared
    expect(usernameInput.value).toBe('');
    expect(passwordInput.value).toBe('');
  });
});

