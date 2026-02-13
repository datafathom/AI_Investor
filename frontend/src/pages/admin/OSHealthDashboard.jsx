import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Activity, HardDrive, Cpu as CpuIcon, Database, Clock } from 'lucide-react';

const OSHealthDashboard = () => {
    const [stats, setStats] = useState(null);
    const [health, setHealth] = useState(null);

    useEffect(() => {
        const load = async () => {
            const [sRes, hRes] = await Promise.all([
                apiClient.get('/orchestrator/stats/usage'),
                apiClient.get('/orchestrator/health/heartbeat')
            ]);
            if (sRes.data.success) setStats(sRes.data.data);
            if (hRes.data.success) setHealth(hRes.data.data);
        };
        const interval = setInterval(load, 2000);
        return () => clearInterval(interval);
    }, []);

    if (!stats) return <div className="p-8 text-white">Connecting to Kernel...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-end">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Activity className="text-emerald-500" /> System Health
                    </h1>
                    <p className="text-slate-500">Resource Utilization & Heartbeat</p>
                </div>
                <div className="text-right">
                    <div className="text-2xl font-mono text-emerald-400 font-bold">{health?.latency || '--'}</div>
                    <div className="text-xs text-slate-500 uppercase">Core Latency</div>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
                {/* CPU */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex justify-between items-center mb-4">
                        <div className="flex items-center gap-2 text-slate-400 font-bold"><CpuIcon size={18} /> CPU Load</div>
                        <span className="text-white font-mono">{stats.cpu_usage}%</span>
                    </div>
                    <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                        <div className="h-full bg-blue-500 transition-all duration-500" style={{ width: `${stats.cpu_usage}%` }}></div>
                    </div>
                </div>

                {/* RAM */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex justify-between items-center mb-4">
                        <div className="flex items-center gap-2 text-slate-400 font-bold"><HardDrive size={18} /> Memory</div>
                        <span className="text-white font-mono">{stats.ram_usage}%</span>
                    </div>
                    <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                        <div className="h-full bg-purple-500 transition-all duration-500" style={{ width: `${stats.ram_usage}%` }}></div>
                    </div>
                </div>

                {/* DISK */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex justify-between items-center mb-4">
                        <div className="flex items-center gap-2 text-slate-400 font-bold"><Database size={18} /> Storage</div>
                        <span className="text-white font-mono">{stats.disk_usage}%</span>
                    </div>
                    <div className="h-2 bg-slate-950 rounded-full overflow-hidden">
                        <div className="h-full bg-orange-500 transition-all duration-500" style={{ width: `${stats.disk_usage}%` }}></div>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex items-center justify-between">
                    <div>
                        <div className="text-slate-500 text-xs font-bold uppercase mb-1">Session Token Cost</div>
                        <div className="text-2xl font-bold text-white">${stats.token_usage_cost.toFixed(2)}</div>
                    </div>
                    <div className="text-right">
                        <div className="text-slate-500 text-xs font-bold uppercase mb-1">Active DB Connections</div>
                        <div className="text-2xl font-bold text-white">{stats.db_connections}</div>
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex items-center gap-4">
                    <Clock size={32} className="text-slate-600" />
                    <div>
                        <div className="text-slate-500 text-xs font-bold uppercase mb-1">Sovereign Uptime</div>
                        <div className="text-2xl font-mono text-emerald-400">{stats.uptime}</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OSHealthDashboard;
