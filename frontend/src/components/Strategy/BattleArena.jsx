import React, { useState, useEffect } from 'react';
import { Play, Pause, RefreshCw, Trophy } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const BattleArena = () => {
    const [isRunning, setIsRunning] = useState(false);
    const [progress, setProgress] = useState(0);
    const [data, setData] = useState([{ time: 0, s1: 1000, s2: 1000 }]);
    const [winner, setWinner] = useState(null);

    useEffect(() => {
        let interval;
        if (isRunning && progress < 100) {
            interval = setInterval(() => {
                setData(prev => {
                    const last = prev[prev.length - 1];
                    // Random walk with drift
                    const s1Change = (Math.random() - 0.45) * 50; // Slight inherent edge
                    const s2Change = (Math.random() - 0.48) * 60; // Higher volt, less edge
                    return [...prev, {
                        time: prev.length,
                        s1: last.s1 + s1Change,
                        s2: last.s2 + s2Change
                    }];
                });
                setProgress(p => p + 1);
            }, 100);
        } else if (progress >= 100) {
            setIsRunning(false);
            const last = data[data.length - 1];
            setWinner(last.s1 > last.s2 ? 'Strategy A' : 'Strategy B');
        }
        return () => clearInterval(interval);
    }, [isRunning, progress, data]);

    const reset = () => {
        setIsRunning(false);
        setProgress(0);
        setData([{ time: 0, s1: 1000, s2: 1000 }]);
        setWinner(null);
    };

    return (
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-4 h-full flex flex-col">
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-sm font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-2">
                    <Trophy size={16} /> Strategy Battle Arena
                </h3>
                <div className="flex gap-2">
                    <button
                        onClick={() => setIsRunning(!isRunning)}
                        disabled={progress >= 100}
                        className={`p-2 rounded ${isRunning ? 'bg-amber-600' : 'bg-emerald-600'} hover:opacity-90 transition-opacity`}
                    >
                        {isRunning ? <Pause size={16} /> : <Play size={16} />}
                    </button>
                    <button onClick={reset} className="p-2 bg-slate-700 rounded hover:bg-slate-600">
                        <RefreshCw size={16} />
                    </button>
                </div>
            </div>

            <div className="flex-1 min-h-[200px] relative">
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <XAxis dataKey="time" hide />
                        <YAxis domain={['auto', 'auto']} hide />
                        <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #334155' }} />
                        <Legend />
                        <Line type="monotone" dataKey="s1" stroke="#34d399" strokeWidth={2} dot={false} name="Strat A (Trend)" />
                        <Line type="monotone" dataKey="s2" stroke="#f472b6" strokeWidth={2} dot={false} name="Strat B (Mean Rev)" />
                    </LineChart>
                </ResponsiveContainer>

                {winner && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black/50 backdrop-blur-sm animate-in zoom-in">
                        <div className="text-center p-6 bg-slate-800 border-2 border-emerald-500 rounded-xl shadow-2xl">
                            <Trophy size={48} className="text-emerald-400 mx-auto mb-2 animate-bounce" />
                            <h2 className="text-2xl font-bold text-white mb-1">{winner} Wins!</h2>
                            <p className="text-emerald-400 font-mono">+{(data[data.length - 1][winner === 'Strategy A' ? 's1' : 's2'] - 1000).toFixed(2)} pts</p>
                        </div>
                    </div>
                )}
            </div>

            <div className="h-2 bg-slate-800 rounded-full mt-4 overflow-hidden">
                <div className="h-full bg-emerald-500 transition-all duration-100" style={{ width: `${progress}%` }}></div>
            </div>
        </div>
    );
};

export default BattleArena;
