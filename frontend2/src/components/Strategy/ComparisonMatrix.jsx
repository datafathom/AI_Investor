import React from 'react';

const ComparisonMatrix = () => {
    // Generate 5x5 Matrix Data
    const matrix = Array.from({ length: 5 }, (_, y) =>
        Array.from({ length: 5 }, (_, x) => {
            const val = 1.5 - (Math.abs(2 - x) * 0.2) - (Math.abs(2 - y) * 0.3) + (Math.random() * 0.2); // Peak in center
            return val.toFixed(2);
        })
    );

    const getColor = (val) => {
        if (val > 1.8) return 'bg-emerald-500 text-black';
        if (val > 1.5) return 'bg-emerald-600/50 text-white';
        if (val > 1.2) return 'bg-slate-700 text-slate-300';
        return 'bg-red-900/50 text-red-300';
    };

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-400 mb-2 uppercase text-center">Optimization Landscape (Sharpe)</h3>
            <div className="flex-1 grid grid-cols-6 gap-1 text-[10px]">
                {/* Y-Axis Label */}
                <div className="row-span-6 flex items-center justify-center -rotate-90 text-slate-500 font-mono uppercase tracking-widest text-[8px] whitespace-nowrap">
                    Stop Loss %
                </div>

                {/* Grid */}
                {matrix.map((row, y) => (
                    <React.Fragment key={y}>
                        {/* Y-Axis Ticks */}
                        <div className="flex items-center justify-end pr-2 text-slate-500 font-mono">
                            {(0.5 * (y + 1)).toFixed(1)}%
                        </div>
                        {row.map((val, x) => (
                            <div
                                key={`${y}-${x}`}
                                className={`rounded flex items-center justify-center font-mono font-bold cursor-help transition-all duration-200 hover:scale-110 hover:z-10 hover:shadow-2xl border border-transparent hover:border-white/40 ${getColor(val)}`}
                                title={`SL: ${(0.5 * (y + 1)).toFixed(1)}%, TP: ${(1 * (x + 1)).toFixed(1)}%`}
                            >
                                {val}
                                {val > 1.8 && <div className="absolute inset-0 bg-white/10 animate-pulse rounded"></div>}
                            </div>
                        ))}
                    </React.Fragment>
                ))}

                {/* X-Axis Labels */}
                <div className="col-start-2 col-span-5 flex justify-between px-2 pt-1 text-slate-500 font-mono">
                    <span>1%</span><span>2%</span><span>3%</span><span>4%</span><span>5%</span>
                </div>
                <div className="col-start-2 col-span-5 text-center text-slate-500 font-mono uppercase tracking-widest text-[8px] mt-1">
                    Take Profit %
                </div>
            </div>
        </div>
    );
};

export default ComparisonMatrix;
