import React from 'react';
import { LayoutGrid } from 'lucide-react';

const WorkspaceMinimap = ({ widgetVisibility, isOpen, toggle }) => {
    if (!isOpen) {
        return (
            <button
                onClick={toggle}
                className="fixed bottom-4 right-4 z-[50] bg-slate-900/80 border border-slate-700 p-2 rounded-lg text-slate-400 hover:text-white hover:border-cyan-500 transition-all shadow-lg interact-hover"
                title="Show Workspace Map"
            >
                <LayoutGrid size={20} />
            </button>
        );
    }

    // Determine grid of active widgets
    // This assumes a known grid or simple listing for now
    const activeWidgets = Object.entries(widgetVisibility || {})
        .filter(([_, visible]) => visible)
        .map(([id]) => id);

    return (
        <div className="fixed bottom-4 right-4 z-[50] w-64 bg-[#0a0a0a]/90 backdrop-blur-md border border-slate-700 rounded-xl shadow-2xl p-4 animate-in slide-in-from-bottom-10 fade-in duration-300">
            <div className="flex justify-between items-center mb-3">
                <span className="text-xs font-bold text-slate-300 uppercase tracking-widest flex items-center gap-2">
                    <LayoutGrid size={14} className="text-cyan-400" /> MiniMap
                </span>
                <button onClick={toggle} className="text-slate-500 hover:text-white text-[10px] uppercase font-bold">
                    Hide
                </button>
            </div>

            <div className="grid grid-cols-2 gap-2 h-32 bg-slate-900/50 rounded border border-slate-800 p-2 relative">
                {/* Visual Representation of Layout */}
                {activeWidgets.map((widgetId, i) => (
                    <div
                        key={widgetId}
                        className="bg-slate-800 border border-slate-600 rounded flex items-center justify-center relative overflow-hidden group hover:border-cyan-500 transition-colors"
                    >
                        <div className="absolute inset-0 bg-slate-700/20 group-hover:bg-cyan-500/10"></div>
                        <span className="text-[8px] text-slate-400 uppercase font-mono truncate px-1">
                            {widgetId.replace('Widget', '')}
                        </span>
                    </div>
                ))}
            </div>

            <div className="mt-2 flex justify-between text-[10px] text-slate-500 font-mono">
                <span>{activeWidgets.length} Active Modules</span>
                <span className="text-green-400">Optimized</span>
            </div>
        </div>
    );
};

export default WorkspaceMinimap;
