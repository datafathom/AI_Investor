import React, { useState, useEffect } from 'react';
import { Bell, BellOff, MessageSquare, AlertTriangle, TrendingUp, Moon } from 'lucide-react';
import './AlertSettings.css';

/**
 * Alert Settings Panel
 * 
 * Toggle notification categories and manage alert preferences.
 * Persists to localStorage.
 */
const AlertSettings = () => {
    const [settings, setSettings] = useState(() => {
        const saved = localStorage.getItem('alertSettings');
        return saved ? JSON.parse(saved) : {
            socialMentions: true,
            riskAlerts: true,
            whaleFlow: true,
            dnd: false
        };
    });

    useEffect(() => {
        localStorage.setItem('alertSettings', JSON.stringify(settings));
    }, [settings]);

    const toggleSetting = (key) => {
        setSettings(prev => ({ ...prev, [key]: !prev[key] }));
    };

    const categories = [
        { key: 'socialMentions', label: 'Social Mentions', icon: MessageSquare, description: 'Reddit, Twitter, StockTwits' },
        { key: 'riskAlerts', label: 'Risk Alerts', icon: AlertTriangle, description: 'Position limits, margin calls' },
        { key: 'whaleFlow', label: 'Whale Flow', icon: TrendingUp, description: 'Institutional sweeps' },
    ];

    return (
        <div className="alert-settings">
            <div className="settings-header">
                <Bell size={16} />
                <h3>Alert Preferences</h3>
            </div>

            <div className="dnd-toggle" onClick={() => toggleSetting('dnd')}>
                <div className="dnd-info">
                    <Moon size={16} />
                    <div>
                        <span className="dnd-label">Do Not Disturb</span>
                        <span className="dnd-desc">Pause all notifications</span>
                    </div>
                </div>
                <div className={`toggle-switch ${settings.dnd ? 'active' : ''}`}>
                    <div className="toggle-knob"></div>
                </div>
            </div>

            <div className="categories-list">
                {categories.map(cat => (
                    <div 
                        key={cat.key} 
                        className={`category-item ${settings.dnd ? 'disabled' : ''}`}
                        onClick={() => !settings.dnd && toggleSetting(cat.key)}
                    >
                        <div className="category-icon">
                            <cat.icon size={16} />
                        </div>
                        <div className="category-info">
                            <span className="category-label">{cat.label}</span>
                            <span className="category-desc">{cat.description}</span>
                        </div>
                        <div className={`toggle-switch ${settings[cat.key] && !settings.dnd ? 'active' : ''}`}>
                            <div className="toggle-knob"></div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="settings-footer">
                {settings.dnd ? (
                    <span className="dnd-active"><BellOff size={12} /> Notifications paused</span>
                ) : (
                    <span>{Object.values(settings).filter(v => v === true).length - 1} categories enabled</span>
                )}
            </div>
        </div>
    );
};

export default AlertSettings;
