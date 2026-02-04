import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const SentimentGraph = () => {
    const [data, setData] = useState([]);

    useEffect(() => {
        // Initial data
        const initial = Array.from({ length: 20 }, (_, i) => ({
            time: i,
            bull: 50 + Math.random() * 20,
            bear: 50 + Math.random() * 20,
            sentiment: 0
        }));
        setData(initial);

        const interval = setInterval(() => {
            setData(prev => {
                const last = prev[prev.length - 1];
                const newBull = 50 + Math.random() * 40;
                const newBear = 50 + Math.random() * 40;
                return [...prev.slice(1), {
                    time: last.time + 1,
                    bull: newBull,
                    bear: newBear,
                    sentiment: (newBull - newBear)
                }];
            });
        }, 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-400 mb-2 uppercase tracking-wider px-2">Live Debate Sentiment</h3>
            <div className="flex-1 min-h-[100px]">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <XAxis dataKey="time" hide />
                        <YAxis domain={[-100, 100]} hide />
                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: 'none' }} itemStyle={{ fontSize: '12px' }} />
                        <Line type="monotone" dataKey="sentiment" stroke="#38bdf8" strokeWidth={2} dot={false} animationDuration={300} />
                    </LineChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default SentimentGraph;
