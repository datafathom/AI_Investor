import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const MonteCarloFan = () => {
    const [paths, setPaths] = useState([]);

    useEffect(() => {
        // Generate 20 random walks
        const newPaths = [];
        for (let i = 0; i < 20; i++) {
            const path = [{ day: 0, val: 100 }];
            for (let d = 1; d <= 30; d++) {
                const prev = path[d - 1].val;
                const change = (Math.random() - 0.48) * 5; // Slight drift up
                path.push({ day: d, val: prev + change });
            }
            newPaths.push(path);
        }
        setPaths(newPaths);
    }, []);

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-500 uppercase mb-2">Equity Projections (MC Sim)</h3>
            <div className="flex-1 min-h-[150px] relative">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart>
                        <XAxis dataKey="day" type="number" hide />
                        <YAxis domain={['auto', 'auto']} hide />
                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155' }} />
                        {paths.map((path, i) => (
                            <Line
                                key={i}
                                data={path}
                                type="monotone"
                                dataKey="val"
                                stroke={i === 0 ? '#10b981' : '#64748b'}
                                strokeWidth={i === 0 ? 3 : 1}
                                strokeOpacity={i === 0 ? 1 : 0.15}
                                className={i === 0 ? 'animate-neon-pulse' : ''}
                                dot={false}
                            />
                        ))}
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default MonteCarloFan;
