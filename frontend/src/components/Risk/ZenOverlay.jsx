import React, { useState, useEffect } from 'react';
import useRiskStore from '../../stores/riskStore';
import './ZenOverlay.css';

/**
 * ZenOverlay - Psychological Safety Interface
 * 
 * Appears when an emotional or risk-based trading lock is active.
 * Provides a countdown timer and a calming visual environment.
 */
const ZenOverlay = () => {
    const { healthStatus, lastSentinelCheck } = useRiskStore();
    const [isVisible, setIsVisible] = useState(false);

    useEffect(() => {
        if (healthStatus === 'CRITICAL' || healthStatus === 'WARNING') {
            setIsVisible(true);
        } else {
            setIsVisible(false);
        }
    }, [healthStatus]);

    if (!isVisible) return null;

    return (
        <div className="zen-overlay">
            <div className="zen-content">
                <div className="zen-header">
                    <h2>Zen Mode Active</h2>
                    <p className="zen-subtitle">Preservation Protocol Engaged</p>
                </div>

                <div className="zen-body">
                    <div className="breathing-circle"></div>
                    <p className="zen-message">
                        The system has detected institutional risk thresholds or emotional instability.
                        Trading is frozen for your capital protection.
                    </p>
                    <div className="cooldown-timer">
                        <span className="timer-label">Estimated Unlock:</span>
                        <span className="timer-value">03:59:42</span>
                    </div>
                </div>

                <div className="zen-footer">
                    <p>Take a deep breath. Step away from the screen.</p>
                </div>
            </div>
        </div>
    );
};

export default ZenOverlay;
