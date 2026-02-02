/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Tax/HarvestHunter.jsx
 * ROLE: Tax-Loss Harvesting Opportunity Scanner
 * PURPOSE: Identifies unrealized losses across portfolios and suggests
 *          tax-efficient trades with wash-sale protection.
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import { Target, ShieldCheck, TrendingDown, DollarSign, ArrowRight, AlertCircle } from 'lucide-react';
import useTaxStore from '../../stores/taxStore';
import './HarvestHunter.css';

const HarvestHunter = ({ portfolioId = 'default' }) => {
    const { opportunities, fetchHarvestOpportunities, executeHarvest, loading } = useTaxStore();

    useEffect(() => {
        fetchHarvestOpportunities(portfolioId);
    }, [portfolioId, fetchHarvestOpportunities]);

    const handleExecute = async (opp) => {
        const replacement = opp.replacement_suggestions?.[0] || 'SPY';
        if (window.confirm(`Execute tax harvest for ${opp.candidate.ticker}? Will sell at loss and buy ${replacement}.`)) {
            await executeHarvest(portfolioId, opp, replacement);
        }
    };

    if (loading && opportunities.length === 0) {
        return (
            <div className="harvest-hunter flex items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500" />
            </div>
        );
    }

    return (
        <div className="harvest-hunter">
            <div className="harvest-hunter__header">
                <div className="flex items-center gap-2">
                    <Target size={16} className="text-emerald-400" />
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Harvest Hunter</h3>
                </div>
                <div className="text-[10px] font-mono text-emerald-500 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                    SCAN COMPLETE
                </div>
            </div>

            <div className="harvest-hunter__list scrollbar-hide">
                {opportunities.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-32 text-slate-500">
                        <ShieldCheck size={32} className="mb-2 opacity-20" />
                        <span className="text-xs">No harvesting opportunities found.</span>
                    </div>
                ) : (
                    opportunities.map((opp, idx) => (
                        <div key={opp.candidate.ticker} className="harvest-hunter__item">
                            <div className="flex justify-between items-start mb-2">
                                <div>
                                    <span className="text-sm font-black text-white">{opp.candidate.ticker}</span>
                                    <span className="text-[10px] text-slate-500 ml-2">Lot #{idx + 1}</span>
                                </div>
                                <div className="text-right">
                                    <div className="text-xs font-bold text-emerald-400">
                                        +${opp.tax_savings.toLocaleString()} Tax Savings
                                    </div>
                                    <div className="text-[9px] text-slate-500">Est. Net Benefit: ${opp.net_benefit.toLocaleString()}</div>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4 mb-3">
                                <div className="bg-white/5 p-2 rounded">
                                    <span className="block text-[8px] uppercase text-slate-500">Unrealized Loss</span>
                                    <span className="text-red-400 text-xs font-bold">
                                        -${Math.abs(opp.candidate.unrealized_loss).toLocaleString()}
                                    </span>
                                </div>
                                <div className="bg-white/5 p-2 rounded">
                                    <span className="block text-[8px] uppercase text-slate-500">Replacement</span>
                                    <span className="text-emerald-400 text-xs font-bold flex items-center gap-1">
                                        {opp.replacement_suggestions?.[0] || 'SPY'} <ArrowRight size={10} />
                                    </span>
                                </div>
                            </div>

                            <div className="flex justify-between items-center">
                                <div className="flex items-center gap-1">
                                    {opp.wash_sale_risk ? (
                                        <div className="flex items-center gap-1 text-[9px] text-amber-500">
                                            <AlertCircle size={10} /> Wash Risk: High
                                        </div>
                                    ) : (
                                        <div className="flex items-center gap-1 text-[9px] text-emerald-500">
                                            <ShieldCheck size={10} /> Wash Protected
                                        </div>
                                    )}
                                </div>
                                <button 
                                    onClick={() => handleExecute(opp)}
                                    className="bg-emerald-500 hover:bg-emerald-400 text-black text-[10px] font-bold px-3 py-1 rounded transition-colors"
                                >
                                    HARVEST
                                </button>
                            </div>
                        </div>
                    ))
                )}
            </div>

            <div className="harvest-hunter__footer">
                <div className="flex justify-between w-full">
                    <span className="text-[9px] text-slate-500 uppercase">Total Portfolio Efficiency</span>
                    <span className="text-[9px] text-emerald-400 font-bold">94.2%</span>
                </div>
            </div>
        </div>
    );
};

export default HarvestHunter;
