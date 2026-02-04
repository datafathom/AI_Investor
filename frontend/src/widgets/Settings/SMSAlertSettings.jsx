/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Settings/SMSAlertSettings.jsx
 * ROLE: Notification Settings
 * PURPOSE: Configure high-priority SMS alerts.
 * ==============================================================================
 */

import React, { useState } from 'react';
import useSMSStore from '../../stores/smsStore';
import './SMSAlertSettings.css';

const SMSAlertSettings = ({ mock = true }) => {
    const { 
        sendTestAlert, 
        updatePreferences, 
        preferences, 
        sending, 
        lastResult, 
        error 
    } = useSMSStore();
    
    const [phoneNumber, setPhoneNumber] = useState('');

    const handleTest = async () => {
        if (!phoneNumber) return;
        await sendTestAlert(phoneNumber, mock);
    };

    const toggleAlert = (key) => {
        const newPrefs = { ...preferences, [key]: !preferences[key] };
        updatePreferences(phoneNumber, newPrefs, mock);
    };

    return (
        <div className="sms-settings-widget">
            <header className="widget-header">
                <h3>SMS Notifications</h3>
                <span className="provider-tag">Twilio</span>
            </header>

            <div className="settings-body">
                <div className="input-group">
                    <label>Phone Number</label>
                    <input 
                        type="tel" 
                        placeholder="+1 (555) 000-0000" 
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                    />
                </div>

                <div className="toggles-list">
                    <h4>Alert Triggers</h4>
                    {Object.entries(preferences).map(([key, enabled]) => (
                        <div key={key} className="toggle-row">
                            <span>{key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}</span>
                            <label className="switch">
                                <input 
                                    type="checkbox" 
                                    checked={enabled} 
                                    onChange={() => toggleAlert(key)} 
                                />
                                <span className="slider round"></span>
                            </label>
                        </div>
                    ))}
                </div>

                <button 
                    className="test-btn" 
                    onClick={handleTest} 
                    disabled={sending || !phoneNumber}
                >
                    {sending ? 'Sending...' : 'Send Test Alert'}
                </button>

                {lastResult && (
                    <div className="status-msg success">
                        ✓ Sent! SID: {lastResult.sid?.substring(0, 8)}...
                    </div>
                )}
                {error && <div className="status-msg error">Error: {error}</div>}
            </div>

            <div className="footer">
                <span>Phase 20 {mock && '(Mock)'}</span>
            </div>
        </div>
    );
};

export default SMSAlertSettings;
