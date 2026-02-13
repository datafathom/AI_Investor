import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { ShieldAlert, TrendingDown, PieChart, Activity } from 'lucide-react';
import { ResponsiveContainer, PieChart as RePie, Pie, Cell, Tooltip } from 'recharts';

const RiskDashboard = () => {
    const [risk, setRisk] = useState(null);
    const [exposures, setExposures] = useState(null);

    useEffect(() => {
        const load = async () => {
            const [rRes, eRes] = await Promise.all([
                apiClient.get('/risk/summary'),
                apiClient.get('/risk/exposures')
            ]);
            if (rRes.data.success) setRisk(rRes.data.data);
            if (eRes.data.success) setExposures(eRes.data.data);
        };
        load();
    }, []);

    if (!risk || !exposures) return <div>Loading Risk Metrics...</div>;

    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <ShieldAlert className="text-red-500" /> Risk Management Console
                </h1>
                <p className="text-slate-500">Portfolio VaR, Exposure & Limits</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">VaR (99%)</div>
                    <div className="text-3xl font-bold text-red-400">${Math.abs(risk.var_99).toLocaleString()}</div>
                    <div className="text-xs text-slate-500 mt-1">Daily Value at Risk</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Portfolio Beta</div>
                    <div className="text-3xl font-bold text-blue-400">{risk.beta}</div>
                    <div className="text-xs text-slate-500 mt-1">vs S&P 500</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Current Drawdown</div>
                    <div className="text-3xl font-bold text-orange-400">{risk.current_drawdown}%</div>
                    <div className="text-xs text-slate-500 mt-1">From High Water Mark</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Sharpe Ratio</div>
                    <div className="text-3xl font-bold text-green-400">{risk.sharpe}</div>
                    <div className="text-xs text-slate-500 mt-1">Risk-Adjusted Return</div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">Sector Exposure</h3>
                    <div className="h-[300px]">
                        <ResponsiveContainer width="100%" height="100%">
                            <RePie>
                                <Pie
                                    data={Object.entries(exposures.sector).map(([k, v]) => ({ name: k, value: v }))}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={80}
                                    fill="#8884d8"
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {Object.entries(exposures.sector).map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                            </RePie>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">Risk Limits Status</h3>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                            <span className="text-sm font-bold">Max Drawdown Stop</span>
                            <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">HEALTHY</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                            <span className="text-sm font-bold">Gross Exposure</span>
                            <span className="text-xs bg-yellow-500/20 text-yellow-400 px-2 py-1 rounded">WARNING (195%)</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                            <span className="text-sm font-bold">Single Position Max</span>
                            <span className="text-xs bg-green-500/20 text-green-400 px-2 py-1 rounded">HEALTHY</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RiskDashboard;
