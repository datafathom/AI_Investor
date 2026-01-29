import React from 'react';
import { Target, BarChart3, TrendingUp, Search } from 'lucide-react';
import VolatilitySurface from '../components/Options/VolatilitySurface';
import StrategyBuilder from '../components/Options/StrategyBuilder';
import GreeksDashboard from '../components/Options/GreeksDashboard';

import './OptionsAnalytics.css';

const OptionsAnalytics = () => {
    return (
        <div className="options-analytics-page bg-slate-950 min-h-screen text-slate-300 p-4 flex flex-col gap-4">
            {/* Header */}
            <div className="flex justify-between items-center mb-1">
                <div className="flex items-center gap-4">
                    <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
                        <Target size={24} className="text-indigo-400" />
                    </div>
                    <div>
                        <h1 className="text-2xl font-bold font-display text-white">Options Analytics</h1>
                        <p className="text-slate-400 text-xs font-mono">Derivatives Pricing & Risk Engine</p>
                    </div>
                </div>

                <div className="flex gap-2">
                    <div className="bg-slate-900 border border-slate-700 px-3 py-1 rounded-lg text-right interact-hover transition-all">
                        <span className="block text-[9px] text-slate-500 uppercase">Implied Vol (30D)</span>
                        <span className="text-base font-mono text-white text-glow-cyan">18.4%</span>
                    </div>
                    <div className="bg-slate-900 border border-slate-700 px-3 py-1 rounded-lg text-right">
                        <span className="block text-[9px] text-slate-500 uppercase">Put/Call Ratio</span>
                        <span className="text-base font-mono text-emerald-400">0.85</span>
                    </div>
                </div>
            </div>

            {/* Top Row: Greeks & Exposure */}
            <div className="glass-panel p-3 bg-slate-900/50 border border-slate-800 rounded-xl glass-premium shadow-indigo-900/20">
                <h3 className="text-xs font-bold text-slate-500 uppercase px-1 mb-2 flex items-center gap-2">
                    <TrendingUp size={12} /> Portfolio Exposure (Greeks)
                </h3>
                <GreeksDashboard />
            </div>

            {/* Main Content Info Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 flex-1">

                {/* Left: Volatility Surface */}
                <div className="lg:col-span-7 glass-panel p-4 bg-slate-900/40 border border-slate-800 rounded-xl flex flex-col glass-premium shadow-sky-900/20">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-lg font-bold text-white flex items-center gap-2">
                            <BarChart3 size={20} className="text-sky-400" /> Volatility Surface
                        </h3>
                        <div className="flex gap-2">
                            {['SPY', 'QQQ', 'IWM'].map(t => (
                                <button key={t} className="px-3 py-1 bg-slate-800 hover:bg-slate-700 rounded text-xs font-bold transition-all interact-hover">{t}</button>
                            ))}
                        </div>
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <VolatilitySurface />
                    </div>
                </div>

                {/* Right: Strategy Builder */}
                <div className="lg:col-span-5 glass-panel p-6 bg-slate-900/40 border border-slate-800 rounded-xl flex flex-col glass-premium shadow-amber-900/20">
                    <div className="flex justify-between items-center mb-4">
                        <h3 className="text-lg font-bold text-white flex items-center gap-2">
                            <Search size={20} className="text-amber-400" /> Strategy Builder
                        </h3>
                    </div>
                    <div className="flex-1 overflow-hidden">
                        <StrategyBuilder />
                    </div>
                </div>

            </div>
        </div>
    );
};

export default OptionsAnalytics;
