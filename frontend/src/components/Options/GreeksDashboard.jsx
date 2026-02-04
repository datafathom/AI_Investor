import React from 'react';

const GreeksDashboard = () => {
    const greeks = [
        { name: 'Delta', val: 0.45, color: 'text-cyan-400', max: 1 },
        { name: 'Gamma', val: 0.08, color: 'text-purple-400', max: 0.2 },
        { name: 'Theta', val: -12.4, color: 'text-orange-400', max: -50 }, // Decay
        { name: 'Vega', val: 0.15, color: 'text-green-400', max: 0.5 }
    ];

    return (
        <div className="flex justify-between gap-2 h-full items-center px-4">
            {greeks.map((g, i) => (
                <div key={i} className="flex flex-col items-center">
                    <div className="relative w-16 h-16 flex items-center justify-center bg-slate-800 rounded-full border-4 border-slate-700">
                        {/* Simple CSS gauge fill simulation */}
                        <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 36 36">
                            <path
                                className={`${g.color.replace('text', 'stroke')} transition-all duration-1000 ${g.name === 'Delta' ? 'animate-neon-pulse' : ''}`}
                                strokeDasharray={`${Math.abs(g.val / g.max) * 100}, 100`}
                                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                fill="none"
                                strokeWidth="3"
                            />
                        </svg>
                        <span className={`font-mono font-bold text-sm ${g.color} ${g.name === 'Delta' ? 'text-glow-cyan' : ''}`}>{g.val}</span>
                    </div>
                    <span className="text-[10px] uppercase font-bold text-slate-500 mt-2">{g.name}</span>
                </div>
            ))}
        </div>
    );
};

export default GreeksDashboard;
