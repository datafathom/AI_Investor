import React, { useState } from 'react';
import { Calculator, TrendingUp } from 'lucide-react';

const FeeRevenueForecast = ({ aum = 10000000 }) => {
    const [bps, setBps] = useState(125); // 1.25%
    
    const annualFee = (aum * bps) / 10000;
    const monthlyFee = annualFee / 12;

    return (
        <div className="glass-premium p-4 rounded-2xl border border-white/5 h-full flex flex-col">
            <h3 className="text-sm font-bold mb-4 flex items-center gap-2 text-primary-light">
                <Calculator size={16} /> REVENUE FORECAST (1.25%)
            </h3>
            
            <div className="flex-1 flex flex-col justify-center gap-6">
                <div className="space-y-1">
                    <div className="text-[10px] text-slate-500 uppercase tracking-widest">Est. Annual Revenue</div>
                    <div className="text-3xl font-black text-white font-mono">
                        ${annualFee.toLocaleString(undefined, { minimumFractionDigits: 0, maximumFractionDigits: 0 })}
                    </div>
                </div>

                <div className="flex justify-between items-center p-3 rounded-xl bg-white/5 border border-white/5">
                    <div>
                        <div className="text-[10px] text-slate-500 uppercase">Monthly Yield</div>
                        <div className="text-lg font-bold text-success font-mono">${monthlyFee.toLocaleString(undefined, { maximumFractionDigits: 0 })}</div>
                    </div>
                    <div className="text-right">
                        <div className="text-[10px] text-slate-500 uppercase">AUM Basis</div>
                        <div className="text-xs font-bold text-slate-300">${(aum/1000000).toFixed(1)}M</div>
                    </div>
                </div>

                <div className="space-y-2">
                    <div className="flex justify-between text-[10px] font-bold">
                        <span className="text-slate-500">ADVISOR MULTIPLIER</span>
                        <span className="text-primary">{bps} BPS</span>
                    </div>
                    <input 
                        type="range" 
                        min="10" 
                        max="250" 
                        value={bps}
                        onChange={(e) => setBps(parseInt(e.target.value))}
                        className="w-full h-1 bg-white/10 rounded-lg appearance-none cursor-pointer accent-primary"
                    />
                </div>
            </div>
        </div>
    );
};

export default FeeRevenueForecast;
