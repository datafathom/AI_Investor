/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Macro/MacroHealthGauge.jsx
 * ROLE: Macro Stability Visualization
 * PURPOSE: Displays a stylized radial gauge representing the overall economic 
 *          health score (0-100) calculated from FRED data.
 *          
 * INTEGRATION POINTS:
 *     - macroStore: Retrieves regime.health_score
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import { useMacroStore } from '../../stores/macroStore';
import './MacroDashboard.css';

const MacroHealthGauge = () => {
    const { regime, fetchRegime, loading } = useMacroStore();

    useEffect(() => {
        if (!regime) fetchRegime();
    }, [regime, fetchRegime]);

    if (loading.regime && !regime) {
        return <div className="macro-gauge macro-gauge--loading">Loading Macro Health...</div>;
    }

    const score = regime?.health_score || 0;
    
    // Determine color based on score
    let statusColor = '#ff4757'; // Red
    let statusLabel = 'CRITICAL';
    
    if (score > 80) {
        statusColor = '#00d4aa'; // Teal/Green
        statusLabel = 'OPTIMAL';
    } else if (score > 60) {
        statusColor = '#00d4ff'; // Blue
        statusLabel = 'HEALTHY';
    } else if (score > 40) {
        statusColor = '#ffa502'; // Orange
        statusLabel = 'STRESSED';
    }

    // Calculate rotation for the needle (0 score = -90deg, 100 score = 90deg)
    const rotation = (score / 100) * 180 - 90;

    return (
        <div className="macro-gauge">
            <h3 className="macro-gauge__title">Macro Health Score</h3>
            
            <div className="macro-gauge__container">
                <svg viewBox="0 0 200 120" className="macro-gauge__svg">
                    {/* Background track */}
                    <path 
                        d="M20,110 A80,80 0 0,1 180,110" 
                        fill="none" 
                        stroke="rgba(255,255,255,0.05)" 
                        strokeWidth="15" 
                        strokeLinecap="round" 
                    />
                    
                    {/* Colored track segment */}
                    <path 
                        d="M20,110 A80,80 0 0,1 180,110" 
                        fill="none" 
                        stroke={statusColor}
                        strokeWidth="15" 
                        strokeLinecap="round" 
                        strokeDasharray="251.32"
                        strokeDashoffset={251.32 * (1 - score/100)}
                        style={{ transition: 'stroke-dashoffset 1s ease-out, stroke 1s ease' }}
                    />
                    
                    {/* Needle */}
                    <line 
                        x1="100" y1="110" x2="100" y2="40" 
                        stroke="#fff" 
                        strokeWidth="3"
                        style={{ 
                            transform: `rotate(${rotation}deg)`, 
                            transformOrigin: '100px 110px',
                            transition: 'transform 1.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)'
                        }}
                    />
                    
                    <circle cx="100" cy="110" r="5" fill="#fff" />
                </svg>
                
                <div className="macro-gauge__value-display">
                    <span className="macro-gauge__score" style={{ color: statusColor }}>{Math.round(score)}</span>
                    <span className="macro-gauge__status">{statusLabel}</span>
                </div>
            </div>
            
            <div className="macro-gauge__footer">
                <span className="macro-gauge__timestamp">
                    System Update: {new Date(regime?.timestamp).toLocaleTimeString()}
                </span>
            </div>
        </div>
    );
};

export default MacroHealthGauge;
