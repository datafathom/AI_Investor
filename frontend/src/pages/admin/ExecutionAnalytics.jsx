import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { BarChart2, TrendingDown, Clock, Activity, AlertCircle } from 'lucide-react';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const ExecutionAnalytics = () => {
    const [slippage, setSlippage] = useState(null);
    const [fills, setFills] = useState([]);

    useEffect(() => {
        const loadData = async () => {
            const [sRes, fRes] = await Promise.all([
                apiClient.get('/trading/analytics/slippage'),
                apiClient.get('/trading/analytics/fills')
            ]);
            if (sRes.data.success) setSlippage(sRes.data.data);
            if (fRes.data.success) setFills(fRes.data.data);
        };
        loadData();
    }, []);

    if (!slippage) return <div className="p-8 text-slate-500">Calculating TCA...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
             <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <BarChart2 className="text-indigo-500" /> Execution Analytics
                </h1>
                <p className="text-slate-500">Transaction Cost Analysis (TCA) & Fill Quality</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
                {/* KPI Cards */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Avg. Slippage</div>
                    <div className="text-3xl font-bold text-red-400 flex items-center gap-2">
                        {slippage.avg_slippage_bps} <span className="text-sm font-normal text-slate-500">bps</span>
                    </div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">vs Arrival Price</div>
                    <div className="text-3xl font-bold text-green-400 flex items-center gap-2">
                        {slippage.vs_arrival_price} <span className="text-sm font-normal text-slate-500">bps</span>
                    </div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 lg:col-span-2">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-4">Slippage Distribution</div>
                    <div className="flex items-end gap-2 h-16">
                        {slippage.slippage_distribution.map((dist, i) => (
                            <div key={i} className="flex-1 flex flex-col items-center gap-1 group">
                                <div 
                                    className="w-full bg-indigo-600/50 rounded-t group-hover:bg-indigo-500 transition-colors relative"
                                    style={{ height: `${(dist.count / 50) * 100}%` }}
                                >
                                    <div className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs font-bold text-white opacity-0 group-hover:opacity-100 transition-opacity">
                                        {dist.count}
                                    </div>
                                </div>
                                <div className="text-[10px] text-slate-500 text-center whitespace-nowrap">{dist.range}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Fill Quality */}
            <h3 className="text-xl font-bold text-white mb-4">Fill Quality Grades</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {fills.map(fill => (
                    <div key={fill.grade} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center text-center">
                        <div className={`w-16 h-16 rounded-full flex items-center justify-center text-2xl font-black mb-4 ${
                            fill.grade === 'A' ? 'bg-green-500/20 text-green-400 border-2 border-green-500' :
                            fill.grade === 'B' ? 'bg-blue-500/20 text-blue-400 border-2 border-blue-500' :
                            fill.grade === 'C' ? 'bg-yellow-500/20 text-yellow-400 border-2 border-yellow-500' :
                            'bg-red-500/20 text-red-400 border-2 border-red-500'
                        }`}>
                            {fill.grade}
                        </div>
                        <div className="text-3xl font-bold text-white mb-1">{(fill.percentage * 100).toFixed(0)}%</div>
                        <div className="text-xs text-slate-500">{fill.desc}</div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ExecutionAnalytics;
