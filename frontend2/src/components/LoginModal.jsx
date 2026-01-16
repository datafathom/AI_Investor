import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { authService } from '../utils/authService';
import './LoginModal.css';

const LoginModal = ({ isOpen, onClose, onLoginSuccess }) => {
    const [isRegister, setIsRegister] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        // Get values directly from form inputs as fallback
        const form = e.target;
        const usernameInput = form.querySelector('input[type="text"]');
        const passwordInput = form.querySelector('input[type="password"]');
        const usernameValue = usernameInput?.value || username || '';
        const passwordValue = passwordInput?.value || password || '';
        
        console.log('Form submitted!', { 
            username, 
            password, 
            usernameValue,
            passwordValue,
            usernameLength: usernameValue?.length, 
            passwordLength: passwordValue?.length 
        });
        setError('');

        // Validate inputs - use form values if state is empty
        const trimmedUsername = (usernameValue || username || '').trim();
        const trimmedPassword = (passwordValue || password || '').trim();
        
        if (!trimmedUsername || !trimmedPassword) {
            console.log('Validation failed:', { trimmedUsername, trimmedPassword, username, password });
            setError('Username and password required');
            return;
        }

        // Update state if we got values from form
        if (usernameValue && !username) {
            setUsername(usernameValue);
        }
        if (passwordValue && !password) {
            setPassword(passwordValue);
        }

        console.log('Starting login with:', { trimmedUsername, trimmedPasswordLength: trimmedPassword.length });
        setLoading(true);

        try {
            let result;
            if (isRegister) {
                console.log('Registering user...');
                result = await authService.register(trimmedUsername, trimmedPassword);
                // Auto-login after registration
                result = await authService.login(trimmedUsername, trimmedPassword);
            } else {
                console.log('Logging in user...');
                result = await authService.login(trimmedUsername, trimmedPassword);
            }
            
            console.log('Login successful:', result);
            
            // Clear form
            setUsername('');
            setPassword('');
            setError('');
            
            // Call success handler and close modal
            if (onLoginSuccess) {
                onLoginSuccess();
            }
            if (onClose) {
                onClose();
            }
        } catch (err) {
            console.error('Login error:', err);
            setError(err.message || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (!isOpen) return null;

    return (
        <AnimatePresence>
            <div className="modal-overlay" onClick={onClose}>
                <motion.div
                    className="auth-modal"
                    initial={{ opacity: 0, scale: 0.9, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.9, y: 20 }}
                    onClick={(e) => e.stopPropagation()}
                >
                    <div className="modal-header">
                        <h2>{isRegister ? 'Create Account' : 'Welcome Back'}</h2>
                        <p className="subtitle">
                            {isRegister ? 'Join the Widget OS community' : 'Sign in to access your dashboard'}
                        </p>
                    </div>

                    <form onSubmit={handleSubmit} noValidate>
                        <div className="input-group">
                            <label>Username</label>
                            <input
                                type="text"
                                value={username}
                                onChange={(e) => {
                                    setUsername(e.target.value);
                                    setError(''); // Clear error when typing
                                }}
                                placeholder="Enter username"
                                autoComplete="username"
                            />
                        </div>
                        <div className="input-group">
                            <label>Password</label>
                            <input
                                type="password"
                                value={password}
                                onChange={(e) => {
                                    const val = e.target.value;
                                    console.log('Password changed:', val?.length, 'chars');
                                    setPassword(val);
                                    setError(''); // Clear error when typing
                                }}
                                onInput={(e) => {
                                    const val = e.target.value;
                                    console.log('Password input:', val?.length, 'chars');
                                    setPassword(val);
                                }}
                                placeholder="••••••••"
                                autoComplete="current-password"
                            />
                        </div>

                        {error && <div className="auth-error">{error}</div>}

                        <button type="submit" className="auth-button" disabled={loading}>
                            {loading ? 'Processing...' : (isRegister ? 'Sign Up' : 'Sign In')}
                        </button>
                    </form>

                    <div className="modal-footer">
                        <button onClick={() => setIsRegister(!isRegister)} className="switch-auth">
                            {isRegister ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
                        </button>
                    </div>
                </motion.div>
            </div>
        </AnimatePresence>
    );
};

export default LoginModal;
