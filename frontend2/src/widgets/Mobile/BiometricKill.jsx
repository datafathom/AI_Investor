import React, { useState, useEffect } from 'react';
import { Fingerprint, Power, AlertTriangle } from 'lucide-react';
import './BiometricKill.css';

const BiometricKill = () => {
    const [progress, setProgress] = useState(0);
    const [active, setActive] = useState(false);
    const [isPressing, setIsPressing] = useState(false);

    useEffect(() => {
        let interval;
        if (isPressing && !active) {
            interval = setInterval(() => {
                setProgress(prev => {
                    if (prev >= 100) {
                        setActive(true);
                        setIsPressing(false);
                        return 100;
                    }
                    return prev + 2; // Adjust speed
                });
            }, 50);
        } else {
            setProgress(0);
        }
        return () => clearInterval(interval);
    }, [isPressing, active]);

    return (
        <div className="biometric-kill-widget mobile-sim">
            <div className="status-bar">
                <span>9:41</span>
                <span>5G</span>
            </div>
            
            <div className="app-content">
                <div className="kill-header">
                    <AlertTriangle size={48} className="text-red-500" />
                    <h2>Emergency Kill Switch</h2>
                    <p>Long Press to Freeze System</p>
                </div>

                <div 
                    className={`kill-trigger ${active ? 'activated' : ''}`}
                    onMouseDown={() => setIsPressing(true)}
                    onMouseUp={() => setIsPressing(false)}
                    onMouseLeave={() => setIsPressing(false)}
                    onTouchStart={() => setIsPressing(true)}
                    onTouchEnd={() => setIsPressing(false)}
                >
                    <div className="progress-ring" style={{ height: `${progress}%` }}></div>
                    <Fingerprint size={64} className="fingerprint-icon" />
                    <span className="label text-red-100">{active ? 'SYSTEM FROZEN' : 'HOLD TO KILL'}</span>
                </div>

                {active && (
                    <div className="kill-confirmation">
                        <h3>KILL SIGNAL SENT</h3>
                        <p>All trading halted. Check desktop for logs.</p>
                        <button onClick={() => setActive(false)} className="reset-btn">Reset Simulator</button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default BiometricKill;
