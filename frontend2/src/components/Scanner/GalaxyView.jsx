import React, { useEffect, useRef } from 'react';

const GalaxyView = () => {
    // Generate star data
    const stars = Array.from({ length: 50 }, (_, i) => ({
        id: i,
        x: (Math.random() - 0.5) * 800,
        y: (Math.random() - 0.5) * 500,
        z: (Math.random() - 0.5) * 1000,
        size: Math.random() * 4 + 1,
        color: Math.random() > 0.5 ? '#10b981' : '#ef4444',
        ticker: `STK${i}`
    }));

    return (
        <div className="w-full h-full relative overflow-hidden bg-black perspective-[1000px] group">
            <h3 className="absolute top-2 left-2 text-xs font-bold text-slate-500 uppercase z-10 pointer-events-none">Market Galaxy 3D</h3>

            <div className="absolute inset-0 flex items-center justify-center transform-style-3d group-hover:rotate-y-12 transition-transform duration-[2000ms] ease-linear">
                {stars.map((star) => (
                    <div
                        key={star.id}
                        className={`absolute rounded-full shadow-[0_0_20px_currentcolor] animate-neon-pulse transition-all duration-300 hover:scale-[3] z-10 cursor-pointer group/star`}
                        style={{
                            transform: `translate3d(${star.x}px, ${star.y}px, ${star.z}px)`,
                            width: `${star.size}px`,
                            height: `${star.size}px`,
                            backgroundColor: star.color,
                            color: star.color
                        }}
                    >
                        <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-[10px] font-mono font-bold text-white opacity-0 group-hover/star:opacity-100 transition-opacity whitespace-nowrap bg-black/80 px-2 py-0.5 rounded border border-white/20 text-glow-cyan shadow-xl">
                            {star.ticker}
                        </span>
                    </div>
                ))}
            </div>

            <div className="absolute bottom-4 left-1/2 -translate-x-1/2 text-slate-600 text-[10px] animate-bounce">
                Drag to Rotate (Simulated)
            </div>
        </div>
    );
};

export default GalaxyView;
