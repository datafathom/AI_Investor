import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const TradeScatter = () => {
    // Mock Trades: X = Entry Efficiency (0-1), Y = Exit Efficiency (0-1)
    const data = Array.from({ length: 50 }, (_, i) => ({
        id: i,
        entry: 0.5 + (Math.random() * 0.5),
        exit: 0.5 + (Math.random() * 0.5),
        pnl: (Math.random() - 0.3) * 1000
    }));

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-500 uppercase mb-2">Trade Execution Efficiency</h3>
            <div className="flex-1 min-h-[150px]">
                <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart margin={{ top: 10, right: 10, bottom: 10, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                        <XAxis type="number" dataKey="entry" name="Entry Eff" unit="%" stroke="#475569" tick={{ fontSize: 10 }} domain={[0.4, 1]} />
                        <YAxis type="number" dataKey="exit" name="Exit Eff" unit="%" stroke="#475569" tick={{ fontSize: 10 }} domain={[0.4, 1]} />
                        <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155' }} />
                        <Scatter name="Trades" data={data} fill="#8884d8">
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.pnl > 0 ? '#10b981' : '#ef4444'} />
                            ))}
                        </Scatter>
                    </ScatterChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default TradeScatter;
