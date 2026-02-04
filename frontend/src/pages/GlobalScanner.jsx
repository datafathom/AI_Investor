import React, { useState } from 'react';
import { StorageService } from '../utils/storageService';
import { Microscope, Globe2, Scan, Filter, Activity, Eye, TrendingUp, TrendingDown, ExternalLink, Zap } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import GalaxyView from '../components/Scanner/GalaxyView';
import FilterBuilder from '../components/Scanner/FilterBuilder';
import SectorCarousel from '../components/Scanner/SectorCarousel';
import DataTable from '../components/DataViz/DataTable';
import { scannerService } from '../services/scannerService';

import './GlobalScanner.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

// Standardized Widget Header (Atomic Design Pattern)
const WidgetHeader = ({ icon: Icon, title, subtitle, colorClass = "text-blue-400" }) => (
    <div className="flex items-center justify-between mb-4 pb-3 border-b border-white/5">
        <div className="flex flex-col">
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-2">
                <Icon size={16} className={colorClass} /> {title}
            </h3>
            {subtitle && <span className="text-[9px] font-mono text-slate-500 mt-0.5 tracking-wider uppercase pl-6">{subtitle}</span>}
        </div>
    </div>
);

const GlobalScanner = () => {
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'galaxy', x: 0, y: 0, w: 9, h: 10 },
            { i: 'pulse', x: 9, y: 0, w: 3, h: 4 },
            { i: 'filters', x: 9, y: 4, w: 3, h: 6 },
            { i: 'matches', x: 0, y: 10, w: 12, h: 10 }
        ]
    };
    const STORAGE_KEY = 'layout_global_scanner_v2';

    const [layouts, setLayouts] = useState(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
        } catch (e) {
            return DEFAULT_LAYOUT;
        }
    });

    const onLayoutChange = (currentLayout, allLayouts) => {
        setLayouts(allLayouts);
        StorageService.set(STORAGE_KEY, allLayouts);
    };

    const columns = [
        { 
            key: 'asset', 
            label: 'Asset', 
            sortable: true,
            render: (val) => (
                <div className="flex flex-col">
                    <span className="font-bold text-slate-100 text-sm">{val}</span>
                    <span className="text-[10px] text-slate-500 font-mono">EQUITY</span>
                </div>
            )
        },
        { 
            key: 'change', 
            label: 'Change %', 
            sortable: true,
            render: (val) => (
                <span className={`font-mono font-bold ${val >= 0 ? 'text-bullish' : 'text-bearish'}`}>
                    {val >= 0 ? '+' : ''}{val}%
                </span>
            )
        },
        { 
            key: 'sector', 
            label: 'Sector', 
            sortable: true,
            render: (val) => (
                <span className="text-[10px] uppercase font-bold tracking-widest bg-slate-800/50 px-2 py-0.5 rounded border border-slate-700 text-slate-400">
                    {val}
                </span>
            )
        },
        { 
            key: 'signal', 
            label: 'AI Signal', 
            sortable: true,
            render: (val) => (
                <div className="flex items-center gap-1.5">
                    <div className={`w-1.5 h-1.5 rounded-full ${val === 'BULLISH' ? 'bg-bullish shadow-[0_0_8px_#10b981]' : 'bg-bearish shadow-[0_0_8px_#f43f5e]'}`} />
                    <span className={`text-[10px] font-black ${val === 'BULLISH' ? 'text-bullish' : 'text-bearish'}`}>{val}</span>
                </div>
            )
        },
        {
            key: 'action',
            label: 'Action',
            align: 'center',
            render: (_, row) => (
                <div className="flex justify-center gap-2">
                    <button className="p-1.5 hover:bg-blue-500/20 rounded transition-colors text-blue-400 group" title="View Detail">
                        <Eye size={14} className="group-hover:scale-110 transition-transform" />
                    </button>
                    <button className="p-1.5 hover:bg-emerald-500/20 rounded transition-colors text-emerald-400 group" title="Quick Trade">
                        <Zap size={14} className="group-hover:scale-110 transition-transform" />
                    </button>
                </div>
            )
        }
    ];

    const [matchData, setMatchData] = useState([]);
    const [pulseData, setPulseData] = useState([]);
    const [loading, setLoading] = useState(true);

    React.useEffect(() => {
        const loadScannerData = async () => {
            setLoading(true);
            try {
                const [matches, pulse] = await Promise.all([
                    scannerService.getLatestMatches(),
                    scannerService.getMarketPulse()
                ]);
                setMatchData(matches);
                setPulseData(pulse);
            } catch (err) {
                console.error("Failed to load scanner data", err);
            } finally {
                setLoading(false);
            }
        };
        loadScannerData();

        const interval = setInterval(loadScannerData, 30000); // 30s refresh
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="full-bleed-page global-scanner-page text-white font-sans">
            <header className="flex justify-between items-center h-16 mb-6">
                <div className="flex items-center gap-4">
                    <div className="p-3 bg-blue-900/30 rounded-xl border border-blue-500/30 shadow-[0_0_20px_rgba(59,130,246,0.15)]">
                        <Globe2 size={32} className="text-blue-400" />
                    </div>
                    <div>
                        <h1 className="text-3xl font-black bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-cyan-300 italic tracking-tight">
                            GLOBAL SCANNER
                        </h1>
                        <p className="text-slate-500 text-[10px] font-mono tracking-widest uppercase mt-0.5">Real-time Asset Discovery Engine</p>
                    </div>
                </div>

                <div className="flex-1 max-w-2xl h-14 mx-8">
                    <SectorCarousel />
                </div>

                <div className="bg-slate-900 text-slate-500 text-[9px] font-bold font-mono px-3 py-1.5 rounded-full border border-slate-800 shadow-inner flex items-center gap-2">
                    <Activity size={10} className="text-green-500" />
                    STATUS: <span className="text-green-400 animate-pulse uppercase">LIVE FEED ACTIVE</span>
                </div>
            </header>

            <div className="scrollable-content-wrapper">
                <ResponsiveGridLayout
                    className="layout h-full"
                    layouts={layouts}
                    onLayoutChange={onLayoutChange}
                    breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                    cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                    rowHeight={40}
                    isDraggable={true}
                    isResizable={true}
                    draggableHandle=".widget-header-drag"
                    margin={[16, 16]}
                >
                    {/* ... (keep widgets as they are but within the grid) ... */}
                    {/* 1. Market Galaxy 3D View */}
                    <div key="galaxy" className="widget-container glass-panel border-slate-800/50">
                        <div className="widget-header-drag p-4 cursor-move">
                            <WidgetHeader icon={Globe2} title="Market Galaxy 3D" subtitle="Visual Correlation Map" />
                        </div>
                        <div className="flex-1 relative bg-black overflow-hidden m-4 mt-0 rounded-lg border border-white/5">
                            <GalaxyView />
                            <div className="absolute top-4 right-4 pointer-events-none text-right">
                                <div className="text-[9px] text-slate-500 uppercase font-black tracking-widest">Active Assets</div>
                                <div className="text-xl font-mono text-white text-glow-cyan">8,492</div>
                            </div>
                        </div>
                    </div>

                    {/* 2. New Market Pulse Widget */}
                    <div key="pulse" className="widget-container glass-panel border-slate-800/50">
                        <div className="widget-header-drag p-4 cursor-move">
                            <WidgetHeader icon={Activity} title="Market Pulse" subtitle="Sector Momentum" colorClass="text-emerald-400" />
                        </div>
                        <div className="px-4 pb-4 flex flex-col gap-3">
                            {pulseData.length > 0 ? pulseData.map(sector => (
                                <div key={sector.name} className="flex items-center justify-between p-2.5 bg-white/5 rounded border border-white/5 hover:bg-white/10 transition-colors">
                                    <span className="text-xs font-bold text-slate-300">{sector.name}</span>
                                    <span className={`text-xs font-mono font-black ${sector.change >= 0 ? 'text-bullish' : 'text-bearish'}`}>
                                        {sector.change >= 0 ? '+' : ''}{sector.change}%
                                    </span>
                                </div>
                            )) : (
                                <div className="text-center text-slate-500 py-8 text-[10px] uppercase font-mono">Initializing Neural Feed...</div>
                            )}
                            <div className="mt-auto pt-4 border-t border-white/5 flex justify-center">
                                <span className="text-[8px] font-black text-slate-500 font-mono tracking-[0.2em] uppercase">
                                    SCAN INTERVAL: <span className="text-blue-400">LIVE</span>
                                </span>
                            </div>
                        </div>
                    </div>

                    {/* 3. Filter Controls */}
                    <div key="filters" className="widget-container glass-panel border-slate-800/50">
                        <div className="widget-header-drag p-4 cursor-move">
                            <WidgetHeader icon={Filter} title="Scanning Parameters" subtitle="Advanced Signal Logic" colorClass="text-amber-400" />
                        </div>
                        <div className="px-4 pb-4 overflow-y-auto scrollbar-hide">
                            <FilterBuilder />
                        </div>
                    </div>

                    {/* 4. Recent Matches (Full Table) */}
                    <div key="matches" className="widget-container glass-panel border-slate-800/50">
                        <div className="widget-header-drag p-4 cursor-move flex justify-between items-center">
                            <WidgetHeader icon={Scan} title="Recent Scanner Matches" subtitle="Institutional Signal Feed" colorClass="text-cyan-400" />
                            <div className="flex gap-2">
                                <button className="text-[9px] bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 px-3 py-1 rounded transition-colors border border-blue-500/30 font-bold uppercase tracking-widest">
                                    Export .CSV
                                </button>
                            </div>
                        </div>
                        <div className="flex-1 px-4 pb-4 overflow-hidden flex flex-col">
                            <div className="flex-1 overflow-auto rounded border border-slate-700/50 bg-black/20 shadow-inner">
                                <DataTable 
                                    columns={columns} 
                                    data={matchData} 
                                    className="border-none"
                                />
                            </div>
                        </div>
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>
        </div>
    );
};

export default GlobalScanner;
