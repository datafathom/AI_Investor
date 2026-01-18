import React, { useState } from 'react';
import { History, TrendingUp, RefreshCw, Calendar, Target, ScatterChart as ScatterIcon } from 'lucide-react';
import CalendarHeatmap from '../components/Portfolio/CalendarHeatmap';
import MonteCarloFan from '../components/Portfolio/MonteCarloFan';
import TradeScatter from '../components/Portfolio/TradeScatter';

const BacktestPortfolio = () => {
    const [isSimulating, setIsSimulating] = useState(false);
    const [progress, setProgress] = useState(100);

    const runSimulation = () => {
        setIsSimulating(true);
        setProgress(0);
        let p = 0;
        const interval = setInterval(() => {
            p += 5;
            setProgress(p);
            if (p >= 100) {
                clearInterval(interval);
                setIsSimulating(false);
            }
        }, 50);
    };

    const stats = {
        totalReturn: "+42.5%",
        sharpeRatio: "2.14",
        maxDrawdown: "-8.4%",
        winRate: "64%"
    };

    return (
        <div className="backtest-portfolio-page bg-slate-950 min-h-screen text-white font-sans p-6 overflow-y-auto">
            <header className="flex justify-between items-center mb-8">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-indigo-900/30 rounded-xl border border-indigo-500/30">
                        <History size={32} className="text-indigo-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-300 to-cyan-300">
                            Backtesting Engine
                        </h1>
                        <p className="text-slate-400 text-sm">Historical Simulation & Stress Testing</p>
                    </div>
                </div>
                <div className="flex gap-4">
                    <button
                        onClick={runSimulation}
                        disabled={isSimulating}
                        className={`flex items-center gap-2 px-6 py-2 rounded-lg font-bold transition-all interact-hover ${isSimulating ? 'bg-slate-700 cursor-wait' : 'bg-indigo-600 hover:bg-indigo-500 hover:shadow-[0_0_20px_rgba(79,70,229,0.4)]'}`}
                    >
                        {isSimulating ? <RefreshCw className="animate-spin" size={18} /> : <History size={18} />}
                        {isSimulating ? `SIMULATING ${progress}%` : "RUN SIMULATION"}
                    </button>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">

                {/* Left Column: Charts */}
                <div className="lg:col-span-3 flex flex-col gap-6">
                    {/* Monte Carlo Fan */}
                    <div className="glass-panel p-6 bg-slate-900/50 border border-slate-800 rounded-xl h-[400px] flex flex-col glass-premium shadow-indigo-900/20">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold text-slate-200 flex items-center gap-2">
                                <TrendingUp size={20} className="text-cyan-400" />
                                Monte Carlo Projections
                            </h2>
                        </div>
                        <MonteCarloFan />
                    </div>

                    {/* Bottom Row */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-[300px]">
                        <div className="glass-panel p-6 bg-slate-900/50 border border-slate-800 rounded-xl flex flex-col glass-premium shadow-green-900/20">
                            <div className="flex items-center gap-2 mb-4 font-bold text-slate-300">
                                <Calendar size={16} className="text-green-400" /> Return Heatmap
                            </div>
                            <CalendarHeatmap />
                        </div>
                        <div className="glass-panel p-6 bg-slate-900/50 border border-slate-800 rounded-xl flex flex-col glass-premium shadow-purple-900/20">
                            <div className="flex items-center gap-2 mb-4 font-bold text-slate-300">
                                <ScatterIcon size={16} className="text-purple-400" /> Trade Efficiency
                            </div>
                            <TradeScatter />
                        </div>
                    </div>
                </div>

                {/* Right Column: Metrics */}
                <div className="lg:col-span-1 flex flex-col gap-4">
                    <div className="glass-panel p-4 border border-slate-700 rounded-xl bg-gradient-to-br from-slate-900 to-indigo-900/20 glass-premium interact-hover">
                        <h3 className="text-xs uppercase text-slate-500 font-bold mb-1">Total Return</h3>
                        <div className="text-3xl font-mono font-bold text-green-400 text-glow-cyan">{stats.totalReturn}</div>
                    </div>
                    <div className="glass-panel p-4 border border-slate-700 rounded-xl bg-gradient-to-br from-slate-900 to-indigo-900/20">
                        <h3 className="text-xs uppercase text-slate-500 font-bold mb-1">Sharpe Ratio</h3>
                        <div className="text-3xl font-mono font-bold text-indigo-400">{stats.sharpeRatio}</div>
                    </div>
                    <div className="glass-panel p-4 border border-slate-700 rounded-xl bg-gradient-to-br from-slate-900 to-indigo-900/20">
                        <h3 className="text-xs uppercase text-slate-500 font-bold mb-1">Max Drawdown</h3>
                        <div className="text-3xl font-mono font-bold text-red-400">{stats.maxDrawdown}</div>
                    </div>
                    <div className="glass-panel p-4 border border-slate-700 rounded-xl bg-gradient-to-br from-slate-900 to-indigo-900/20">
                        <h3 className="text-xs uppercase text-slate-500 font-bold mb-1">Win Rate</h3>
                        <div className="text-3xl font-mono font-bold text-cyan-400">{stats.winRate}</div>
                    </div>

                    <div className="mt-4 p-4 bg-slate-800/50 rounded-xl border border-slate-700 flex-1">
                        <h3 className="text-xs uppercase text-slate-500 font-bold mb-4">Latest Signals</h3>
                        <div className="space-y-2">
                            {[1, 2, 3, 4].map(i => (
                                <div key={i} className="flex justify-between items-center text-xs p-2 bg-slate-900 rounded border border-slate-800 hover:border-indigo-500/50 transition-all hover:scale-[1.02] interact-hover cursor-pointer group">
                                    <span className="font-bold text-white group-hover:text-cyan-400 transition-colors">SPY</span>
                                    <span className={i % 2 === 0 ? "text-green-400" : "text-red-400"}>{i % 2 === 0 ? "LONG" : "SHORT"}</span>
                                    <span className="font-mono text-slate-500">2m ago</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

            </div>
        </div>
    );
};

export default BacktestPortfolio;
