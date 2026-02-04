import React from 'react';

const CalendarHeatmap = () => {
    // Generate 365 days of Mock Data
    const days = Array.from({ length: 365 }, (_, i) => {
        const val = Math.random() > 0.3 ? (Math.random() - 0.45) * 5 : 0; // Skewed slightly positive
        return { val };
    });

    const getColor = (val) => {
        if (val === 0) return 'bg-slate-800';
        if (val > 2) return 'bg-green-500';
        if (val > 1) return 'bg-green-600/80';
        if (val > 0) return 'bg-green-900/50';
        if (val < -2) return 'bg-red-500';
        if (val < -1) return 'bg-red-600/80';
        return 'bg-red-900/50';
    };

    return (
        <div className="h-full flex flex-col">
            <h3 className="text-xs font-bold text-slate-500 uppercase mb-2">Daily P&L Heatmap (YTD)</h3>
            <div className="flex-1 flex flex-wrap gap-1 content-start overflow-hidden">
                {days.map((d, i) => (
                    <div
                        key={i}
                        className={`w-3 h-3 rounded-[1px] ${getColor(d.val)} hover:ring-2 ring-white transition-all cursor-crosshair hover:scale-150 hover:z-10 shadow-lg`}
                        title={`Day ${i + 1}: ${d.val > 0 ? '+' : ''}${d.val.toFixed(2)}%`}
                    ></div>
                ))}
            </div>
            <div className="flex gap-4 mt-2 text-[10px] text-slate-500 items-center justify-end">
                <span>More Loss</span>
                <div className="flex gap-1">
                    <div className="w-3 h-3 bg-red-500 rounded-[1px]"></div>
                    <div className="w-3 h-3 bg-slate-800 rounded-[1px]"></div>
                    <div className="w-3 h-3 bg-green-500 rounded-[1px]"></div>
                </div>
                <span>More Profit</span>
            </div>
        </div>
    );
};

export default CalendarHeatmap;
