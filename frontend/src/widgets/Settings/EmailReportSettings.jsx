/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Settings/EmailReportSettings.jsx
 * ROLE: Notification Settings
 * PURPOSE: Configure email subscriptions and reports.
 * ==============================================================================
 */

import React, { useState } from 'react';
import useEmailStore from '../../stores/emailStore';
import './EmailReportSettings.css';

const EmailReportSettings = ({ mock = true }) => {
    const { sendTestEmail, updatePreferences, preferences, sending, lastResult, error } = useEmailStore();
    const [email, setEmail] = useState('');
    
    const handleTest = async () => {
        if (!email) return;
        await sendTestEmail(email, mock);
    };

    const togglePref = (key) => {
        const newPrefs = { ...preferences, [key]: !preferences[key] };
        updatePreferences(email, newPrefs, mock);
    };

    return (
        <div className="email-settings-widget">
            <header className="widget-header">
                <h3>Email Reports</h3>
                <span className="provider-tag">SendGrid</span>
            </header>

            <div className="settings-body">
                <div className="input-group">
                    <label>Recipient Email</label>
                    <input 
                        type="email" 
                        placeholder="user@example.com" 
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                </div>

                <div className="toggles-list">
                    <h4>Subscriptions</h4>
                    {Object.entries(preferences).map(([key, enabled]) => (
                        <div key={key} className="toggle-row">
                            <span>{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</span>
                            <label className="switch">
                                <input 
                                    type="checkbox" 
                                    checked={enabled} 
                                    onChange={() => togglePref(key)} 
                                />
                                <span className="slider round"></span>
                            </label>
                        </div>
                    ))}
                </div>

                <button 
                    className="test-btn" 
                    onClick={handleTest} 
                    disabled={sending || !email}
                >
                    {sending ? 'Sending...' : 'Send Test Email'}
                </button>

                {lastResult && (
                    <div className="status-msg success">
                        ✓ Sent! ID: {lastResult.id?.substring(0, 8)}...
                    </div>
                )}
                {error && <div className="status-msg error">Error: {error}</div>}
            </div>

            <div className="footer">
                <span> {mock && '(Mock)'}</span>
            </div>
        </div>
    );
};

export default EmailReportSettings;
