import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { FileText, RefreshCw, Volume2, TrendingUp, TrendingDown } from 'lucide-react';

const ExecSummaryPage = () => {
    const [summary, setSummary] = useState(null);

    useEffect(() => {
        loadSummary();
    }, []);

    const loadSummary = async () => {
        const res = await apiClient.get('/reporting/executive-summary');
        if (res.data.success) setSummary(res.data.data);
    };

    const regenerate = async (tone) => {
        const res = await apiClient.post('/reporting/narrative/regenerate', null, { params: { tone } });
        if (res.data.success) alert(res.data.data.new_summary); // In productive app, update state
    };

    if (!summary) return <div>Generating AI Insights...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <FileText className="text-indigo-500" /> Executive Summary
                    </h1>
                    <p className="text-slate-500">AI-Generated Portfolio Narrative</p>
                </div>
                <div className="flex gap-2">
                    <button onClick={() => regenerate('Casual')} className="bg-slate-800 text-xs px-3 py-1 rounded hover:bg-slate-700">Casual</button>
                    <button onClick={() => regenerate('Professional')} className="bg-slate-800 text-xs px-3 py-1 rounded hover:bg-slate-700">Pro</button>
                    <button onClick={() => regenerate('Urgent')} className="bg-slate-800 text-xs px-3 py-1 rounded hover:bg-slate-700">Urgent</button>
                </div>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 mb-8 relative">
                <div className="absolute top-4 right-4 text-slate-500">
                    <Volume2 size={20} className="hover:text-white cursor-pointer" />
                </div>
                <h3 className="text-xl font-bold text-white mb-4">Portfolio Commentary</h3>
                <p className="text-lg leading-relaxed text-slate-300">
                    {summary.summary}
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">Top 3 Things to Watch</h3>
                    <ul className="space-y-3">
                        {summary.top_3_watch.map((item, i) => (
                            <li key={i} className="flex items-start gap-3">
                                <span className="bg-indigo-500/20 text-indigo-400 font-bold px-2 rounded-full text-sm">{i+1}</span>
                                <span className="text-slate-300">{item}</span>
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-4">Outliers & Anomalies</h3>
                    <div className="flex flex-wrap gap-2">
                        {summary.outliers.map((o, i) => (
                            <span key={i} className={`px-3 py-1 rounded text-sm font-bold ${o.includes('-') ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                                {o}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ExecSummaryPage;
