import React, { useState, useEffect, useRef } from 'react';
import { Skull, AlertOctagon } from 'lucide-react';
import useTaskbarStore from '../../stores/taskbarStore';
import './KillSwitch.css';

const KillSwitch = () => {
    const { 
        killSwitchState, 
        startArming, 
        cancelArming, 
        triggerKillSwitch,
        resetKillSwitch,
        setKillMFAOpen
    } = useTaskbarStore();

    const [progress, setProgress] = useState(0);
    const pressTimer = useRef(null);
    const PRESS_DURATION = 3000; // 3 seconds

    const handleMouseDown = () => {
        if (killSwitchState === 'active') {
            resetKillSwitch();
            return;
        }
        startArming();
        let startTime = Date.now();
        
        pressTimer.current = setInterval(() => {
            const elapsed = Date.now() - startTime;
            const newProgress = Math.min((elapsed / PRESS_DURATION) * 100, 100);
            setProgress(newProgress);

            if (elapsed >= PRESS_DURATION) {
                clearInterval(pressTimer.current);
                setKillMFAOpen(true);
                // The triggerKillSwitch logic will be moved to the MFA success handler in App.jsx
                console.log("MFA Requested for Kill Switch");
            }
        }, 50);
    };

    const handleMouseUp = () => {
        if (killSwitchState === 'active') return;
        clearInterval(pressTimer.current);
        cancelArming();
        setProgress(0);
    };

    return (
        <div 
            className={`kill-switch-container ${killSwitchState}`}
            onMouseDown={handleMouseDown}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
        >
            <div className="kill-ring" style={{ width: `${progress}%` }} />
            <div className="kill-icon">
                {killSwitchState === 'active' ? (
                    <Skull className="animate-pulse" size={20} color="#fff" />
                ) : (
                    <AlertOctagon size={20} color={progress > 0 ? "#ff4757" : "#57606f"} />
                )}
            </div>
            {killSwitchState === 'active' && <div className="kill-overlay" />}
        </div>
    );
};

export default KillSwitch;
