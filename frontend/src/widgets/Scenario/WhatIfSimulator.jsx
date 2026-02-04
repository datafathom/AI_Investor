import React, { useState } from 'react';
import { Zap, TrendingDown, TrendingUp, Play, RotateCcw } from 'lucide-react';
import './WhatIfSimulator.css';

/**
 * What-If Impact Simulator (Phase 16)
 * 
 * Drag-and-drop macro event simulator with portfolio revaluation.
 */
const WhatIfSimulator = () => {
    const [activeScenarios, setActiveScenarios] = useState([]);
    const [portfolioImpact, setPortfolioImpact] = useState(0);

    const scenarios = [
        { id: 1, name: 'Fed Rate Hike +50bps', impact: -3.5, category: 'rates' },
        { id: 2, name: 'Oil Spike +20%', impact: -1.2, category: 'commodity' },
        { id: 3, name: 'Tech Selloff -15%', impact: -8.5, category: 'sector' },
        { id: 4, name: 'USD Strength +5%', impact: -0.8, category: 'fx' },
        { id: 5, name: 'Recession Signal', impact: -12.0, category: 'macro' },
        { id: 6, name: 'Fed Pivot Dovish', impact: +7.5, category: 'rates' },
    ];

    const toggleScenario = (scenario) => {
        const isActive = activeScenarios.find(s => s.id === scenario.id);
        if (isActive) {
            setActiveScenarios(activeScenarios.filter(s => s.id !== scenario.id));
            setPortfolioImpact(prev => prev - scenario.impact);
        } else {
            setActiveScenarios([...activeScenarios, scenario]);
            setPortfolioImpact(prev => prev + scenario.impact);
        }
    };

    const resetScenarios = () => {
        setActiveScenarios([]);
        setPortfolioImpact(0);
    };

    return (
        <div className="what-if-simulator">
            <div className="widget-header">
                <Zap size={16} />
                <h3>What-If Simulator</h3>
                <button className="reset-btn" onClick={resetScenarios}>
                    <RotateCcw size={12} /> Reset
                </button>
            </div>

            <div className="impact-display">
                <span className="label">Portfolio Impact</span>
                <span className={`value ${portfolioImpact >= 0 ? 'positive' : 'negative'}`}>
                    {portfolioImpact >= 0 ? '+' : ''}{portfolioImpact.toFixed(1)}%
                </span>
            </div>

            <div className="scenarios-grid">
                {scenarios.map(scenario => {
                    const isActive = activeScenarios.find(s => s.id === scenario.id);
                    return (
                        <div 
                            key={scenario.id}
                            className={`scenario-card ${isActive ? 'active' : ''} ${scenario.impact >= 0 ? 'bullish' : 'bearish'}`}
                            onClick={() => toggleScenario(scenario)}
                        >
                            <div className="scenario-header">
                                {scenario.impact >= 0 ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
                                <span className="scenario-name">{scenario.name}</span>
                            </div>
                            <span className="scenario-impact">
                                {scenario.impact >= 0 ? '+' : ''}{scenario.impact}%
                            </span>
                        </div>
                    );
                })}
            </div>

            <button className="run-simulation-btn">
                <Play size={14} /> Run Full Simulation
            </button>
        </div>
    );
};

export default WhatIfSimulator;
