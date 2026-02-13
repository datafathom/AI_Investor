import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Play, Pause, RotateCw, Settings, BarChart2 } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const BacktestEngine = () => {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [config, setConfig] = useState({ strategy: 'Moving Average Crossover', symbol: 'AAPL', start_date: '2025-01-01', initial_capital: 10000 });

    const runBacktest = async () => {
        setLoading(true);
        try {
            const runRes = await apiClient.post('/backtest/run', config);
            if (runRes.data.success) {
                // Poll for results (mocked immediate return here)
                const res = await apiClient.get(`/backtest/${runRes.data.data.id}/results`);
                if (res.data.success) setResults(res.data.data);
            }
        } catch (e) { console.error(e); } 
        finally { setLoading(false); }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <RotateCw className="text-cyan-500" /> Backtest Engine
                </h1>
                <p className="text-slate-500">Historical Strategy Validation & Optimization</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Configuration Panel */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                        <Settings size={18} /> Configuration
                    </h3>
                    <div className="space-y-4">
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Strategy</label>
                            <select className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white">
                                <option>Moving Average Crossover</option>
                                <option>Mean Reversion (Bollinger)</option>
                                <option>RSI Momentum</option>
                            </select>
                        </div>
                        <div>
                            <label className="block text-xs uppercase text-slate-500 mb-1">Symbol</label>
                            <input 
                                value={config.symbol}
                                onChange={e => setConfig({...config, symbol: e.target.value})}
                                className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white font-mono"
                            />
                        </div>
                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label className="block text-xs uppercase text-slate-500 mb-1">Start Date</label>
                                <input type="date" className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white" />
                            </div>
                            <div>
                                <label className="block text-xs uppercase text-slate-500 mb-1">Capital</label>
                                <input type="number" defaultValue={10000} className="w-full bg-slate-950 border border-slate-700 rounded p-2 text-white" />
                            </div>
                        </div>
                        <button 
                            onClick={runBacktest}
                            disabled={loading}
                            className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-3 rounded mt-4"
                        >
                            {loading ? 'RUNNING SIMULATION...' : 'START BACKTEST'}
                        </button>
                    </div>
                </div>

                {/* Results Panel */}
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    {results ? (
                        <>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                                <div className="bg-slate-950 p-4 rounded border border-slate-800">
                                    <div className="text-xs text-slate-500 uppercase">Total Return</div>
                                    <div className="text-2xl font-bold text-green-400">+{results.metrics.total_return_pct}%</div>
                                </div>
                                <div className="bg-slate-950 p-4 rounded border border-slate-800">
                                    <div className="text-xs text-slate-500 uppercase">Sharpe Ratio</div>
                                    <div className="text-2xl font-bold text-blue-400">{results.metrics.sharpe}</div>
                                </div>
                                <div className="bg-slate-950 p-4 rounded border border-slate-800">
                                    <div className="text-xs text-slate-500 uppercase">Max Drawdown</div>
                                    <div className="text-2xl font-bold text-red-400">{results.metrics.max_drawdown}%</div>
                                </div>
                                <div className="bg-slate-950 p-4 rounded border border-slate-800">
                                    <div className="text-xs text-slate-500 uppercase">Win Rate</div>
                                    <div className="text-2xl font-bold text-purple-400">{(results.metrics.win_rate * 100).toFixed(0)}%</div>
                                </div>
                            </div>

                            <div className="h-[300px]">
                                <ResponsiveContainer width="100%" height="100%">
                                    <AreaChart data={results.equity_curve}>
                                        <defs>
                                            <linearGradient id="colorEquity" x1="0" y1="0" x2="0" y2="1">
                                                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3}/>
                                                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0}/>
                                            </linearGradient>
                                        </defs>
                                        <XAxis dataKey="time" stroke="#475569" />
                                        <YAxis stroke="#475569" domain={['auto', 'auto']} />
                                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                                        <Area type="monotone" dataKey="equity" stroke="#06b6d4" fillOpacity={1} fill="url(#colorEquity)" />
                                    </AreaChart>
                                </ResponsiveContainer>
                            </div>
                        </>
                    ) : (
                        <div className="h-full flex items-center justify-center text-slate-500 flex-col gap-4">
                            <BarChart2 size={48} className="opacity-20" />
                            <p>Run a backtest to visualize performance metrics.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default BacktestEngine;
