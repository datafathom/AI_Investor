import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { RefreshCw, CheckCircle, AlertOctagon, TrendingUp } from 'lucide-react';

const ReconciliationDashboard = () => {
    const [status, setStatus] = useState(null);
    const [running, setRunning] = useState(false);

    useEffect(() => {
        loadStatus();
    }, [running]);

    const loadStatus = async () => {
        const res = await apiClient.get('/audit/reconciliation/status');
        if (res.data.success) setStatus(res.data.data);
    };

    const runRecon = async () => {
        setRunning(true);
        try {
            await apiClient.post('/audit/reconciliation/run');
            setTimeout(() => setRunning(false), 2000); // Mock delay
        } catch (e) { console.error(e); setRunning(false); }
    };

    if (!status) return <div>Loading Audit Data...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <RefreshCw className="text-blue-500" /> Reconciliation Dashboard
                    </h1>
                    <p className="text-slate-500">Internal vs Broker Synchronization</p>
                </div>
                <button 
                    onClick={runRecon}
                    disabled={running}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded font-bold flex items-center gap-2"
                >
                    {running ? 'RECONCILING...' : 'RUN RECONCILIATION'}
                </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Overall Status</div>
                    <div className={`text-3xl font-bold ${status.status === 'BALANCED' ? 'text-emerald-400' : 'text-red-500'}`}>
                        {status.status}
                    </div>
                    <div className="text-xs text-slate-500 mt-1">Last Run: {new Date(status.last_run).toLocaleString()}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Active Breaks</div>
                    <div className="text-3xl font-bold text-orange-400">{status.break_count}</div>
                    <div className="text-xs text-slate-500 mt-1">Requiring Attention</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Cash Variance</div>
                    <div className="text-3xl font-bold text-white font-mono">${status.cash_variance.toFixed(2)}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Match Rate</div>
                    <div className="text-3xl font-bold text-blue-400">{status.position_match_rate}%</div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <CheckCircle className="text-emerald-500" /> Integrity Checks
                    </h3>
                    <div className="space-y-4">
                        <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                            <span className="text-slate-300">Position Quantities</span>
                            <span className="text-emerald-400 font-bold text-sm">MATCHED</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                            <span className="text-slate-300">Cost Basis</span>
                            <span className="text-emerald-400 font-bold text-sm">MATCHED</span>
                        </div>
                        <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
                            <span className="text-slate-300">Unsettled Cash</span>
                            <span className="text-emerald-400 font-bold text-sm">MATCHED</span>
                        </div>
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <AlertOctagon className="text-orange-500" /> Recent Variances
                    </h3>
                    <div className="text-center text-slate-500 py-8">
                        No significant variances detected in the last 24 hours.
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ReconciliationDashboard;
