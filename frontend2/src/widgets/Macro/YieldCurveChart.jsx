/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Macro/YieldCurveChart.jsx
 * ROLE: Interest Rate Term Structure Visualization
 * PURPOSE: Plots Treasury yields from 1M to 30Y. Highlights inversions 
 *          (e.g., 2Y > 10Y) which are historical recession predictors.
 *          
 * INTEGRATION POINTS:
 *     - macroStore: Retrieves yieldCurve data
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import { useMacroStore } from '../../stores/macroStore';
import { 
    LineChart, Line, XAxis, YAxis, CartesianGrid, 
    Tooltip, ResponsiveContainer, AreaChart, Area, ReferenceArea
} from 'recharts';
import './MacroDashboard.css';

const YieldCurveChart = () => {
    const { yieldCurve, fetchYieldCurve, loading } = useMacroStore();

    useEffect(() => {
        if (!yieldCurve) fetchYieldCurve();
    }, [yieldCurve, fetchYieldCurve]);

    if (loading.yieldCurve && !yieldCurve) {
        return <div className="yield-curve yield-curve--loading">Analyzing Yield Curve...</div>;
    }

    if (!yieldCurve?.curve) {
        return <div className="yield-curve yield-curve--empty">No yield data available.</div>;
    }

    const maturitiesOrder = ["1M", "3M", "6M", "1Y", "2Y", "5Y", "7Y", "10Y", "20Y", "30Y"];
    const chartData = maturitiesOrder
        .filter(m => yieldCurve.curve[m] !== undefined)
        .map(m => ({
            name: m,
            yield: yieldCurve.curve[m]
        }));

    const isCurrentlyInverted = yieldCurve.is_inverted;

    return (
        <div className="yield-curve">
            <div className="yield-curve__header">
                <h3 className="yield-curve__title">US Treasury Yield Curve</h3>
                {isCurrentlyInverted && (
                    <span className="yield-curve__badge yield-curve__badge--inverted">INVERTED</span>
                )}
            </div>

            <div className="yield-curve__chart-container">
                <ResponsiveContainer width="100%" height={240}>
                    <AreaChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                        <defs>
                            <linearGradient id="colorYield" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor={isCurrentlyInverted ? "#ff4757" : "#00d4ff"} stopOpacity={0.3}/>
                                <stop offset="95%" stopColor={isCurrentlyInverted ? "#ff4757" : "#00d4ff"} stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                        <XAxis 
                            dataKey="name" 
                            stroke="#888" 
                            fontSize={12} 
                            tickLine={false}
                            axisLine={false}
                        />
                        <YAxis 
                            stroke="#888" 
                            fontSize={12} 
                            tickLine={false} 
                            axisLine={false}
                            domain={['dataMin - 0.5', 'dataMax + 0.5']}
                            tickFormatter={(val) => `${val}%`}
                        />
                        <Tooltip 
                            contentStyle={{ 
                                backgroundColor: '#1a1f2e', 
                                border: '1px solid rgba(255,255,255,0.1)',
                                borderRadius: '8px'
                            }}
                            itemStyle={{ color: '#fff' }}
                            formatter={(value) => [`${value}%`, 'Yield']}
                        />
                        <Area 
                            type="monotone" 
                            dataKey="yield" 
                            stroke={isCurrentlyInverted ? "#ff4757" : "#00d4ff"} 
                            strokeWidth={3}
                            fillOpacity={1} 
                            fill="url(#colorYield)" 
                            animationDuration={1500}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            <div className="yield-curve__stats">
                <div className="yield-curve__stat">
                    <span className="yield-curve__label">10Y-2Y Spread:</span>
                    <span className={`yield-curve__value ${yieldCurve.spread_10y_2y < 0 ? 'negative' : ''}`}>
                        {yieldCurve.spread_10y_2y > 0 ? '+' : ''}{yieldCurve.spread_10y_2y}%
                    </span>
                </div>
                <div className="yield-curve__stat">
                    <span className="yield-curve__label">Regime:</span>
                    <span className="yield-curve__value">REMNANT</span>
                </div>
            </div>
        </div>
    );
};

export default YieldCurveChart;
