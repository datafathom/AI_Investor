import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Route, Network, Globe, Zap, Settings, ArrowRight } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

const SmartOrderRouter = () => {
    const [stats, setStats] = useState([]);
    const [rules, setRules] = useState([]);

    useEffect(() => {
        const loadData = async () => {
            try {
                const [sRes, rRes] = await Promise.all([
                    apiClient.get('/execution/routing/stats'),
                    apiClient.get('/execution/routing/rules')
                ]);
                if (sRes.data.success) setStats(sRes.data.data);
                if (rRes.data.success) setRules(rRes.data.data);
            } catch (e) { console.error(e); }
        };
        loadData();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
             <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Route className="text-cyan-500" /> Smart Order Router
                </h1>
                <p className="text-slate-500">Venue Analysis & Best Execution Logic</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                {/* Latency & Fill Rate Chart */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                        <Network size={16} /> Venue Performance
                    </h3>
                    <div className="h-64">
                         <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={stats}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                                <XAxis dataKey="venue" stroke="#475569" />
                                <YAxis stroke="#475569" />
                                <Tooltip 
                                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#e2e8f0' }}
                                />
                                <Bar dataKey="fill_rate" fill="#06b6d4" name="Fill Rate" />
                                <Bar dataKey="avg_latency_ms" fill="#64748b" name="Latency (ms)" />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Routing Logic */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-white font-bold mb-4 flex items-center gap-2">
                        <Settings size={16} /> Active Routing Rules
                    </h3>
                    <div className="space-y-3">
                        {rules.map(rule => (
                            <div key={rule.id} className="bg-slate-950 p-4 rounded border border-slate-800 flex justify-between items-center group hover:border-cyan-500/50 transition-colors">
                                <div>
                                    <div className="font-bold text-slate-200">{rule.name}</div>
                                    <div className="text-xs font-mono text-slate-500">{rule.condition}</div>
                                </div>
                                <div className={`px-2 py-1 rounded text-xs font-bold ${rule.enabled ? 'bg-green-500/20 text-green-400' : 'bg-slate-800 text-slate-500'}`}>
                                    {rule.enabled ? 'ACTIVE' : 'DISABLED'}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Venue Detail Cards */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
                {stats.map(venue => (
                    <div key={venue.venue} className="bg-slate-900 border border-slate-800 rounded-xl p-4 hover:bg-slate-800/50 transition-colors">
                        <div className="text-xs uppercase font-bold text-slate-500 mb-2">{venue.venue}</div>
                        <div className="text-2xl font-bold text-white mb-1">{(venue.fill_rate * 100).toFixed(0)}%</div>
                        <div className="text-xs text-slate-400 flex justify-between">
                            <span>{venue.avg_latency_ms}ms</span>
                            <span className={venue.reversion_ms < 0 ? 'text-green-400' : 'text-red-400'}>
                                {venue.reversion_ms}ms Rev
                            </span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SmartOrderRouter;
