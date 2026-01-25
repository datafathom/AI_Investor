import React, { useEffect, useState } from 'react';
import { AlertTriangle, TrendingDown, Calculator, ToggleLeft, ToggleRight, Calendar } from 'lucide-react';
import { useTaxStore } from '../../stores/taxStore';
import './TaxHarvesting.css';

/**
 * Tax-Loss Harvesting Widget
 * 
 * Displays unrealized losses eligible for harvesting
 * with wash-sale protection indicators.
 * Connected to TaxHarvestService.
 */
const TaxLossHarvesting = () => {
    const { 
        harvestCandidates, 
        totalPotentialSavings, 
        autoHarvestEnabled, 
        toggleAutoHarvest,
        fetchHarvestCandidates,
        isLoading
    } = useTaxStore();

    useEffect(() => {
        fetchHarvestCandidates('default_portfolio', 100);
    }, []);

    return (
        <div className="tax-harvesting-widget h-full flex flex-col">
            <div className="widget-header flex justify-between items-center mb-4">
                <h3 className="font-bold text-white">Tax-Loss Harvesting</h3>
                <div 
                    className={`auto-toggle flex items-center gap-2 cursor-pointer ${autoHarvestEnabled ? 'text-green-400' : 'text-slate-500'}`} 
                    onClick={() => toggleAutoHarvest(!autoHarvestEnabled)}
                >
                    {autoHarvestEnabled ? <ToggleRight size={24} className="active" /> : <ToggleLeft size={24} />}
                    <span className="text-sm font-medium">Auto-Harvest</span>
                </div>
            </div>

            <div className="summary-cards grid grid-cols-2 gap-3 mb-4">
                <div className="summary-card bg-slate-900/50 p-3 rounded-lg border border-slate-800 flex items-center gap-3">
                    <div className="p-2 rounded-full bg-red-500/10 text-red-500">
                        <TrendingDown size={18} />
                    </div>
                    <div>
                        <span className="block text-xs text-slate-500 mb-0.5">Harvestable Losses</span>
                        <span className="text-lg font-bold text-red-400">
                            ${Math.abs(harvestCandidates.reduce((sum, c) => sum + c.unrealized_loss, 0)).toLocaleString()}
                        </span>
                    </div>
                </div>
                <div className="summary-card bg-slate-900/50 p-3 rounded-lg border border-slate-800 flex items-center gap-3">
                    <div className="p-2 rounded-full bg-green-500/10 text-green-500">
                        <Calculator size={18} />
                    </div>
                    <div>
                        <span className="block text-xs text-slate-500 mb-0.5">Est. Tax Savings</span>
                        <span className="text-lg font-bold text-green-400">
                            ${totalPotentialSavings.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                        </span>
                    </div>
                </div>
            </div>

            <div className="tax-lots-table flex-1 overflow-hidden flex flex-col bg-slate-900/30 rounded-lg border border-slate-800/50">
                <div className="table-header grid grid-cols-4 p-3 border-b border-slate-800 text-xs font-bold text-slate-400 uppercase tracking-wider">
                    <span>Symbol</span>
                    <span>Hold Period</span>
                    <span className="text-right">Unrealized</span>
                    <span className="text-right">Status</span>
                </div>
                <div className="overflow-y-auto custom-scrollbar flex-1">
                    {isLoading ? (
                        <div className="p-4 text-center text-slate-500">Analyzing portfolio...</div>
                    ) : harvestCandidates.length === 0 ? (
                        <div className="p-4 text-center text-slate-500">No harvestable losses found.</div>
                    ) : (
                        harvestCandidates.map((lot, idx) => (
                            <div key={idx} className={`table-row grid grid-cols-4 p-3 border-b border-slate-800/30 hover:bg-slate-800/50 transition-colors items-center ${lot.wash_sale_risk ? 'opacity-75' : ''}`}>
                                <div className="flex flex-col">
                                    <span className="font-bold text-white">{lot.ticker}</span>
                                    <span className="text-[10px] text-slate-500">Basis: ${lot.cost_basis.toLocaleString()}</span>
                                </div>
                                <div className="text-xs text-slate-400">
                                    {lot.holding_period_days} days
                                    <span className="block text-[10px] text-slate-600">{lot.is_long_term ? 'Long Term' : 'Short Term'}</span>
                                </div>
                                <div className="text-right font-medium text-red-400">
                                    -${lot.unrealized_loss.toLocaleString()}
                                </div>
                                <div className="text-right flex justify-end">
                                    {lot.wash_sale_risk ? (
                                        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded text-[10px] font-bold bg-orange-500/10 text-orange-500 border border-orange-500/20">
                                            <AlertTriangle size={10} /> WASH SALE
                                        </span>
                                    ) : (
                                        <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold bg-green-500/10 text-green-500 border border-green-500/20">
                                            ELIGIBLE
                                        </span>
                                    )}
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>

            <div className="widget-footer mt-3 flex items-center gap-2 text-xs text-slate-500">
                <Calendar size={12} />
                <span>Tax Year 2026 | 30-day wash sale window monitored</span>
            </div>
        </div>
    );
};

export default TaxLossHarvesting;
