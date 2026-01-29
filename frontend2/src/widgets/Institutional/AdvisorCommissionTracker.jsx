import React from 'react';
import { Landmark, TrendingUp } from 'lucide-react';

const AdvisorCommissionTracker = () => {
    return (
        <div className="glass-premium p-4 rounded-2xl border border-white/5 h-full flex flex-col overflow-hidden relative">
            <div className="absolute top-0 right-0 w-32 h-32 bg-primary/10 blur-3xl rounded-full -mr-16 -mt-16" />
            
            <h3 className="text-sm font-bold mb-4 flex items-center gap-2 text-success-light relative">
                <Landmark size={16} /> COMMISSIONS TRACKER
            </h3>
            
            <div className="flex-1 flex flex-col justify-between relative">
                <div className="space-y-4">
                    <div>
                        <div className="text-[10px] text-slate-500 uppercase tracking-widest mb-1">MTD Earnings</div>
                        <div className="flex items-baseline gap-2">
                            <span className="text-3xl font-black text-white">$42,850</span>
                            <span className="text-xs font-bold text-success flex items-center">
                                <TrendingUp size={10} /> +12%
                            </span>
                        </div>
                    </div>

                    <div className="h-16 flex items-end gap-1 px-1">
                        {[40, 60, 45, 70, 55, 85, 65, 95].map((h, i) => (
                            <div 
                                key={i} 
                                className="flex-1 bg-gradient-to-t from-primary/20 to-primary rounded-t-sm"
                                style={{ height: `${h}%` }}
                            />
                        ))}
                    </div>
                </div>

                <div className="grid grid-cols-2 gap-2 mt-4">
                    <div className="p-2 rounded-lg bg-white/5 border border-white/5">
                        <div className="text-[8px] text-slate-500 uppercase">Avg Management Fee</div>
                        <div className="text-xs font-bold text-white">0.95%</div>
                    </div>
                    <div className="p-2 rounded-lg bg-white/5 border border-white/5">
                        <div className="text-[8px] text-slate-500 uppercase">Payout Ratio</div>
                        <div className="text-xs font-bold text-white">45.0%</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default AdvisorCommissionTracker;
