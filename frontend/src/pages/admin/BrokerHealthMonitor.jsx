import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Activity, Server, AlertTriangle, checkCircle } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip } from 'recharts';

const BrokerHealthMonitor = () => {
    const [health, setHealth] = useState([]);

    useEffect(() => {
        const loadData = async () => {
            try {
                const res = await apiClient.get('/broker/health/');
                if (res.data.success) setHealth(res.data.data);
            } catch (e) { console.error(e); }
        };
        loadData();
        const interval = setInterval(loadData, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
             <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Activity className="text-red-500" /> Broker Health Monitor
                </h1>
                <p className="text-slate-500">API Latency, Error Rates & Status</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {health.map(b => (
                    <div key={b.broker} className={`bg-slate-900 border rounded-xl p-6 ${
                        b.status === 'DOWN' ? 'border-red-500' : 
                        b.status === 'DEGRADED' ? 'border-yellow-500' : 
                        'border-slate-800'
                    }`}>
                        <div className="flex justify-between items-start mb-4">
                            <h3 className="font-bold text-white text-lg">{b.broker}</h3>
                            <span className={`px-2 py-1 rounded text-xs font-bold ${
                                b.status === 'OPERATIONAL' ? 'bg-green-500/20 text-green-400' :
                                b.status === 'DEGRADED' ? 'bg-yellow-500/20 text-yellow-400' :
                                'bg-red-500/20 text-red-400'
                            }`}>{b.status}</span>
                        </div>
                        
                        <div className="space-y-4">
                            <div>
                                <div className="flex justify-between text-xs text-slate-500 mb-1">Latency</div>
                                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                                     <div 
                                        className={`h-full ${b.latency_ms > 100 ? 'bg-red-500' : 'bg-green-500'}`}
                                        style={{ width: `${Math.min(b.latency_ms, 200) / 2}%` }}
                                     />
                                </div>
                                <div className="text-right text-xs font-mono text-slate-300 mt-1">{b.latency_ms}ms</div>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                <div>
                                    <div className="text-[10px] uppercase text-slate-500">Error Rate</div>
                                    <div className={`text-lg font-bold ${b.error_rate > 1 ? 'text-red-400' : 'text-slate-200'}`}>
                                        {b.error_rate}%
                                    </div>
                                </div>
                                <div>
                                    <div className="text-[10px] uppercase text-slate-500">Rate Limits</div>
                                    <div className="text-lg font-bold text-slate-200">{b.rate_limit_usage}%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="text-white font-bold mb-4">Global Latency Comparison</h3>
                <div className="h-64">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={health}>
                            <XAxis dataKey="broker" stroke="#475569" />
                            <YAxis stroke="#475569" />
                            <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                            <Bar dataKey="latency_ms" fill="#3b82f6" name="Latency (ms)" />
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
};

export default BrokerHealthMonitor;
