/**
 * ==============================================================================
 * FILE: frontend2/src/pages/GoogleAuthCallback.jsx
 * ROLE: Google OAuth Callback Handler Page
 * PURPOSE: Handles Google OAuth callback and processes authentication result.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/auth/google/callback: Backend callback handler
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import './GoogleAuthCallback.css';

const GoogleAuthCallback = () => {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [status, setStatus] = useState('processing');
    const [error, setError] = useState(null);

    useEffect(() => {
        const handleCallback = async () => {
            const code = searchParams.get('code');
            const state = searchParams.get('state');
            const errorParam = searchParams.get('error');

            if (errorParam) {
                setError(`OAuth error: ${errorParam}`);
                setStatus('error');
                return;
            }

            if (!code) {
                setError('Missing authorization code');
                setStatus('error');
                return;
            }

            try {
                // Send code to backend for processing
                const response = await fetch('/api/v1/auth/google/callback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ code, state })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Authentication failed');
                }

                const data = await response.json();

                if (data.success) {
                    // Store session token
                    if (data.session_token) {
                        localStorage.setItem('auth_token', data.session_token);
                    }

                    // Store user info
                    if (data.user) {
                        localStorage.setItem('user', JSON.stringify(data.user));
                    }

                    // Store Google tokens (encrypted in production)
                    if (data.tokens) {
                        localStorage.setItem('google_tokens', JSON.stringify(data.tokens));
                    }

                    setStatus('success');

                    // Redirect to dashboard after short delay
                    setTimeout(() => {
                        navigate('/dashboard');
                    }, 2000);
                } else {
                    throw new Error('Authentication failed');
                }
            } catch (err) {
                console.error('Google OAuth callback error:', err);
                setError(err.message);
                setStatus('error');
            }
        };

        handleCallback();
    }, [searchParams, navigate]);

    return (
        <div className="google-auth-callback">
            <div className="google-auth-callback__container">
                {status === 'processing' && (
                    <>
                        <div className="google-auth-callback__spinner"></div>
                        <h2>Processing authentication...</h2>
                        <p>Please wait while we complete your Google sign-in.</p>
                    </>
                )}

                {status === 'success' && (
                    <>
                        <div className="google-auth-callback__success">✓</div>
                        <h2>Authentication successful!</h2>
                        <p>Redirecting to your dashboard...</p>
                    </>
                )}

                {status === 'error' && (
                    <>
                        <div className="google-auth-callback__error">✕</div>
                        <h2>Authentication failed</h2>
                        <p>{error || 'An error occurred during authentication.'}</p>
                        <button
                            className="google-auth-callback__retry"
                            onClick={() => navigate('/login')}
                        >
                            Return to Login
                        </button>
                    </>
                )}
            </div>
        </div>
    );
};

export default GoogleAuthCallback;
