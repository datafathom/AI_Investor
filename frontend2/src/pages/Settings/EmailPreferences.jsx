/**
 * ==============================================================================
 * FILE: frontend2/src/pages/Settings/EmailPreferences.jsx
 * ROLE: Email Preferences Settings Page
 * PURPOSE: Allows users to configure email notification preferences, including
 *          which types of emails to receive and their frequency.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/gmail/stats: Gmail sending statistics
 *     - /api/v1/gmail/preview: Template preview
 *     - Email preferences API: Save user preferences
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import './EmailPreferences.css';

const API_BASE = '/api/v1/gmail';

const EMAIL_TYPES = [
    {
        id: 'margin_alert',
        name: 'Margin Alerts',
        description: 'Notifications when margin levels drop below threshold',
        defaultEnabled: true,
        frequency: 'instant'
    },
    {
        id: 'daily_summary',
        name: 'Daily Portfolio Summary',
        description: 'End-of-day portfolio performance summary',
        defaultEnabled: true,
        frequency: 'daily'
    },
    {
        id: 'trade_confirmation',
        name: 'Trade Confirmations',
        description: 'Email confirmation for executed trades',
        defaultEnabled: true,
        frequency: 'instant'
    },
    {
        id: 'earnings_reminder',
        name: 'Earnings Reminders',
        description: 'Reminders for upcoming earnings calls',
        defaultEnabled: true,
        frequency: 'daily'
    },
    {
        id: 'dividend_notification',
        name: 'Dividend Notifications',
        description: 'Notifications when dividends are paid',
        defaultEnabled: true,
        frequency: 'instant'
    },
    {
        id: 'password_reset',
        name: 'Password Reset',
        description: 'Password reset and security notifications',
        defaultEnabled: true,
        frequency: 'instant'
    }
];

const FREQUENCY_OPTIONS = [
    { value: 'instant', label: 'Instant' },
    { value: 'daily', label: 'Daily Digest' },
    { value: 'weekly', label: 'Weekly Digest' },
    { value: 'off', label: 'Off' }
];

const EmailPreferences = () => {
    const [preferences, setPreferences] = useState({});
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [stats, setStats] = useState(null);
    const [testEmailStatus, setTestEmailStatus] = useState(null);

    useEffect(() => {
        loadPreferences();
        loadStats();
    }, []);

    const loadPreferences = async () => {
        // In production, load from API
        // For now, use defaults
        const defaultPrefs = {};
        EMAIL_TYPES.forEach(type => {
            defaultPrefs[type.id] = {
                enabled: type.defaultEnabled,
                frequency: type.frequency
            };
        });
        setPreferences(defaultPrefs);
    };

    const loadStats = async () => {
        try {
            const response = await fetch(`${API_BASE}/stats`);
            if (response.ok) {
                const data = await response.json();
                setStats(data);
            }
        } catch (err) {
            console.error('Failed to load stats:', err);
        }
    };

    const handleToggle = (emailTypeId) => {
        setPreferences(prev => ({
            ...prev,
            [emailTypeId]: {
                ...prev[emailTypeId],
                enabled: !prev[emailTypeId]?.enabled
            }
        }));
    };

    const handleFrequencyChange = (emailTypeId, frequency) => {
        setPreferences(prev => ({
            ...prev,
            [emailTypeId]: {
                ...prev[emailTypeId],
                enabled: frequency !== 'off',
                frequency: frequency
            }
        }));
    };

    const handleSave = async () => {
        setSaving(true);
        try {
            // In production, save to API
            await new Promise(resolve => setTimeout(resolve, 500));
            setTestEmailStatus({ type: 'success', message: 'Preferences saved successfully' });
            setTimeout(() => setTestEmailStatus(null), 3000);
        } catch (err) {
            setTestEmailStatus({ type: 'error', message: 'Failed to save preferences' });
        } finally {
            setSaving(false);
        }
    };

    const handleTestEmail = async (emailTypeId) => {
        setTestEmailStatus({ type: 'sending', message: 'Sending test email...' });
        
        try {
            // Get user's email from profile or use default
            const userEmail = localStorage.getItem('user_email') || 'user@example.com';
            
            const response = await fetch(`${API_BASE}/send-template`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    to: userEmail,
                    template_name: emailTypeId,
                    template_context: {
                        // Mock context for testing
                        portfolio_value: 100000,
                        margin_level: 150,
                        symbol: 'AAPL',
                        price: 150.25,
                        quantity: 10
                    }
                })
            });

            if (response.ok) {
                setTestEmailStatus({ type: 'success', message: 'Test email sent successfully!' });
            } else {
                throw new Error('Failed to send test email');
            }
        } catch (err) {
            console.error('Test email failed:', err);
            setTestEmailStatus({ type: 'error', message: 'Failed to send test email' });
        }
        
        setTimeout(() => setTestEmailStatus(null), 3000);
    };

    return (
        <div className="email-preferences">
            <div className="email-preferences__header">
                <h2>📧 Email Preferences</h2>
                <p>Configure which email notifications you'd like to receive</p>
            </div>

            {/* Statistics */}
            {stats && (
                <div className="email-preferences__stats">
                    <div className="stat-item">
                        <span className="stat-label">Emails Sent Today:</span>
                        <span className="stat-value">{stats.sends_today} / {stats.quota_limit}</span>
                    </div>
                    <div className="stat-item">
                        <span className="stat-label">Remaining:</span>
                        <span className="stat-value">{stats.remaining}</span>
                    </div>
                </div>
            )}

            {/* Status Message */}
            {testEmailStatus && (
                <div className={`email-preferences__status email-preferences__status--${testEmailStatus.type}`}>
                    {testEmailStatus.message}
                </div>
            )}

            {/* Email Type Preferences */}
            <div className="email-preferences__list">
                {EMAIL_TYPES.map(type => {
                    const pref = preferences[type.id] || { enabled: type.defaultEnabled, frequency: type.frequency };
                    
                    return (
                        <div key={type.id} className="email-preference-item">
                            <div className="email-preference-item__header">
                                <div className="email-preference-item__info">
                                    <h3>{type.name}</h3>
                                    <p>{type.description}</p>
                                </div>
                                <label className="toggle-switch">
                                    <input
                                        type="checkbox"
                                        checked={pref.enabled}
                                        onChange={() => handleToggle(type.id)}
                                    />
                                    <span className="toggle-slider"></span>
                                </label>
                            </div>
                            
                            {pref.enabled && (
                                <div className="email-preference-item__controls">
                                    <label className="frequency-label">
                                        Frequency:
                                        <select
                                            value={pref.frequency}
                                            onChange={(e) => handleFrequencyChange(type.id, e.target.value)}
                                            className="frequency-select"
                                        >
                                            {FREQUENCY_OPTIONS.map(opt => (
                                                <option key={opt.value} value={opt.value}>
                                                    {opt.label}
                                                </option>
                                            ))}
                                        </select>
                                    </label>
                                    <button
                                        className="test-email-btn"
                                        onClick={() => handleTestEmail(type.id)}
                                        disabled={testEmailStatus?.type === 'sending'}
                                    >
                                        📤 Send Test Email
                                    </button>
                                </div>
                            )}
                        </div>
                    );
                })}
            </div>

            {/* Save Button */}
            <div className="email-preferences__actions">
                <button
                    className="save-btn"
                    onClick={handleSave}
                    disabled={saving}
                >
                    {saving ? 'Saving...' : '💾 Save Preferences'}
                </button>
            </div>
        </div>
    );
};

export default EmailPreferences;
