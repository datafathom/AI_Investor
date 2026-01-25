/**
 * ==============================================================================
 * FILE: frontend2/src/components/Auth/FacebookLoginButton.jsx
 * ROLE: Facebook OAuth Login Button
 * PURPOSE: Facebook-branded login button following official branding guidelines.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/auth/facebook/login: OAuth initiation endpoint
 *     - /api/v1/auth/facebook/callback: OAuth callback handler
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState } from 'react';
import './FacebookLoginButton.css';

/**
 * FacebookLoginButton Component
 */
const FacebookLoginButton = ({ 
    onSuccess, 
    onError,
    scopes = [],
    text = "Continue with Facebook",
    size = "standard" // standard, large
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
            
            const response = await fetch(`/api/v1/auth/facebook/login?${params.toString()}`);
            
            if (!response.ok) {
                throw new Error('Failed to initiate Facebook login');
            }
            
            const data = await response.json();
            
            // Redirect to Facebook OAuth page
            window.location.href = data.authorization_url;
            
        } catch (error) {
            console.error('Facebook login failed:', error);
            if (onError) {
                onError(error);
            }
            setLoading(false);
        }
    };

    return (
        <button
            className={`facebook-login-btn facebook-login-btn--${size}`}
            onClick={handleClick}
            disabled={loading}
            type="button"
        >
            {loading ? (
                <span className="facebook-login-btn__spinner">⏳</span>
            ) : (
                <>
                    <svg
                        className="facebook-login-btn__icon"
                        width="20"
                        height="20"
                        viewBox="0 0 20 20"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            d="M20 10C20 4.477 15.523 0 10 0S0 4.477 0 10c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V10h2.54V7.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V10h2.773l-.443 2.89h-2.33v6.988C16.343 19.128 20 14.991 20 10z"
                            fill="#1877F2"
                        />
                    </svg>
                    <span className="facebook-login-btn__text">{text}</span>
                </>
            )}
        </button>
    );
};

export default FacebookLoginButton;
