import React, { useEffect } from 'react';
import { ShieldCheck, AlertTriangle } from 'lucide-react';
import useImpactStore from '../../stores/impactStore';
import './ESGScores.css';

const CircularGauge = ({ label, value, color }) => {
    return (
        <div className="gauge-wrapper">
            <div 
                className="circular-gauge" 
                style={{ 
                    '--gauge-percent': `${value * 3.6}deg`,
                    '--gauge-color': color
                }}
            >
                <div className="gauge-inner">
                    <strong>{value}</strong>
                    <small>/100</small>
                </div>
            </div>
            <span className="gauge-label">{label}</span>
        </div>
    );
};

const ESGScores = () => {
    const { esgScores, fetchESGData, isLoading } = useImpactStore();

    useEffect(() => {
        fetchESGData();
    }, []);

    if (isLoading || !esgScores) return <div className="esg-scores">Loading ESG Data...</div>;

    const { score, karma_score, sin_stocks } = esgScores;
    const s = score || { environmental: 0, social: 0, governance: 0 };

    return (
        <div className="esg-scores">
            <div className="esg-header">
                <h3><ShieldCheck size={18} className="text-blue-400" /> ESG Composite</h3>
                <span className="text-xs bg-blue-500/20 text-blue-300 px-2 py-1 rounded border border-blue-500/30">
                    Grade: {s.grade}
                </span>
            </div>

            <div className="gauges-container">
                <CircularGauge label="Environmental" value={s.environmental} color="#4ade80" />
                <CircularGauge label="Social" value={s.social} color="#60a5fa" />
                <CircularGauge label="Governance" value={s.governance} color="#f472b6" />
            </div>

            <div className="karma-score-bar">
                <div className="karma-label">
                    <span>Portfolio Karma</span>
                    <strong>{karma_score} / 100</strong>
                </div>
                <div className="karma-stars">
                    {'★'.repeat(Math.round(karma_score / 20))}
                    <span className="opacity-30">{'★'.repeat(5 - Math.round(karma_score / 20))}</span>
                </div>
            </div>

            {sin_stocks && sin_stocks.length > 0 && (
                <div className="sin-stock-alert">
                    <AlertTriangle size={20} className="sin-icon" />
                    <div className="sin-details">
                        <strong>Sin Stock Alert</strong>
                        <span>{sin_stocks.length} positions violate filters ({sin_stocks.map(x => x.ticker).join(', ')})</span>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ESGScores;
