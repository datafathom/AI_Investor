import React, { useEffect } from 'react';
import { Flame, TrendingUp, TrendingDown, Clock } from 'lucide-react';
import useWeb3Store from '../../stores/web3Store';
import './GasPulse.css';

const GasPulse = () => {
    const { gasMetrics, fetchGasMetrics } = useWeb3Store();
    const data = gasMetrics?.ethereum || { 
        low: 0, average: 0, high: 0, trend: 'stable', nextBlock: 0 
    };

    useEffect(() => {
        fetchGasMetrics('ethereum');
        const interval = setInterval(() => fetchGasMetrics('ethereum'), 5000);
        return () => clearInterval(interval);
    }, [fetchGasMetrics]);

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
                    <span className="gas-value">{Math.round(data.low)}</span>
                    <span className="gas-unit">gwei</span>
                </div>
                <div className="gas-metric primary">
                    <span className="gas-label">Average</span>
                    <div className="gas-value-large">
                        {Math.round(data.average)}
                    </div>
                     <span className="gas-unit">gwei</span>
                </div>
                <div className="gas-metric">
                    <span className="gas-label">High (Fast)</span>
                    <span className="gas-value">{Math.round(data.high)}</span>
                    <span className="gas-unit">gwei</span>
                </div>
            </div>

            <div className="gas-footer">
                <div className="gas-trend">
                    Trend: {getTrendIcon()}
                </div>
                <div className="gas-eta">
                    <Clock size={14} /> Next Block: ~{data.nextBlock}s
                </div>
            </div>
        </div>
    );
};

export default GasPulse;
