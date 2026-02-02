/**
 * ==============================================================================
 * FILE: frontend2/src/components/Brokerage/RobinhoodConnect.jsx
 * ROLE: Robinhood Connection Component
 * PURPOSE: Secure modal for entering Robinhood credentials and connecting
 *          account for portfolio aggregation.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/robinhood/connect: Connection endpoint
 *     - /api/v1/robinhood/holdings: Holdings retrieval
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import './RobinhoodConnect.css';

const API_BASE = '/robinhood';

const RobinhoodConnect = ({ isOpen, onClose, onSuccess, onError }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [mfaCode, setMfaCode] = useState('');
    const [requiresMFA, setRequiresMFA] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const response = await apiClient.post(`${API_BASE}/connect`, {
                username,
                password,
                mfa_code: mfaCode || undefined
            });

            const data = response.data;

            if (onSuccess) {
                onSuccess(data);
            }

            // Close modal
            if (onClose) {
                onClose();
            }

            // Reset form
            setUsername('');
            setPassword('');
            setMfaCode('');
            setRequiresMFA(false);

        } catch (err) {
            console.error('Robinhood connection failed:', err);
            setError(err.message);
            if (onError) {
                onError(err);
            }
        } finally {
            setLoading(false);
        }
    };

    const handleClose = () => {
        setUsername('');
        setPassword('');
        setMfaCode('');
        setRequiresMFA(false);
        setError(null);
        if (onClose) {
            onClose();
        }
    };

    if (!isOpen) return null;

    return (
        <div className="robinhood-connect-overlay" onClick={handleClose}>
            <div className="robinhood-connect-modal" onClick={(e) => e.stopPropagation()}>
                <div className="robinhood-connect__header">
                    <h3>🔗 Connect Robinhood Account</h3>
                    <button className="robinhood-connect__close" onClick={handleClose}>
                        ✕
                    </button>
                </div>

                <form onSubmit={handleSubmit} className="robinhood-connect__form">
                    <div className="robinhood-connect__info">
                        <p>Connect your Robinhood account to sync portfolio data.</p>
                        <p className="robinhood-connect__note">
                            ⚠️ Credentials are encrypted and stored securely. Read-only access only.
                        </p>
                    </div>

                    {error && (
                        <div className="robinhood-connect__error">
                            {error}
                        </div>
                    )}

                    <div className="robinhood-connect__field">
                        <label htmlFor="username">Username</label>
                        <input
                            id="username"
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter Robinhood username"
                            required
                            disabled={loading}
                        />
                    </div>

                    <div className="robinhood-connect__field">
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter Robinhood password"
                            required
                            disabled={loading}
                        />
                    </div>

                    {requiresMFA && (
                        <div className="robinhood-connect__field">
                            <label htmlFor="mfa">MFA Code</label>
                            <input
                                id="mfa"
                                type="text"
                                value={mfaCode}
                                onChange={(e) => setMfaCode(e.target.value)}
                                placeholder="Enter 6-digit MFA code"
                                maxLength={6}
                                disabled={loading}
                            />
                            <p className="robinhood-connect__mfa-hint">
                                Check your authenticator app for the code
                            </p>
                        </div>
                    )}

                    <div className="robinhood-connect__actions">
                        <button
                            type="button"
                            className="robinhood-connect__cancel"
                            onClick={handleClose}
                            disabled={loading}
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className="robinhood-connect__submit"
                            disabled={loading}
                        >
                            {loading ? 'Connecting...' : 'Connect'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default RobinhoodConnect;
