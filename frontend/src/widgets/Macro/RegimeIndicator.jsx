/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Macro/RegimeIndicator.jsx
 * ROLE: Economic Status Indicator
 * PURPOSE: Displays the current macro regime (EXPANSION, STAGFLATION, etc.) 
 *          and a tag-cloud of active economic signals.
 *          
 * INTEGRATION POINTS:
 *     - macroStore: Retrieves regime.status and regime.signals
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React from 'react';
import { useMacroStore } from '../../stores/macroStore';
import './MacroDashboard.css';

const RegimeIndicator = () => {
    const { regime } = useMacroStore();

    if (!regime) return <div className="regime-indicator regime-indicator--empty">Waiting for regime analysis...</div>;

    const getStatusInfo = (status) => {
        switch (status) {
            case 'EXPANSION':
                return { label: 'Expansion', icon: '🚀', color: '#00d4aa', desc: 'Positive growth with stable inflation.' };
            case 'RECESSION_WARNING':
                return { label: 'Recession Warning', icon: '⚠️', color: '#ffa502', desc: 'Leading indicators flagging potential contraction.' };
            case 'CONTRACTION':
                return { label: 'Contraction', icon: '📉', color: '#ff4757', desc: 'Negative GDP growth and rising unemployment.' };
            case 'STAGFLATION':
                return { label: 'Stagflation', icon: '🔥', color: '#ff7f50', desc: 'High inflation coupled with stagnant growth.' };
            case 'SLOWDOWN':
                return { label: 'Slowdown', icon: '⏳', color: '#00d4ff', desc: 'Decelerating growth metrics.' };
            default:
                return { label: status, icon: '🔍', color: '#888', desc: 'Analyzing macro environment.' };
        }
    };

    const statusInfo = getStatusInfo(regime.status);

    return (
        <div className="regime-indicator">
            <div className="regime-indicator__header" style={{ borderLeftColor: statusInfo.color }}>
                <div className="regime-indicator__icon-box" style={{ backgroundColor: `${statusInfo.color}15`, color: statusInfo.color }}>
                    {statusInfo.icon}
                </div>
                <div className="regime-indicator__title-group">
                    <h2 className="regime-indicator__title">{statusInfo.label}</h2>
                    <p className="regime-indicator__desc">{statusInfo.desc}</p>
                </div>
            </div>

            <div className="regime-indicator__signals">
                <span className="regime-indicator__signals-label">Economic Signals:</span>
                <div className="regime-indicator__tag-cloud">
                    {regime.signals && regime.signals.length > 0 ? (
                        regime.signals.map((signal, idx) => (
                            <span key={idx} className="regime-indicator__tag">
                                {signal.replace(/_/g, ' ')}
                            </span>
                        ))
                    ) : (
                        <span className="regime-indicator__tag regime-indicator__tag--neutral">Stable Environment</span>
                    )}
                </div>
            </div>

            <div className="regime-indicator__data-grid">
                {Object.entries(regime.metrics).map(([key, val], idx) => (
                    <div key={idx} className="regime-indicator__metric-item">
                        <span className="regime-indicator__metric-name">{key.replace(/_/g, ' ')}</span>
                        <span className="regime-indicator__metric-value">
                            {typeof val === 'number' ? val.toFixed(2) : val}
                            {key === 'UNEMPLOYMENT' || key === 'FED_FUNDS' || key === 'GDP_GROWTH' ? '%' : ''}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default RegimeIndicator;
