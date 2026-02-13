import React from 'react';

const FactorHeatmap = ({ exposures }) => {
    if (!exposures) return null;

    const factors = Object.keys(exposures);
    const maxVal = Math.max(...Object.values(exposures).map(Math.abs));

    const getColor = (val) => {
        // -1 (Red) to 0 (Gray) to 1 (Green)
        // Normalized against maxVal approx 1.5 usually
        const intensity = Math.min(Math.abs(val) / 1.5, 1);
        if (val > 0) return `rgba(16, 185, 129, ${intensity})`; // emerald
        return `rgba(239, 68, 68, ${intensity})`; // red
    };

    return (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {factors.map(f => (
                <div key={f} className="bg-slate-900 border border-slate-800 p-4 rounded-lg flex flex-col items-center">
                    <span className="text-slate-500 font-bold text-xs uppercase mb-2">{f}</span>
                    <div 
                        className="w-16 h-16 rounded-full flex items-center justify-center font-mono font-bold text-white transition-all border-2 border-slate-800"
                        style={{ backgroundColor: getColor(exposures[f]) }}
                    >
                        {exposures[f] > 0 ? '+' : ''}{exposures[f]}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default FactorHeatmap;
