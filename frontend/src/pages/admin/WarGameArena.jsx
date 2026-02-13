import React, { useState } from 'react';
import apiClient from '../../services/apiClient';
import { Sword, Users, Shield } from 'lucide-react';

const WarGameArena = () => {
    const [simStatus, setSimStatus] = useState(null);

    const startWarGame = async () => {
        const res = await apiClient.post('/stress/wargame/start', null, { params: { adversary_count: 3 } });
        if (res.data.success) setSimStatus(res.data.data);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Sword className="text-red-500" /> War Game Arena
                    </h1>
                    <p className="text-slate-500">Multi-Agent Adversarial Simulation</p>
                </div>
                <button onClick={startWarGame} className="bg-red-600 hover:bg-red-500 text-white font-bold py-2 px-6 rounded flex items-center gap-2">
                    START SIMULATION
                </button>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6 flex items-center gap-2">
                        <Users className="text-slate-400" /> Active Agents
                    </h3>
                    
                    {!simStatus ? (
                        <div className="text-center text-slate-600 py-12">Waiting for deployment...</div>
                    ) : (
                        <div className="space-y-4">
                            {simStatus.agents.map((agent, i) => (
                                <div key={i} className="flex justify-between items-center p-4 bg-slate-950 rounded border border-slate-800">
                                    <div className="font-bold text-white">{agent}</div>
                                    <span className="text-xs bg-red-900/50 text-red-200 px-2 py-1 rounded border border-red-800">HOSTILE</span>
                                </div>
                            ))}
                            <div className="flex justify-between items-center p-4 bg-slate-950 rounded border border-emerald-900/50">
                                <div className="font-bold text-white">Our Strategy Agent</div>
                                <span className="text-xs bg-emerald-900/50 text-emerald-200 px-2 py-1 rounded border border-emerald-800">DEFENDING</span>
                            </div>
                        </div>
                    )}
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 relative overflow-hidden">
                    {simStatus && (
                        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-slate-900 to-red-900/20 pointer-events-none"></div>
                    )}
                    
                    <h3 className="font-bold text-white mb-6 flex items-center gap-2 relative z-10">
                        <Shield className="text-blue-500" /> Simulation Outcome
                    </h3>

                    {simStatus ? (
                        <div className="relative z-10">
                            <div className="text-center py-8">
                                <div className="text-5xl font-bold text-white mb-2">{simStatus.strategy_score}/100</div>
                                <div className="text-slate-400 text-sm uppercase font-bold tracking-widest">Survivability Score</div>
                            </div>
                            
                            <div className="bg-slate-950 p-6 rounded border border-slate-800 text-center">
                                <div className="text-xl font-bold text-emerald-400 uppercase tracking-widest">{simStatus.outcome}</div>
                            </div>
                        </div>
                    ) : (
                        <div className="text-center text-slate-600 py-16 relative z-10">
                            Run simulation to test strategy resilience.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default WarGameArena;
