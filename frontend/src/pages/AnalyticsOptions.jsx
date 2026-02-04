/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AnalyticsOptions.jsx
 * ROLE: Options Analytics Page
 * PURPOSE: Displays advanced market analytics widgets (GEX, Fama-French).
 *          Serves as the container for Phase 2 implementation of deep-dive tools.
 *          Enabled with Drag & Resize functionality via react-grid-layout.
 * ==============================================================================
 */
import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Responsive, WidthProvider } from 'react-grid-layout';
import useNavigationStore from '../stores/navigationStore';
import FearGreedWidget from '../widgets/FearGreedWidget';
import KafkaStreamMonitor from '../widgets/KafkaStreamMonitor';
import HypeMeterWidget from '../widgets/HypeMeterWidget';

import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import './AnalyticsOptions.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

// Internal widget components replaced inline to inject drag handles
// const GEXWidget = () => ... 
// const FamaFrenchWidget = () => ...

const AnalyticsOptions = () => {
    const location = useLocation();
    const setCurrentRoute = useNavigationStore((state) => state.setCurrentRoute);

    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'kafka', x: 0, y: 0, w: 12, h: 4 },
            { i: 'feargreed', x: 0, y: 4, w: 6, h: 6 },
            { i: 'hype', x: 6, y: 4, w: 6, h: 6 },
            { i: 'gex', x: 0, y: 10, w: 6, h: 6 },
            { i: 'ff', x: 6, y: 10, w: 6, h: 6 },
            { i: 'iv', x: 0, y: 16, w: 12, h: 6 }
        ]
    };

    const STORAGE_KEY = 'layout_analytics_options_v4';

    const ALL_LAYOUTS = {
        lg: DEFAULT_LAYOUT.lg,
        md: DEFAULT_LAYOUT.lg,
        sm: DEFAULT_LAYOUT.lg,
        xs: DEFAULT_LAYOUT.lg,
        xxs: DEFAULT_LAYOUT.lg
    };

    const [layouts, setLayouts] = useState(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? JSON.parse(saved) : ALL_LAYOUTS;
        } catch (e) {
            return ALL_LAYOUTS;
        }
    });

    useEffect(() => {
        setCurrentRoute(location.pathname);
    }, [location, setCurrentRoute]);

    const onLayoutChange = (currentLayout, allLayouts) => {
        setLayouts(allLayouts);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    };

    const resetLayout = () => {
        localStorage.removeItem(STORAGE_KEY);
        setLayouts(DEFAULT_LAYOUT);
        window.location.reload();
    };

    return (
        <div className="options-analytics-page full-bleed-page" data-tour-id="options-chain">
            <header className="page-header-flex">
                <h1 className="page-title">Options Analytics & Risk</h1>
                <button onClick={resetLayout} className="btn-utility ripple">Reset Layout</button>
            </header>
            
            <div className="scrollable-content-wrapper">
                <ResponsiveGridLayout
                    className="layout"
                    layouts={layouts}
                    onLayoutChange={onLayoutChange}
                    breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                    cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                    rowHeight={80}
                    isDraggable={true}
                    isResizable={true}
                    draggableHandle=".glass-panel-header"
                    margin={[16, 16]}
                >
                    <div key="kafka" className="widget-container">
                        <div className="glass-panel glass-premium h-full flex flex-col">
                            <div className="glass-panel-header p-3 border-b border-white/10 flex justify-between items-center cursor-move">
                                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Kafka Stream Monitor</h3>
                                <div className="flex items-center gap-2">
                                    <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                                    <span className="text-green-500 text-[9px] font-mono">LINKED</span>
                                </div>
                            </div>
                            <div className="flex-1 overflow-y-auto">
                                <KafkaStreamMonitor hideHeader={true} />
                            </div>
                        </div>
                    </div>

                    <div key="feargreed" className="widget-container">
                        <div className="glass-panel glass-premium h-full flex flex-col">
                             <div className="glass-panel-header p-3 border-b border-white/10 flex justify-between items-center cursor-move">
                                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Fear & Greed Index</h3>
                            </div>
                            <div className="flex-1 p-6 overflow-y-auto">
                                <FearGreedWidget />
                            </div>
                        </div>
                    </div>

                    <div key="hype" className="widget-container">
                        <div className="glass-panel glass-premium h-full flex flex-col">
                             <div className="glass-panel-header p-3 border-b border-white/10 flex justify-between items-center cursor-move">
                                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Sentiment Hype Meter</h3>
                            </div>
                            <div className="flex-1 p-6 overflow-y-auto">
                                <HypeMeterWidget hideHeader={true} />
                            </div>
                        </div>
                    </div>

                    <div key="gex" className="widget-container">
                        <div className="glass-panel glass-premium h-full flex flex-col">
                            <div className="glass-panel-header p-3 border-b border-white/10 flex justify-between items-center cursor-move">
                                <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Gamma Exposure (GEX)</h2>
                                <p className="text-[9px] text-slate-500 hidden sm:block">Market Maker Positioning</p>
                            </div>
                            <div className="flex-1 p-6 overflow-y-auto flex flex-col">
                                <div className="gex-chart-placeholder flex-1 min-h-[150px] flex items-end gap-2 border-b border-white/10 mb-4 relative">
                                    <div className="bar positive w-4 bg-green-500/50 rounded-t" style={{height: '60%'}}></div>
                                    <div className="bar negative w-4 bg-red-500/50 rounded-b" style={{height: '40%', alignSelf: 'flex-start'}}></div>
                                    <div className="bar positive w-4 bg-green-500/50 rounded-t" style={{height: '80%'}}></div>
                                    <div className="absolute top-1/2 left-0 right-0 h-px bg-white/20"></div>
                                </div>
                                <div className="flex justify-between text-[10px] font-mono">
                                    <span>Net GEX: <span className="text-green-400">+$4.2B</span></span>
                                    <span>Zero Gamma: <span className="text-amber-400">4450</span></span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div key="ff" className="widget-container">
                        <div className="glass-panel glass-premium h-full flex flex-col">
                             <div className="glass-panel-header p-3 border-b border-white/10 flex justify-between items-center cursor-move">
                                <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Factor Decomposition</h2>
                            </div>
                            <div className="flex-1 p-6 overflow-y-auto">
                                <div className="grid grid-cols-1 gap-2">
                                    {[
                                        { l: 'Mkt-RF', v: '+1.2', c: 'text-green-400' },
                                        { l: 'SMB', v: '-0.4', c: 'text-red-400' },
                                        { l: 'HML', v: '+0.8', c: 'text-green-400' },
                                        { l: 'RMW', v: '0.0', c: 'text-slate-400' }
                                    ].map((f, i) => (
                                        <div key={i} className="flex justify-between p-3 bg-white/5 rounded border border-white/5 text-[11px]">
                                            <span className="font-bold text-slate-500">{f.l}</span>
                                            <span className={f.c}>{f.v}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    <div key="iv" className="widget-container">
                        <div className="glass-panel glass-premium h-full flex flex-col">
                            <div className="glass-panel-header p-3 border-b border-white/10 flex justify-between items-center cursor-move">
                                <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest">IV Surface</h2>
                            </div>
                            <div className="flex-1 bg-white/5 flex items-center justify-center p-8 italic text-slate-600 text-xs">
                                [3D Volatility Plot Rendering Engine]
                            </div>
                        </div>
                    </div>
                </ResponsiveGridLayout>

                <div className="scroll-buffer-200" />
            </div>
        </div>
    );
};

export default AnalyticsOptions;
