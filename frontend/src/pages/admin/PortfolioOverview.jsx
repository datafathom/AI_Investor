import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { PieChart, TrendingUp, DollarSign, Activity } from 'lucide-react';
import { Pie, PieChart as RechartsPie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

const PortfolioOverview = () => {
    const [summary, setSummary] = useState(null);
    const [holdings, setHoldings] = useState([]);

    useEffect(() => {
        const load = async () => {
            const [sRes, hRes] = await Promise.all([
                apiClient.get('/portfolio/summary'),
                apiClient.get('/portfolio/holdings')
            ]);
            if (sRes.data.success) setSummary(sRes.data.data);
            if (hRes.data.success) setHoldings(hRes.data.data);
        };
        load();
    }, []);

    if (!summary) return <div>Loading Portfolio Data...</div>;

    const allocationData = Object.entries(summary.allocation).map(([name, value]) => ({ name, value }));
    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <PieChart className="text-blue-500" /> Portfolio Overview
                </h1>
                <p className="text-slate-500">Asset Allocation & Performance Metrics</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Net Liquidation Value</div>
                    <div className="text-3xl font-bold text-white font-mono">${summary.nlv.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Daily P&L</div>
                    <div className={`text-3xl font-bold font-mono ${summary.daily_pl >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                        {summary.daily_pl >= 0 ? '+' : ''}${summary.daily_pl.toLocaleString()}
                    </div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">YTD P&L</div>
                    <div className={`text-3xl font-bold font-mono ${summary.ytd_pl >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                        {summary.ytd_pl >= 0 ? '+' : ''}${summary.ytd_pl.toLocaleString()}
                    </div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Buying Power</div>
                    <div className="text-3xl font-bold text-purple-400 font-mono">${summary.buying_power.toLocaleString()}</div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">Asset Allocation</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <RechartsPie
                                data={allocationData}
                                cx="50%"
                                cy="50%"
                                innerRadius={60}
                                outerRadius={80}
                                fill="#8884d8"
                                paddingAngle={5}
                                dataKey="value"
                            >
                                {allocationData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </RechartsPie>
                        </ResponsiveContainer>
                    </div>
                    <div className="flex justify-center gap-4 text-xs">
                        {allocationData.map((entry, index) => (
                            <div key={index} className="flex items-center gap-1">
                                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: COLORS[index % COLORS.length] }}></span>
                                <span className="text-slate-300">{entry.name} ({entry.value}%)</span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="p-4 bg-slate-950 border-b border-slate-800 font-bold text-white flex items-center gap-2">
                        <TrendingUp size={18} className="text-emerald-500" /> Top Holdings
                    </div>
                    <table className="w-full text-left">
                        <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                            <tr>
                                <th className="p-4">Symbol</th>
                                <th className="p-4">Qty</th>
                                <th className="p-4">Price</th>
                                <th className="p-4">Market Value</th>
                                <th className="p-4">Gain %</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            {holdings.map(h => (
                                <tr key={h.symbol} className="border-b border-slate-800 hover:bg-slate-800/50">
                                    <td className="p-4 font-bold text-white">{h.symbol}</td>
                                    <td className="p-4 text-slate-300">{h.qty}</td>
                                    <td className="p-4 font-mono text-slate-400">${h.price.toFixed(2)}</td>
                                    <td className="p-4 font-mono font-bold text-white">${h.market_value.toLocaleString()}</td>
                                    <td className={`p-4 font-bold ${h.gain_pct >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                        {h.gain_pct > 0 ? '+' : ''}{h.gain_pct}%
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default PortfolioOverview;
