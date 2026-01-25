import React from 'react';
import { Leaf, Heart, TrendingUp, BarChart3 } from 'lucide-react';
import './ESGDashboard.css';

/**
 * ESG Score Aggregator (Phase 17)
 * 
 * Environmental, Social, Governance scores with carbon footprint tracking.
 */
const ESGDashboard = () => {
    const scores = {
        environmental: 72,
        social: 68,
        governance: 85,
        overall: 75,
    };

    const carbonData = {
        current: 125, // tons CO2
        benchmark: 180,
        reduction: -30.5,
    };

    const holdings = [
        { name: 'MSFT', esg: 89, carbon: 'Low', impact: '+2.3%' },
        { name: 'AAPL', esg: 82, carbon: 'Low', impact: '+1.8%' },
        { name: 'XOM', esg: 45, carbon: 'High', impact: '-0.5%' },
        { name: 'TSLA', esg: 78, carbon: 'Medium', impact: '+3.2%' },
    ];

    const renderGauge = (value, label, color) => (
        <div className="esg-gauge">
            <svg viewBox="0 0 36 36">
                <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke="var(--border-primary)"
                    strokeWidth="3"
                />
                <path
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    fill="none"
                    stroke={color}
                    strokeWidth="3"
                    strokeDasharray={`${value}, 100`}
                />
            </svg>
            <span className="gauge-value">{value}</span>
            <span className="gauge-label">{label}</span>
        </div>
    );

    return (
        <div className="esg-dashboard">
            <div className="widget-header">
                <Leaf size={16} />
                <h3>ESG Impact</h3>
            </div>

            <div className="esg-scores">
                {renderGauge(scores.environmental, 'E', '#4ade80')}
                {renderGauge(scores.social, 'S', '#60a5fa')}
                {renderGauge(scores.governance, 'G', '#a78bfa')}
            </div>

            <div className="overall-score">
                <span className="label">Overall ESG Score</span>
                <span className="value">{scores.overall}</span>
                <span className="rating">A-</span>
            </div>

            <div className="carbon-section">
                <div className="carbon-header">
                    <BarChart3 size={12} />
                    <span>Carbon Footprint</span>
                </div>
                <div className="carbon-stats">
                    <div className="stat">
                        <span className="stat-value">{carbonData.current}</span>
                        <span className="stat-label">tons CO2</span>
                    </div>
                    <div className="stat positive">
                        <span className="stat-value">{carbonData.reduction}%</span>
                        <span className="stat-label">vs benchmark</span>
                    </div>
                </div>
            </div>

            <div className="holdings-esg">
                <h4>Holdings by ESG</h4>
                {holdings.map((h, i) => (
                    <div key={i} className="holding-row">
                        <span className="holding-name">{h.name}</span>
                        <span className={`esg-score ${h.esg >= 70 ? 'high' : h.esg >= 50 ? 'medium' : 'low'}`}>
                            {h.esg}
                        </span>
                        <span className={`carbon-tag ${h.carbon.toLowerCase()}`}>{h.carbon}</span>
                        <span className={`impact ${parseFloat(h.impact) >= 0 ? 'positive' : 'negative'}`}>
                            {h.impact}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ESGDashboard;
