import React from 'react';

const VolatilitySurface = () => {
    // Mock Vol Surface Data (Strikes x Expiries)
    const expiries = ['7 DTE', '30 DTE', '60 DTE', '90 DTE', '180 DTE'];
    const strikes = [380, 390, 400, 410, 420, 430, 440, 450];

    // Generate IV mock data (Smile shape)
    const getIV = (expiryIdx, strikeIdx) => {
        const center = 3; // 410 is roughly center
        const dist = Math.abs(strikeIdx - center);
        const timePremium = (5 - expiryIdx) * 2;
        return (15 + (dist * 1.5) + timePremium + Math.random()).toFixed(1);
    };

    const getColor = (iv) => {
        const val = parseFloat(iv);
        if (val > 25) return 'bg-red-500/80 text-white';
        if (val > 20) return 'bg-orange-500/80 text-white';
        if (val > 18) return 'bg-amber-500/60 text-white';
        return 'bg-blue-500/40 text-blue-100';
    };

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-500 uppercase px-2 mb-2">Volatility Surface (IV%)</h3>
            <div className="flex-1 grid grid-cols-6 gap-1 overflow-auto p-2">

                {/* Header Row (Strikes) */}
                <div className="col-span-1"></div>
                {expiries.map((exp, i) => (
                    <div key={i} className="text-center text-[10px] font-mono text-slate-500">{exp}</div>
                ))}

                {/* Grid Rows */}
                {strikes.map((strike, sIdx) => (
                    <React.Fragment key={sIdx}>
                        {/* Row Label (Strike) */}
                        <div className="flex items-center justify-end pr-2 font-mono text-xs text-slate-400 font-bold border-r border-slate-700">
                            ${strike}
                        </div>

                        {/* Cells */}
                        {expiries.map((_, eIdx) => {
                            const iv = getIV(eIdx, sIdx);
                            return (
                                <div
                                    key={`${sIdx}-${eIdx}`}
                                    className={`rounded-sm flex items-center justify-center text-[10px] font-mono cursor-crosshair transition-all duration-300 hover:scale-125 hover:z-20 hover:shadow-2xl border border-transparent hover:border-white/60 ${getColor(iv)}`}
                                    title={`Strike: ${strike}, Expiry: ${expiries[eIdx]}, IV: ${iv}%`}
                                >
                                    {iv}
                                </div>
                            );
                        })}
                    </React.Fragment>
                ))}
            </div>
        </div>
    );
};

export default VolatilitySurface;
