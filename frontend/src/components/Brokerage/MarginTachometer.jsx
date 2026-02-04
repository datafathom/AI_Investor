import React, { useState } from 'react';
import { AlertCircle } from 'lucide-react';

const MarginTachometer = () => {
    // Value 0 to 100
    const [marginUsage, setMarginUsage] = useState(65);
    const [crashScenario, setCrashScenario] = useState(0);

    const adjustedUsage = Math.min(100, marginUsage + (crashScenario * 1.5));

    return (
        <div className="h-full flex flex-col items-center justify-center p-4">
            <h3 className="text-xs font-bold text-slate-500 uppercase mb-4 tracking-wider">Margin Health</h3>

            <div className="relative w-48 h-24 mb-4">
                {/* Gauge Background */}
                <div className="absolute top-0 left-0 w-full h-full bg-slate-800 rounded-t-full overflow-hidden">
                    <div className="w-full h-full bg-[conic-gradient(from_-90deg_at_50%_100%,#10b981_0deg_90deg,#f59e0b_90deg_144deg,#ef4444_144deg_180deg)] opacity-20"></div>
                </div>

                {/* Needle */}
                <div
                    className="absolute bottom-0 left-1/2 w-1.5 h-20 bg-white origin-bottom transition-all duration-700 ease-out z-10 shadow-[0_0_10px_rgba(255,255,255,0.8)]"
                    style={{ transform: `translateX(-50%) rotate(${(adjustedUsage * 1.8) - 90}deg)` }}
                ></div>

                <div className="absolute bottom-0 left-1/2 w-32 text-center -translate-x-1/2 -translate-y-2">
                    <span className={`text-2xl font-black font-mono transition-colors duration-300 ${adjustedUsage > 90 ? 'text-red-500 animate-pulse text-glow-red' : adjustedUsage > 70 ? 'text-amber-500 text-glow-gold' : 'text-emerald-500 text-glow-cyan'}`}>
                        {adjustedUsage.toFixed(0)}%
                    </span>
                </div>
            </div>

            <div className="w-full space-y-2">
                <div className="flex justify-between text-xs text-slate-400">
                    <span>Simulate Crash</span>
                    <span className="text-red-400">-{crashScenario}%</span>
                </div>
                <input
                    type="range" min="0" max="30" step="1"
                    value={crashScenario}
                    onChange={(e) => setCrashScenario(Number(e.target.value))}
                    className="w-full h-1 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-red-500"
                />
            </div>

            {adjustedUsage > 90 && (
                <div className="mt-4 flex items-center gap-2 text-red-400 text-xs font-bold border border-red-500/30 p-2 rounded bg-red-900/10 animate-pulse">
                    <AlertCircle size={14} /> MARGIN CALL RISK
                </div>
            )}
        </div>
    );
};

export default MarginTachometer;
