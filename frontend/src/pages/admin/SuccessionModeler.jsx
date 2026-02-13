import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Play, AlertOctagon } from 'lucide-react';

const SuccessionModeler = () => {
    const [scenario, setScenario] = useState(null);
    const [loading, setLoading] = useState(false);

    const runScenario = async (type) => {
        setLoading(true);
        const res = await apiClient.post('/wealth/scenarios/run', null, { params: { event_type: type } });
        if (res.data.success) setScenario(res.data.data);
        setLoading(false);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Play className="text-orange-500" /> Succession & Life Event Modeler
                </h1>
                <p className="text-slate-500">Run "What-If" Scenarios for Estate Planning</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-fit">
                    <h3 className="font-bold text-white mb-6">Select Scenario</h3>
                    <div className="space-y-3">
                        <button 
                            onClick={() => runScenario("Grantor Passing")}
                            className="w-full text-left p-4 bg-slate-950 hover:bg-slate-800 rounded border border-slate-800 hover:border-slate-600 transition-all"
                        >
                            <div className="font-bold text-white">Grantor Passing</div>
                            <div className="text-xs text-slate-500">Simulate estate tax settlement and asset transfer.</div>
                        </button>
                        <button 
                            onClick={() => runScenario("Incapacitation")}
                            className="w-full text-left p-4 bg-slate-950 hover:bg-slate-800 rounded border border-slate-800 hover:border-slate-600 transition-all"
                        >
                            <div className="font-bold text-white">Incapacitation / Disability</div>
                            <div className="text-xs text-slate-500">Activate Power of Attorney and Successor Trustee.</div>
                        </button>
                        <button 
                            onClick={() => runScenario("Business Sale")}
                            className="w-full text-left p-4 bg-slate-950 hover:bg-slate-800 rounded border border-slate-800 hover:border-slate-600 transition-all"
                        >
                            <div className="font-bold text-white">Liquidity Event (Business Sale)</div>
                            <div className="text-xs text-slate-500">Model tax impact of large windfall.</div>
                        </button>
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 min-h-[300px] flex flex-col justify-center">
                    {loading ? (
                        <div className="text-center text-slate-500 animate-pulse">Running Simulation...</div>
                    ) : scenario ? (
                        <div className="animate-in fade-in slide-in-from-bottom-4 duration-500">
                            <div className="flex items-center gap-2 mb-6">
                                <AlertOctagon className="text-red-500" />
                                <h3 className="text-xl font-bold text-white">{scenario.scenario} Impact</h3>
                            </div>
                            
                            <div className="space-y-4">
                                <div className="p-4 bg-slate-950 rounded border border-red-900/30">
                                    <div className="text-xs uppercase text-slate-500 font-bold mb-1">Financial Impact</div>
                                    <div className="text-lg font-bold text-white">{scenario.impact}</div>
                                </div>
                                
                                <div className="p-4 bg-slate-950 rounded border border-orange-900/30">
                                    <div className="text-xs uppercase text-slate-500 font-bold mb-1">Liquidity Gap</div>
                                    <div className="text-lg font-bold text-orange-400">${scenario.liquidity_gap.toLocaleString()}</div>
                                </div>

                                <div>
                                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Recommended Actions</div>
                                    <ul className="list-disc list-inside space-y-1 text-slate-300">
                                        {scenario.recommendations.map((r, i) => (
                                            <li key={i}>{r}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="text-center text-slate-500">
                            Select a scenario to view impact analysis.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default SuccessionModeler;
