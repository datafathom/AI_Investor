import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Lock, Unlock, ShieldAlert, BrainCircuit } from 'lucide-react';

const AutonomyController = () => {
    const [constraints, setConstraints] = useState([]);
    const [level, setLevel] = useState(0);

    const load = async () => {
        const cRes = await apiClient.get('/orchestrator/constraints');
        if (cRes.data.success) setConstraints(cRes.data.data);
    };

    useEffect(() => { load(); }, []);

    const updateLevel = async (newLevel) => {
        const res = await apiClient.put('/orchestrator/autonomy/level', null, { params: { level: newLevel } });
        if (res.data.success) setLevel(res.data.data.level);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <BrainCircuit className="text-purple-500" /> Sovereign Autonomy Control
                </h1>
                <p className="text-slate-500">Governance, Constraints & Safety Protocols</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <div>
                     <div className="flex justify-between items-end mb-4">
                        <h3 className="font-bold text-white text-xl">Autonomy Level</h3>
                        <div className="text-3xl font-black text-purple-400">Lvl {level}</div>
                     </div>
                     
                     <div className="relative h-12 bg-slate-900 rounded-full border border-slate-700 mb-8 flex items-center px-2">
                        {[0, 2, 4, 6, 8, 10].map(l => (
                            <button 
                                key={l}
                                onClick={() => updateLevel(l)}
                                className={`w-1/6 h-8 rounded-full text-xs font-bold transition-all ${level >= l ? 'bg-purple-600 text-white shadow-[0_0_15px_rgba(147,51,234,0.5)]' : 'bg-transparent text-slate-600'}`}
                            >
                                {l === 0 ? 'MANUAL' : l === 5 ? 'CO-PILOT' : l === 10 ? 'SOVEREIGN' : l}
                            </button>
                        ))}
                     </div>
                     
                     <div className="p-6 bg-slate-950 rounded border border-purple-900/30 text-center">
                        <p className="text-slate-300 mb-2 font-bold">Current Mode: {level < 5 ? 'Human Oversight Required' : level < 9 ? 'AI Co-Pilot (Approval Needed)' : 'Fully Autonomous Execution'}</p>
                        <p className="text-xs text-slate-500">System executes trades, manages risks, and optimizes portfolio within defined constraints.</p>
                     </div>
                </div>

                <div>
                    <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                        <ShieldAlert className="text-red-500" /> Hard Constraints (NEVER BREAK)
                    </h3>
                    <div className="space-y-3">
                        {constraints.map((c, i) => (
                            <div key={i} className="flex justify-between items-center p-4 bg-slate-900 rounded border border-slate-700">
                                <div className="flex items-center gap-3">
                                    {c.locked ? <Lock size={16} className="text-red-400" /> : <Unlock size={16} className="text-slate-500" />}
                                    <span className="font-mono text-sm text-slate-200">{c.rule}</span>
                                </div>
                                <span className="text-xs font-bold text-emerald-500 bg-emerald-900/20 px-2 py-1 rounded">ACTIVE</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            <div className="mt-12 pt-8 border-t border-slate-800 text-center">
                <button className="bg-red-600 hover:bg-red-700 text-white font-black py-4 px-12 rounded shadow-[0_0_30px_rgba(220,38,38,0.4)] hover:shadow-[0_0_50px_rgba(220,38,38,0.6)] transition-all border-2 border-red-500">
                    PANIC: LIQUIDATE & SHUTDOWN
                </button>
                <p className="text-xs text-red-500/50 mt-4 uppercase font-bold tracking-widest">Emergency Override Only</p>
            </div>
        </div>
    );
};

export default AutonomyController;
