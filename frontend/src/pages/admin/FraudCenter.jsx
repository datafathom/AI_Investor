import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Fingerprint, Lock, ShieldCheck } from 'lucide-react';

const FraudCenter = () => {
    const [alerts, setAlerts] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/fraud/alerts');
            if (res.data.success) setAlerts(res.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Fingerprint className="text-indigo-500" /> Fraud Detection Center
                </h1>
                <p className="text-slate-500">Security Monitoring & Anomaly Detection</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <div className="p-4 bg-slate-950 font-bold text-white border-b border-slate-800 flex justify-between items-center">
                        <span>Security Alerts</span>
                        <span className="text-xs bg-red-500 px-2 py-1 rounded text-white">{alerts.length} NEW</span>
                    </div>
                    {alerts.map(alert => (
                        <div key={alert.id} className="p-4 border-b border-slate-800 hover:bg-slate-800/50 flex gap-4">
                            <div className="mt-1">
                                <ShieldCheck className={alert.severity === 'HIGH' ? 'text-red-500' : 'text-yellow-500'} />
                            </div>
                            <div className="flex-1">
                                <div className="flex justify-between">
                                    <h4 className="font-bold text-white">{alert.type}</h4>
                                    <span className="text-xs text-slate-500 font-mono">{new Date(alert.timestamp).toLocaleTimeString()}</span>
                                </div>
                                <p className="text-sm text-slate-400 mt-1">{alert.details}</p>
                                <div className="mt-2 flex gap-2">
                                    <button className="text-xs bg-slate-800 hover:bg-slate-700 text-white px-3 py-1 rounded">Investigate</button>
                                    <button className="text-xs bg-red-900/20 hover:bg-red-900/40 text-red-400 px-3 py-1 rounded border border-red-900/30">Block IP</button>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>

                <div className="space-y-6">
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                            <Lock size={18} className="text-green-500" /> Security Status
                        </h3>
                        <div className="space-y-3">
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-400">Firewall</span>
                                <span className="text-green-400 font-bold">ACTIVE</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-400">Withdrawal Lock</span>
                                <span className="text-green-400 font-bold">ENABLED (24h)</span>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-slate-400">IP Whitelist</span>
                                <span className="text-green-400 font-bold">STRICT</span>
                            </div>
                        </div>
                    </div>
                    
                    <div className="bg-indigo-900/20 border border-indigo-900/50 rounded-xl p-6">
                        <h3 className="font-bold text-indigo-300 mb-2">Automated Protection</h3>
                        <p className="text-sm text-indigo-200/70">
                            The system is monitoring for velocity anomalies and unauthorized device access. 
                            High-severity alerts will trigger an automatic trading freeze.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default FraudCenter;
