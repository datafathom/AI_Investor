import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { PieChart, AlertTriangle } from 'lucide-react';

const FeeAuditor = () => {
    const [stats, setStats] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/audit/fees');
            if (res.data.success) setStats(res.data.data);
        };
        load();
    }, []);

    if (!stats) return <div>Loading Fee Data...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <PieChart className="text-pink-500" /> Fee & Commission Auditor
                </h1>
                <p className="text-slate-500">Cost Analysis & Overcharge Detection</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Total Fees YTD</div>
                    <div className="text-3xl font-bold text-white font-mono">${stats.total_ytd.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Avg Cost (bps)</div>
                    <div className="text-3xl font-bold text-blue-400">{stats.avg_bps} bps</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Potential Savings</div>
                    <div className="text-3xl font-bold text-emerald-400 font-mono">${stats.potential_savings.toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Overcharges</div>
                    <div className="text-3xl font-bold text-red-500">{stats.overcharges_detected}</div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                    <AlertTriangle className="text-red-500" /> Audit Findings
                </h3>
                {stats.overcharges_detected > 0 ? (
                    <div className="p-4 bg-red-900/20 border border-red-900/50 rounded flex justify-between items-center text-red-200">
                        <div>
                            <strong>Potential Overcharge Detected</strong>
                            <div className="text-sm opacity-80">Trade txn_055 executed at 0.05% comms (Schedule: 0.03%). Refund claim generated.</div>
                        </div>
                        <button className="bg-red-700 hover:bg-red-600 text-white px-3 py-1 rounded text-sm">Review Claim</button>
                    </div>
                ) : (
                    <div className="text-slate-500">No fee discrepancies found.</div>
                )}
            </div>
        </div>
    );
};

export default FeeAuditor;
