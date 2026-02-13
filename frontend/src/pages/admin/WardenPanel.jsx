import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Target, Ban, Globe } from 'lucide-react';

const WardenPanel = () => {
    const [threats, setThreats] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/warden/threats');
            if (res.data.success) setThreats(res.data.data);
        };
        load();
        const interval = setInterval(load, 5000); // Live updates
        return () => clearInterval(interval);
    }, []);

    const blockIp = async (ip) => {
        await apiClient.post(`/warden/actions/block`, null, { params: { ip } });
        // Refresh?
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Target className="text-red-500" /> Warden Control Panel
                </h1>
                <p className="text-slate-500">Real-time Threat Neutralization & IP Blocking</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="p-4 bg-slate-950 font-bold text-white border-b border-slate-800 flex justify-between items-center">
                        <span className="flex items-center gap-2"><ActivityIcon /> Live Threat Stream</span>
                        <span className="text-xs bg-red-600 px-2 py-1 rounded text-white animate-pulse">LIVE</span>
                    </div>
                    <div className="h-[400px] overflow-y-auto">
                        <table className="w-full text-left">
                            <thead className="text-slate-500 text-xs uppercase bg-slate-950 sticky top-0">
                                <tr>
                                    <th className="p-4">Type</th>
                                    <th className="p-4">Source</th>
                                    <th className="p-4">Location</th>
                                    <th className="p-4">Status</th>
                                    <th className="p-4">Action</th>
                                </tr>
                            </thead>
                            <tbody className="text-sm">
                                {threats.map(t => (
                                    <tr key={t.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                        <td className="p-4 font-bold text-white">{t.type.replace('_', ' ')}</td>
                                        <td className="p-4 font-mono text-cyan-400">{t.source}</td>
                                        <td className="p-4 flex items-center gap-2">
                                            <Globe size={14} className="text-slate-500" /> {t.location}
                                        </td>
                                        <td className="p-4">
                                            <span className={`px-2 py-1 rounded text-xs font-bold ${
                                                t.status === 'BLOCKED' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400'
                                            }`}>
                                                {t.status}
                                            </span>
                                        </td>
                                        <td className="p-4">
                                            {t.status !== 'BLOCKED' && (
                                                <button 
                                                    onClick={() => blockIp(t.source)}
                                                    className="text-xs bg-red-900/30 hover:bg-red-900/50 text-red-400 border border-red-900/50 px-3 py-1 rounded flex items-center gap-1"
                                                >
                                                    <Ban size={12} /> BLOCK
                                                </button>
                                            )}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">Defense Stats</h3>
                    <div className="space-y-4">
                        <div className="p-4 bg-slate-950 rounded border border-slate-800 text-center">
                            <div className="text-3xl font-bold text-white">142</div>
                            <div className="text-xs text-slate-500 uppercase">Attacks Blocked (24h)</div>
                        </div>
                        <div className="p-4 bg-slate-950 rounded border border-slate-800 text-center">
                            <div className="text-3xl font-bold text-white">12</div>
                            <div className="text-xs text-slate-500 uppercase">Banned IPs</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

const ActivityIcon = () => (
    <svg className="w-4 h-4 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
    </svg>
);

export default WardenPanel;
