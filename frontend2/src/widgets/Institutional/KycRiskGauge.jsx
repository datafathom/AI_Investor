import React from 'react';
import { ShieldCheck, ShieldAlert } from 'lucide-react';

const KycRiskGauge = ({ status = 'Verified' }) => {
    const isFlagged = status === 'Flagged';
    const isPending = status === 'Pending';

    return (
        <div className="glass-premium p-4 rounded-2xl border border-white/5 h-full flex flex-col">
            <h3 className="text-sm font-bold mb-4 flex items-center gap-2 text-danger-light">
                <ShieldCheck size={16} /> COMPLIANCE RISK GAUGE
            </h3>
            
            <div className="flex-1 flex flex-col justify-between">
                <div className="flex items-center justify-between p-4 rounded-2xl bg-white/5 border border-white/5 overflow-hidden relative">
                    {isFlagged && <div className="absolute inset-0 bg-danger/10 animate-pulse" />}
                    
                    <div className="flex flex-col gap-1 relative">
                        <span className="text-[10px] text-slate-500 uppercase">Current Status</span>
                        <span className={`text-xl font-black ${
                            isFlagged ? "text-danger" : isPending ? "text-warning" : "text-success"
                        }`}>
                            {status.toUpperCase()}
                        </span>
                    </div>

                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center border-2 relative ${
                        isFlagged ? "bg-danger/20 border-danger/40 text-danger" : 
                        isPending ? "bg-warning/20 border-warning/40 text-warning" : 
                        "bg-success/20 border-success/40 text-success"
                    }`}>
                        {isFlagged ? <ShieldAlert size={24} /> : <ShieldCheck size={24} />}
                    </div>
                </div>

                <div className="space-y-3 mt-4">
                    <div className="flex justify-between text-[9px] uppercase font-bold text-slate-500">
                        <span>Risk exposure profile</span>
                        <span className="text-white">Minimal</span>
                    </div>
                    <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden flex">
                        <div className="h-full bg-success w-4/5" />
                        <div className="h-full bg-warning w-1/5" />
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-[8px] font-bold">
                        <div className="flex items-center gap-1.5 text-success">
                            <div className="w-1.5 h-1.5 rounded-full bg-current" />
                            SEC COMPLIANT
                        </div>
                        <div className="flex items-center gap-1.5 text-success">
                            <div className="w-1.5 h-1.5 rounded-full bg-current" />
                            GDPR VERIFIED
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default KycRiskGauge;
