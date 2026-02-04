import React, { useState } from 'react';
import { Smartphone, Fingerprint, Bell, Vibrate, Shield } from 'lucide-react';
import './MobileActions.css';

/**
 * Mobile Quick Actions Widget 
 * 
 * Biometric kill switch and push notification trade authorization.
 */
const MobileActions = () => {
    const [biometricEnabled, setBiometricEnabled] = useState(true);
    const [pushAuth, setPushAuth] = useState(true);
    const [hapticFeedback, setHapticFeedback] = useState(true);

    const recentAuths = [
        { action: 'Kill Switch Activated', method: 'FaceID', time: '2 min ago', status: 'approved' },
        { action: 'Buy NVDA 100 shares', method: 'Fingerprint', time: '15 min ago', status: 'approved' },
        { action: 'Withdraw $50,000', method: 'FaceID + PIN', time: '1 hour ago', status: 'denied' },
    ];

    return (
        <div className="mobile-actions">
            <div className="widget-header">
                <Smartphone size={16} />
                <h3>Mobile Security</h3>
            </div>

            <div className="settings-list">
                <div className="setting-row" onClick={() => setBiometricEnabled(!biometricEnabled)}>
                    <div className="setting-icon">
                        <Fingerprint size={18} />
                    </div>
                    <div className="setting-info">
                        <span className="setting-name">Biometric Kill Switch</span>
                        <span className="setting-desc">FaceID / Fingerprint required</span>
                    </div>
                    <div className={`toggle ${biometricEnabled ? 'on' : ''}`}>
                        <div className="toggle-knob"></div>
                    </div>
                </div>

                <div className="setting-row" onClick={() => setPushAuth(!pushAuth)}>
                    <div className="setting-icon">
                        <Bell size={18} />
                    </div>
                    <div className="setting-info">
                        <span className="setting-name">Push Trade Authorization</span>
                        <span className="setting-desc">Approve trades via notification</span>
                    </div>
                    <div className={`toggle ${pushAuth ? 'on' : ''}`}>
                        <div className="toggle-knob"></div>
                    </div>
                </div>

                <div className="setting-row" onClick={() => setHapticFeedback(!hapticFeedback)}>
                    <div className="setting-icon">
                        <Vibrate size={18} />
                    </div>
                    <div className="setting-info">
                        <span className="setting-name">Haptic Alerts</span>
                        <span className="setting-desc">Vibration patterns for alerts</span>
                    </div>
                    <div className={`toggle ${hapticFeedback ? 'on' : ''}`}>
                        <div className="toggle-knob"></div>
                    </div>
                </div>
            </div>

            <div className="auth-history">
                <h4><Shield size={12} /> Recent Authorizations</h4>
                {recentAuths.map((auth, i) => (
                    <div key={i} className={`auth-row ${auth.status}`}>
                        <div className="auth-info">
                            <span className="auth-action">{auth.action}</span>
                            <span className="auth-method">{auth.method}</span>
                        </div>
                        <div className="auth-meta">
                            <span className="auth-time">{auth.time}</span>
                            <span className={`auth-status ${auth.status}`}>{auth.status}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default MobileActions;
