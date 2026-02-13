import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Eye, AlertTriangle, Search } from 'lucide-react';

const TradeSurveillance = () => {
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/compliance/surveillance/alerts');
            if (res.data.success) setAlerts(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Eye className="text-indigo-500" /> Trade Surveillance
                </h1>
                <p className="text-slate-500">Market Abuse Detection & Pattern Recognition</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="p-4 bg-slate-950 font-bold text-white border-b border-slate-800 flex justify-between items-center">
                        <span>Surveillance Alerts</span>
                        <div className="flex gap-2">
                            <input placeholder="Filter by Symbol..." className="bg-slate-900 border border-slate-700 rounded px-2 py-1 text-xs text-white" />
                        </div>
                    </div>
                    <table className="w-full text-left">
                        <thead className="text-slate-500 text-xs uppercase bg-slate-950">
                            <tr>
                                <th className="p-4">Type</th>
                                <th className="p-4">Symbol</th>
                                <th className="p-4">Time</th>
                                <th className="p-4">Severity</th>
                                <th className="p-4">Action</th>
                            </tr>
                        </thead>
                        <tbody className="text-sm">
                            {alerts.map(alert => (
                                <tr key={alert.id} className="border-b border-slate-800 hover:bg-slate-800/50">
                                    <td className="p-4 font-bold text-white">{alert.type.replace('_', ' ')}</td>
                                    <td className="p-4 font-mono text-cyan-400">{alert.symbol}</td>
                                    <td className="p-4 text-slate-400 font-mono">{new Date(alert.timestamp).toLocaleTimeString()}</td>
                                    <td className="p-4">
                                        <span className={`px-2 py-1 rounded text-xs font-bold ${
                                            alert.severity === 'HIGH' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400'
                                        }`}>
                                            {alert.severity}
                                        </span>
                                    </td>
                                    <td className="p-4">
                                        <button className="text-slate-500 hover:text-white transition-colors">
                                            <Search size={16} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <AlertTriangle className="text-orange-500" /> Pattern Analysis
                    </h3>
                    <div className="space-y-4">
                        <div className="p-3 bg-slate-950 rounded border border-slate-800">
                            <h4 className="font-bold text-slate-300 text-sm mb-1">Spoofing Detection</h4>
                            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                                <div className="bg-orange-500 h-full w-[15%]"></div>
                            </div>
                            <div className="text-xs text-slate-500 mt-1">Low Activity</div>
                        </div>
                        <div className="p-3 bg-slate-950 rounded border border-slate-800">
                            <h4 className="font-bold text-slate-300 text-sm mb-1">Wash Trading</h4>
                            <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                                <div className="bg-red-500 h-full w-[45%]"></div>
                            </div>
                            <div className="text-xs text-slate-500 mt-1">Elevated Risk</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TradeSurveillance;
