import React from 'react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const ResourceTimeline = () => {
    // Generate mock data for last 20 points
    const data = Array.from({ length: 20 }, (_, i) => ({
        time: i,
        cpu: 20 + Math.random() * 30,
        memory: 40 + Math.random() * 10
    }));

    return (
        <div className="w-full h-full flex flex-col">
            <h3 className="text-[10px] uppercase font-bold text-slate-500 mb-2 px-2">System Resources (Last 1h)</h3>
            <div className="flex-1 min-h-[100px]">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorCpu" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="colorMem" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <Tooltip
                            contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', fontSize: '12px' }}
                            itemStyle={{ color: '#cbd5e1' }}
                        />
                        <Area type="monotone" dataKey="cpu" stroke="#06b6d4" fillOpacity={1} fill="url(#colorCpu)" strokeWidth={2} />
                        <Area type="monotone" dataKey="memory" stroke="#8b5cf6" fillOpacity={1} fill="url(#colorMem)" strokeWidth={2} />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
            <div className="flex justify-between px-2 text-[10px] text-slate-500 font-mono mt-1">
                <span className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-cyan-500"></div> CPU avg 35%</span>
                <span className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-violet-500"></div> MEM avg 42%</span>
            </div>
        </div>
    );
};

export default ResourceTimeline;
