import React from 'react';
import { Power, Activity, Cpu, Clock } from 'lucide-react';

export const AgentCard = ({ agent, onRestart }) => {
    const getStatusColor = (status) => {
        switch (status) {
            case 'WORKING': return 'text-emerald-400 border-emerald-500/20 bg-emerald-500/10';
            case 'IDLE': return 'text-slate-400 border-slate-700 bg-slate-800/50';
            case 'THINKING': return 'text-cyan-400 border-cyan-500/20 bg-cyan-500/10';
            case 'ERROR': return 'text-red-400 border-red-500/20 bg-red-500/10';
            case 'OFFLINE': return 'text-slate-600 border-slate-800 bg-slate-900';
            default: return 'text-slate-400';
        }
    };

    return (
        <div className={`border rounded-xl p-4 transition-all hover:scale-[1.02] ${getStatusColor(agent.status).replace('text-', 'border-')}`}>
            <div className="flex justify-between items-start mb-3">
                <div>
                    <h3 className="font-bold text-white text-sm">{agent.name}</h3>
                    <div className="flex items-center gap-2 mt-1">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${getStatusColor(agent.status)}`}>
                            {agent.status}
                        </span>
                        <span className="text-[10px] text-slate-500 font-mono">{agent.id}</span>
                    </div>
                </div>
                <button 
                    onClick={() => onRestart(agent.id)}
                    className="p-1.5 hover:bg-slate-800 rounded text-slate-500 hover:text-white transition-colors"
                >
                    <Power size={14} />
                </button>
            </div>

            <div className="grid grid-cols-2 gap-2 mt-4">
                <div className="flex items-center gap-2 text-slate-400 text-xs">
                    <Activity size={12} />
                    <span>TPM: <span className="text-white font-mono">{agent.tpm}</span></span>
                </div>
                <div className="flex items-center gap-2 text-slate-400 text-xs text-right justify-end">
                    <Clock size={12} />
                    <span>{agent.uptime_percent}%</span>
                </div>
            </div>
            
            <div className="mt-3 pt-3 border-t border-dashed border-slate-800 text-[10px] text-slate-600 font-mono flex justify-between">
                <span>v{agent.version}</span>
                <span>{agent.role}</span>
            </div>
        </div>
    );
};
