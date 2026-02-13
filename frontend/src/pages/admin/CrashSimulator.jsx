import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Activity, AlertTriangle } from 'lucide-react';

const CrashSimulator = () => {
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const runSim = async () => {
        setLoading(true);
        const res = await apiClient.post('/stress/simulate/crash', null, { params: { scenario_id: "2008" } });
        if (res.data.success) setResult(res.data.data);
        setLoading(false);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Activity className="text-red-500" /> Market Crash Simulator
                </h1>
                <p className="text-slate-500">Historical & "What-If" Crisis Modeling</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-fit">
                    <h3 className="font-bold text-white mb-6">Scenario Selection</h3>
                    <div className="space-y-3">
                        {['2008 Global Financial Crisis', '2000 Dot Com Bubble', '2020 COVID Crash'].map(s => (
                            <button 
                                key={s}
                                onClick={runSim}
                                className="w-full text-left p-4 bg-slate-950 hover:bg-slate-800 rounded border border-slate-800 hover:border-slate-600 transition-all text-sm font-bold text-slate-300"
                            >
                                {s}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6 min-h-[400px] flex flex-col justify-center">
                    {loading ? (
                        <div className="text-center text-slate-500 animate-pulse">Simulating Market Crash...</div>
                    ) : result ? (
                        <div className="animate-in fade-in zoom-in duration-300">
                            <h2 className="text-2xl font-bold text-white mb-6 text-center">{result.scenario} Impact</h2>
                            
                            <div className="grid grid-cols-2 gap-6 mb-8">
                                <div className="p-4 bg-red-950/30 border border-red-900 rounded text-center">
                                    <div className="text-xs uppercase text-red-400 font-bold mb-1">Portfolio Impact</div>
                                    <div className="text-3xl font-bold text-white">{result.portfolio_impact}%</div>
                                </div>
                                <div className="p-4 bg-red-950/30 border border-red-900 rounded text-center">
                                    <div className="text-xs uppercase text-red-400 font-bold mb-1">Max Drawdown</div>
                                    <div className="text-3xl font-bold text-white">{result.max_drawdown}%</div>
                                </div>
                            </div>

                            <div className="bg-slate-950 p-6 rounded border border-slate-800">
                                <h4 className="font-bold text-white mb-4 flex items-center gap-2">
                                    <AlertTriangle className="text-yellow-500" size={18} /> Breach Points
                                </h4>
                                <ul className="list-disc list-inside space-y-2 text-slate-300">
                                    {result.breach_points.map((bp, i) => (
                                        <li key={i}>{bp}</li>
                                    ))}
                                </ul>
                            </div>
                            
                            <div className="text-center text-slate-500 mt-6 text-sm">
                                Estimated Recovery Time: {result.recovery_days} Days
                            </div>
                        </div>
                    ) : (
                        <div className="text-center text-slate-500 flex flex-col items-center">
                            <Activity size={48} className="mb-4 opacity-20" />
                            <p>Select a scenario to visualize portfolio performance under stress.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default CrashSimulator;
