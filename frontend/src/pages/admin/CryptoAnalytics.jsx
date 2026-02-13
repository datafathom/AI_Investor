import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { BarChart, AlertTriangle } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const CryptoAnalytics = () => {
    const [risk, setRisk] = useState(null);
    const [pnl, setPnl] = useState([]);

    useEffect(() => {
        const load = async () => {
            const [rRes, pRes] = await Promise.all([
                apiClient.get('/crypto/analytics/risk'),
                apiClient.get('/crypto/analytics/performance')
            ]);
            if (rRes.data.success) setRisk(rRes.data.data);
            if (pRes.data.success) setPnl(pRes.data.data);
        };
        load();
    }, []);

    if (!risk) return <div>Loading Analytics...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <BarChart className="text-indigo-500" /> Crypto Portfolio Analytics
                </h1>
                <p className="text-slate-500">Risk Metrics & Performance Attribution</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Sharpe Ratio</div>
                    <div className="text-3xl font-bold text-emerald-400 font-mono">{risk.sharpe}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Max Drawdown</div>
                    <div className="text-3xl font-bold text-red-500 font-mono">{risk.max_drawdown}%</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">30d Volatility</div>
                    <div className="text-3xl font-bold text-orange-400 font-mono">{risk.volatility_30d}%</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">SPY Correlation</div>
                    <div className="text-3xl font-bold text-blue-400 font-mono">{risk.correlation_spy}</div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-4">P&L History</h3>
                <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={pnl} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                            <defs>
                                <linearGradient id="colorPnl" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                                    <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                                </linearGradient>
                            </defs>
                            <XAxis dataKey="date" stroke="#64748b" />
                            <YAxis stroke="#64748b" />
                            <Tooltip />
                            <Area type="monotone" dataKey="pnl" stroke="#10b981" fillOpacity={1} fill="url(#colorPnl)" />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default CryptoAnalytics;
