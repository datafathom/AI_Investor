import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Globe, Crosshair, Cpu, Zap } from 'lucide-react';

const TacticalCommandCenter = () => {
    const [state, setState] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/orchestrator/global-state');
            if (res.data.success) setState(res.data.data);
        };
        load();
        const interval = setInterval(load, 5000); // Polling for "Real-Time" feel
        return () => clearInterval(interval);
    }, []);

    const execute = async (cmd) => {
        if (window.confirm(`EXECUTE: ${cmd}?`)) {
            await apiClient.post('/orchestrator/tactical/action', null, { params: { cmd } });
            alert("COMMAND SENT");
        }
    };

    if (!state) return <div className="p-8 text-white">Initializing Tactical Link...</div>;

    return (
        <div className="p-4 h-full overflow-y-auto text-slate-200 bg-black">
            <header className="mb-6 flex justify-between items-end border-b border-slate-800 pb-4">
                <div>
                    <h1 className="text-3xl font-black text-white flex items-center gap-3 uppercase tracking-wider">
                        <Crosshair className="text-red-500 animate-pulse" /> Tactical Operations Center
                    </h1>
                    <p className="text-slate-500 font-mono text-xs">DEFCON {state.defcon} // SYS.STATUS: {state.status}</p>
                </div>
                <div className="text-right">
                    <div className="text-4xl font-black text-emerald-500 font-mono">{state.active_services}</div>
                    <div className="text-xs text-slate-500 uppercase">Active Services</div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100%-100px)]">
                {/* 3D Sphere Placeholder */}
                <div className="lg:col-span-2 bg-slate-900/50 border border-slate-800 rounded-xl relative overflow-hidden flex items-center justify-center">
                    <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-blue-900/20 via-slate-950 to-black"></div>
                    <div className="relative z-10 text-center">
                        <Globe size={128} className="text-cyan-500/50 animate-spin-slow duration-[20s]" />
                        <div className="mt-4 text-xs font-mono text-cyan-500">GLOBAL_NEURAL_LINK_ACTIVE</div>
                    </div>
                    
                    {/* Floating Dept Status */}
                    <div className="absolute top-4 left-4 space-y-2">
                        {state.departments.map(d => (
                            <div key={d.id} className="flex items-center gap-2 text-xs font-mono bg-black/50 p-1 rounded backdrop-blur-sm border border-slate-800">
                                <div className={`w-2 h-2 rounded-full ${d.health > 90 ? 'bg-emerald-500' : 'bg-yellow-500'}`}></div>
                                <span className="text-slate-300 w-16">{d.name}</span>
                                <span className="text-slate-500">LOAD: {d.load}%</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Command & Control */}
                <div className="flex flex-col gap-4">
                    <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex-1">
                        <h3 className="font-bold text-white mb-4 flex items-center gap-2">
                            <Zap className="text-yellow-500" size={16} /> Critical Action Ticker
                        </h3>
                        <div className="space-y-2 font-mono text-xs overflow-y-auto max-h-64">
                            {state.critical_actions.map((act, i) => (
                                <div key={i} className="p-2 bg-slate-950 border-l-2 border-yellow-500 text-yellow-100/80">
                                    {act}
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="bg-red-950/20 border border-red-900/50 rounded-xl p-4">
                        <h3 className="font-bold text-red-500 mb-4 text-sm uppercase tracking-widest">Rapid Response Matrix</h3>
                        <div className="grid grid-cols-2 gap-2">
                            <button onClick={() => execute("KILL ALL TRADES")} className="bg-red-900/50 hover:bg-red-800 text-red-200 text-xs font-bold py-3 rounded border border-red-800">
                                KILL SWITCH
                            </button>
                            <button onClick={() => execute("HEDGE 100%")} className="bg-orange-900/50 hover:bg-orange-800 text-orange-200 text-xs font-bold py-3 rounded border border-orange-800">
                                FULL HEDGE
                            </button>
                            <button onClick={() => execute("REBOOT CORE")} className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold py-3 rounded border border-slate-600">
                                REBOOT CORE
                            </button>
                            <button onClick={() => execute("ISOLATE NET")} className="bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold py-3 rounded border border-slate-600">
                                AIR GAP
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default TacticalCommandCenter;
