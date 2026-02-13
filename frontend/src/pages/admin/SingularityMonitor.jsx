import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Activity, ShieldCheck, AlertTriangle, Lock, Unlock } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

const SingularityMonitor = () => {
    const [status, setStatus] = useState(null);
    const [trajectory, setTrajectory] = useState([]);
    const [thresholds, setThresholds] = useState([]);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const [sRes, tRes, thRes] = await Promise.all([
                apiClient.get('/singularity/status'),
                apiClient.get('/singularity/trajectory'),
                apiClient.get('/singularity/thresholds')
            ]);
            
            if (sRes.data.success) setStatus(sRes.data.data);
            if (tRes.data.success) setTrajectory(tRes.data.data);
            if (thRes.data.success) setThresholds(thRes.data.data);
        } catch (e) {
            console.error(e);
        }
    };

    if (!status) return <div className="p-8 text-slate-500">Connecting to Overwatch...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Activity className="text-red-500 animate-pulse" /> Singularity Monitor
                </h1>
                <p className="text-slate-500">Autonomous Capability Tracking & Safety Thresholds</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Autonomy Level</div>
                    <div className="text-4xl font-black text-white">L{status.autonomy_level}</div>
                    <div className="text-xs text-slate-400 mt-2">Self-directed goals enabled</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Self-Mod Rate</div>
                    <div className="text-2xl font-bold text-purple-400">{status.self_modification_rate}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Safety Protocols</div>
                    <div className="flex items-center gap-2 text-green-400 font-bold">
                        <Lock size={16} /> {status.safety_protocols.toUpperCase()}
                    </div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Human Intervention</div>
                    <div className="text-2xl font-bold text-blue-400">{status.human_intervention_rate}</div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Trajectory Chart */}
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-white font-bold mb-6">Capability Trajectory (Projected)</h3>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <LineChart data={trajectory}>
                                <XAxis dataKey="month" stroke="#475569" />
                                <YAxis stroke="#475569" />
                                <Tooltip 
                                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#1e293b' }}
                                    itemStyle={{ color: '#e2e8f0' }}
                                />
                                <Line type="monotone" dataKey="capability_score" stroke="#8b5cf6" strokeWidth={2} dot={false} />
                                <Line type="monotone" dataKey="resource_usage" stroke="#3b82f6" strokeWidth={2} dot={false} strokeDasharray="5 5" />
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Thresholds */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-white font-bold mb-6">Safety Thresholds</h3>
                    <div className="space-y-6">
                        {thresholds.map((t, i) => (
                            <div key={i}>
                                <div className="flex justify-between text-sm mb-1">
                                    <span className="text-slate-300">{t.name}</span>
                                    <span className={`text-xs font-bold uppercase ${t.status === 'safe' ? 'text-green-500' : 'text-red-500'}`}>{t.status}</span>
                                </div>
                                <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                                     {/* Mock progress calculation */}
                                    <div 
                                        className={`h-full rounded-full ${t.status === 'safe' ? 'bg-blue-500' : 'bg-red-500'}`}
                                        style={{ width: '45%' }}
                                    ></div>
                                </div>
                                <div className="flex justify-between text-xs text-slate-500 mt-1">
                                    <span>{t.current}</span>
                                    <span>Limit: {t.limit}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SingularityMonitor;
