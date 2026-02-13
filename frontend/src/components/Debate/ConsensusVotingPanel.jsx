import React, { useState, useEffect } from 'react';
import { debateService } from '../../services/debateService';
import { CheckCircle, XCircle, MinusCircle, User, Activity } from 'lucide-react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const VoteGauge = ({ percentage, threshold = 70 }) => {
    const radius = 40;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (percentage / 100) * circumference;
    const color = percentage >= threshold ? 'text-emerald-500' : 'text-slate-500';

    return (
        <div className="relative flex items-center justify-center w-32 h-32">
            <svg className="w-full h-full transform -rotate-90">
                <circle
                    className="text-slate-800"
                    strokeWidth="8"
                    stroke="currentColor"
                    fill="transparent"
                    r={radius}
                    cx="64"
                    cy="64"
                />
                <circle
                    className={`${color} transition-all duration-1000 ease-out`}
                    strokeWidth="8"
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                    strokeLinecap="round"
                    stroke="currentColor"
                    fill="transparent"
                    r={radius}
                    cx="64"
                    cy="64"
                />
            </svg>
            <div className="absolute text-center">
                <span className={`text-2xl font-bold ${color}`}>{percentage}%</span>
                <div className="text-[10px] text-slate-500">APPROVAL</div>
            </div>
        </div>
    );
};

export const ConsensusVotingPanel = ({ sessionId }) => {
    // Mock data fetching or integrate prop
    const [stats, setStats] = useState({
        approval_pct: 0,
        votes: {
            "The Bull": { vote: "APPROVE", reasoning: "Strong trend" },
            "The Bear": { vote: "REJECT", reasoning: "Overbought" }
        },
        decision: "PENDING"
    });

    // In real app, fetch from /sessions/{id}/votes
    // For now, let's assume parent passes data or we mock it
    
    const votesList = Object.entries(stats.votes).map(([agent, data]) => ({
        agent,
        ...data
    }));

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 flex flex-col gap-4">
             <div className="flex justify-between items-center mb-2">
                <h3 className="font-bold text-white flex items-center gap-2">
                    <Activity size={16} className="text-cyan-500" /> Consensus Engine
                </h3>
                <span className={`px-2 py-0.5 text-xs rounded font-bold ${stats.decision === 'APPROVE' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-slate-800 text-slate-400'}`}>
                    {stats.decision}
                </span>
            </div>

            <div className="flex items-center justify-between">
                <VoteGauge percentage={stats.approval_pct} />
                
                <div className="flex-1 pl-4 space-y-2">
                    {votesList.map((v, i) => (
                        <div key={i} className="flex items-center justify-between text-xs bg-slate-950 p-2 rounded border border-slate-800">
                            <div className="flex items-center gap-2">
                                <span className="text-slate-300 font-bold">{v.agent}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className={`font-bold ${v.vote === 'APPROVE' ? 'text-emerald-400' : v.vote === 'REJECT' ? 'text-red-400' : 'text-slate-500'}`}>
                                    {v.vote}
                                </span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
            
            <button className="w-full bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs py-2 rounded flex items-center justify-center gap-2 transition-colors">
                <User size={12} /> Override Decision
            </button>
        </div>
    );
};
