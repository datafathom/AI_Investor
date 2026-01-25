import React, { useState, useEffect } from 'react';
import { Flame, TrendingUp, TrendingDown, Clock } from 'lucide-react';
import './GasPulse.css';

const GasPulse = () => {
    const [gasData, setGasData] = useState({
        low: 15,
        average: 18,
        high: 25,
        trend: 'stable',
        nextBlock: 12
    });

    useEffect(() => {
        const interval = setInterval(() => {
            // Mock simulation of gas fluctuation
            setGasData(prev => ({
                low: Math.max(10, prev.low + (Math.random() - 0.5) * 2),
                average: Math.max(12, prev.average + (Math.random() - 0.5) * 3),
                high: Math.max(20, prev.high + (Math.random() - 0.5) * 4),
                trend: Math.random() > 0.5 ? 'rising' : 'falling',
                nextBlock: Math.floor(Math.random() * 15)
            }));
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    const getTrendIcon = () => {
        if (gasData.trend === 'rising') return <TrendingUp color="#ff4d4d" />;
        if (gasData.trend === 'falling') return <TrendingDown color="#00cc66" />;
        return <div className="gas-stable">-</div>;
    };

    return (
        <div className="gas-pulse-widget">
            <div className="gas-header">
                <h3><Flame size={18} className="gas-icon" /> Ethereum Gas Pulse</h3>
                <div className="gas-live-indicator">
                    <span className="pulse-dot"></span> LIVE
                </div>
            </div>

            <div className="gas-meter-container">
                <div className="gas-metric">
                    <span className="gas-label">Low (Slow)</span>
                    <span className="gas-value">{Math.round(gasData.low)}</span>
                    <span className="gas-unit">gwei</span>
                </div>
                <div className="gas-metric primary">
                    <span className="gas-label">Average</span>
                    <div className="gas-value-large">
                        {Math.round(gasData.average)}
                    </div>
                     <span className="gas-unit">gwei</span>
                </div>
                <div className="gas-metric">
                    <span className="gas-label">High (Fast)</span>
                    <span className="gas-value">{Math.round(gasData.high)}</span>
                    <span className="gas-unit">gwei</span>
                </div>
            </div>

            <div className="gas-footer">
                <div className="gas-trend">
                    Trend: {getTrendIcon()}
                </div>
                <div className="gas-eta">
                    <Clock size={14} /> Next Block: ~{gasData.nextBlock}s
                </div>
            </div>
        </div>
    );
};

export default GasPulse;
