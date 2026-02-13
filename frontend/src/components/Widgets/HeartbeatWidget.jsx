import React, { useState, useEffect } from 'react';
import { agentService } from '../../services/agentService';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { HeartPulse, AlertTriangle } from 'lucide-react';

export const HeartbeatWidget = () => {
    const [heartbeats, setHeartbeats] = useState([]);
    const [history, setHistory] = useState([]);

    useEffect(() => {
        const interval = setInterval(fetchHeartbeats, 2000);
        return () => clearInterval(interval);
    }, []);

    const fetchHeartbeats = async () => {
        try {
            const res = await agentService.getHeartbeats();
            setHeartbeats(res);
            
            // Update history chart (count of alive agents)
            const aliveCount = res.filter(a => a.is_alive).length;
            setHistory(prev => {
                const newHistory = [...prev, { time: new Date().toLocaleTimeString(), count: aliveCount }];
                if (newHistory.length > 20) newHistory.shift(); // Keep last 20 ticks
                return newHistory;
            });
        } catch (e) {
            console.error("Failed to fetch heartbeats");
        }
    };

    const aliveCount = heartbeats.filter(a => a.is_alive).length;
    const deadCount = heartbeats.length - aliveCount;
    const healthPercent = heartbeats.length > 0 ? (aliveCount / heartbeats.length) * 100 : 100;

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 h-full flex flex-col">
            <div className="flex justify-between items-center mb-4">
                <h3 className="font-bold text-white flex items-center gap-2">
                    <HeartPulse className="text-pink-500" /> Heartbeat Monitor
                </h3>
                <span className={`text-xs font-bold px-2 py-1 rounded ${healthPercent > 90 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-red-500/20 text-red-400'}`}>
                    {healthPercent.toFixed(1)}% Health
                </span>
            </div>

            <div className="flex-1 min-h-[100px]">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={history}>
                        <defs>
                            <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#ec4899" stopOpacity={0.3}/>
                                <stop offset="95%" stopColor="#ec4899" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <Tooltip contentStyle={{backgroundColor: '#0f172a', borderColor: '#334155'}} />
                        <Area type="monotone" dataKey="count" stroke="#ec4899" fillOpacity={1} fill="url(#colorCount)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-2 gap-2 mt-4">
                <div className="bg-slate-950 p-2 rounded text-center border border-slate-800">
                    <div className="text-xs text-slate-500 uppercase">Alive</div>
                    <div className="text-xl font-bold text-emerald-400">{aliveCount}</div>
                </div>
                <div className="bg-slate-950 p-2 rounded text-center border border-slate-800">
                    <div className="text-xs text-slate-500 uppercase">Dead</div>
                    <div className="text-xl font-bold text-red-400">{deadCount}</div>
                </div>
            </div>

            {deadCount > 0 && (
                <div className="mt-4 p-3 bg-red-500/10 border border-red-500/20 rounded flex items-start gap-3">
                    <AlertTriangle size={16} className="text-red-500 mt-0.5" />
                    <div>
                        <div className="text-xs font-bold text-red-400">Critical Alerts</div>
                        <div className="text-[10px] text-red-300/80 mt-1">
                            {deadCount} agents are unresponsive. Check logs immediately.
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};
