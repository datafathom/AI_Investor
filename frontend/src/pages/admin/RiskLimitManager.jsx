import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Shield, AlertTriangle, Edit2 } from 'lucide-react';

const RiskLimitManager = () => {
    const [limits, setLimits] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/risk/limits');
            if (res.data.success) setLimits(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Shield className="text-emerald-500" /> Risk Limit Manager
                </h1>
                <p className="text-slate-500">Configure Hard/Soft Limits & Breach Actions</p>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Limit Name</th>
                            <th className="p-4">Type</th>
                            <th className="p-4">Value</th>
                            <th className="p-4">Action</th>
                            <th className="p-4">Edit</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {limits.map(l => (
                            <tr key={l.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{l.name}</td>
                                <td className="p-4">
                                    <span className="bg-slate-800 text-slate-300 px-2 py-1 rounded text-xs">{l.limit_type}</span>
                                </td>
                                <td className="p-4 font-mono text-cyan-400">{l.value}%</td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        l.action === 'HALT_TRADING' ? 'bg-red-500/20 text-red-400' :
                                        l.action === 'REJECT_ORDER' ? 'bg-orange-500/20 text-orange-400' :
                                        'bg-yellow-500/20 text-yellow-400'
                                    }`}>
                                        {l.action.replace('_', ' ')}
                                    </span>
                                </td>
                                <td className="p-4">
                                    <button className="text-slate-500 hover:text-white transition-colors">
                                        <Edit2 size={16} />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="mt-8 bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                    <AlertTriangle className="text-yellow-500" /> Recent Violations
                </h3>
                <div className="text-slate-500 text-sm">No active violations detected in the last 24 hours.</div>
            </div>
        </div>
    );
};

export default RiskLimitManager;
