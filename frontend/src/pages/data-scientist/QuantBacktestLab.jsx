import React, { useState } from 'react';
import { quantService } from '../../services/quantService';
import { StrategyBuilder } from '../../components/builders/StrategyBuilder';
import { toast } from 'sonner';
import { FlaskConical, TrendingUp, Activity, GitBranch } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const QuantBacktestLab = () => {
    const [results, setResults] = useState(null);
    const [monteCarlo, setMonteCarlo] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleRunBacktest = async (strategy) => {
        try {
            setLoading(true);
            const res = await quantService.runBacktest(strategy);
            setResults(res);
            
            // Auto run Monte Carlo
            const mcParams = { 
                start_price: res.equity_curve[res.equity_curve.length-1].equity,
                days: 252,
                mu: 0.0005,
                sigma: 0.015,
                paths: 200
            };
            const mc = await quantService.runMonteCarlo(mcParams);
            setMonteCarlo(mc);
            
            toast.success("Backtest complete");
        } catch (e) {
            toast.error("Backtest failed");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 h-full flex flex-col bg-slate-950 text-slate-200 overflow-y-auto">
             <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <FlaskConical className="text-purple-500" /> Quant Backtest Lab
                    </h1>
                    <p className="text-slate-400 mt-2">Design, test, and validate algorithmic strategies.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left: Strategy Builder */}
                <div className="lg:col-span-1">
                    <StrategyBuilder onRun={handleRunBacktest} />
                    
                    {results && (
                        <div className="mt-6 bg-slate-900 border border-slate-800 rounded-xl p-6">
                            <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider mb-4">Metrics</h3>
                            <div className="grid grid-cols-2 gap-4">
                                <div className="p-3 bg-slate-800 rounded border border-slate-700">
                                    <div className="text-xs text-slate-500">Total Return</div>
                                    <div className={results.metrics.total_return > 0 ? "text-emerald-400 font-bold" : "text-red-400 font-bold"}>
                                        {results.metrics.total_return}%
                                    </div>
                                </div>
                                <div className="p-3 bg-slate-800 rounded border border-slate-700">
                                    <div className="text-xs text-slate-500">Max Drawdown</div>
                                    <div className="text-red-400 font-bold">{results.metrics.max_drawdown}%</div>
                                </div>
                                <div className="p-3 bg-slate-800 rounded border border-slate-700">
                                    <div className="text-xs text-slate-500">Sharpe Ratio</div>
                                    <div className="text-white font-bold">{results.metrics.sharpe_ratio}</div>
                                </div>
                                <div className="p-3 bg-slate-800 rounded border border-slate-700">
                                    <div className="text-xs text-slate-500">Win Rate</div>
                                    <div className="text-white font-bold">{results.metrics.win_rate}%</div>
                                </div>
                            </div>
                        </div>
                    )}
                </div>

                {/* Right: Charts */}
                <div className="lg:col-span-2 space-y-6">
                    {/* Equity Curve */}
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 min-h-[300px] flex flex-col">
                        <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider mb-4 flex items-center gap-2">
                            <TrendingUp size={16} /> Equity Curve
                        </h3>
                        {results ? (
                             <div className="flex-1">
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart data={results.equity_curve}>
                                        <XAxis dataKey="date" hide />
                                        <YAxis domain={['auto', 'auto']} stroke="#475569" fontSize={12} />
                                        <Tooltip contentStyle={{backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9'}} />
                                        <Line type="monotone" dataKey="equity" stroke="#8b5cf6" strokeWidth={2} dot={false} />
                                    </LineChart>
                                </ResponsiveContainer>
                             </div>
                        ) : (
                            <div className="flex-1 flex items-center justify-center text-slate-600 border border-dashed border-slate-800 rounded">
                                Run a strategy to see performance.
                            </div>
                        )}
                    </div>

                    {/* Monte Carlo */}
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 min-h-[300px] flex flex-col">
                        <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider mb-4 flex items-center gap-2">
                             <GitBranch size={16} /> Monte Carlo Simulation (Forward)
                        </h3>
                        {monteCarlo ? (
                             <div className="flex-1">
                                <ResponsiveContainer width="100%" height="100%">
                                    <LineChart>
                                        <XAxis hide />
                                        <YAxis domain={['auto', 'auto']} stroke="#475569" fontSize={12} />
                                        {monteCarlo.paths.map((path, i) => (
                                            <Line key={i} data={path.map((v, idx) => ({ idx, val: v }))} dataKey="val" stroke="#3b82f6" strokeOpacity={0.1} dot={false} />
                                        ))}
                                    </LineChart>
                                </ResponsiveContainer>
                                <div className="mt-2 text-xs text-slate-500 text-center">
                                    Estimated 95th Percentile Outcome: ${monteCarlo.percentiles.p95}
                                </div>
                             </div>
                        ) : (
                             <div className="flex-1 flex items-center justify-center text-slate-600 border border-dashed border-slate-800 rounded">
                                Simulation pending results.
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default QuantBacktestLab;
