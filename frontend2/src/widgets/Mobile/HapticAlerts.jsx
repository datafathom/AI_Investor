import React, { useState } from 'react';
import { Bell, Volume2, Smartphone } from 'lucide-react';
import './HapticAlerts.css';

const HapticAlerts = () => {
    const [lastPattern, setLastPattern] = useState(null);

    const testVibration = (pattern, name) => {
        setLastPattern(name);
        // Simulator visual feedback only
        if (navigator.vibrate) {
            // Real vibration if supported (rare on desktop)
            navigator.vibrate(pattern);
        }
        
        // Reset after animation
        setTimeout(() => setLastPattern(null), 1000);
    };

    return (
        <div className="haptic-alerts-widget mobile-sim">
             <div className="status-bar">
                <span>9:43</span>
                <span>5G</span>
            </div>

            <div className="app-content">
                <div className="settings-header">
                    <h2>Alert Settings</h2>
                </div>

                <div className="settings-group">
                    <h3>Vibration Patterns</h3>
                    
                    <div className="setting-item" onClick={() => testVibration([200], 'info')}>
                        <div className="icon-box info"><Bell size={20} /></div>
                        <div className="setting-label">
                            <span>Info Alert</span>
                            <span className="sub">Single Pulse</span>
                        </div>
                        <button className="test-btn">Test</button>
                    </div>

                    <div className="setting-item" onClick={() => testVibration([200, 100, 200], 'warning')}>
                        <div className="icon-box warning"><AlertTriangle size={20} /></div>
                        <div className="setting-label">
                            <span>Warning</span>
                            <span className="sub">Double Pulse</span>
                        </div>
                        <button className="test-btn">Test</button>
                    </div>

                    <div className="setting-item" onClick={() => testVibration([1000], 'critical')}>
                        <div className="icon-box critical"><Smartphone size={20} /></div>
                        <div className="setting-label">
                            <span>Critical</span>
                            <span className="sub">Long Vibration</span>
                        </div>
                        <button className="test-btn">Test</button>
                    </div>
                </div>

                <div className="vibration-visualizer">
                    <div className={`phone-mock ${lastPattern === 'info' ? 'shake-sm' : lastPattern === 'warning' ? 'shake-md' : lastPattern === 'critical' ? 'shake-lg' : ''}`}>
                         <Smartphone size={80} color="#333" />
                         {lastPattern && <span className="vibe-text">VIBRATING: {lastPattern.toUpperCase()}</span>}
                    </div>
                </div>
            </div>
        </div>
    );
};

// Start Lucide Icon import fix
import { AlertTriangle } from 'lucide-react';

export default HapticAlerts;
