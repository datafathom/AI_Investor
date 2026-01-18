import React, { useState } from 'react';
import { Microscope, Globe2, Scan, Filter } from 'lucide-react';
import GalaxyView from '../components/Scanner/GalaxyView';
import FilterBuilder from '../components/Scanner/FilterBuilder';
import SectorCarousel from '../components/Scanner/SectorCarousel';

import './GlobalScanner.css'; // Assuming you might add specific styles here

const GlobalScanner = () => {
    return (
        <div className="global-scanner-page bg-slate-950 min-h-screen text-white font-sans p-6 flex flex-col gap-6">
            <header className="flex justify-between items-center h-16">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-blue-900/30 rounded-xl border border-blue-500/30">
                        <Globe2 size={32} className="text-blue-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-300">
                            Global Scanner
                        </h1>
                        <p className="text-slate-400 text-sm">Real-time Asset Discovery Engine</p>
                    </div>
                </div>

                {/* Sector Carousel in Header Area */}
                <div className="flex-1 max-w-2xl h-14 mx-8">
                    <SectorCarousel />
                </div>

                <div className="bg-slate-900 text-slate-500 text-xs font-mono px-3 py-1 rounded border border-slate-800">
                    SCAN INTERVAL: <span className="text-green-400 animate-pulse">LIVE</span>
                </div>
            </header>

            <div className="flex-1 grid grid-cols-12 gap-6 overflow-hidden min-h-[500px]">
                {/* Main Galaxy View */}
                <div className="col-span-12 lg:col-span-9 glass-panel p-0 rounded-xl overflow-hidden border border-slate-800 relative bg-black">
                    <GalaxyView />

                    {/* Overlay Stats */}
                    <div className="absolute top-4 right-4 pointer-events-none text-right">
                        <div className="text-[10px] text-slate-500 uppercase font-bold tracking-widest">Visible Assets</div>
                        <div className="text-xl font-mono text-white text-glow-cyan">8,492</div>
                    </div>
                </div>

                {/* Right Filter Panel */}
                <div className="col-span-12 lg:col-span-3 flex flex-col gap-6">
                    <div className="glass-panel p-6 bg-slate-900/40 border border-slate-800 rounded-xl flex-1 flex flex-col glass-premium shadow-blue-900/20">
                        <FilterBuilder />
                    </div>

                    <div className="glass-panel p-4 bg-slate-900/40 border border-slate-800 rounded-xl h-1/3 glass-premium shadow-cyan-900/20">
                        <h3 className="text-xs font-bold text-slate-500 uppercase mb-2 flex items-center gap-2">
                            <Scan size={12} /> Recent Matches
                        </h3>
                        <div className="space-y-1 overflow-y-auto h-full pr-1">
                            {['NVDA', 'AMD', 'PLTR', 'TSLA', 'COIN'].map((ticker, i) => (
                                <div key={ticker} className="flex justify-between items-center p-2 bg-slate-800/50 hover:bg-slate-800 rounded border border-transparent hover:border-blue-500/50 cursor-pointer group transition-all hover:scale-[1.02] interact-hover">
                                    <span className="font-bold text-sm text-white group-hover:text-blue-400 transition-colors">{ticker}</span>
                                    <span className="font-mono text-xs text-green-400 text-glow-cyan">+{2.5 + i * 0.4}%</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default GlobalScanner;
