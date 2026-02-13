import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Bell, Plus, Trash2 } from 'lucide-react';

const AlertCenter = () => {
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/alerts/');
            if (res.data.success) setAlerts(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
             <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Bell className="text-yellow-500" /> Price Alert Center
                    </h1>
                    <p className="text-slate-500">Real-time Notifications & Triggers</p>
                </div>
                <button className="bg-yellow-600 hover:bg-yellow-500 text-black px-4 py-2 rounded font-bold flex items-center gap-2">
                    <Plus size={18} /> NEW ALERT
                </button>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <table className="w-full text-left">
                    <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                        <tr>
                            <th className="p-4">Symbol</th>
                            <th className="p-4">Condition</th>
                            <th className="p-4">Value</th>
                            <th className="p-4">Status</th>
                            <th className="p-4">Action</th>
                        </tr>
                    </thead>
                    <tbody className="text-sm">
                        {alerts.map(alert => (
                            <tr key={alert.id} className="border-b border-slate-800 hover:bg-slate-800/50 transition-colors">
                                <td className="p-4 font-bold text-white font-mono">{alert.symbol}</td>
                                <td className="p-4 text-slate-300">{alert.condition}</td>
                                <td className="p-4 font-mono text-cyan-400">{alert.value}</td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        alert.status === 'ACTIVE' ? 'bg-green-500/20 text-green-400' : 'bg-red-500/20 text-red-400'
                                    }`}>
                                        {alert.status}
                                    </span>
                                </td>
                                <td className="p-4">
                                     <button className="text-slate-500 hover:text-red-400 transition-colors">
                                        <Trash2 size={18} />
                                     </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AlertCenter;
