import React, { useState, useEffect } from 'react';
import { Activity, Shield, Terminal, AlertOctagon, Heart, Zap, ShieldAlert, Cpu } from 'lucide-react';
import NetworkMap from '../components/MissionControl/NetworkMap';
import ResourceTimeline from '../components/MissionControl/ResourceTimeline';

const MissionControl = () => {
    const [systemPulse, setSystemPulse] = useState(true);
    const [logs, setLogs] = useState([
        { time: '12:00:01', source: 'DATA', message: 'Ingesting AlphaVantage feed...' },
        { time: '12:00:05', source: 'RISK', message: 'Margin check: OK' },
        { time: '12:00:10', source: 'AGENT', message: 'Alpha_Zero signal: BUY TSLA' }
    ]);
    const [defconLevel, setDefconLevel] = useState(4);
    const [defconColor, setDefconColor] = useState('bg-green-500');

    // Mock States - In real app, fetch from backend
    const allocation = { buckets: { SHIELD: 0.4, ALPHA: 0.5, CASH: 0.1 } };
    const execution = { balance: 24500000 };
    const risk = { var_95_daily: 124500, freeze_reason: "Nominal Operations" };

    useEffect(() => {
        const interval = setInterval(() => setSystemPulse(p => !p), 1000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="mission-control-container bg-slate-950 min-h-screen text-slate-300 p-6 flex flex-col gap-4 font-sans">
            {/* TOP BAR: System Status */}
            <div className="grid grid-cols-12 gap-4 mb-2">
                <div className="col-span-8 glass-panel p-4 flex items-center justify-between relative overflow-hidden bg-slate-900/40 border-slate-800 rounded-xl glass-premium shadow-cyan-900/20 shadow-2xl">
                    <div className="flex items-center gap-4 z-10 transition-transform duration-300 hover:scale-[1.01]">
                        <Activity className={`text-cyan-400 ${systemPulse ? 'opacity-100' : 'opacity-50'} transition-opacity animate-neon-pulse`} size={24} />
                        <div>
                            <h1 className="text-2xl font-bold text-white tracking-widest uppercase text-glow-cyan">Mission Control</h1>
                            <span className="text-cyan-500 text-xs font-mono">SYSTEM ONLINE /// UPTIME: 99.98%</span>
                        </div>
                    </div>

                    {/* Resource Timeline Widget */}
                    <div className="w-64 h-16 z-10 opacity-80 hover:opacity-100 transition-opacity">
                        <ResourceTimeline />
                    </div>

                    <div className="flex gap-8 z-10">
                        <div className="text-center">
                            <span className="block text-slate-500 uppercase text-[10px]">Active Agents</span>
                            <span className="text-xl font-bold text-white">12</span>
                        </div>
                        <div className="text-center">
                            <span className="block text-slate-500 uppercase text-[10px]">Latency</span>
                            <span className="text-xl font-bold text-green-400">42ms</span>
                        </div>
                    </div>

                    <div className="absolute -right-10 -bottom-10 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
                </div>

                <div className={`col-span-4 glass-panel p-4 flex flex-col justify-center items-center rounded-xl border-2 ${defconLevel < 2 ? 'bg-red-950/20 border-red-500' : 'bg-slate-900/40 border-slate-800'}`}>
                    <h2 className="text-lg font-bold uppercase tracking-widest text-white mb-1">Global Threat Level</h2>
                    <div className="text-5xl font-black text-white drop-shadow-lg">DEFCON {defconLevel}</div>
                    <span className="text-slate-400 bg-black/20 px-2 rounded mt-2 uppercase text-[10px]">
                        {risk?.freeze_reason || "Nominal Operations"}
                    </span>
                </div>
            </div>

            {/* MAIN DASHBOARD GRID */}
            <div className="grid grid-cols-12 gap-4 flex-1 h-[calc(100vh-180px)]">
                {/* LEFT COLUMN: Capital Allocation */}
                <div className="col-span-12 lg:col-span-3 glass-panel p-6 flex flex-col h-full bg-slate-900/40 border border-slate-800 rounded-xl">
                    <h3 className="flex items-center gap-2 text-sm font-bold text-white mb-6 uppercase border-b border-slate-800 pb-3">
                        <ShieldAlert size={16} className="text-blue-400" /> Capital Allocation
                    </h3>

                    <div className="flex-1 flex flex-col gap-6">
                        <div className="relative h-48 w-48 mx-auto">
                            <svg viewBox="0 0 36 36" className="w-full h-full rotate-[-90deg]">
                                <circle cx="18" cy="18" r="15.915" fill="none" stroke="#1e293b" strokeWidth="4" />
                                <circle cx="18" cy="18" r="15.915" fill="none" stroke="#22c55e" strokeWidth="4"
                                    strokeDasharray={`${allocation.buckets.CASH * 100}, 100`} />
                                <circle cx="18" cy="18" r="15.915" fill="none" stroke="#ef4444" strokeWidth="4"
                                    strokeDasharray={`${allocation.buckets.ALPHA * 100}, 100`} strokeDashoffset={`-${allocation.buckets.CASH * 100}`} />
                                <circle cx="18" cy="18" r="15.915" fill="none" stroke="#3b82f6" strokeWidth="4"
                                    strokeDasharray={`${allocation.buckets.SHIELD * 100}, 100`} strokeDashoffset={`-${(allocation.buckets.CASH + allocation.buckets.ALPHA) * 100}`} />
                            </svg>
                            <div className="absolute inset-0 flex items-center justify-center flex-col">
                                <span className="text-2xl font-bold text-white font-mono">${(execution?.balance / 1000000).toFixed(1)}M</span>
                                <span className="text-[10px] text-slate-500 font-bold">NAV</span>
                            </div>
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between items-center p-3 bg-blue-900/20 rounded border border-blue-500/20">
                                <span className="text-xs text-blue-300 font-bold">SHIELD</span>
                                <span className="font-mono text-white">{(allocation.buckets.SHIELD * 100).toFixed(1)}%</span>
                            </div>
                            <div className="flex justify-between items-center p-3 bg-red-900/20 rounded border border-red-500/20">
                                <span className="text-xs text-red-300 font-bold">ALPHA</span>
                                <span className="font-mono text-white">{(allocation.buckets.ALPHA * 100).toFixed(1)}%</span>
                            </div>
                            <div className="flex justify-between items-center p-3 bg-green-900/20 rounded border border-green-500/20">
                                <span className="text-xs text-green-300 font-bold">CASH</span>
                                <span className="font-mono text-white">{(allocation.buckets.CASH * 100).toFixed(1)}%</span>
                            </div>
                        </div>
                    </div>
                </div>

                {/* CENTER COLUMN: Live Feed & Map */}
                <div className="col-span-12 lg:col-span-6 flex flex-col gap-4 h-full">
                    <div className="glass-panel p-0 flex-1 relative overflow-hidden bg-slate-900/10 border border-slate-800 rounded-xl">
                        <NetworkMap />
                    </div>

                    <div className="glass-panel p-4 h-64 bg-slate-900/40 border border-slate-800 rounded-xl flex flex-col">
                        <h3 className="flex items-center gap-2 text-sm font-bold text-white mb-2 uppercase font-mono">
                            <Terminal size={16} className="text-green-400" /> Live System Logs
                        </h3>
                        <div className="flex-1 overflow-y-auto font-mono text-[10px] space-y-1 pr-2 scrollbar-thin">
                            {logs.map((log, i) => (
                                <div key={i} className="flex gap-4 p-2 border-b border-white/5 hover:bg-white/5">
                                    <span className="text-slate-500">{log.time}</span>
                                    <span className={`font-bold ${log.source === 'RISK' ? 'text-red-400' : 'text-blue-400'}`}>[{log.source}]</span>
                                    <span className="text-slate-300">{log.message}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* RIGHT COLUMN: Risk Governor */}
                <div className="col-span-12 lg:col-span-3 glass-panel p-6 flex flex-col h-full bg-slate-900/40 border border-slate-800 rounded-xl">
                    <h3 className="flex items-center gap-2 text-sm font-bold text-white mb-6 uppercase border-b border-slate-800 pb-3">
                        <AlertOctagon size={16} className="text-orange-400" /> Risk Governor
                    </h3>

                    <div className="space-y-8">
                        <div>
                            <span className="block text-[10px] uppercase text-slate-500 mb-2 font-bold tracking-widest">Value at Risk (Daily)</span>
                            <div className="text-4xl font-black text-white font-mono border-l-4 border-orange-500 pl-4">
                                ${risk.var_95_daily.toLocaleString()}
                            </div>
                        </div>

                        <div>
                            <span className="block text-[10px] uppercase text-slate-500 mb-2 font-bold tracking-widest">Portfolio Beta</span>
                            <div className="text-4xl font-black text-white font-mono border-l-4 border-yellow-500 pl-4">
                                0.85
                            </div>
                        </div>

                        <div className="space-y-3">
                            <div className="flex justify-between items-center text-xs font-bold">
                                <span className="text-slate-400">Leverage (Max 4x)</span>
                                <span className="text-white">1.2x</span>
                            </div>
                            <div className="w-full bg-slate-800 rounded-full h-1.5">
                                <div className="bg-orange-500 h-1.5 rounded-full" style={{ width: '30%' }}></div>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-2 mt-auto">
                            {['DRAWDOWN', 'VOLATILITY', 'LIQUIDITY', 'EXPOSURE'].map(type => (
                                <div key={type} className="bg-green-900/20 text-green-400 border border-green-500/30 p-2 rounded text-center text-[9px] font-black tracking-tighter">
                                    {type} NOMINAL
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MissionControl;
