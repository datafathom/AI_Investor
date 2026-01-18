import React from 'react';
import { X, TrendingUp, TrendingDown, DollarSign, Shield } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const SenatorModal = ({ senator, onClose }) => {
    if (!senator) return null;

    // Mock Performance Data
    const data = Array.from({ length: 30 }, (_, i) => ({
        day: i,
        portfolio: 100 + Math.random() * 20 + (i * 0.5),
        sp500: 100 + Math.random() * 10 + (i * 0.2)
    }));

    return (
        <div className="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 animate-in fade-in duration-200">
            <div className="bg-[#0f172a] border border-amber-500/30 rounded-xl w-full max-w-4xl shadow-2xl relative overflow-hidden flex flex-col max-h-[90vh]">

                {/* Header */}
                <div className="p-6 border-b border-amber-500/20 bg-amber-900/10 flex justify-between items-start">
                    <div className="flex gap-4">
                        <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center border-2 border-amber-400 shadow-[0_0_15px_rgba(251,191,36,0.5)]">
                            <span className="text-2xl font-bold text-amber-100">{senator.party}</span>
                        </div>
                        <div>
                            <h2 className="text-2xl font-bold text-white mb-1">Senator {senator.id}</h2>
                            <div className="flex gap-3 text-xs font-mono text-amber-500/80">
                                <span className="px-2 py-0.5 bg-amber-500/10 rounded border border-amber-500/20">COMMITTEE: FINANCE</span>
                                <span className="px-2 py-0.5 bg-amber-500/10 rounded border border-amber-500/20">STATE: NY</span>
                            </div>
                        </div>
                    </div>
                    <button onClick={onClose} className="text-slate-400 hover:text-white hover:bg-white/10 p-2 rounded-full transition-colors">
                        <X size={24} />
                    </button>
                </div>

                {/* Body */}
                <div className="p-6 overflow-y-auto grid grid-cols-1 lg:grid-cols-3 gap-6">

                    {/* Main Chart */}
                    <div className="lg:col-span-2 space-y-6">
                        <div className="glass-panel-gold p-4 h-80">
                            <h3 className="text-sm font-bold text-slate-300 mb-4 flex items-center gap-2">
                                <TrendingUp size={16} className="text-green-400" /> Alpha Generation vs S&P 500
                            </h3>
                            <ResponsiveContainer width="100%" height="100%">
                                <AreaChart data={data}>
                                    <defs>
                                        <linearGradient id="colorPort" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                                            <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                                        </linearGradient>
                                    </defs>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                                    <XAxis dataKey="day" hide />
                                    <YAxis domain={['auto', 'auto']} fontSize={10} tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} />
                                    <Tooltip contentStyle={{ backgroundColor: '#1e293b', borderColor: '#475569' }} />
                                    <Area type="monotone" dataKey="portfolio" stroke="#f59e0b" strokeWidth={2} fillOpacity={1} fill="url(#colorPort)" name="Senator Portfolio" />
                                    <Area type="monotone" dataKey="sp500" stroke="#64748b" strokeWidth={2} strokeDasharray="5 5" fill="transparent" name="S&P 500" />
                                </AreaChart>
                            </ResponsiveContainer>
                        </div>

                        {/* Recent Suspicious Trades */}
                        <div>
                            <h3 className="text-sm font-bold text-slate-300 mb-3">Detected Anomalies</h3>
                            <div className="space-y-2">
                                {[1, 2, 3].map(i => (
                                    <div key={i} className="flex items-center justify-between p-3 bg-red-900/10 border border-red-500/20 rounded hover:bg-red-900/20 transition-colors">
                                        <div className="flex items-center gap-3">
                                            <Shield size={16} className="text-red-400" />
                                            <div>
                                                <div className="text-white font-bold text-sm">Bought $500k NVDA Calls</div>
                                                <div className="text-[10px] text-slate-500">2 days before CHIPS Act vote</div>
                                            </div>
                                        </div>
                                        <div className="text-right">
                                            <div className="text-green-400 font-mono font-bold">+142%</div>
                                            <div className="text-[10px] text-slate-500">Unrealized</div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* Stats Sidebar */}
                    <div className="space-y-4">
                        <div className="p-4 bg-slate-800/50 rounded-lg border border-slate-700">
                            <label className="text-xs text-slate-500 uppercase font-bold">Total Net Worth</label>
                            <div className="text-2xl font-mono text-white font-bold flex items-center gap-1">
                                <DollarSign size={20} className="text-green-500" /> 142.5M
                            </div>
                        </div>
                        <div className="p-4 bg-slate-800/50 rounded-lg border border-slate-700">
                            <label className="text-xs text-slate-500 uppercase font-bold">Win Rate (YTD)</label>
                            <div className="text-2xl font-mono text-amber-400 font-bold">94.2%</div>
                            <div className="text-[10px] text-slate-500 mt-1">Vs Market Avg: 62%</div>
                        </div>
                        <div className="p-4 bg-slate-800/50 rounded-lg border border-slate-700">
                            <label className="text-xs text-slate-500 uppercase font-bold">Top Sector</label>
                            <div className="text-xl text-white font-bold">Defense & Aero</div>
                            <div className="w-full bg-slate-700 h-1.5 rounded-full mt-2">
                                <div className="bg-amber-500 h-1.5 rounded-full w-[75%]"></div>
                            </div>
                        </div>

                        <button className="w-full py-3 bg-amber-600 hover:bg-amber-500 text-black font-bold rounded-lg transition-colors shadow-lg shadow-amber-900/20">
                            CLONE PORTFOLIO
                        </button>
                    </div>

                </div>
            </div>
        </div>
    );
};

export default SenatorModal;
