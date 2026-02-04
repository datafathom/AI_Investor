
import React, { useState, useRef, useEffect } from 'react';
import { motion, useAnimation } from 'framer-motion';
import { Power, AlertOctagon } from 'lucide-react';
import './KillSwitch.css';

const KillSwitch = ({ onTrigger }) => {
    const [isPressed, setIsPressed] = useState(false);
    const [progress, setProgress] = useState(0);
    const pressTimer = useRef(null);
    const controls = useAnimation();

    const LONG_PRESS_DURATION = 3000; // 3 seconds

    useEffect(() => {
        let interval;
        if (isPressed) {
            const startTime = Date.now();
            interval = setInterval(() => {
                const elapsed = Date.now() - startTime;
                const p = Math.min((elapsed / LONG_PRESS_DURATION) * 100, 100);
                setProgress(p);

                if (p >= 100) {
                    clearInterval(interval);
                    triggerKill();
                }
            }, 16);
        } else {
            setProgress(0);
        }

        return () => clearInterval(interval);
    }, [isPressed]);

    const triggerKill = () => {
        setIsPressed(false);
        setProgress(0);
        
        // Haptic feedback if available (Vibration API)
        if (navigator.vibrate) navigator.vibrate([200, 100, 200, 100, 500]);
        
        onTrigger();
    };

    const handlePointerDown = () => {
        setIsPressed(true);
        controls.start({ scale: 0.9 });
    };

    const handlePointerUp = () => {
        setIsPressed(false);
        controls.start({ scale: 1 });
    };

    return (
        <div className="kill-switch-container">
            <motion.div 
                className={`kill-switch-button ${progress > 0 ? 'active' : ''}`}
                onPointerDown={handlePointerDown}
                onPointerUp={handlePointerUp}
                onPointerLeave={handlePointerUp}
                animate={controls}
                whileHover={{ scale: 1.05 }}
            >
                <div className="ks-icon-wrapper">
                    {progress >= 100 ? <AlertOctagon size={28} /> : <Power size={28} />}
                </div>
                
                {/* Visual Progress Ring */}
                <svg className="ks-progress-ring" viewBox="0 0 100 100">
                    <circle 
                        className="ks-ring-bg" 
                        cx="50" cy="50" r="45" 
                    />
                    <circle 
                        className="ks-ring-progress" 
                        cx="50" cy="50" r="45" 
                        strokeDasharray="283"
                        strokeDashoffset={283 - (283 * progress) / 100}
                    />
                </svg>

                {/* Pulse Effect when active */}
                {isPressed && (
                    <div className="ks-pulse-ring"></div>
                )}
            </motion.div>
            
            {isPressed && (
                <div className="ks-warning-tooltip">
                    HOLD TO KILL ({Math.ceil((3000 - (progress/100)*3000)/1000)}s)
                </div>
            )}
        </div>
    );
};

export default KillSwitch;
