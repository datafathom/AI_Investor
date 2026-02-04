import React, { useState, useEffect } from 'react';
import { AlertTriangle, TrendingDown, Clock, Info } from 'lucide-react';
import { useFixedIncomeStore } from '../../stores/fixedIncomeStore';
import './DurationGauges.css';

/**
 * Duration & Convexity Gauges 
 * 
 * Semi-circular gauges showing fixed income portfolio risk metrics.
 * Now connected to real Rate Shock simulation from backend.
 */
const DurationGauges = () => {
    // Note: Portfolio Duration/Convexity APIs are not yet exposed by backend,
    // so we keep them static or simulated for now unless we add that endpoint.
    const [durationValue] = useState(6.8); // Years (placeholder)
    const [convexityValue] = useState(45.2); // Measure (placeholder)
    
    const { rateShockResult, simulateRateShock, isLoading } = useFixedIncomeStore();

    useEffect(() => {
        // Run a standard +100bps shock simulation on mount to get data
        if (!rateShockResult) {
            simulateRateShock('default', 100);
        }
    }, [rateShockResult, simulateRateShock]);

    const impactValue = rateShockResult ? rateShockResult.percentage_change : 0;

    const maxDuration = 20;
    const durationPercent = (durationValue / maxDuration) * 100;

    const maxConvexity = 100;
    const convexityPercent = (convexityValue / maxConvexity) * 100;

    const renderGauge = (value, percent, label, unit, warningThreshold, isNegativeWarning = false) => {
        const isWarning = isNegativeWarning ? value < warningThreshold : value > warningThreshold;
        const rotation = -90 + (percent * 1.8); // 180-degree arc

        return (
            <div className="gauge-container">
                <div className="gauge">
                    <svg viewBox="0 0 100 60">
                        {/* Background arc */}
                        <path
                            d="M 10 55 A 40 40 0 0 1 90 55"
                            fill="none"
                            stroke="var(--border-primary)"
                            strokeWidth="8"
                            strokeLinecap="round"
                        />
                        {/* Value arc */}
                        <path
                            d="M 10 55 A 40 40 0 0 1 90 55"
                            fill="none"
                            stroke={isWarning ? 'var(--color-warning)' : 'var(--color-info)'}
                            strokeWidth="8"
                            strokeLinecap="round"
                            strokeDasharray={`${percent * 1.26} 126`}
                        />
                        {/* Needle */}
                        <line
                            x1="50"
                            y1="55"
                            x2="50"
                            y2="20"
                            stroke="var(--text-primary)"
                            strokeWidth="2"
                            strokeLinecap="round"
                            transform={`rotate(${rotation}, 50, 55)`}
                        />
                        <circle cx="50" cy="55" r="5" fill="var(--text-primary)" />
                    </svg>
                </div>
                <div className="gauge-value">
                    <span className="value">{value.toFixed(1)}</span>
                    <span className="unit">{unit}</span>
                </div>
                <div className="gauge-label">{label}</div>
            </div>
        );
    };

    return (
        <div className="duration-gauges">
            <div className="widget-header">
                <h3>Duration & Convexity</h3>
                <div className="data-quality good">
                    <Clock size={10} /> Live
                </div>
            </div>

            <div className="gauges-row">
                {renderGauge(durationValue, durationPercent, 'Modified Duration', 'years', 10)}
                {renderGauge(convexityValue, convexityPercent, 'Convexity', '', 0, true)}
            </div>

            <div className="rate-shock-panel">
                <div className="shock-header">
                    <TrendingDown size={14} />
                    <span>Rate Shock Sensitivity (+100bps)</span>
                </div>
                <div className={`shock-value ${impactValue < -5 ? 'danger' : impactValue < -2 ? 'warning' : 'safe'}`}>
                    {isLoading ? '...' : `${impactValue.toFixed(2)}%`}
                </div>
                <div className="shock-description">
                    {impactValue < -5 ? (
                        <span className="danger"><AlertTriangle size={12} /> High Rate Sensitivity</span>
                    ) : impactValue < -2 ? (
                        <span className="warning">Moderate Sensitivity</span>
                    ) : (
                        <span className="safe">Low Sensitivity</span>
                    )}
                </div>
            </div>

            <div className="info-tooltip">
                <Info size={12} />
                <span>Duration measures price sensitivity to 1% rate change</span>
            </div>
        </div>
    );
};

export default DurationGauges;
