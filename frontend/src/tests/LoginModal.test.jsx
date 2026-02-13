import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import LoginModal from '../components/LoginModal';
import { authService } from '../utils/authService';

// Mock authService
vi.mock('../utils/authService', () => ({
    authService: {
        login: vi.fn(),
        register: vi.fn(),
        setSession: vi.fn(),
    }
}));

// Mock SocialLoginButtons to isolate unit test
vi.mock('../components/Auth/SocialLoginButtons', () => ({
    default: ({ onAuthSuccess }) => (
        <button onClick={() => onAuthSuccess({ token: 'mock-token', user: { id: '1' } })}>
            Mock Social Login
        </button>
    )
}));

describe('LoginModal Component', () => {
    const mockOnClose = vi.fn();
    const mockOnLoginSuccess = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should not render when isOpen is false', () => {
        const { queryByText } = render(
            <LoginModal isOpen={false} onClose={mockOnClose} />
        );
        expect(queryByText('Welcome Back')).toBeNull();
    });

    it('should render correctly when isOpen is true', () => {
        render(<LoginModal isOpen={true} onClose={mockOnClose} />);
        expect(screen.getByText('Welcome Back')).toBeTruthy();
        expect(screen.getByLabelText(/email address/i)).toBeTruthy();
        expect(screen.getByLabelText(/password/i)).toBeTruthy();
    });

    it('should handle login submission successfully', async () => {
        authService.login.mockResolvedValue({ success: true, token: 'jwt123' });

        const { container } = render(<LoginModal isOpen={true} onClose={mockOnClose} onLoginSuccess={mockOnLoginSuccess} />);

        fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'test@aiinvestor.com' } });
        fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'test_pass_123' } });

        // Submit form directly
        fireEvent.submit(container.querySelector('form'));

        await waitFor(() => {
            expect(authService.login).toHaveBeenCalledWith('test@aiinvestor.com', 'test_pass_123');
            expect(mockOnLoginSuccess).toHaveBeenCalled();
        });
    });

    it('should handle login errors', async () => {
        authService.login.mockRejectedValue(new Error('Invalid credentials'));

        render(<LoginModal isOpen={true} onClose={mockOnClose} />);

        fireEvent.change(screen.getByLabelText(/email address/i), { target: { value: 'fail@example.com' } });
        fireEvent.change(screen.getByLabelText(/password/i), { target: { value: 'wrongpass' } });

        fireEvent.submit(screen.getByLabelText(/email address/i).closest('form'));

        await waitFor(() => {
            expect(screen.getByText('Invalid credentials')).toBeTruthy();
        });
    });

    it('should switch between login and register modes', () => {
        render(<LoginModal isOpen={true} onClose={mockOnClose} />);

        const switchButton = screen.getByText("Don't have an account? Sign Up");
        fireEvent.click(switchButton);

        expect(screen.getByText('Create Account')).toBeTruthy();
    });
});
