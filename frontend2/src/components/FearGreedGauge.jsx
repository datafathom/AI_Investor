import React, { useEffect, useState } from 'react';
import './FearGreedGauge.css';
import { marketService } from '../services/marketService';

const FearGreedGauge = ({ refreshInterval = 60000 }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const fetchData = async () => {
        try {
            setLoading(true);
            const result = await marketService.getFearGreedIndex();
            setData(result);
            setError(null);
        } catch (err) {
            console.error(err);
            setError('Failed to load market sentiment');
            // Mock data fallback if desired, or just show error
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, refreshInterval);
        return () => clearInterval(interval);
    }, [refreshInterval]);

    const getRotation = (score) => {
        // Map 0-100 to -90 to 90 degrees
        return (score / 100) * 180 - 90;
    };

    const getColorClass = (label) => {
        switch (label) {
            case 'EXTREME_FEAR': return 'color-extreme-fear';
            case 'FEAR': return 'color-fear';
            case 'NEUTRAL': return 'color-neutral';
            case 'GREED': return 'color-greed';
            case 'EXTREME_GREED': return 'color-extreme-greed';
            default: return 'color-neutral';
        }
    };

    if (loading && !data) return <div className="loading-spinner">Loading...</div>;
    if (error) return <div className="error-message">{error}</div>;

    const { score, label, components } = data;
    const rotation = getRotation(score);
    const colorClass = getColorClass(label);

    return (
        <div className="fear-greed-gauge-container">
            <div className="gauge-header">Market Sentiment</div>

            <div className="gauge-svg-wrapper">
                <svg viewBox="0 0 200 120" className="gauge-svg">
                    {/* Gradient Definitions */}
                    <defs>
                        <linearGradient id="gaugeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#ff4d4d" />
                            <stop offset="25%" stopColor="#ff9f43" />
                            <stop offset="50%" stopColor="#feca57" />
                            <stop offset="75%" stopColor="#1dd1a1" />
                            <stop offset="100%" stopColor="#5f27cd" />
                        </linearGradient>
                    </defs>

                    {/* Background Arc */}
                    <path
                        d="M 20 100 A 80 80 0 0 1 180 100"
                        fill="none"
                        stroke="#333"
                        strokeWidth="15"
                        strokeLinecap="round"
                    />

                    {/* Colored Arc (could use segments, but gradient is nice) */}
                    <path
                        d="M 20 100 A 80 80 0 0 1 180 100"
                        fill="none"
                        stroke="url(#gaugeGradient)"
                        strokeWidth="15"
                        strokeLinecap="round"
                        opacity="0.8"
                    />

                    {/* Needle */}
                    <g className="gauge-needle" style={{ transform: `rotate(${rotation}deg)` }}>
                        <line x1="100" y1="100" x2="100" y2="30" stroke="#fff" strokeWidth="4" strokeLinecap="round" />
                        <circle cx="100" cy="100" r="6" fill="#fff" />
                    </g>

                    {/* Ticks/Labels */}
                    <g className="gauge-ticks">
                        <text x="20" y="115" textAnchor="middle">0</text>
                        <text x="100" y="115" textAnchor="middle">50</text>
                        <text x="180" y="115" textAnchor="middle">100</text>
                    </g>
                </svg>

                <div className="gauge-value">
                    <div className={`gauge-score ${colorClass}`}>{Math.round(score)}</div>
                    <div className={`gauge-label ${colorClass}`}>{label.replace('_', ' ')}</div>
                </div>
            </div>

            <div className="gauge-components">
                {components && Object.entries(components).map(([key, value]) => (
                    <div key={key} className={`component-item ${getColorClass(data.label)}`}>
                        <span className="component-label">{key.replace('_', ' ').toUpperCase()}</span>
                        <span className="component-score">{Math.round(value.score)}/100</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default FearGreedGauge;
