import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { ShieldCheck, AlertCircle } from 'lucide-react';

const TrustAdmin = () => {
    const [compliance, setCompliance] = useState([]);
    const [distributions, setDistributions] = useState([]);

    useEffect(() => {
        const load = async () => {
            const [cRes, dRes] = await Promise.all([
                apiClient.get('/wealth/trusts/compliance'),
                apiClient.get('/wealth/trusts/distributions')
            ]);
            if (cRes.data.success) setCompliance(cRes.data.data);
            if (dRes.data.success) setDistributions(dRes.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <ShieldCheck className="text-blue-500" /> Trust Administration
                </h1>
                <p className="text-slate-500">Fiduciary Compliance & Distributions</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6">Compliance Rules</h3>
                    <div className="space-y-4">
                        {compliance.map((c, i) => (
                            <div key={i} className="p-4 bg-slate-950 rounded border border-slate-800 flex justify-between items-center">
                                <div>
                                    <div className="font-bold text-white">{c.rule}</div>
                                    <div className="text-xs text-slate-500">Last Check: {c.last_check || 'Pending'}</div>
                                    {c.action_needed && <div className="text-xs text-red-400 mt-1">{c.action_needed}</div>}
                                </div>
                                <div className={`px-2 py-1 rounded text-xs font-bold ${c.status === 'COMPLIANCE' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-yellow-500/20 text-yellow-400'}`}>
                                    {c.status}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6 flex items-center gap-2">
                        <AlertCircle className="text-orange-500" size={20} /> Pending Distributions
                    </h3>
                    <div className="space-y-4">
                        {distributions.length === 0 && <div className="text-slate-500">No pending distributions.</div>}
                        {distributions.map((d, i) => (
                            <div key={i} className="p-4 bg-slate-950 rounded border border-orange-900/30">
                                <div className="flex justify-between mb-2">
                                    <span className="font-bold text-white">{d.beneficiary}</span>
                                    <span className="font-bold text-orange-400">${d.amount.toLocaleString()}</span>
                                </div>
                                <div className="text-xs text-slate-500">{d.trust}</div>
                                <div className="text-xs text-slate-400 mt-1 italic">"{d.reason}"</div>
                                <div className="mt-3 flex gap-2">
                                    <button className="flex-1 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold py-1 rounded">APPROVE</button>
                                    <button className="flex-1 bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold py-1 rounded">DENY</button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TrustAdmin;
