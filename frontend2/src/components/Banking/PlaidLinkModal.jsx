/**
 * ==============================================================================
 * FILE: frontend2/src/components/Banking/PlaidLinkModal.jsx
 * ROLE: Plaid Link Modal Component
 * PURPOSE: Initializes Plaid Link for bank account connection. Handles
 *          success, error, and abort callbacks.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/plaid/link-token: Get link token
 *     - /api/v1/plaid/exchange-token: Exchange public token
 *     - Plaid Link SDK: Frontend Plaid integration
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect, useState, useRef } from 'react';
import './PlaidLinkModal.css';

const API_BASE = '/api/v1/plaid';

const PlaidLinkModal = ({ isOpen, onClose, onSuccess, onError }) => {
    const [linkToken, setLinkToken] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const plaidRef = useRef(null);

    useEffect(() => {
        if (isOpen && !linkToken) {
            createLinkToken();
        }
    }, [isOpen]);

    useEffect(() => {
        if (linkToken && isOpen && window.Plaid) {
            initializePlaidLink();
        }
    }, [linkToken, isOpen]);

    const createLinkToken = async () => {
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch(`${API_BASE}/link-token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    client_name: 'AI Investor'
                })
            });

            if (!response.ok) {
                throw new Error('Failed to create link token');
            }

            const data = await response.json();
            setLinkToken(data.link_token);
        } catch (err) {
            console.error('Failed to create link token:', err);
            setError('Failed to initialize bank connection. Please try again.');
            if (onError) {
                onError(err);
            }
        } finally {
            setLoading(false);
        }
    };

    const initializePlaidLink = () => {
        if (!window.Plaid || !linkToken) return;

        // Destroy existing instance if any
        if (plaidRef.current) {
            plaidRef.current.destroy();
        }

        // Get environment from config (sandbox/development/production)
        const environment = process.env.REACT_APP_PLAID_ENV || 'sandbox';

        plaidRef.current = window.Plaid.create({
            token: linkToken,
            env: environment,
            onSuccess: handlePlaidSuccess,
            onExit: handlePlaidExit,
            onEvent: handlePlaidEvent
        });

        // Open Plaid Link
        plaidRef.current.open();
    };

    const handlePlaidSuccess = async (publicToken, metadata) => {
        try {
            // Exchange public token for access token
            const response = await fetch(`${API_BASE}/exchange-token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    public_token: publicToken
                })
            });

            if (!response.ok) {
                throw new Error('Failed to exchange token');
            }

            const data = await response.json();

            if (onSuccess) {
                onSuccess({
                    public_token: publicToken,
                    accounts: data.accounts,
                    item_id: data.item_id,
                    metadata: metadata
                });
            }

            // Close modal
            if (onClose) {
                onClose();
            }
        } catch (err) {
            console.error('Failed to exchange token:', err);
            setError('Failed to complete bank connection. Please try again.');
            if (onError) {
                onError(err);
            }
        }
    };

    const handlePlaidExit = (err, metadata) => {
        if (err) {
            console.error('Plaid Link error:', err);
            setError(err.error_message || 'Bank connection was cancelled.');
            if (onError) {
                onError(err);
            }
        } else {
            // User closed without error
            if (onClose) {
                onClose();
            }
        }
    };

    const handlePlaidEvent = (eventName, metadata) => {
        console.log('Plaid event:', eventName, metadata);
        // Handle events like SUBMIT_CREDENTIALS, SELECT_INSTITUTION, etc.
    };

    const handleClose = () => {
        if (plaidRef.current) {
            plaidRef.current.destroy();
            plaidRef.current = null;
        }
        setLinkToken(null);
        setError(null);
        if (onClose) {
            onClose();
        }
    };

    if (!isOpen) return null;

    return (
        <div className="plaid-link-modal-overlay" onClick={handleClose}>
            <div className="plaid-link-modal" onClick={(e) => e.stopPropagation()}>
                <div className="plaid-link-modal__header">
                    <h3>🔗 Connect Bank Account</h3>
                    <button className="plaid-link-modal__close" onClick={handleClose}>
                        ✕
                    </button>
                </div>

                <div className="plaid-link-modal__content">
                    {loading && (
                        <div className="plaid-link-modal__loading">
                            <div className="spinner"></div>
                            <p>Initializing secure connection...</p>
                        </div>
                    )}

                    {error && (
                        <div className="plaid-link-modal__error">
                            <p>⚠️ {error}</p>
                            <button onClick={createLinkToken} className="retry-btn">
                                Try Again
                            </button>
                        </div>
                    )}

                    {linkToken && !error && (
                        <div className="plaid-link-modal__info">
                            <p>You will be redirected to Plaid to securely connect your bank account.</p>
                            <p className="plaid-link-modal__note">
                                Your credentials are never shared with us. Plaid uses bank-level encryption.
                            </p>
                        </div>
                    )}

                    {/* Plaid Link will render here */}
                    <div id="plaid-link-container"></div>
                </div>
            </div>
        </div>
    );
};

export default PlaidLinkModal;
