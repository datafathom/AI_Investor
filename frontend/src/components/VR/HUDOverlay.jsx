import React from 'react';
import { Crosshair, Shield, Activity, Wifi } from 'lucide-react';

const HUDOverlay = () => {
    return (
        <div className="absolute inset-0 pointer-events-none p-8 flex flex-col justify-between z-20">
            {/* Top Bar */}
            <div className="flex justify-between items-start">
                <div className="flex gap-4">
                    <div className="glass-panel p-4 flex flex-col items-center justify-center">
                        <div className="text-[10px] text-cyan-400 uppercase font-mono mb-1">Shield Integrity</div>
                        <div className="text-xl font-bold text-white flex items-center gap-2">
                            <Shield size={16} className="text-cyan-400" /> 100%
                        </div>
                    </div>
                    <div className="glass-panel p-4 flex flex-col items-center justify-center">
                        <div className="text-[10px] text-red-400 uppercase font-mono mb-1">Market Volatility</div>
                        <div className="text-xl font-bold text-white flex items-center gap-2">
                            <Activity size={16} className="text-red-400" /> HIGH
                        </div>
                    </div>
                </div>

                <div className="flex flex-col items-end gap-1">
                    <div className="flex gap-1 text-cyan-400">
                        <span className="w-8 h-1 bg-cyan-500 shadow-[0_0_10px_#22d3ee]"></span>
                        <span className="w-1 h-1 bg-cyan-500 shadow-[0_0_10px_#22d3ee]"></span>
                        <span className="w-1 h-1 bg-cyan-500 shadow-[0_0_10px_#22d3ee]"></span>
                    </div>
                    <div className="text-xs font-mono text-cyan-300 flex items-center gap-2">
                        SYSTEM ONLINE <Wifi size={12} className="animate-pulse" />
                    </div>
                </div>
            </div>

            {/* Center Reticle */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-50">
                <Crosshair size={64} className="text-cyan-400 animate-pulse" />
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[200px] h-[200px] border border-cyan-500/20 rounded-full"></div>
            </div>

            {/* Bottom Bar */}
            <div className="flex justify-between items-end">
                <div className="text-xs font-mono text-cyan-500/80 max-w-[200px] glass-panel-header px-4 py-2 border-l-2 border-cyan-500">
                    <p>{'>'} INITIALIZING NEURAL LINK...</p>
                    <p>{'>'} CONNECTED TO ALPHA_ZERO</p>
                    <p>{'>'} READY FOR INPUT</p>
                </div>
                <div className="glass-panel h-20 w-72 flex flex-col justify-center px-6 items-end border-r-4 border-cyan-500">
                    <span className="text-5xl font-black text-white italic tracking-tighter">VR-OS</span>
                    <span className="text-[10px] text-cyan-500 font-mono tracking-[0.3em] mt-1">IMMERSIVE INTERFACE</span>
                </div>
            </div>
        </div>
    );
};

export default HUDOverlay;
