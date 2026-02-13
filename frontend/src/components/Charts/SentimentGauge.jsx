import React from 'react';

const SentimentGauge = ({ score }) => {
    // Score is -100 to 100
    const normalized = (score + 100) / 200; // 0 to 1
    
    const getColor = (s) => {
        if (s > 50) return '#10b981'; // emerald-500
        if (s > 20) return '#34d399'; // emerald-400
        if (s > -20) return '#94a3b8'; // slate-400
        if (s > -50) return '#f87171'; // red-400
        return '#ef4444'; // red-500
    };

    const color = getColor(score);
    const rotation = -90 + (normalized * 180); // -90 deg (left) to 90 deg (right)

    return (
        <div className="relative w-40 h-24 flex items-end justify-center overflow-hidden">
             {/* Background Arc */}
            <div className="absolute top-0 w-36 h-36 rounded-full border-[12px] border-slate-800 border-b-0 border-l-0 border-r-0 aspect-square"
                 style={{ clipPath: 'polygon(0 0, 100% 0, 100% 50%, 0 50%)', transform: 'rotate(180deg)' }}>
            </div>
            
            {/* Needle */}
            <div className="absolute bottom-0 left-1/2 w-1 h-20 bg-slate-600 origin-bottom transition-transform duration-700 ease-out z-10"
                 style={{ transform: `translateX(-50%) rotate(${rotation}deg)` }}>
                <div className="absolute -top-1 left-1/2 w-3 h-3 bg-white rounded-full -translate-x-1/2"></div>
            </div>

            {/* Pivot */}
            <div className="absolute bottom-0 w-4 h-4 bg-slate-200 rounded-full z-20"></div>

            {/* Labels */}
            <div className="absolute top-8 left-2 text-[10px] text-red-500 font-bold">BEAR</div>
            <div className="absolute top-2 left-1/2 -translate-x-1/2 text-[10px] text-slate-500 font-bold">NEUTRAL</div>
            <div className="absolute top-8 right-2 text-[10px] text-emerald-500 font-bold">BULL</div>

             {/* Value */}
             <div className="absolute bottom-6 font-mono font-bold text-xl" style={{ color }}>
                 {score > 0 ? '+' : ''}{score}
             </div>
        </div>
    );
};

export default SentimentGauge;
