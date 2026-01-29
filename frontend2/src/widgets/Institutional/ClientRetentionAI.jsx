import React from 'react';
import { BrainCircuit, AlertTriangle } from 'lucide-react';

const ClientRetentionAI = ({ score = 92.5 }) => {
    const isAtRisk = score < 80;

    return (
        <div className="glass-premium p-4 rounded-2xl border border-white/5 h-full flex flex-col">
            <h3 className="text-sm font-bold mb-4 flex items-center gap-2 text-accent-light">
                <BrainCircuit size={16} /> CLIENT RETENTION AI
            </h3>
            
            <div className="flex-1 flex flex-col items-center justify-center gap-4">
                <div className="relative w-32 h-32">
                    <svg className="w-full h-full" viewBox="0 0 36 36">
                        <path
                            className="text-white/5"
                            strokeDasharray="100, 100"
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="3"
                        />
                        <path
                            className={isAtRisk ? "text-danger" : "text-success"}
                            strokeDasharray={`${score}, 100`}
                            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="3"
                            strokeLinecap="round"
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center">
                        <span className="text-2xl font-black text-white">{score}%</span>
                        <span className="text-[8px] uppercase text-slate-500 font-bold">Health</span>
                    </div>
                </div>

                <div className="w-full space-y-2">
                    <div className={`p-2 rounded-lg border flex items-center gap-2 ${
                        isAtRisk ? "bg-danger/10 border-danger/30 text-danger" : "bg-success/10 border-success/30 text-success"
                    }`}>
                        <AlertTriangle size={12} className={!isAtRisk && "opacity-0"} />
                        <span className="text-[10px] font-bold uppercase">
                            {isAtRisk ? "High Churn Risk Detected" : "Stable Client Relations"}
                        </span>
                    </div>
                    <p className="text-[9px] text-slate-500 text-center px-4">
                        ML model predicts 7% uplift in retention if quarterly review is scheduled this week.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default ClientRetentionAI;
