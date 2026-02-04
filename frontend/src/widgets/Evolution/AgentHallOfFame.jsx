import React from 'react';
import { Crown, Zap, Play, Target, Share2 } from 'lucide-react';
import useEvolutionStore from '../../stores/evolutionStore';
import './AgentHallOfFame.css';

const AgentHallOfFame = ({ onSelectAgent }) => {
    const { hallOfFame } = useEvolutionStore();

    // Mock data if hallOfFame is empty for demo/roadmap
    const displayAgents = hallOfFame.length > 0 ? hallOfFame : [
        { id: 'elite_1', name: 'Alpha-Omega', fitness: 0.985, generation: 42, genes: { rsi_period: 14, rsi_buy: 30, rsi_sell: 70 } },
        { id: 'elite_2', name: 'Sidewinder', fitness: 0.942, generation: 38, genes: { rsi_period: 10, rsi_buy: 28, rsi_sell: 75 } },
        { id: 'elite_3', name: 'Zenith Vector', fitness: 0.910, generation: 45, genes: { rsi_period: 21, rsi_buy: 25, rsi_sell: 80 } },
    ];

    return (
        <div className="agent-hall-of-fame glass-premium p-6 rounded-3xl border border-cyan-500/10">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-sm font-black text-cyan-400 uppercase tracking-widest flex items-center gap-2">
                    <Crown size={16} /> Elite Hall of Fame
                </h3>
                <span className="text-[10px] font-mono text-slate-500 uppercase">Top 1% Genomes</span>
            </div>

            <div className="space-y-3">
                {displayAgents.map((agent, index) => (
                    <div 
                        key={agent.id} 
                        className="group p-4 rounded-xl bg-white/5 border border-white/5 hover:border-cyan-500/30 hover:bg-cyan-500/5 transition-all cursor-pointer flex items-center justify-between"
                        onClick={() => onSelectAgent?.(agent)}
                    >
                        <div className="flex items-center gap-4">
                            <div className={`w-8 h-8 rounded-lg flex items-center justify-center font-black text-xs ${
                                index === 0 ? 'bg-yellow-500/20 text-yellow-500' : 
                                index === 1 ? 'bg-slate-300/20 text-slate-300' : 
                                'bg-orange-600/20 text-orange-600'
                            }`}>
                                #{index + 1}
                            </div>
                            <div>
                                <h4 className="text-sm font-bold text-white group-hover:text-cyan-400 transition-colors">{agent.name}</h4>
                                <div className="flex items-center gap-3 text-[9px] text-slate-500 font-mono uppercase">
                                    <span>Gen {agent.generation}</span>
                                    <span>•</span>
                                    <span className="flex items-center gap-1"><Target size={10} /> {(agent.fitness * 100).toFixed(1)}%</span>
                                </div>
                            </div>
                        </div>

                        <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button className="p-2 rounded-lg bg-cyan-600 text-white shadow-lg shadow-cyan-500/20">
                                <Play size={12} fill="currentColor" />
                            </button>
                            <button className="p-2 rounded-lg bg-white/10 text-slate-400 hover:text-white">
                                <Zap size={12} />
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <button className="w-full mt-6 py-3 rounded-xl border border-white/5 text-[10px] font-black text-slate-500 uppercase tracking-widest hover:bg-white/5 hover:text-white transition-all flex items-center justify-center gap-2">
                <Share2 size={12} /> EXPORT_GENOME_REGISTRY
            </button>
        </div>
    );
};

export default AgentHallOfFame;
