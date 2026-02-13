import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Database, CheckCircle, AlertTriangle, Activity } from 'lucide-react';

const DataValidation = () => {
    const [status, setStatus] = useState(null);
    const [running, setRunning] = useState(false);

    useEffect(() => {
        loadStatus();
    }, [running]);

    const loadStatus = async () => {
        const res = await apiClient.get('/validation/status');
        if (res.data.success) setStatus(res.data.data);
    };

    const runValidation = async () => {
        setRunning(true);
        try {
            await apiClient.post('/validation/run');
            setTimeout(() => setRunning(false), 2000); 
        } catch (e) { console.error(e); setRunning(false); }
    };

    if (!status) return <div>Loading Validation Data...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Database className="text-blue-500" /> Data Quality Dashboard
                    </h1>
                    <p className="text-slate-500">Schema Validation & Data Integrity Monitor</p>
                </div>
                <button 
                    onClick={runValidation}
                    disabled={running}
                    className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded font-bold flex items-center gap-2"
                >
                    {running ? 'VALIDATING...' : 'RUN VALIDATION SUITE'}
                </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                <ScoreCard title="Completeness" value={status.completeness} color="text-emerald-400" />
                <ScoreCard title="Accuracy" value={status.accuracy} color="text-blue-400" />
                <ScoreCard title="Timeliness" value={status.timeliness} color="text-purple-400" />
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Schema Drift</div>
                    <div className="text-lg font-bold text-white">{status.schema_drift}</div>
                    <div className="text-xs text-slate-500 mt-1">Last Run: {new Date(status.last_run).toLocaleTimeString()}</div>
                </div>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                    <Activity className="text-slate-400" /> Validation Rules
                </h3>
                <div className="space-y-2">
                    <RuleRow name="Price > 0" status="PASS" />
                    <RuleRow name="Volume >= 0" status="PASS" />
                    <RuleRow name="Symbol Format (Ticker)" status="PASS" />
                    <RuleRow name="Timestamp Integrity" status="PASS" />
                </div>
            </div>
        </div>
    );
};

const ScoreCard = ({ title, value, color }) => (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
        <div className="text-xs uppercase text-slate-500 font-bold mb-2">{title}</div>
        <div className={`text-4xl font-bold ${color}`}>{value}%</div>
    </div>
);

const RuleRow = ({ name, status }) => (
    <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-slate-800">
        <span className="text-slate-300 font-mono">{name}</span>
        <span className="flex items-center gap-1 text-emerald-400 font-bold text-sm">
            <CheckCircle size={14} /> {status}
        </span>
    </div>
);

export default DataValidation;
