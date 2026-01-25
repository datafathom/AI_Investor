/**
 * ==============================================================================
 * FILE: frontend2/src/components/Auth/GoogleLoginButton.jsx
 * ROLE: Google OAuth Login Button
 * PURPOSE: Google-branded login button following official branding guidelines.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/auth/google/login: OAuth initiation endpoint
 *     - /api/v1/auth/google/callback: OAuth callback handler
 *     
 * BRANDING:
 *     - Follows Google Sign-In Branding Guidelines
 *     - Uses official Google colors and styling
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState } from 'react';
import './GoogleLoginButton.css';

/**
 * GoogleLoginButton Component
 */
const GoogleLoginButton = ({ 
    onSuccess, 
    onError,
    scopes = [],
    text = "Sign in with Google",
    size = "standard" // standard, large, icon
}) => {
    const [loading, setLoading] = useState(false);

    const handleClick = async () => {
        setLoading(true);
        
        try {
            // Get authorization URL
            const params = new URLSearchParams();
            if (scopes.length > 0) {
                params.set('scopes', scopes.join(','));
            }
            
            const response = await fetch(`/api/v1/auth/google/login?${params.toString()}`);
            
            if (!response.ok) {
                throw new Error('Failed to initiate Google login');
            }
            
            const data = await response.json();
            
            // Redirect to Google OAuth page
            window.location.href = data.authorization_url;
            
        } catch (error) {
            console.error('Google login failed:', error);
            if (onError) {
                onError(error);
            }
            setLoading(false);
        }
    };

    return (
        <button
            className={`google-login-btn google-login-btn--${size}`}
            onClick={handleClick}
            disabled={loading}
            type="button"
        >
            {loading ? (
                <span className="google-login-btn__spinner">⏳</span>
            ) : (
                <>
                    <svg
                        className="google-login-btn__icon"
                        width="18"
                        height="18"
                        viewBox="0 0 18 18"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <g fill="#000" fillRule="evenodd">
                            <path
                                d="M9 3.48c1.69 0 2.83.73 3.48 1.34l2.54-2.48C13.46.89 11.43 0 9 0 5.48 0 2.44 2.02.96 4.96l2.91 2.26C4.6 5.05 6.62 3.48 9 3.48z"
                                fill="#EA4335"
                            />
                            <path
                                d="M17.64 9.2c0-.74-.06-1.28-.19-1.84H9v3.34h4.96c-.21 1.18-.84 2.18-1.79 2.85l2.91 2.26c2.27-2.09 3.56-5.17 3.56-8.61z"
                                fill="#4285F4"
                            />
                            <path
                                d="M3.88 10.78A5.54 5.54 0 0 1 3.58 9c0-.62.11-1.22.29-1.78L.96 4.96A9.008 9.008 0 0 0 0 9c0 1.45.35 2.82.96 4.04l2.92-2.26z"
                                fill="#FBBC05"
                            />
                            <path
                                d="M9 18c2.43 0 4.47-.8 5.96-2.18l-2.91-2.26c-.76.53-1.78.9-3.05.9-2.34 0-4.32-1.58-5.04-3.74L.96 13.04C2.45 15.98 5.48 18 9 18z"
                                fill="#34A853"
                            />
                        </g>
                    </svg>
                    <span className="google-login-btn__text">{text}</span>
                </>
            )}
        </button>
    );
};

export default GoogleLoginButton;
