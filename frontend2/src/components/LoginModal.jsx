import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';
import { authService } from '../utils/authService';
import SocialLoginButtons from './Auth/SocialLoginButtons';
import './LoginModal.css';

const LoginModal = ({ isOpen, onClose, onLoginSuccess }) => {
    const [isRegister, setIsRegister] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        try {
            if (isRegister) {
                await authService.register(email, password);
                await authService.login(email, password);
            } else {
                await authService.login(email, password);
            }
            if (onLoginSuccess) onLoginSuccess();
            if (onClose) onClose();
        } catch (err) {
            setError(err.message || 'Authentication failed');
        } finally {
            setLoading(false);
        }
    };

    const handleSocialSuccess = (data) => {
        authService.setSession(data.token, data.user);
        if (onLoginSuccess) onLoginSuccess();
        if (onClose) onClose();
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay" onClick={onClose}>
            <div className={`auth-modal ${isRegister ? 'mode-register' : 'mode-login'}`} onClick={(e) => e.stopPropagation()}>
                <div className="modal-header">
                    <h2>{isRegister ? 'Create Account' : 'Welcome Back'}</h2>
                    <p className="subtitle">
                        {isRegister ? 'Join the AI Investor community' : 'Login to access your dashboard'}
                    </p>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <label>Email Address</label>
                        <input
                            type="text"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Enter your email or username"
                            required
                        />
                    </div>
                    <div className="input-group">
                        <label>Password</label>
                        <div className="password-field">
                            <input
                                type={showPassword ? 'text' : 'password'}
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                placeholder="••••••••"
                                required
                            />
                            <button 
                                type="button" 
                                className="password-toggle"
                                onClick={() => setShowPassword(!showPassword)}
                                tabIndex="-1"
                            >
                                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                            </button>
                        </div>
                    </div>

                    {error && <div className="auth-error">{error}</div>}

                    <button type="submit" className="auth-button" disabled={loading}>
                        {loading ? 'Processing...' : (isRegister ? 'Sign Up' : 'Login')}
                    </button>
                </form>

                <SocialLoginButtons onAuthSuccess={handleSocialSuccess} />

                <div className="modal-footer">
                    <button onClick={() => setIsRegister(!isRegister)} className="switch-auth">
                        {isRegister ? 'Already have an account? Login' : "Don't have an account? Sign Up"}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default LoginModal;
