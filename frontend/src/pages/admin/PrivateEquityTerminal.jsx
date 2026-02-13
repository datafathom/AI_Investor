import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Briefcase, TrendingUp, AlertCircle } from 'lucide-react';

const PrivateEquityTerminal = () => {
    const [calls, setCalls] = useState([]);
    const [benchmarks, setBenchmarks] = useState(null);

    useEffect(() => {
        const load = async () => {
            const [cRes, bRes] = await Promise.all([
                apiClient.get('/assets/pe/capital-calls'),
                apiClient.get('/assets/pe/benchmarks')
            ]);
            if (cRes.data.success) setCalls(cRes.data.data);
            if (bRes.data.success) setBenchmarks(bRes.data.data);
        };
        load();
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Briefcase className="text-purple-500" /> Private Equity Terminal
                </h1>
                <p className="text-slate-500">Capital Calls, Distributions & Performance Metrics</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
                {benchmarks && (
                    <>
                        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                            <div className="text-xs uppercase text-slate-500 font-bold mb-2">Net IRR</div>
                            <div className="text-3xl font-bold text-emerald-400">{benchmarks.irr_net}%</div>
                        </div>
                        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                            <div className="text-xs uppercase text-slate-500 font-bold mb-2">TVPI</div>
                            <div className="text-3xl font-bold text-blue-400">{benchmarks.tvpi}x</div>
                        </div>
                        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                            <div className="text-xs uppercase text-slate-500 font-bold mb-2">DPI</div>
                            <div className="text-3xl font-bold text-orange-400">{benchmarks.dpi}x</div>
                        </div>
                        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                            <div className="text-xs uppercase text-slate-500 font-bold mb-2">PME (S&P 500)</div>
                            <div className="text-3xl font-bold text-slate-200">{benchmarks.pme_spy}x</div>
                        </div>
                    </>
                )}
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                    <AlertCircle className="text-yellow-500" size={20} /> Upcoming Capital Calls
                </h3>
                <div className="space-y-4">
                    {calls.map((c, i) => (
                        <div key={i} className="bg-slate-950 border border-yellow-500/30 p-4 rounded flex justify-between items-center">
                            <div>
                                <div className="font-bold text-white">{c.fund}</div>
                                <div className="text-xs text-slate-500">Due: {c.due_date}</div>
                            </div>
                            <div className="text-right">
                                <div className="text-xl font-bold text-white">${c.amount.toLocaleString()}</div>
                                <div className="text-xs uppercase text-yellow-500 font-bold">{c.status}</div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default PrivateEquityTerminal;
