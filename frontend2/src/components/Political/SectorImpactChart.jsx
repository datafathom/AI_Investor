import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const SectorImpactChart = () => {
    const data = [
        { name: 'Tech', value: 85, impact: 'high' },
        { name: 'Energy', value: 65, impact: 'medium' },
        { name: 'Health', value: 45, impact: 'medium' },
        { name: 'Finance', value: 90, impact: 'high' },
        { name: 'Defense', value: 75, impact: 'high' },
    ];

    return (
        <div className="h-full w-full flex flex-col">
            <h3 className="text-sm font-bold text-amber-200 mb-2 uppercase tracking-wider flex justify-between">
                <span>Legislative Pressure</span>
                <span className="text-[10px] text-slate-400 font-normal">Bill Volume by Sector</span>
            </h3>
            <div className="flex-1 min-h-[150px]">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                        <XAxis type="number" hide />
                        <YAxis dataKey="name" type="category" width={60} tick={{ fill: '#94a3b8', fontSize: 10 }} axisLine={false} tickLine={false} />
                        <Tooltip
                            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', fontSize: '12px' }}
                            itemStyle={{ color: '#fbbf24' }}
                            cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                        />
                        <Bar dataKey="value" radius={[0, 4, 4, 0]} barSize={12}>
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.value > 80 ? '#ef4444' : '#f59e0b'} />
                            ))}
                        </Bar>
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default SectorImpactChart;
