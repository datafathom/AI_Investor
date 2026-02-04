import React from 'react';

const ConsensusMeter = ({ score = 65 }) => {
    // Score -100 (Strong Bear) to 100 (Strong Bull)
    // Normalized 0-100 for gauge
    const normalized = (score + 100) / 2; // 0 to 100

    return (
        <div className="bg-slate-900/50 p-4 rounded border border-slate-700 flex flex-col items-center">
            <h3 className="text-xs font-bold text-slate-400 mb-4 uppercase tracking-wider">Consensus Verdict</h3>

            <div className="relative w-48 h-24 overflow-hidden mb-2">
                {/* Gauge Background */}
                <div className="absolute top-0 left-0 w-full h-full bg-slate-800 rounded-t-full"></div>

                {/* Zones */}
                <div className="absolute top-0 left-0 w-full h-full rounded-t-full bg-[conic-gradient(from_-90deg_at_50%_100%,#ef4444_0deg_36deg,#f59e0b_36deg_72deg,#64748b_72deg_108deg,#3b82f6_108deg_144deg,#22c55e_144deg_180deg)] opacity-30"></div>

                {/* Needle */}
                <div
                    className="absolute bottom-0 left-1/2 w-1 h-20 bg-white origin-bottom transition-transform duration-1000 ease-out"
                    style={{ transform: `translateX(-50%) rotate(${(normalized * 1.8) - 90}deg)` }}
                ></div>
                <div className="absolute bottom-0 left-1/2 w-4 h-4 bg-white rounded-full -translate-x-1/2 translate-y-2"></div>
            </div>

            <div className="text-2xl font-bold text-white mt-1">
                {score > 50 ? 'STRONG BUY' : (score > 20 ? 'BUY' : (score < -50 ? 'STRONG SELL' : (score < -20 ? 'SELL' : 'HOLD')))}
            </div>
            <div className={`text-sm font-mono ${score > 0 ? 'text-green-400' : (score < 0 ? 'text-red-400' : 'text-slate-400')}`}>
                {score > 0 ? '+' : ''}{score} POINTS
            </div>
        </div>
    );
};

export default ConsensusMeter;
