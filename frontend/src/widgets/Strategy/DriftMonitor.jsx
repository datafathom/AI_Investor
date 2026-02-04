/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Strategy/DriftMonitor.jsx
 * ROLE: Model Drift & Statistical Fidelity Visualizer
 * PURPOSE: Monitors live performance vs backtest benchmarks to detect 
 *          statistical divergence (Model Drift).
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import { Activity, ShieldAlert, LineChart, Cpu, RefreshCw, BarChart } from 'lucide-react';
import useAlgoStore from '../../stores/algoStore';
import './DriftMonitor.css';

const DriftMonitor = ({ strategyId }) => {
    const { drift, fetchDrift, isLoading } = useAlgoStore();

    useEffect(() => {
        if (strategyId) {
            fetchDrift(strategyId);
            const interval = setInterval(() => fetchDrift(strategyId), 30000);
            return () => clearInterval(interval);
        }
    }, [strategyId, fetchDrift]);

    if (!drift) {
        return (
            <div className="drift-monitor flex items-center justify-center">
                <span className="text-slate-500 text-xs">Awaiting primary stream...</span>
            </div>
        );
    }

    const getStatusColor = (status) => {
        switch (status) {
            case 'critical': return 'var(--color-error-bold)';
            case 'warning': return 'var(--color-warning-bold)';
            case 'nominal': return 'var(--color-success-bold)';
            default: return 'var(--color-neutral-muted)';
        }
    };

    return (
        <div className="drift-monitor">
            <div className="drift-monitor__header">
                <div className="flex items-center gap-2">
                    <Cpu size={16} className="text-blue-400" />
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Statistical Drift Monitor</h3>
                </div>
                <div 
                    className="flex items-center gap-1.5 px-2 py-0.5 rounded-full bg-white/5 border border-white/10"
                    style={{ borderColor: getStatusColor(drift.status) + '44' }}
                >
                    <div 
                        className="w-1.5 h-1.5 rounded-full animate-pulse" 
                        style={{ backgroundColor: getStatusColor(drift.status) }} 
                    />
                    <span className="text-[9px] font-black uppercase" style={{ color: getStatusColor(drift.status) }}>
                        {drift.status}
                    </span>
                </div>
            </div>

            <div className="drift-monitor__main">
                <div className="drift-monitor__score-gauge">
                    <svg viewBox="0 0 100 50">
                        <path 
                            d="M 10 45 A 35 35 0 0 1 90 45" 
                            fill="none" 
                            stroke="rgba(255,255,255,0.05)" 
                            strokeWidth="8" 
                            strokeLinecap="round" 
                        />
                        <path 
                            d="M 10 45 A 35 35 0 0 1 90 45" 
                            fill="none" 
                            stroke={getStatusColor(drift.status)} 
                            strokeWidth="8" 
                            strokeLinecap="round"
                            strokeDasharray="125"
                            strokeDashoffset={125 - (drift.drift_score * 125)}
                            style={{ transition: 'stroke-dashoffset 1s ease-out' }}
                        />
                    </svg>
                    <div className="drift-monitor__score-text">
                        <span className="text-xl font-black text-white">{(drift.drift_score * 100).toFixed(1)}%</span>
                        <span className="text-[8px] text-slate-500 uppercase mt-1">Divergence</span>
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-2 mt-4">
                    <div className="drift-monitor__metric">
                        <div className="flex justify-between items-center mb-1">
                            <span className="text-[9px] text-slate-400">P&L Divergence</span>
                            <span className={`text-[10px] font-bold ${drift.pnl_divergence < 0 ? 'text-red-400' : 'text-emerald-400'}`}>
                                {(drift.pnl_divergence * 100).toFixed(2)}%
                            </span>
                        </div>
                        <div className="drift-monitor__progress-bg">
                            <div 
                                className="drift-monitor__progress-fill" 
                                style={{ 
                                    width: `${Math.abs(drift.pnl_divergence * 100)}%`,
                                    backgroundColor: drift.pnl_divergence < 0 ? 'var(--color-error)' : 'var(--color-success)'
                                }}
                            />
                        </div>
                    </div>
                    <div className="drift-monitor__metric">
                        <div className="flex justify-between items-center mb-1">
                            <span className="text-[9px] text-slate-400">Volatility Gap</span>
                            <span className="text-[10px] font-bold text-blue-400">
                                {(drift.vol_divergence * 100).toFixed(2)}%
                            </span>
                        </div>
                        <div className="drift-monitor__progress-bg">
                            <div 
                                className="drift-monitor__progress-fill bg-blue-500" 
                                style={{ width: `${drift.vol_divergence * 100}%` }}
                            />
                        </div>
                    </div>
                </div>
            </div>

            <div className="drift-monitor__footer">
                <div className="flex items-center gap-3 text-[9px] font-mono text-slate-600">
                    <div className="flex items-center gap-1">
                        <Activity size={10} /> χ²: {drift.metrics?.chi_square.toFixed(2)}
                    </div>
                    <div className="flex items-center gap-1">
                        <BarChart size={10} /> p: {drift.metrics?.p_value.toFixed(3)}
                    </div>
                </div>
                <button 
                    onClick={() => fetchDrift(strategyId)}
                    className="p-1 hover:bg-white/5 rounded transition-colors"
                >
                    <RefreshCw size={12} className={isLoading ? 'animate-spin' : 'text-slate-500'} />
                </button>
            </div>
        </div>
    );
};

export default DriftMonitor;
