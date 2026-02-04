import React from 'react';
import { Leaf, Users, Scale, AlertOctagon } from 'lucide-react';
import './ESGGauges.css';

const ESGGauges = () => {
    // Mock Scores
    const scores = {
        environmental: 82,
        social: 65,
        governance: 91,
        total: 79
    };

    return (
        <div className="esg-gauges-widget">
            <div className="widget-header">
                <h3><Leaf size={18} className="text-green-400" /> ESG Score Aggregator</h3>
                <div className="total-score">
                    <span className="lbl">Portfolio Karma</span>
                    <span className="val good">{scores.total}/100</span>
                </div>
            </div>

            <div className="gauges-container">
                <div className="gauge-card">
                    <div className="gauge-icon environmental"><Leaf size={24} /></div>
                    <div className="gauge-info">
                        <span className="title">Environmental</span>
                        <div className="progress-bar">
                            <div className="fill env" style={{ width: `${scores.environmental}%` }}></div>
                        </div>
                        <span className="score">{scores.environmental}</span>
                    </div>
                </div>

                <div className="gauge-card">
                    <div className="gauge-icon social"><Users size={24} /></div>
                    <div className="gauge-info">
                        <span className="title">Social</span>
                        <div className="progress-bar">
                            <div className="fill soc" style={{ width: `${scores.social}%` }}></div>
                        </div>
                        <span className="score">{scores.social}</span>
                    </div>
                </div>

                <div className="gauge-card">
                    <div className="gauge-icon governance"><Scale size={24} /></div>
                    <div className="gauge-info">
                        <span className="title">Governance</span>
                        <div className="progress-bar">
                            <div className="fill gov" style={{ width: `${scores.governance}%` }}></div>
                        </div>
                        <span className="score">{scores.governance}</span>
                    </div>
                </div>
            </div>

            <div className="sin-stock-alert">
                <div className="alert-content">
                    <AlertOctagon size={20} />
                    <div className="text-box">
                        <span className="alert-title">Sin Stock Detected</span>
                        <span className="alert-msg">Ticker <strong>GAMBL</strong> flagged in 'Gambling'. Sell recommended to improve 'Social' score.</span>
                    </div>
                </div>
                <button className="sell-action-btn">Quick Sell</button>
            </div>
        </div>
    );
};

export default ESGGauges;
