import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Landmark, TrendingUp, DollarSign, Activity } from 'lucide-react';

const TreasuryDashboard = () => {
    const [summary, setSummary] = useState(null);
    const [forecast, setForecast] = useState([]);

    useEffect(() => {
        const load = async () => {
            const [sRes, fRes] = await Promise.all([
                apiClient.get('/treasury/summary'),
                apiClient.get('/treasury/forecast')
            ]);
            if (sRes.data.success) setSummary(sRes.data.data);
            if (fRes.data.success) setForecast(fRes.data.data);
        };
        load();
    }, []);

    if (!summary) return <div>Loading Treasury Data...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Landmark className="text-emerald-500" /> Corporate Treasury
                </h1>
                <p className="text-slate-500">Cash Management & Liquidity Forecasting</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Total Cash</div>
                    <div className="text-3xl font-bold text-white font-mono">${summary.total_cash.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Buying Power</div>
                    <div className="text-3xl font-bold text-blue-400 font-mono">${summary.buying_power.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Settled Cash</div>
                    <div className="text-3xl font-bold text-emerald-400 font-mono">${summary.settled_cash.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Liquidity Ratio</div>
                    <div className="text-3xl font-bold text-purple-400">{summary.liquidity_ratio}x</div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <TrendingUp className="text-blue-500" /> 30-Day Cash Forecast
                    </h3>
                    <div className="space-y-4">
                        {forecast.map((f, i) => (
                            <div key={i} className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                                <span className="text-slate-300">{f.date}</span>
                                <div className="flex items-center gap-2">
                                    <div className="h-2 w-24 bg-slate-800 rounded-full overflow-hidden">
                                        <div className="h-full bg-blue-500" style={{ width: '70%' }}></div>
                                    </div>
                                    <span className="text-white font-mono font-bold">${f.balance.toLocaleString()}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <Activity className="text-orange-500" /> Liquidity Alerts
                    </h3>
                    <div className="p-4 bg-emerald-900/20 border border-emerald-900/50 rounded flex items-center gap-3">
                        <DollarSign className="text-emerald-500" />
                        <div>
                            <div className="font-bold text-emerald-400">Optimal Liquidity</div>
                            <div className="text-xs text-slate-400">Cash reserves are sufficient for projected 30-day burn rate.</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TreasuryDashboard;
