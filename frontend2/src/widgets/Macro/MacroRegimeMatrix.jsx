/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Macro/MacroRegimeMatrix.jsx
 * ROLE: 2x2 Economic Regime Visualization
 * PURPOSE: Plots the current macro environment on a Growth vs. Inflation axis.
 *          Shows the directional shift of the economy.
 * ==============================================================================
 */

import React, { useMemo } from 'react';
import { useMacroStore } from '../../stores/macroStore';
import './MacroRegimeMatrix.css';

const MacroRegimeMatrix = () => {
    const { regime } = useMacroStore();

    const matrixData = useMemo(() => {
        if (!regime || !regime.metrics) return null;

        const gdp = regime.metrics.GDP_GROWTH || 0;
        const inflation = regime.metrics.INFLATION ? (regime.metrics.INFLATION - 300) / 2 : 0; // Rough normalization for index 300
        
        // Normalize to -1 to 1 for the 2x2 grid
        // Assuming GDP 2% is neutral, >5% is high, <0% is low
        const x = Math.max(-1, Math.min(1, (gdp - 2) / 3));
        
        // Assuming 3% inflation is neutral, >6% is high, <1% is low
        // Using a simpler heuristic if we don't have YoY cpi directly in metrics
        const y = Math.max(-1, Math.min(1, (inflation - 3) / 3));

        return { x, y, status: regime.status };
    }, [regime]);

    if (!matrixData) {
        return <div className="macro-matrix macro-matrix--loading">Analyzing Economic Vectors...</div>;
    }

    const { x, y, status } = matrixData;

    // Convert -1/1 coordinates to 0-100% for CSS placement
    const left = ((x + 1) / 2) * 100;
    const top = ((1 - y) / 2) * 100; // Invert Y for top-down coordinate system

    return (
        <div className="macro-matrix">
            <div className="macro-matrix__container">
                {/* Quadrant Labels */}
                <div className="macro-matrix__quadrant macro-matrix__quadrant--top-left">
                    <span className="macro-matrix__quadrant-label">Stagflation</span>
                    <span className="macro-matrix__quadrant-desc">Low Growth / High Inflation</span>
                </div>
                <div className="macro-matrix__quadrant macro-matrix__quadrant--top-right">
                    <span className="macro-matrix__quadrant-label">Expansion</span>
                    <span className="macro-matrix__quadrant-desc">High Growth / High Inflation</span>
                </div>
                <div className="macro-matrix__quadrant macro-matrix__quadrant--bottom-left">
                    <span className="macro-matrix__quadrant-label">Recession</span>
                    <span className="macro-matrix__quadrant-desc">Low Growth / Low Inflation</span>
                </div>
                <div className="macro-matrix__quadrant macro-matrix__quadrant--bottom-right">
                    <span className="macro-matrix__quadrant-label">Goldilocks</span>
                    <span className="macro-matrix__quadrant-desc">High Growth / Low Inflation</span>
                </div>

                {/* Axes */}
                <div className="macro-matrix__axis macro-matrix__axis--horizontal">
                    <span className="macro-matrix__axis-label macro-matrix__axis-label--left">Low Growth</span>
                    <span className="macro-matrix__axis-label macro-matrix__axis-label--right">High Growth</span>
                </div>
                <div className="macro-matrix__axis macro-matrix__axis--vertical">
                    <span className="macro-matrix__axis-label macro-matrix__axis-label--top">High Inflation</span>
                    <span className="macro-matrix__axis-label macro-matrix__axis-label--bottom">Low Inflation</span>
                </div>

                {/* Current State Marker */}
                <div 
                    className={`macro-matrix__marker macro-matrix__marker--${status.toLowerCase()}`}
                    style={{ left: `${left}%`, top: `${top}%` }}
                >
                    <div className="macro-matrix__marker-dot" />
                    <div className="macro-matrix__marker-pulse" />
                    <div className="macro-matrix__marker-label">{status}</div>
                    
                    {/* Directional Vector (Mocked for now, needs historical data) */}
                    <svg className="macro-matrix__vector" width="40" height="40" viewBox="0 0 40 40">
                        <path d="M 20 20 L 35 15" stroke="currentColor" strokeWidth="2" markerEnd="url(#arrowhead)" />
                        <defs>
                            <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="0" refY="3.5" orient="auto">
                                <polygon points="0 0, 10 3.5, 0 7" fill="currentColor" />
                            </marker>
                        </defs>
                    </svg>
                </div>
            </div>

            <div className="macro-matrix__legend">
                <div className="macro-matrix__legend-item">
                    <span className="macro-matrix__legend-dot" style={{ background: 'var(--accent-primary)' }} />
                    <span>Current Regime</span>
                </div>
                <div className="macro-matrix__legend-item">
                    <span className="macro-matrix__legend-line" />
                    <span>Directional Shift</span>
                </div>
            </div>
        </div>
    );
};

export default MacroRegimeMatrix;
