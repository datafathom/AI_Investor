import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { ClipboardCheck, Shield, AlertCircle } from 'lucide-react';

const ComplianceTracker = () => {
    const [status, setStatus] = useState(null);
    const [rules, setRules] = useState([]);

    useEffect(() => {
        const load = async () => {
            const [sRes, rRes] = await Promise.all([
                apiClient.get('/compliance/status'),
                apiClient.get('/compliance/rules')
            ]);
            if (sRes.data.success) setStatus(sRes.data.data);
            if (rRes.data.success) setRules(rRes.data.data);
        };
        load();
    }, []);

    const acknowledge = async (id) => {
        await apiClient.post(`/compliance/ack/${id}`);
        // Refresh rules...
        const rRes = await apiClient.get('/compliance/rules');
        if (rRes.data.success) setRules(rRes.data.data);
    };

    if (!status) return <div>Loading Compliance Data...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <ClipboardCheck className="text-emerald-500" /> Compliance Tracker
                </h1>
                <p className="text-slate-500">Regulatory Adherence & Rule Management</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Health Score</div>
                    <div className="text-4xl font-bold text-emerald-400">{status.score}/100</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Active Rules</div>
                    <div className="text-3xl font-bold text-white">{status.active_rules}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Pending Tasks</div>
                    <div className="text-3xl font-bold text-yellow-500">{status.pending_tasks}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Last Audit</div>
                    <div className="text-lg font-bold text-slate-300">{status.last_audit}</div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-6 flex items-center gap-2">
                    <Shield size={18} className="text-blue-500" /> Regulatory Requirements
                </h3>
                <div className="space-y-4">
                    {rules.map(rule => (
                        <div key={rule.id} className="flex items-center justify-between p-4 bg-slate-950 rounded border border-slate-800">
                            <div className="flex items-center gap-4">
                                <div className={`w-2 h-2 rounded-full ${rule.status === 'COMPLIANT' ? 'bg-emerald-500' : 'bg-yellow-500'}`} />
                                <div>
                                    <div className="font-bold text-white">{rule.name}</div>
                                    {rule.due_date && <div className="text-xs text-slate-500">Due: {rule.due_date}</div>}
                                </div>
                            </div>
                            <div className="flex items-center gap-4">
                                <span className={`text-xs font-bold px-2 py-1 rounded ${
                                    rule.status === 'COMPLIANT' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-yellow-500/20 text-yellow-400'
                                }`}>
                                    {rule.status}
                                </span>
                                {rule.status !== 'COMPLIANT' && (
                                    <button 
                                        onClick={() => acknowledge(rule.id)}
                                        className="text-xs bg-blue-600 hover:bg-blue-500 text-white px-3 py-1 rounded"
                                    >
                                        Mark Done
                                    </button>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default ComplianceTracker;
