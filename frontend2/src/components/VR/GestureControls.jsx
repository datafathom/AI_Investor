import React from 'react';
import { Hand, ArrowUp, ArrowDown, ArrowLeft, ArrowRight, MousePointer2 } from 'lucide-react';

const GestureControls = () => {
    return (
        <div className="absolute bottom-20 left-1/2 -translate-x-1/2 flex items-center gap-8 z-30">
            {/* Left Hand */}
            <div className="flex flex-col items-center gap-2 group cursor-pointer opacity-50 hover:opacity-100 transition-opacity">
                <div className="w-16 h-16 rounded-full border-2 border-dashed border-cyan-500 flex items-center justify-center bg-cyan-900/20 backdrop-blur">
                    <Hand size={24} className="text-cyan-400 rotate-[-15deg]" />
                </div>
                <span className="text-[10px] text-cyan-400 uppercase tracking-widest bg-black/50 px-2 rounded">Select</span>
            </div>

            {/* D-Pad Simulation */}
            <div className="grid grid-cols-3 gap-2 transformer hover:scale-110 transition-transform">
                <div></div>
                <button className="w-12 h-12 rounded bg-slate-800/80 border border-slate-600 hover:bg-cyan-600 hover:border-cyan-400 text-white flex items-center justify-center shadow-lg active:scale-95 transition-all">
                    <ArrowUp size={20} />
                </button>
                <div></div>

                <button className="w-12 h-12 rounded bg-slate-800/80 border border-slate-600 hover:bg-cyan-600 hover:border-cyan-400 text-white flex items-center justify-center shadow-lg active:scale-95 transition-all">
                    <ArrowLeft size={20} />
                </button>
                <div className="w-12 h-12 rounded-full border border-cyan-500/50 flex items-center justify-center animate-pulse">
                    <MousePointer2 size={16} className="text-cyan-400" />
                </div>
                <button className="w-12 h-12 rounded bg-slate-800/80 border border-slate-600 hover:bg-cyan-600 hover:border-cyan-400 text-white flex items-center justify-center shadow-lg active:scale-95 transition-all">
                    <ArrowRight size={20} />
                </button>

                <div></div>
                <button className="w-12 h-12 rounded bg-slate-800/80 border border-slate-600 hover:bg-cyan-600 hover:border-cyan-400 text-white flex items-center justify-center shadow-lg active:scale-95 transition-all">
                    <ArrowDown size={20} />
                </button>
                <div></div>
            </div>

            {/* Right Hand */}
            <div className="flex flex-col items-center gap-2 group cursor-pointer opacity-50 hover:opacity-100 transition-opacity">
                <div className="w-16 h-16 rounded-full border-2 border-dashed border-cyan-500 flex items-center justify-center bg-cyan-900/20 backdrop-blur">
                    <Hand size={24} className="text-cyan-400 rotate-[15deg]" />
                </div>
                <span className="text-[10px] text-cyan-400 uppercase tracking-widest bg-black/50 px-2 rounded">Grab</span>
            </div>
        </div>
    );
};

export default GestureControls;
