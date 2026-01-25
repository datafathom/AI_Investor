import React from 'react';
import { TrendingDown, ShieldCheck, RefreshCw, Calendar } from 'lucide-react';
import useScenarioStore from '../../stores/scenarioStore';
import './ForecastChart.css';

const ForecastChart = () => {
    const { impactResults, recoveryProjection, hedgeSufficiency } = useScenarioStore();
    
    const impact = impactResults?.portfolio_impact_pct || 0;
    const path = recoveryProjection?.path || [];

    // Simple SVG path generator for recovery
    const generatePath = () => {
        if (path.length < 2) return "M0,100 C50,160 150,180 400,120";
        let d = `M0,100`;
        const widthPerStep = 400 / (path.length - 1);
        path.forEach((val, i) => {
            const x = i * widthPerStep;
            // Map portfolio value to SVG Y (100 is baseline, 180 is deep drop)
            const y = 100 + (1 - val/1000000) * 400; 
            d += ` L${x},${Math.min(195, y)}`;
        });
        return d;
    };

    return (
        <div className="forecast-chart-widget">
            <div className="widget-header">
                <h3><TrendingDown size={18} className="text-cyan-400" /> Portfolio Revaluation Forecast</h3>
                <div className="header-stats">
                    <div className="stat">
                        <span className="label">Shock Impact</span>
                        <span className={`val ${impact < 0 ? 'negative' : 'positive'}`}>
                            {impact.toFixed(1)}%
                        </span>
                    </div>
                </div>
            </div>

            <div className="chart-area-mock">
                <svg width="100%" height="100%" viewBox="0 0 400 200" preserveAspectRatio="none">
                    <line x1="0" y1="100" x2="400" y2="100" stroke="rgba(255,255,255,0.1)" strokeDasharray="4" />
                    <path d={generatePath()} fill="none" stroke={impact < 0 ? "#ef4444" : "#10b981"} strokeWidth="2" />
                    <path d={`${generatePath()} L400,200 L0,200 Z`} fill="url(#shockGradient)" opacity="0.2" />
                    
                    <defs>
                        <linearGradient id="shockGradient" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="0%" stopColor={impact < 0 ? "#ef4444" : "#10b981"} stopOpacity="0.5"/>
                            <stop offset="100%" stopColor={impact < 0 ? "#ef4444" : "#10b981"} stopOpacity="0"/>
                        </linearGradient>
                    </defs>
                </svg>
                <div className="chart-label baseline">Baseline</div>
                <div className="chart-label shock">Recovery Path</div>
            </div>

            <div className="analysis-panel">
                <div className="shield-indicator">
                    <ShieldCheck size={24} className={hedgeSufficiency > 0.5 ? "text-green-400" : "text-yellow-400"} />
                    <div className="shield-text">
                        <div className="status">{hedgeSufficiency > 0.8 ? "Fully Hedged" : hedgeSufficiency > 0.3 ? "Partially Hedged" : "Under-Hedged"}</div>
                        <div className="sub">Hedge Efficiency: {(hedgeSufficiency * 100).toFixed(0)}%</div>
                    </div>
                </div>
                
                <div className="recovery-time">
                    <div className="icon"><Calendar size={16} /></div>
                    <div className="text">
                        <span>Est. Recovery</span>
                        <strong>{recoveryProjection?.days || '--'} Days</strong>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForecastChart;
