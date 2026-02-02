/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Risk/OrderImpactSimulator.jsx
 * ROLE: Pre-trade Risk & Greeks Impact Engine
 * PURPOSE: Simulates how a pending order affects portfolio margin,
 *          Greeks (Delta/Gamma), and risk compliance before execution.
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { ShieldAlert, Zap, TrendingUp, BarChart, Info, ShieldCheck } from 'lucide-react';
import useRiskStore from '../../stores/riskStore';
import './OrderImpactSimulator.css';

const OrderImpactSimulator = ({ tradePayload }) => {
    const { orderImpact, fetchOrderImpact } = useRiskStore();

    useEffect(() => {
        if (tradePayload && tradePayload.symbol) {
            fetchOrderImpact(tradePayload);
        }
    }, [tradePayload, fetchOrderImpact]);

    if (!orderImpact) {
        return (
            <div className="impact-simulator flex items-center justify-center">
                <span className="text-slate-500 text-xs animate-pulse">CALCULATING PROJECTION...</span>
            </div>
        );
    }

    const { greeks_impact, margin_impact, risk_verdict, reasons } = orderImpact;

    const getVerdictColor = (verdict) => {
        switch (verdict) {
            case 'SAFE': return 'text-emerald-400';
            case 'CAUTION': return 'text-amber-400';
            case 'DANGER': return 'text-red-400';
            default: return 'text-slate-400';
        }
    };

    return (
        <div className="impact-simulator">
            <div className="impact-simulator__header">
                <div className="flex items-center gap-2">
                    <Zap size={16} className="text-amber-400" />
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Order Impact Simulator</h3>
                </div>
                <div className={`px-2 py-0.5 rounded text-[10px] font-black border ${getVerdictColor(risk_verdict)} border-current bg-current/5`}>
                    {risk_verdict}
                </div>
            </div>

            <div className="impact-simulator__grid">
                <div className="impact-simulator__section">
                    <span className="text-[10px] text-slate-500 uppercase mb-2 block">Greeks Drift</span>
                    <div className="flex flex-col gap-2">
                        <div className="flex justify-between items-center bg-white/5 p-1.5 rounded">
                            <span className="text-[10px] text-slate-400">Δ Delta</span>
                            <span className={`text-[10px] font-mono ${greeks_impact.delta >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                {greeks_impact.delta >= 0 ? '+' : ''}{greeks_impact.delta.toFixed(2)}
                            </span>
                        </div>
                        <div className="flex justify-between items-center bg-white/5 p-1.5 rounded">
                            <span className="text-[10px] text-slate-400">Γ Gamma</span>
                            <span className="text-[10px] font-mono text-blue-400">
                                +{greeks_impact.gamma.toFixed(5)}
                            </span>
                        </div>
                    </div>
                </div>

                <div className="impact-simulator__section">
                    <span className="text-[10px] text-slate-500 uppercase mb-2 block">Margin Impact</span>
                    <div className="flex flex-col gap-2">
                        <div className="flex justify-between items-center bg-white/5 p-1.5 rounded">
                            <span className="text-[10px] text-slate-400">Requirement</span>
                            <span className="text-[10px] font-mono text-white">
                                ${margin_impact.requirement.toLocaleString()}
                            </span>
                        </div>
                        <div className="flex justify-between items-center bg-white/5 p-1.5 rounded">
                            <span className="text-[10px] text-slate-400">Buying Power</span>
                            <span className="text-[10px] font-mono text-white">
                                -${margin_impact.buying_power_used.toLocaleString()}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            <div className="impact-simulator__reasons mt-4">
                {reasons.length > 0 ? (
                    reasons.map((r, i) => (
                        <div key={i} className="flex items-start gap-2 text-[10px] text-amber-500/80 mb-1">
                            <ShieldAlert size={12} className="shrink-0 mt-0.5" />
                            <span>{r}</span>
                        </div>
                    ))
                ) : (
                    <div className="flex items-center gap-2 text-[10px] text-emerald-500/80">
                        <ShieldCheck size={12} />
                        <span>Order satisfies all risk Sentinels.</span>
                    </div>
                )}
            </div>

            <div className="impact-simulator__footer">
                <div className="flex justify-between items-center w-full text-[9px] text-slate-600 font-mono">
                    <span>EST. POST-TRADE LIQUIDITY:</span>
                    <span className="text-white">${margin_impact.available_after.toLocaleString()}</span>
                </div>
            </div>
        </div>
    );
};

export default OrderImpactSimulator;
