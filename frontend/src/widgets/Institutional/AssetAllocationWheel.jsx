import React, { useState } from 'react';
import { PieChart, RefreshCcw } from 'lucide-react';

const AssetAllocationWheel = () => {
    const [allocations, setAllocations] = useState([
        { type: 'Equity', weight: 60, color: 'text-primary' },
        { type: 'Fixed Income', weight: 30, color: 'text-accent' },
        { type: 'Cash/Alt', weight: 10, color: 'text-success' },
    ]);

    return (
        <div className="glass-premium p-4 rounded-2xl border border-white/5 h-full flex flex-col">
            <h3 className="text-sm font-bold mb-4 flex items-center gap-2 text-primary-light">
                <PieChart size={16} /> STRATEGY REBALANCING
            </h3>
            
            <div className="flex-1 flex flex-col gap-4">
                <div className="flex-1 flex items-center justify-center">
                    <div className="relative w-32 h-32 flex items-center justify-center">
                        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                            {allocations.map((a, idx) => {
                                const offset = allocations.slice(0, idx).reduce((sum, item) => sum + item.weight, 0);
                                return (
                                    <circle
                                        key={a.type}
                                        cx="18" cy="18" r="15.9155"
                                        fill="none"
                                        className={a.color.replace('text-', 'stroke-')}
                                        strokeWidth="3.5"
                                        strokeDasharray={`${a.weight} 100`}
                                        strokeDashoffset={-offset}
                                    />
                                );
                            })}
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center flex-col">
                            <span className="text-[8px] text-slate-500 font-bold uppercase">Drift</span>
                            <span className="text-lg font-black text-white">4.2%</span>
                        </div>
                    </div>
                </div>

                <div className="grid grid-cols-1 gap-1">
                    {allocations.map(a => (
                        <div key={a.type} className="flex items-center justify-between text-[10px] p-1.5 rounded bg-white/5">
                            <div className="flex items-center gap-2">
                                <div className={`w-2 h-2 rounded-full ${a.color.replace('text-', 'bg-')}`} />
                                <span className="text-slate-300 font-bold uppercase tracking-tighter">{a.type}</span>
                            </div>
                            <span className="font-mono text-white">{a.weight}%</span>
                        </div>
                    ))}
                </div>

                <button className="w-full py-2 bg-primary/20 hover:bg-primary/30 text-primary text-[10px] font-black rounded-lg transition-all flex items-center justify-center gap-2 border border-primary/30">
                    <RefreshCcw size={12} /> REBALANCE NOW
                </button>
            </div>
        </div>
    );
};

export default AssetAllocationWheel;
