/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AnalyticsOptions.jsx
 * ROLE: Options Analytics Page
 * PURPOSE: Displays advanced market analytics widgets (GEX, Fama-French).
 *          Serves as the container for Phase 2 implementation of deep-dive tools.
 * ==============================================================================
 */
import React, { useEffect } from 'react';
import useNavigationStore from '../stores/navigationStore';
import { useLocation } from 'react-router-dom';
import FearGreedWidget from '../widgets/FearGreedWidget';
import KafkaStreamMonitor from '../widgets/KafkaStreamMonitor';
import HypeMeterWidget from '../widgets/HypeMeterWidget';
import './AnalyticsOptions.css';

// Placeholder widgets
const GEXWidget = () => (
    <div className="glass card widget-gex">
        <header>
            <h2>Gamma Exposure (GEX)</h2>
            <p>Market Maker Positioning</p>
        </header>
        <div className="gex-chart-placeholder">
            {/* D3/Recharts would go here */}
            <div className="bar positive" style={{height: '60%'}}></div>
            <div className="bar negative" style={{height: '40%'}}></div>
            <div className="bar positive" style={{height: '80%'}}></div>
            <div className="zero-line"></div>
        </div>
        <div className="metric-row">
            <span>Net GEX: <span className="positive">+$4.2B</span></span>
            <span>Zero Gamma: <span className="neutral">4450</span></span>
        </div>
    </div>
);

const FamaFrenchWidget = () => (
    <div className="glass card widget-ff">
        <header>
            <h2>Factor Decomposition</h2>
            <p>Fama-French 5-Factor Model</p>
        </header>
        <div className="factor-grid">
            <div className="factor-item"><span className="label">Mkt-RF</span><span className="val positive">+1.2</span></div>
            <div className="factor-item"><span className="label">SMB</span><span className="val negative">-0.4</span></div>
            <div className="factor-item"><span className="label">HML</span><span className="val positive">+0.8</span></div>
            <div className="factor-item"><span className="label">RMW</span><span className="val neutral">0.0</span></div>
            <div className="factor-item"><span className="label">CMA</span><span className="val negative">-0.2</span></div>
        </div>
    </div>
);

const AnalyticsOptions = () => {
    const location = useLocation();
    const setCurrentRoute = useNavigationStore((state) => state.setCurrentRoute);

    useEffect(() => {
        setCurrentRoute(location.pathname);
    }, [location, setCurrentRoute]);

    return (
        <div className="analytics-options-container" data-tour-id="options-chain">
            <h1 className="page-title">Options Analytics & Risk</h1>
            
            <div className="widgets-grid">
                {/* Phase 2 Widgets */}
                <div className="glass card" style={{ gridRow: 'span 2' }}>
                    <KafkaStreamMonitor />
                </div>
                <div className="glass card">
                    <FearGreedWidget />
                </div>
                <div className="glass card">
                    <HypeMeterWidget />
                </div>

                {/* Analytical Placeholders */}
                <GEXWidget />
                <FamaFrenchWidget />
                
                {/* IV Surface Placeholder */}
                <div className="glass card widget-iv">
                     <header>
                        <h2>IV Surface</h2>
                        <p>3D Volatility Skew</p>
                    </header>
                    <div className="iv-placeholder">
                        [3D Plot Area]
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AnalyticsOptions;
