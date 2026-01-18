import React, { useState } from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Plus, Trash2 } from 'lucide-react';

const StrategyBuilder = () => {
    const [legs, setLegs] = useState([
        { type: 'Call', action: 'Buy', strike: 410, qty: 1, premium: 5.2 },
        { type: 'Call', action: 'Sell', strike: 420, qty: 1, premium: 2.1 }
    ]);

    // Generate Payoff Diagram Data
    const generatePayoff = () => {
        const data = [];
        for (let price = 380; price <= 450; price += 1) {
            let pnl = 0;
            legs.forEach(leg => {
                let legPnl = 0;
                if (leg.type === 'Call') {
                    const intrinsic = Math.max(0, price - leg.strike);
                    legPnl = (intrinsic - leg.premium) * 100 * leg.qty;
                    if (leg.action === 'Sell') legPnl *= -1;
                } else {
                    const intrinsic = Math.max(0, leg.strike - price);
                    legPnl = (intrinsic - leg.premium) * 100 * leg.qty;
                    if (leg.action === 'Sell') legPnl *= -1;
                }
                pnl += legPnl;
            });
            data.push({ price, pnl });
        }
        return data;
    };

    return (
        <div className="h-full flex flex-col gap-4">
            <h3 className="text-xs font-bold text-slate-500 uppercase px-2 flex justify-between">
                <span>Payoff Analyzer</span>
                <button className="text-cyan-400 flex items-center gap-1 hover:text-cyan-300"><Plus size={12} /> ADD LEG</button>
            </h3>

            <div className="flex-1 min-h-[150px] bg-slate-900/50 rounded border border-slate-700 p-2 relative">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={generatePayoff()}>
                        <defs>
                            <linearGradient id="splitColor" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="0.49" stopColor="#10b981" stopOpacity={0.4} />
                                <stop offset="0.51" stopColor="#ef4444" stopOpacity={0.4} />
                            </linearGradient>
                        </defs>
                        <XAxis dataKey="price" hide />
                        <YAxis hide />
                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155' }} />
                        <ReferenceLine y={0} stroke="#64748b" strokeDasharray="3 3" />
                        <Area type="monotone" dataKey="pnl" stroke="#f59e0b" fill="url(#splitColor)" strokeWidth={2} />
                    </AreaChart>
                </ResponsiveContainer>
                <div className="absolute top-2 left-2 text-xs font-mono text-slate-400">Max Profit: <span className="text-green-400">$310</span></div>
            </div>

            <div className="space-y-1 overflow-y-auto max-h-[100px]">
                {legs.map((leg, i) => (
                    <div key={i} className="flex items-center justify-between p-2 bg-slate-800 rounded text-xs border border-transparent hover:border-indigo-500/50 transition-all hover:scale-[1.01] interact-hover shadow-lg">
                        <div className="flex gap-2">
                            <span className={`font-bold ${leg.action === 'Buy' ? 'text-green-400' : 'text-red-400'}`}>{leg.action}</span>
                            <span className="text-slate-300">{leg.qty}x {leg.type} {leg.strike}</span>
                        </div>
                        <div className="flex gap-2 items-center">
                            <span className="font-mono text-slate-500">${leg.premium}</span>
                            <button className="text-slate-600 hover:text-red-400"><Trash2 size={12} /></button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default StrategyBuilder;
