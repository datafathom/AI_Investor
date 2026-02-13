import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Bell, Trash2 } from 'lucide-react';

const UnifiedAlertCenter = () => {
    const [alerts, setAlerts] = useState([]);

    const load = async () => {
        const res = await apiClient.get('/orchestrator/alerts/unified');
        if (res.data.success) setAlerts(res.data.data);
    };

    useEffect(() => { load(); }, []);

    const clearAll = async () => {
        await apiClient.post('/orchestrator/alerts/clear');
        setAlerts([]);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Bell className="text-yellow-500" /> Unified Alert Matrix
                    </h1>
                    <p className="text-slate-500">Centralized Notification & Event Stream</p>
                </div>
                <button onClick={clearAll} className="flex items-center gap-2 text-xs font-bold text-slate-500 hover:text-white transition-colors">
                    <Trash2 size={14} /> CLEAR ALL
                </button>
            </header>

            <div className="space-y-4">
                {alerts.length === 0 && <div className="text-center py-12 text-slate-600">All quiet on the western front.</div>}
                
                {alerts.map(a => (
                    <div key={a.id} className={`p-4 rounded border flex items-center justify-between ${
                        a.severity === 'CRITICAL' ? 'bg-red-950/20 border-red-900' :
                        a.severity === 'WARNING' ? 'bg-yellow-950/20 border-yellow-900' :
                        'bg-slate-900 border-slate-800'
                    }`}>
                        <div className="flex items-center gap-4">
                            <div className={`w-2 h-12 rounded ${
                                a.severity === 'CRITICAL' ? 'bg-red-500' :
                                a.severity === 'WARNING' ? 'bg-yellow-500' :
                                'bg-blue-500'
                            }`}></div>
                            <div>
                                <div className="flex items-center gap-2 mb-1">
                                    <span className={`text-xs font-bold px-1 rounded ${
                                        a.severity === 'CRITICAL' ? 'text-red-400 bg-red-950' :
                                        a.severity === 'WARNING' ? 'text-yellow-400 bg-yellow-950' :
                                        'text-blue-400 bg-blue-950'
                                    }`}>{a.severity}</span>
                                    <span className="text-xs text-slate-500 uppercase tracking-wide">{a.source}</span>
                                </div>
                                <div className="font-bold text-white">{a.msg}</div>
                            </div>
                        </div>
                        <div className="text-xs text-slate-500 font-mono">{a.time}</div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default UnifiedAlertCenter;
