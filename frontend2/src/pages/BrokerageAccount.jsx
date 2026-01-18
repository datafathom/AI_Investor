import React, { useState, useEffect } from 'react';
import { brokerageService } from '../services/brokerageService';
import { TrendingUp, DollarSign, Activity, PieChart, Wallet, Zap } from 'lucide-react';
import { SimpleLineChart } from '../components/Charts/SimpleCharts';
import MarginTachometer from '../components/Brokerage/MarginTachometer';
import TaxLotOptimizer from '../components/Brokerage/TaxLotOptimizer';
import PLWaterfall from '../components/Brokerage/PLWaterfall';
import './BrokerageAccount.css';

const BrokerageAccount = () => {
    const [summary, setSummary] = useState(brokerageService.getAccountSummary());
    const [equityData, setEquityData] = useState(generateMockEquity());

    // ... Subscription logic (omitted for brevity in demo update, keeping mock data flow if needed)

    const formatCurrency = (val) => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency', currency: 'USD', minimumFractionDigits: 2
        }).format(val);
    };

    return (
        <div className="brokerage-container bg-slate-950 min-h-screen text-slate-200 p-6 flex flex-col gap-6 font-sans">

            {/* Header / Hero Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="metric-card glass-panel p-6 relative overflow-hidden bg-slate-900/40 border border-slate-800 rounded-xl">
                    <div className="absolute top-0 right-0 p-4 opacity-10"><DollarSign size={64} /></div>
                    <label className="text-emerald-400 uppercase text-xs font-bold tracking-wider mb-2 block">Total Liquidity</label>
                    <div className="text-3xl font-mono font-bold text-white text-glow-cyan">
                        {formatCurrency(summary.liquidity)}
                    </div>
                </div>

                <div className="metric-card glass-panel p-6 relative overflow-hidden bg-slate-900/40 border border-slate-800 rounded-xl">
                    <div className="absolute top-0 right-0 p-4 opacity-10"><Activity size={64} /></div>
                    <label className="text-secondary uppercase text-xs font-bold tracking-wider mb-2 block">Day P&L</label>
                    <div className={`text-3xl font-mono font-bold ${summary.dailyPL >= 0 ? 'text-green-400 text-glow-cyan' : 'text-red-400 text-glow-red'}`}>
                        {summary.dailyPL >= 0 ? '+' : ''}{formatCurrency(summary.dailyPL)}
                    </div>
                </div>

                {/* New Feature: Margin Tachometer */}
                <div className="col-span-2 glass-panel p-2 bg-slate-900/40 border border-slate-800 rounded-xl flex items-center justify-center relative overflow-hidden glass-premium shadow-indigo-900/20">
                    <MarginTachometer />
                </div>
            </div>

            {/* Main Grid */}
            <div className="grid grid-cols-12 gap-6 flex-1">

                {/* Left Column: Chart & Positions */}
                <div className="col-span-12 lg:col-span-8 flex flex-col gap-6">
                    {/* Performance Chart */}
                    <div className="glass-panel p-6 bg-slate-900/40 border border-slate-800 rounded-xl h-[350px] glass-premium shadow-green-900/20">
                        <div className="flex justify-between items-center mb-4">
                            <h3 className="font-bold text-lg flex items-center gap-2 text-white">
                                <TrendingUp className="text-green-400" /> Account Performance
                            </h3>
                        </div>
                        <div className="h-[280px] w-full">
                            <SimpleLineChart data={equityData} dataKey="Value" color="#4ade80" />
                        </div>
                    </div>

                    {/* Positions Table */}
                    <div className="glass-panel p-6 bg-slate-900/40 border border-slate-800 rounded-xl flex-1 glass-premium shadow-slate-900/20">
                        <h3 className="font-bold text-lg mb-4 flex items-center gap-2 text-white">
                            <Wallet className="text-blue-400" /> Holdings
                        </h3>
                        <table className="w-full text-left font-mono text-sm text-slate-400">
                            <thead>
                                <tr className="border-b border-slate-700 uppercase text-xs">
                                    <th className="pb-3 text-slate-500">Symbol</th>
                                    <th className="pb-3 text-right text-slate-500">Qty</th>
                                    <th className="pb-3 text-right text-slate-500">Avg Cost</th>
                                    <th className="pb-3 text-right text-slate-500">Market Value</th>
                                    <th className="pb-3 text-right text-slate-500">P/L Open</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-slate-800">
                                {summary.positions.map((pos) => (
                                    <tr key={pos.symbol} className="hover:bg-slate-800/50 transition-all cursor-default group border-l-4 border-l-transparent hover:border-l-indigo-500/50 interact-hover">
                                        <td className="py-3 font-bold text-white">{pos.symbol}</td>
                                        <td className="py-3 text-right">{pos.qty}</td>
                                        <td className="py-3 text-right">${pos.avgPrice.toFixed(2)}</td>
                                        <td className="py-3 text-right text-white">${(pos.qty * pos.currentPrice).toLocaleString()}</td>
                                        <td className={`py-3 text-right font-bold ${pos.pl >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                                            {pos.pl >= 0 ? '+' : ''}{formatCurrency(pos.pl)}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                {/* Right Column: New Features */}
                <div className="col-span-12 lg:col-span-4 flex flex-col gap-6">
                    {/* Tax Optimizer */}
                    <div className="glass-panel p-4 bg-slate-900/40 border border-slate-800 rounded-xl h-[300px] glass-premium shadow-amber-900/20">
                        <TaxLotOptimizer />
                    </div>

                    {/* Waterfall Attribution */}
                    <div className="glass-panel p-4 bg-slate-900/40 border border-slate-800 rounded-xl h-[300px] glass-premium shadow-blue-900/20">
                        <PLWaterfall />
                    </div>
                </div>

            </div>
        </div>
    );
};

// Mock Helper
const generateMockEquity = () => {
    let eq = 100000;
    return Array.from({ length: 50 }, (_, i) => {
        eq = eq * (1 + (Math.random() - 0.45) * 0.01);
        return { name: i, Value: eq };
    });
}

export default BrokerageAccount;
