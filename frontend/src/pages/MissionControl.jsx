import React, { useState, useEffect } from 'react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import { Activity, Shield, ShieldAlert, Zap, Terminal, AlertOctagon } from 'lucide-react';
import { StorageService } from '../utils/storageService';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import './MissionControl.css'; // Import custom styles
import NetworkMap from '../components/MissionControl/NetworkMap';
import ResourceTimeline from '../components/MissionControl/ResourceTimeline';
import WidgetWindow from '../components/MissionControl/WidgetWindow';

const ResponsiveGridLayout = WidthProvider(Responsive);


const MissionControl = () => {
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'header', x: 0, y: 0, w: 8, h: 3 },
            { i: 'threat', x: 8, y: 0, w: 4, h: 3 },
            { i: 'allocation', x: 0, y: 3, w: 3, h: 14 },
            { i: 'map', x: 3, y: 3, w: 6, h: 9 },
            { i: 'logs', x: 3, y: 12, w: 6, h: 5 },
            { i: 'risk', x: 9, y: 3, w: 3, h: 14 }
        ]
    };
    const STORAGE_KEY = 'layout_mission_control_v2'; // Bump version

    const [layouts, setLayouts] = useState(() => {
        try {
            const saved = StorageService.get(STORAGE_KEY);
            return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
        } catch (e) {
            return DEFAULT_LAYOUT;
        }
    });

    const onLayoutChange = (currentLayout, allLayouts) => {
        setLayouts(allLayouts);
        StorageService.set(STORAGE_KEY, allLayouts);
    };
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
        <div className="mission-control-page text-slate-300 font-sans">
            <div className="scrollable-content-wrapper">
                <ResponsiveGridLayout
                    className="layout"
                    layouts={layouts}
                    onLayoutChange={onLayoutChange}
                    breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                    cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                    rowHeight={40}
                    isDraggable={true}
                    isResizable={true}
                    draggableHandle=".glass-panel, h3"
                    margin={[10, 10]}
                >
                {/* WIDGET: Mission Control Header */}
                <div key="header">
                    <div className="glass-panel p-4 flex items-center justify-between relative overflow-hidden bg-slate-900/40 border-slate-800 rounded-xl glass-premium shadow-cyan-900/20 shadow-2xl h-full">
                        <div className="flex items-center gap-4 z-10 transition-transform duration-300 hover:scale-[1.01]">
                            <Activity className={`text-cyan-400 ${systemPulse ? 'opacity-100' : 'opacity-50'} transition-opacity animate-neon-pulse`} size={24} />
                            <div>
                                <h1 className="text-2xl font-bold text-white tracking-widest uppercase text-glow-cyan">Mission Control</h1>
                                <span className="text-cyan-500 text-xs font-mono">SYSTEM ONLINE /// V3.2.0</span>
                            </div>
                        </div>

                        {/* Resource Timeline Widget */}
                        <div className="hidden md:block w-64 h-16 z-10 opacity-80 hover:opacity-100 transition-opacity">
                            <ResourceTimeline />
                        </div>

                        <div className="flex gap-4 md:gap-8 z-10">
                            <div className="text-center">
                                <span className="block text-slate-500 uppercase text-[8px] md:text-[10px]">Active Agents</span>
                                <span className="text-lg md:text-xl font-bold text-white">12</span>
                            </div>
                            <div className="text-center">
                                <span className="block text-slate-500 uppercase text-[8px] md:text-[10px]">Latency</span>
                                <span className="text-lg md:text-xl font-bold text-green-400">42ms</span>
                            </div>
                        </div>

                        <div className="absolute -right-10 -bottom-10 w-64 h-64 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none animate-pulse"></div>
                    </div>
                </div>

                {/* WIDGET: Threat Level */}
                <div key="threat">
                    <WidgetWindow title="Global Threat Level" icon={Shield}>
                        <div className={`flex flex-col justify-center items-center h-full text-center ${defconLevel < 2 ? 'bg-red-950/20' : ''}`}>
                            <div className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-500 mb-1">Defense Condition</div>
                            <div className="text-6xl font-black text-white drop-shadow-[0_0_15px_rgba(255,255,255,0.3)]">
                                {defconLevel}
                            </div>
                            <div className={`mt-3 px-4 py-1 rounded text-[10px] font-black uppercase tracking-widest border ${defconLevel < 2 ? 'border-red-500 text-red-400' : 'border-slate-800 text-slate-400'}`}>
                                {risk?.freeze_reason || "Nominal Operations"}
                            </div>
                        </div>
                    </WidgetWindow>
                </div>

                {/* LEFT COLUMN: Capital Allocation */}
                <div key="allocation">
                    <WidgetWindow title="Capital Allocation" icon={ShieldAlert}>
                        <div className="allocation-layout flex flex-col h-full gap-8">
                            <div className="relative aspect-square w-full max-w-[200px] mx-auto">
                                <svg viewBox="0 0 36 36" className="w-full h-full rotate-[-90deg]">
                                    <circle cx="18" cy="18" r="15.915" fill="none" stroke="#1e293b" strokeWidth="4" className="light:stroke-slate-200" />
                                    <circle cx="18" cy="18" r="15.915" fill="none" stroke="#22c55e" strokeWidth="4"
                                        strokeDasharray={`${allocation.buckets.CASH * 100}, 100`} />
                                    <circle cx="18" cy="18" r="15.915" fill="none" stroke="#ef4444" strokeWidth="4"
                                        strokeDasharray={`${allocation.buckets.ALPHA * 100}, 100`} strokeDashoffset={`-${allocation.buckets.CASH * 100}`} />
                                    <circle cx="18" cy="18" r="15.915" fill="none" stroke="#3b82f6" strokeWidth="4"
                                        strokeDasharray={`${allocation.buckets.SHIELD * 100}, 100`} strokeDashoffset={`-${(allocation.buckets.CASH + allocation.buckets.ALPHA) * 100}`} />
                                </svg>
                                <div className="absolute inset-0 flex items-center justify-center flex-col">
                                    <span className="text-2xl font-bold text-white font-mono light:text-slate-900">${(execution?.balance / 1000000).toFixed(1)}M</span>
                                    <span className="text-[10px] text-slate-500 font-bold tracking-widest uppercase">NAV</span>
                                </div>
                            </div>

                            <div className="allocation-legend space-y-2 mt-auto">
                                <div className="flex justify-between items-center p-3 bg-blue-900/10 rounded border border-blue-500/10 light:bg-blue-50 light:border-blue-100">
                                    <span className="text-[10px] text-blue-400 font-black uppercase">SHIELD</span>
                                    <span className="font-mono text-sm font-bold text-white light:text-blue-900">{(allocation.buckets.SHIELD * 100).toFixed(1)}%</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-red-900/10 rounded border border-red-500/10 light:bg-red-50 light:border-red-100">
                                    <span className="text-[10px] text-red-400 font-black uppercase">ALPHA</span>
                                    <span className="font-mono text-sm font-bold text-white light:text-red-900">{(allocation.buckets.ALPHA * 100).toFixed(1)}%</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-green-900/10 rounded border border-green-500/10 light:bg-green-50 light:border-green-100">
                                    <span className="text-[10px] text-green-400 font-black uppercase">CASH</span>
                                    <span className="font-mono text-sm font-bold text-white light:text-green-900">{(allocation.buckets.CASH * 100).toFixed(1)}%</span>
                                </div>
                            </div>
                        </div>
                    </WidgetWindow>
                </div>

                {/* CENTER COLUMN: Live Feed & Map */}
                <div key="map">
                    <WidgetWindow title="Master Network Mesh" icon={Zap}>
                        <div className="p-0 h-full relative overflow-hidden rounded-lg">
                            <NetworkMap />
                        </div>
                    </WidgetWindow>
                </div>
                
                <div key="logs">
                    <WidgetWindow title="Live System Logs" icon={Terminal}>
                        <div className="terminal-window h-full flex flex-col p-2">
                            <div className="flex-1 overflow-y-auto font-mono text-[10px] space-y-1 terminal-sticky-bottom scrollbar-none">
                                {[...logs].reverse().map((log, i) => (
                                    <div key={i} className="flex gap-4 py-1.5 border-b border-white/5 hover:bg-white/5 terminal-text">
                                        <span className="text-slate-500 opacity-60 font-black">{log.time}</span>
                                        <div className={`px-1.5 py-0.5 rounded text-[8px] font-black tracking-widest ${log.source === 'RISK' ? 'bg-red-500/20 text-red-400' : 'bg-blue-500/20 text-blue-400'}`}>
                                            {log.source}
                                        </div>
                                        <span className="text-slate-300 flex-1 break-words">{log.message}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </WidgetWindow>
                </div>

                {/* RIGHT COLUMN: Risk Governor */}
                <div key="risk">
                    <WidgetWindow title="Risk Governor" icon={AlertOctagon}>
                        <div className="space-y-6 flex flex-col h-full">
                            <div className="border-l-4 border-orange-500 pl-4 py-2 bg-orange-500/5">
                                <span className="block text-[8px] md:text-[10px] uppercase text-slate-500 mb-1 font-bold tracking-widest">Value at Risk (Daily)</span>
                                <div className="metric-heavy font-black text-white font-mono light:text-slate-900">
                                    ${risk.var_95_daily.toLocaleString()}
                                </div>
                            </div>

                            <div className="border-l-4 border-yellow-500 pl-4 py-2 bg-yellow-500/5">
                                <span className="block text-[8px] md:text-[10px] uppercase text-slate-500 mb-1 font-bold tracking-widest">Portfolio Beta</span>
                                <div className="metric-heavy font-black text-white font-mono light:text-slate-900">
                                    0.85
                                </div>
                            </div>

                            <div className="space-y-3">
                                <div className="flex justify-between items-center text-[10px] font-bold tracking-widest uppercase text-slate-400">
                                    <span>Leverage (Max 4x)</span>
                                    <span className="text-white light:text-slate-900">1.2x</span>
                                </div>
                                <div className="w-full bg-slate-800 light:bg-slate-200 rounded-full h-1.5 overflow-hidden">
                                    <div className="bg-orange-500 h-1.5 rounded-full shadow-[0_0_10px_rgba(249,115,22,0.3)]" style={{ width: '30%' }}></div>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-2 mt-auto">
                                {['DRAWDOWN', 'VOLATILITY', 'LIQUIDITY', 'EXPOSURE'].map(type => (
                                    <div key={type} className="bg-green-900/10 text-green-400 border border-green-500/10 p-2.5 rounded text-center text-[9px] font-black tracking-tighter light:bg-green-50 light:border-green-100 dark:text-green-500">
                                        <div className="mb-0.5 opacity-60 text-[7px]">{type}</div>
                                        NOMINAL
                                    </div>
                                ))}
                            </div>
                        </div>
                    </WidgetWindow>
                </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer - Explicit height to force scroll past floating UI */}
                <div style={{ height: '150px', width: '100%', flexShrink: 0 }} />
            </div>
        </div>
    );
};

export default MissionControl;
