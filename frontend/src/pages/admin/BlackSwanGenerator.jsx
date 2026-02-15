import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { CloudLightning, Zap } from 'lucide-react';

const BlackSwanGenerator = () => {
    const [event, setEvent] = useState(null);

    const generate = async () => {
        const res = await apiClient.post('/stress/generate/black-swan');
        if (res.data.success) setEvent(res.data.data);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <CloudLightning className="text-purple-500" /> Black Swan Generator
                    </h1>
                    <p className="text-slate-500">Randomized Extreme Event Simulation</p>
                </div>
                <button onClick={generate} className="bg-purple-600 hover:bg-purple-500 text-white font-bold py-2 px-6 rounded flex items-center gap-2">
                    <Zap size={18} /> GENERATE CHAOS
                </button>
            </header>

            <div className="flex justify-center mt-12">
                {event ? (
                    <div className="bg-slate-900 border border-slate-700 rounded-xl p-8 max-w-2xl w-full animate-in zoom-in duration-300 relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-purple-500 via-pink-500 to-red-500"></div>
                        
                        <h2 className="text-3xl font-bold text-white mb-2">{event.event_name}</h2>
                        <div className="text-purple-400 font-bold mb-6 text-lg">{event.impact_type}</div>

                        <div className="grid grid-cols-2 gap-6 mb-8">
                            <div className="p-4 bg-slate-950 rounded">
                                <div className="text-xs uppercase text-slate-500 font-bold mb-1">Financial Impact</div>
                                <div className="font-bold text-white">{event.estimated_loss}</div>
                            </div>
                            <div className="p-4 bg-slate-950 rounded">
                                <div className="text-xs uppercase text-slate-500 font-bold mb-1">Tail Risk</div>
                                <div className="font-bold text-white">Extreme (&gt;3σ)</div>
                            </div>
                        </div>

                        <div>
                            <h3 className="font-bold text-white mb-3 text-lg">⚠️ Emergency Handbook</h3>
                            <ul className="space-y-2">
                                {event.emergency_actions.map((action, i) => (
                                    <li key={i} className="flex items-center gap-3 bg-slate-950 p-3 rounded border border-slate-800">
                                        <span className="bg-red-500/20 text-red-400 font-bold px-2 rounded text-xs">ACTION</span>
                                        <span className="text-slate-300 font-medium">{action}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ) : (
                    <div className="text-center text-slate-600 mt-20">
                        <CloudLightning size={80} className="mx-auto mb-6 opacity-20" />
                        <h3 className="text-xl font-bold mb-2">System Stable</h3>
                        <p>Click "Generate Chaos" to simulate a low-probability, high-impact event.</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default BlackSwanGenerator;
