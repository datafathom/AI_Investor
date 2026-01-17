
import React, { useState, useEffect } from 'react';
import { homeostasisService } from '../../../services/homeostasisService';
import { Heart, Zap, Target, ShieldCheck, TrendingUp } from 'lucide-react';
import './HomeostasisWidget.css';

const HomeostasisWidget = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStatus = async () => {
            const data = await homeostasisService.getStatus();
            if (data) setStatus(data);
            setLoading(false);
        };
        fetchStatus();

        // Refresh every 30 seconds
        const interval = setInterval(fetchStatus, 30000);
        return () => clearInterval(interval);
    }, []);

    if (loading) return <div className="loading">Initializing Homeostasis...</div>;
    if (!status) return <div className="error">Homeostasis Offline</div>;

    const score = status.homeostasis_score || 0;
    const isEnough = status.preservation_mode;

    return (
        <div className="homeostasis-widget glass">
            <div className="widget-header">
                <Target className="icon-target" />
                <h3>Total Homeostasis</h3>
            </div>

            <div className="gauge-container">
                <div className="gauge-background">
                    <div
                        className={`gauge-fill ${isEnough ? 'enough' : ''}`}
                        style={{ width: `${score}%` }}
                    ></div>
                </div>
                <div className="gauge-labels">
                    <span>$0</span>
                    <span className="current-score">{Math.round(score)}% to "Enough"</span>
                    <span>${(status.target / 1000000).toFixed(1)}M</span>
                </div>
            </div>

            <div className="metrics-grid">
                <div className="metric-card">
                    <TrendingUp className="metric-icon" />
                    <div className="metric-info">
                        <label>Net Worth</label>
                        <span>${status.net_worth?.toLocaleString()}</span>
                    </div>
                </div>
                <div className="metric-card">
                    <Zap className={`metric-icon ${status.autopilot ? 'active' : ''}`} />
                    <div className="metric-info">
                        <label>Autopilot</label>
                        <span>{status.autopilot ? 'ACTIVE' : 'OFFLINE'}</span>
                    </div>
                </div>
            </div>

            <div className={`status-banner ${isEnough ? 'preservation' : 'growth'}`}>
                {isEnough ? (
                    <>
                        <ShieldCheck className="banner-icon" />
                        <span>Preservation Mode Engaged</span>
                    </>
                ) : (
                    <>
                        <TrendingUp className="banner-icon" />
                        <span>Aggressive Growth Phase</span>
                    </>
                )}
            </div>

            <button
                className="philanthropy-btn"
                onClick={() => homeostasisService.donate(100)}
            >
                <Heart className="btn-icon" />
                Donate Surplus Alpha ($100)
            </button>
        </div>
    );
};

export default HomeostasisWidget;
