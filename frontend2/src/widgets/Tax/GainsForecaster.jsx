import React, { useState, useEffect } from 'react';
import { Calendar, DollarSign, ArrowRight, BarChart } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { useTaxStore } from '../../stores/taxStore';
import './GainsForecaster.css';

/**
 * Capital Gains Forecaster
 * 
 * Visualizes projected tax liability under different
 * harvesting scenarios.
 */
const GainsForecaster = () => {
    const { gainsProjection, projectGains, isLoading } = useTaxStore();
    const [scenario, setScenario] = useState('hold');

    useEffect(() => {
        projectGains('default_portfolio', scenario);
    }, [scenario]);

    // Format data for chart (simple comparison bar since we have aggregated projection)
    const chartData = gainsProjection ? [
        { name: 'Short Term', gains: gainsProjection.net_short_term, tax: gainsProjection.net_short_term * 0.32 },
        { name: 'Long Term', gains: gainsProjection.net_long_term, tax: gainsProjection.net_long_term * 0.15 },
    ] : [];

    return (
        <div className="gains-forecaster-widget h-full flex flex-col p-4 bg-slate-900/40 rounded-xl border border-slate-800">
            <div className="widget-header flex justify-between items-center mb-4">
                <h3 className="flex items-center gap-2 font-bold text-white">
                    <Calendar size={18} className="text-purple-400" /> Capital Gains Forecaster
                </h3>
            </div>

            <div className="scenario-tabs flex gap-2 mb-4 p-1 bg-slate-950 rounded-lg w-fit border border-slate-800/50">
                <button 
                    className={`px-3 py-1.5 text-xs font-bold rounded-md transition-all ${scenario === 'hold' ? 'bg-slate-700 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'}`}
                    onClick={() => setScenario('hold')}
                >
                    Hold Strategy
                </button>
                <button 
                    className={`px-3 py-1.5 text-xs font-bold rounded-md transition-all ${scenario === 'harvest_selective' ? 'bg-indigo-600/80 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'}`}
                    onClick={() => setScenario('harvest_selective')}
                >
                    Harvest Selective
                </button>
                <button 
                    className={`px-3 py-1.5 text-xs font-bold rounded-md transition-all ${scenario === 'harvest_all' ? 'bg-emerald-600/80 text-white shadow-sm' : 'text-slate-500 hover:text-slate-300'}`}
                    onClick={() => setScenario('harvest_all')}
                >
                    Harvest Max
                </button>
            </div>

            <div className="flex-1 flex gap-4 min-h-0">
                <div className="stats-col w-1/3 flex flex-col justify-center space-y-3">
                    <div className="stat-box bg-slate-950/50 p-3 rounded-lg border border-slate-800">
                        <span className="text-[10px] text-slate-500 uppercase tracking-wider block mb-1">Projected Liability</span>
                        <span className="text-2xl font-black text-white">
                            ${gainsProjection?.total_tax_liability.toLocaleString(undefined, { maximumFractionDigits: 0 }) || '0'}
                        </span>
                        <div className="mt-1 text-xs text-slate-400 flex items-center justify-between">
                            Effective Rate: <span className="text-orange-400 font-bold">{(gainsProjection?.effective_rate * 100)?.toFixed(1)}%</span>
                        </div>
                    </div>
                </div>

                <div className="chart-col flex-1 min-h-[120px]">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={chartData} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
                             <defs>
                                <linearGradient id="colorGains" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.8}/>
                                    <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.3} vertical={false} />
                            <XAxis dataKey="name" stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} />
                            <YAxis stroke="#64748b" fontSize={10} tickLine={false} axisLine={false} tickFormatter={(val) => `$${val/1000}k`} />
                            <Tooltip 
                                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f8fafc', fontSize: '12px' }}
                                formatter={(val) => [`$${val.toLocaleString()}`, '']}
                            />
                            <Area type="monotone" dataKey="gains" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorGains)" name="Net Gains" activeDot={{ r: 4 }} />
                            <Area type="monotone" dataKey="tax" stroke="#f97316" fill="#f97316" fillOpacity={0.6} name="Tax Liability" />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default GainsForecaster;

