import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';

const PLWaterfall = () => {
    // Breakdown of PnL Attribution
    const data = [
        { name: 'Core Equities', val: 12500 },
        { name: 'Options Hedges', val: -3200 },
        { name: 'Crypto', val: 4100 },
        { name: 'Forex', val: -800 },
        { name: 'Fees/Comms', val: -150 },
        { name: 'Dividends', val: 560 },
        { name: 'Total Net', val: 13010, isTotal: true }
    ];

    // Cumulative data for waterfall logic
    let cum = 0;
    const chartData = data.map(d => {
        const start = cum;
        const end = d.isTotal ? 0 : cum + d.val;
        if (!d.isTotal) cum = end;

        return {
            ...d,
            start: d.isTotal ? 0 : start,
            end: d.isTotal ? d.val : end,
            fill: d.isTotal ? '#3b82f6' : (d.val >= 0 ? '#10b981' : '#ef4444')
        };
    });

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-500 uppercase mb-2">Performance Attribution</h3>
            <div className="flex-1 min-h-[150px]">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={chartData}>
                        <XAxis dataKey="name" stroke="#475569" tick={{ fontSize: 10 }} interval={0} />
                        <YAxis stroke="#475569" tick={{ fontSize: 10 }} />
                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155' }} />
                        <ReferenceLine y={0} stroke="#64748b" />
                        <Bar dataKey="end" radius={[2, 2, 0, 0]} className="cursor-pointer">
                            {chartData.map((entry, index) => (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={entry.fill}
                                    className="hover:opacity-80 transition-opacity"
                                />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default PLWaterfall;
