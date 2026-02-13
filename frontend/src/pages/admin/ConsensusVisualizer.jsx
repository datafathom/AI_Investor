import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { MessagesSquare, ThumbsUp, ThumbsDown } from 'lucide-react';

const ConsensusVisualizer = () => {
    const [debates, setDebates] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/orchestrator/consensus/active');
            if (res.data.success) setDebates(res.data.data);
        };
        const interval = setInterval(load, 3000); // Live Consensus
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <MessagesSquare className="text-orange-500" /> Multi-Agent Consensus
                </h1>
                <p className="text-slate-500">Real-Time Decision Debate Visualizer</p>
            </header>

            <div className="grid grid-cols-1 gap-8">
                {debates.length === 0 && <div className="text-slate-500">No active debates. System aligned.</div>}
                
                {debates.map(d => (
                    <div key={d.id} className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                        <div className="flex justify-between items-start mb-6">
                            <div>
                                <h3 className="text-xl font-bold text-white">{d.topic}</h3>
                                <div className="flex items-center gap-2 mt-2">
                                    <span className="text-xs font-bold bg-orange-900/30 text-orange-400 px-2 py-1 rounded border border-orange-900">{d.status}</span>
                                    <span className="text-xs text-slate-500">Threshold: {(d.threshold * 100).toFixed(0)}%</span>
                                </div>
                            </div>
                            <div className="text-right">
                                <div className="text-4xl font-bold text-slate-200">{(d.progress * 100).toFixed(0)}%</div>
                                <div className="text-xs text-slate-500">Consensus</div>
                            </div>
                        </div>

                        {/* Progress Bar */}
                        <div className="h-4 bg-slate-950 rounded-full mb-8 overflow-hidden relative border border-slate-800">
                             <div className="absolute top-0 bottom-0 left-[70%] w-0.5 bg-white/30 z-10" title="Threshold"></div>
                             <div className={`h-full transition-all duration-500 ${d.progress >= d.threshold ? 'bg-emerald-500' : 'bg-orange-500'}`} style={{ width: `${d.progress * 100}%` }}></div>
                        </div>

                        {/* Votes */}
                        <div className="space-y-3">
                            {d.votes.map((v, i) => (
                                <div key={i} className="flex gap-4 p-4 bg-slate-950 rounded border border-slate-800 items-start animate-in slide-in-from-left duration-300" style={{ animationDelay: `${i * 100}ms` }}>
                                    <div className={`p-2 rounded-full ${v.vote === 'YES' ? 'bg-emerald-900/50 text-emerald-400' : 'bg-red-900/50 text-red-400'}`}>
                                        {v.vote === 'YES' ? <ThumbsUp size={16} /> : <ThumbsDown size={16} />}
                                    </div>
                                    <div className="flex-1">
                                        <div className="font-bold text-white text-sm">{v.agent}</div>
                                        <div className="text-slate-400 text-sm italic">"{v.reason}"</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ConsensusVisualizer;
