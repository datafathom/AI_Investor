import React, { useEffect, useState } from 'react';
import { Flame, TrendingDown, TrendingUp, Clock, Zap } from 'lucide-react';
import { useWeb3Store } from '../../stores/web3Store';

const GasPulse = () => {
    const { gasMetrics, optimalWindow, fetchGasMetrics, fetchOptimalWindow } = useWeb3Store();
    const [selectedChain, setSelectedChain] = useState('ethereum');

    useEffect(() => {
        fetchGasMetrics(selectedChain);
        fetchOptimalWindow(); // Global mostly, but we call it once
        
        const interval = setInterval(() => fetchGasMetrics(selectedChain), 5000); // Poll every 5s
        return () => clearInterval(interval);
    }, [selectedChain]);

    const metrics = gasMetrics[selectedChain];

    if (!metrics) return <div className="flex items-center justify-center h-full text-slate-500">Loading Gas Data...</div>;

    const isHigh = metrics.base_fee_gwei > 50;
    const isLow = metrics.base_fee_gwei < 20;

    return (
        <div className="gas-pulse h-full flex flex-col gap-4">
            {/* Main Gas Gauge */}
            <div className="flex items-center justify-between">
                <div className="flex flex-col">
                    <span className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">Base Fee</span>
                    <div className="flex items-baseline gap-1">
                        <span className={`text-4xl font-black ${isHigh ? 'text-red-500' : isLow ? 'text-green-500' : 'text-yellow-500'}`}>
                            {metrics.base_fee_gwei}
                        </span>
                        <span className="text-slate-500 text-sm font-bold">GWEI</span>
                    </div>
                </div>
                
                <div className={`p-3 rounded-full ${isHigh ? 'bg-red-500/20 text-red-500 animate-pulse' : isLow ? 'bg-green-500/20 text-green-500' : 'bg-yellow-500/20 text-yellow-500'}`}>
                    <Flame size={24} fill="currentColor" className="opacity-80" />
                </div>
            </div>

            {/* Price Estimates */}
            <div className="grid grid-cols-3 gap-2">
                <div className="bg-slate-900/50 p-2 rounded-lg border border-slate-800 text-center">
                    <div className="text-[10px] text-slate-500">Instant</div>
                    <div className="text-sm font-bold text-white">${metrics.estimated_usd.instant}</div>
                </div>
                <div className="bg-slate-900/50 p-2 rounded-lg border border-slate-800 text-center">
                    <div className="text-[10px] text-slate-500">Fast</div>
                    <div className="text-sm font-bold text-white">${metrics.estimated_usd.high}</div>
                </div>
                <div className="bg-slate-900/50 p-2 rounded-lg border border-slate-800 text-center">
                    <div className="text-[10px] text-slate-500">Standard</div>
                    <div className="text-sm font-bold text-white">${metrics.estimated_usd.medium}</div>
                </div>
            </div>

            {/* Optimal Window */}
            {optimalWindow && (
                <div className="bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border border-indigo-500/20 rounded-xl p-3 flex items-center justify-between">
                    <div>
                        <div className="flex items-center gap-1.5 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-0.5">
                            <Clock size={12} /> Optimal Window
                        </div>
                        <div className="text-white text-sm">
                            {new Date(optimalWindow.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} 
                            <span className="text-slate-500 mx-1">-</span>
                            {new Date(optimalWindow.end_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                        </div>
                    </div>
                    <div className="text-right">
                        <div className="text-[10px] text-slate-400">Est. Savings</div>
                        <div className="text-lg font-bold text-green-400">{optimalWindow.expected_savings_percent}%</div>
                    </div>
                </div>
            )}

            {/* Action Queue Button (Mock) */}
            <button className="w-full mt-auto py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white rounded-lg transition-colors border border-slate-700 flex items-center justify-center gap-2 text-sm font-medium group">
                <Zap size={14} className="group-hover:text-yellow-400 transition-colors" />
                Queue Tx for Low Gas
            </button>
        </div>
    );
};

export default GasPulse;
