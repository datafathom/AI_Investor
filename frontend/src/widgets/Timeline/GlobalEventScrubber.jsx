/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Timeline/GlobalEventScrubber.jsx
 * ROLE: Historical "Chaos Event" Backtest Scrubber
 * PURPOSE: Allows users to drag through major historical market events and
 *          run instantaneous Monte Carlo backtests of their current strategy.
 * ==============================================================================
 */

import React, { useState, useMemo } from 'react';
import { History, AlertTriangle, Play, ChevronLeft, ChevronRight } from 'lucide-react';
import useBacktestStore from '../../stores/backtestStore';
import './GlobalEventScrubber.css';

const CHAOS_EVENTS = [
    { 
        id: 'black-monday-87', 
        name: '1987 Black Monday', 
        year: 1987, 
        desc: 'Sudden 22% crash in a single day.',
        params: { mu: -0.20, sigma: 0.85, days: 10 }
    },
    { 
        id: 'dot-com-00', 
        name: 'Dot-Com Bubble Burst', 
        year: 2000, 
        desc: 'Prolonged tech sector liquidation.',
        params: { mu: -0.15, sigma: 0.30, days: 180 }
    },
    { 
        id: 'gfc-08', 
        name: '2008 Financial Crisis', 
        year: 2008, 
        desc: 'Systemic banking collapse & recession.',
        params: { mu: -0.40, sigma: 0.45, days: 252 }
    },
    { 
        id: 'covid-20', 
        name: '2020 COVID Crash', 
        year: 2020, 
        desc: 'Unprecedented volatility and V-shaped recovery.',
        params: { mu: -0.30, sigma: 0.65, days: 60 }
    },
    { 
        id: 'inflation-22', 
        name: '2022 Inflation Pivot', 
        year: 2022, 
        desc: 'Rapid rate hikes and bond market routing.',
        params: { mu: -0.12, sigma: 0.22, days: 252 }
    }
];

const GlobalEventScrubber = () => {
    const { runSimulation, setParams, isSimulating, ruinProbability } = useBacktestStore();
    const [activeIndex, setActiveIndex] = useState(CHAOS_EVENTS.length - 1);
    const activeEvent = CHAOS_EVENTS[activeIndex];

    const runEventSim = async () => {
        setParams(activeEvent.params);
        await runSimulation();
    };

    return (
        <div className="event-scrubber">
            <div className="event-scrubber__header">
                <div className="flex items-center gap-2">
                    <History size={16} className="text-amber-400" />
                    <h3 className="text-sm font-bold text-white uppercase tracking-wider">Chaos Scrubber</h3>
                </div>
                <div className="text-[10px] font-mono text-amber-500/80 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                    HISTORICAL REPLAY
                </div>
            </div>

            {/* Timeline Slider */}
            <div className="event-scrubber__timeline-container">
                <div className="event-scrubber__timeline">
                    {CHAOS_EVENTS.map((event, idx) => (
                        <div 
                            key={event.id}
                            className={`event-scrubber__node ${idx === activeIndex ? 'active' : ''}`}
                            onClick={() => setActiveIndex(idx)}
                        >
                            <div className="event-scrubber__node-dot" />
                            <span className="event-scrubber__node-year">{event.year}</span>
                        </div>
                    ))}
                    <div className="event-scrubber__track" />
                </div>
            </div>

            {/* Event Details Card */}
            <div className="event-scrubber__event-card">
                <div className="flex justify-between items-start mb-2">
                    <h4 className="text-white text-base font-black">{activeEvent.name}</h4>
                    <button 
                        onClick={runEventSim}
                        disabled={isSimulating}
                        className="p-2 bg-amber-500 rounded-full text-black hover:bg-amber-400 transition-colors disabled:opacity-50"
                    >
                        <Play size={16} fill="black" />
                    </button>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed mb-4">
                    {activeEvent.desc}
                </p>

                <div className="grid grid-cols-3 gap-2">
                    <div className="bg-white/5 p-2 rounded border border-white/5">
                        <span className="block text-[8px] uppercase text-slate-500">Exp. Return</span>
                        <span className="text-white text-xs font-bold">{(activeEvent.params.mu * 100).toFixed(0)}%</span>
                    </div>
                    <div className="bg-white/5 p-2 rounded border border-white/5">
                        <span className="block text-[8px] uppercase text-slate-500">Volatility</span>
                        <span className="text-white text-xs font-bold">{(activeEvent.params.sigma * 100).toFixed(0)}%</span>
                    </div>
                    <div className="bg-white/5 p-2 rounded border border-white/5">
                        <span className="block text-[8px] uppercase text-slate-500">Duration</span>
                        <span className="text-white text-xs font-bold">{activeEvent.params.days}d</span>
                    </div>
                </div>
            </div>

            {/* Result Toast Integration (Mini) */}
            {ruinProbability > 0 && (
                <div className="mt-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-3 animate-in fade-in slide-in-from-bottom-2">
                    <AlertTriangle size={20} className="text-red-400" />
                    <div>
                        <p className="text-[10px] uppercase text-red-400 font-bold">Survivability Warning</p>
                        <p className="text-white text-xs">Strategy {ruinProbability > 0.3 ? 'FAILED' : 'VULNERABLE'} under this regime.</p>
                    </div>
                </div>
            )}
        </div>
    );
};

export default GlobalEventScrubber;
