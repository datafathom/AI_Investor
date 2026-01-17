/**
 * ==============================================================================
 * FILE: FearGreedGauge.jsx
 * ROLE: Fear & Greed Index Visualization Component
 * PURPOSE: 
 *     Displays the proprietary Fear & Greed Composite Index (0-100) as an
 *     animated gauge with color-coded zones and real-time updates.
 * 
 * ROADMAP: Phase 12 - The "Fear & Greed" Composite Index
 * 
 * ZONES:
 *     0-20:  Extreme Fear (Green - BUY zone)
 *     20-40: Fear (Light Green)
 *     40-60: Neutral (Yellow)
 *     60-80: Greed (Orange)
 *     80-100: Extreme Greed (Red - SELL zone)
 * ==============================================================================
 */

import React, { useState, useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import './FearGreedGauge.css';

const API_BASE = ''; // Use same-origin API (Express server)

/**
 * FearGreedGauge - Phase 12 Dashboard Widget
 * 
 * @param {Object} props
 * @param {boolean} props.autoRefresh - Enable auto-refresh (default: true)
 * @param {number} props.refreshInterval - Refresh interval in ms (default: 60000)
 * @param {string[]} props.symbols - Symbols to analyze (default: SPY,QQQ,AAPL)
 */
export default function FearGreedGauge({
    autoRefresh = true,
    refreshInterval = 60000,
    symbols = ['SPY', 'QQQ', 'AAPL']
}) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [lastUpdate, setLastUpdate] = useState(null);

    const fetchFearGreedIndex = useCallback(async () => {
        try {
            setLoading(true);
            const symbolsParam = symbols.join(',');
            const response = await fetch(
                `${API_BASE}/api/v1/market/fear-greed?symbols=${symbolsParam}&mock=true`
            );

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            const result = await response.json();
            setData(result);
            setLastUpdate(new Date());
            setError(null);
        } catch (err) {
            console.error('Failed to fetch Fear & Greed Index:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [symbols]);

    useEffect(() => {
        fetchFearGreedIndex();

        if (autoRefresh) {
            const interval = setInterval(fetchFearGreedIndex, refreshInterval);
            return () => clearInterval(interval);
        }
    }, [fetchFearGreedIndex, autoRefresh, refreshInterval]);

    /**
     * Calculate needle rotation based on score (0-100 maps to -90 to +90 degrees)
     */
    const getNeedleRotation = (score) => {
        // Score 0 = -90deg (left), Score 100 = +90deg (right)
        return ((score / 100) * 180) - 90;
    };

    /**
     * Get zone color based on score
     */
    const getZoneColor = (score) => {
        if (score < 20) return '#22c55e'; // Extreme Fear - Green
        if (score < 40) return '#84cc16'; // Fear - Light Green
        if (score < 60) return '#eab308'; // Neutral - Yellow
        if (score < 80) return '#f97316'; // Greed - Orange
        return '#ef4444'; // Extreme Greed - Red
    };

    /**
     * Get signal badge color
     */
    const getSignalColor = (signal) => {
        const colors = {
            'BUY': '#22c55e',
            'ACCUMULATE': '#84cc16',
            'HOLD': '#eab308',
            'REDUCE': '#f97316',
            'SELL': '#ef4444'
        };
        return colors[signal] || '#6b7280';
    };

    if (loading && !data) {
        return (
            <div className="fear-greed-gauge fear-greed-loading">
                <div className="gauge-spinner" />
                <span>Loading Fear & Greed Index...</span>
            </div>
        );
    }

    if (error && !data) {
        return (
            <div className="fear-greed-gauge fear-greed-error">
                <span className="error-icon"></span>
                <span>Error: {error}</span>
                <button onClick={fetchFearGreedIndex}>Retry</button>
            </div>
        );
    }

    const score = data?.score ?? 50;
    const label = data?.label ?? 'NEUTRAL';
    const signal = data?.signal ?? 'HOLD';
    const recommendation = data?.recommendation ?? '';
    const rotation = getNeedleRotation(score);
    const zoneColor = getZoneColor(score);

    return (
        <div className="fear-greed-gauge">
            <div className="gauge-header">
                <h3>Fear & Greed Index</h3>
                <span
                    className="signal-badge"
                    style={{ backgroundColor: getSignalColor(signal) }}
                >
                    {signal}
                </span>
            </div>

            {/* SVG Gauge */}
            <div className="gauge-container">
                <svg viewBox="0 0 200 120" className="gauge-svg">
                    {/* Background arc zones */}
                    <defs>
                        <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#22c55e" />
                            <stop offset="20%" stopColor="#84cc16" />
                            <stop offset="40%" stopColor="#eab308" />
                            <stop offset="70%" stopColor="#f97316" />
                            <stop offset="100%" stopColor="#ef4444" />
                        </linearGradient>
                    </defs>

                    {/* Gauge arc background */}
                    <path
                        d="M 20 100 A 80 80 0 0 1 180 100"
                        fill="none"
                        stroke="url(#gaugeGradient)"
                        strokeWidth="12"
                        strokeLinecap="round"
                        className="gauge-arc"
                    />

                    {/* Tick marks */}
                    {[0, 20, 40, 60, 80, 100].map((tick) => {
                        const angle = ((tick / 100) * 180 - 90) * (Math.PI / 180);
                        const innerRadius = 70;
                        const outerRadius = 85;
                        const x1 = 100 + innerRadius * Math.cos(angle);
                        const y1 = 100 + innerRadius * Math.sin(angle);
                        const x2 = 100 + outerRadius * Math.cos(angle);
                        const y2 = 100 + outerRadius * Math.sin(angle);
                        return (
                            <line
                                key={tick}
                                x1={x1}
                                y1={y1}
                                x2={x2}
                                y2={y2}
                                stroke="rgba(255,255,255,0.5)"
                                strokeWidth="2"
                            />
                        );
                    })}

                    {/* Needle */}
                    <g
                        className="gauge-needle"
                        style={{ transform: `rotate(${rotation}deg)`, transformOrigin: '100px 100px' }}
                    >
                        <polygon
                            points="100,25 96,100 104,100"
                            fill={zoneColor}
                            className="needle-shape"
                        />
                        <circle cx="100" cy="100" r="8" fill="#1f2937" stroke={zoneColor} strokeWidth="3" />
                    </g>

                    {/* Score display */}
                    <text x="100" y="85" textAnchor="middle" className="gauge-score">
                        {Math.round(score)}
                    </text>
                    <text x="100" y="100" textAnchor="middle" className="gauge-label">
                        {label.replace('_', ' ')}
                    </text>
                </svg>

                {/* Zone labels */}
                <div className="gauge-zone-labels">
                    <span className="zone-label extreme-fear">Extreme Fear</span>
                    <span className="zone-label neutral">Neutral</span>
                    <span className="zone-label extreme-greed">Extreme Greed</span>
                </div>
            </div>

            {/* Recommendation */}
            <div className="gauge-recommendation">
                <p>{recommendation}</p>
            </div>

            {/* Components breakdown */}
            {data?.components && (
                <div className="gauge-components">
                    <h4>Component Scores</h4>
                    <div className="component-grid">
                        {Object.entries(data.components).map(([key, comp]) => (
                            <div key={key} className="component-item">
                                <span className="component-name">
                                    {key.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                                </span>
                                <div className="component-bar">
                                    <div
                                        className="component-fill"
                                        style={{
                                            width: `${comp.score}%`,
                                            backgroundColor: getZoneColor(comp.score)
                                        }}
                                    />
                                </div>
                                <span className="component-score">{Math.round(comp.score)}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Footer */}
            <div className="gauge-footer">
                <span className="last-update">
                    Updated: {lastUpdate?.toLocaleTimeString() || 'N/A'}
                </span>
                <button
                    className="refresh-btn"
                    onClick={fetchFearGreedIndex}
                    disabled={loading}
                >
                    {loading ? '' : ''}
                </button>
            </div>
        </div>
    );
}

FearGreedGauge.propTypes = {
    autoRefresh: PropTypes.bool,
    refreshInterval: PropTypes.number,
    symbols: PropTypes.arrayOf(PropTypes.string)
};
