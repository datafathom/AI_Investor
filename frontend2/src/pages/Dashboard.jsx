import React, { useEffect, useMemo, useState, useRef, useCallback, Suspense, lazy } from 'react';
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import './Dashboard.css';
import { useColorPalette } from '../hooks/useColorPalette';
import { useWidgetLayout } from '../hooks/useWidgetLayout';
import WindowHeader from '../components/WindowHeader';
import { SimpleBarChart, SimplePieChart, SimpleLineChart, SimpleAreaChart } from '../components/Charts/SimpleCharts';
import { authService } from '../utils/authService';
import io from 'socket.io-client';
import { Activity, Zap, TrendingUp, Globe, Clock, ShieldAlert, Cpu as CpuIcon, Trash2, Layout } from 'lucide-react';
import { useToast } from '../context/ToastContext';
import PageHeader from '../components/Navigation/PageHeader';

// AI Investor Widgets
import MonitorWidget from '../components/AI_Investor/Views/MonitorWidget';
import CommandWidget from '../components/AI_Investor/Views/CommandWidget';
import TerminalWidget from '../components/Terminal/TerminalWidget';
import ResearchWidget from '../components/AI_Investor/Views/ResearchWidget';
import PortfolioWidget from '../components/AI_Investor/Views/PortfolioWidget';
import DockerWidget from '../components/DockerWidget';
import WindowManagerWidget from '../components/WindowManager/WindowManagerWidget';
import HomeostasisWidget from '../components/AI_Investor/Views/HomeostasisWidget';
import SystemLogWidget from '../components/Terminal/SystemLogWidget';
const OptionsChainWidget = lazy(() => import('../widgets/OptionsChain/OptionsChainWidget'));
const MarketDepthWidget = lazy(() => import('../widgets/DOM/DOMWidget'));
const TradeTapeWidget = lazy(() => import('../components/AI_Investor/Views/TradeTapeWidget'));

// Lazy load heavy chart components
const SimpleScatterPlot = lazy(() => import('../components/Charts/SimpleCharts').then(module => ({ default: module.SimpleScatterPlot })));
const MovingAverageChart = lazy(() => import('../components/Charts/SimpleCharts').then(module => ({ default: module.MovingAverageChart })));
const AudioWaveform = lazy(() => import('../components/Charts/SimpleCharts').then(module => ({ default: module.AudioWaveform })));

const WIDGET_TITLES = {
    'monitor-view': 'Market Monitor',
    'command-view': 'Command Center',
    'research-view': 'Data Research',
    'portfolio-view': 'Live Portfolio',
    'window-manager': 'Window Manager',
    api: 'API Integration',
    palette: 'Color System',
    docker: 'Docker Containers',
    checklist: 'Launch Checklist',
    telemetry: 'Server Telemetry',
    ux: 'Experience Controls',
    socketio: 'Socket.io Realtime',
    'ping-api': 'Ping API',
    'server-status': 'Server Status',
    'bar-chart': 'Bar Chart',
    'pie-chart': 'Pie Chart',
    'line-chart': 'Line Chart',
    'area-chart': 'Area Chart',
    'scatter-plot': 'Scatter Plot',
    'moving-average': 'Moving Average',
    'audio-waveform': 'Audio Waveform',
    'homeostasis-view': 'Total Homeostasis',
    'options-chain-view': 'Options Chain / Greeks',
    'market-depth-view': 'Level 2 Market Depth (DOM)',
    'trade-tape-view': 'Live Trade Tape (Time & Sales)',
    'terminal-view': 'System Console',
    'system-log-view': 'System Log'
};

const DEFAULT_LAYOUT = [
    { i: 'monitor-view', x: 0, y: 0, w: 24, h: 20, minW: 16, minH: 14, maxW: 48 },
    { i: 'command-view', x: 24, y: 0, w: 24, h: 10, minW: 16, minH: 10, maxW: 48 },
    { i: 'portfolio-view', x: 24, y: 10, w: 24, h: 16, minW: 16, minH: 12, maxW: 48 },
    { i: 'research-view', x: 0, y: 20, w: 24, h: 18, minW: 16, minH: 12, maxW: 48 },
    { i: 'homeostasis-view', x: 24, y: 26, w: 24, h: 16, minW: 16, minH: 12, maxW: 48 },
    { i: 'options-chain-view', x:0, y: 38, w: 24, h: 15, minW: 16, minH: 12, maxW: 48 },
    { i: 'market-depth-view', x: 24, y: 42, w: 12, h: 15, minW: 8, minH: 12, maxW: 24 },
    { i: 'trade-tape-view', x: 36, y: 42, w: 12, h: 15, minW: 8, minH: 12, maxW: 24 },
    { i: 'terminal-view', x: 0, y: 53, w: 24, h: 10, minW: 16, minH: 8, maxW: 48 },
    { i: 'system-log-view', x: 24, y: 53, w: 24, h: 10, minW: 16, minH: 8, maxW: 48 },
    { i: 'bar-chart', x: 24, y: 63, w: 24, h: 12, minW: 16, minH: 10, maxW: 48 },
    { i: 'socketio', x: 0, y: 63, w: 48, h: 8, minW: 16, minH: 6, maxW: 48 },
];

const Dashboard = ({
    setToast,
    handleViewSource,
    globalLock,
    isDarkMode,
    widgetStates,
    setWidgetStates,
    widgetVisibility,
    setWidgetVisibility
}) => {
    const { layout, setLayout, resetLayout } = useWidgetLayout();
    const { showToast } = useToast();
    const [gridWidth, setGridWidth] = useState(1200);
    // Removed showLockModal state in favor of toasts
    const [marketPulse, setMarketPulse] = useState({
        sentiment: 'BULLISH',
        volatility: 'LOW',
        nextEvent: 'FOMC (2h)',
        activeAgents: 12
    });

    // Handler for drag attempts when locked
    const handleDragAttempt = useCallback(() => {
        if (globalLock) {
            showToast('LAYOUT LOCKED: Enable editing via the Selection menu.', 'warning');
        }
    }, [globalLock, showToast]);

    const handleClearLogs = useCallback(() => {
        setLogs([]);
        showToast('System logs cleared.', 'info');
    }, [showToast]);

    // Mock data for Bar Chart
    const barChartData = useMemo(() => [
        {
            label: 'Market Volume',
            values: [
                { x: 'NVDA', y: 4500 },
                { x: 'TSLA', y: 3200 },
                { x: 'AAPL', y: 2800 },
                { x: 'MSFT', y: 2100 },
                { x: 'AMD', y: 1900 },
                { x: 'SPY', y: 5200 },
            ]
        }
    ], []);

    // Mock logs for the terminal
    const [logs, setLogs] = useState([
        { timestamp: Date.now() - 5000, message: 'System initialized. All agents online.', type: 'info' },
        { timestamp: Date.now() - 4000, message: 'Market data feed connected: NASDAQ/WSS', type: 'success' },
        { timestamp: Date.now() - 3000, message: 'Running momentum scans on SPY, NVDA, TSLA...', type: 'info' },
        { timestamp: Date.now() - 2000, message: 'Alert: Unusual options activity detected in NVDA.', type: 'warning' },
        { timestamp: Date.now() - 1000, message: 'Trade executed: BUY 100 TSLA @ 218.42', type: 'success' },
    ]);

    useEffect(() => {
        const interval = setInterval(() => {
            const newLog = {
                timestamp: Date.now(),
                message: `Kernel heartbeat: Process ${Math.floor(Math.random() * 9999)} ok. Memory: 42.1GB/128GB`,
                type: 'info'
            };
            setLogs(prev => [...prev.slice(-49), newLog]);
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    // Throttle layout changes
    const layoutChangeTimerRef = useRef(null);
    const pendingLayoutRef = useRef(null);

    // Mobile Logic
    const isMobile = gridWidth < 768;

    // Force single column stack on mobile, preserve desktop layout otherwise
    const displayLayout = useMemo(() => {
        if (!isMobile) return layout.filter(item => widgetVisibility[item.i] !== false);

        // Sort by Y position to maintain natural reading order
        const sorted = [...layout].filter(item => widgetVisibility[item.i] !== false).sort((a, b) => a.y - b.y || a.x - b.x);

        let yOffset = 0;
        return sorted.map(item => {
            const newItem = {
                ...item,
                x: 0,
                w: 48, // Full width (cols={48})
                minW: 1, // Reset constraints for mobile flow
                maxW: 48,
                y: yOffset,
                isDraggable: false, // Disable drag on mobile to prevent chaos
                isResizable: false
            };
            yOffset += (newItem.h || 4); // Stack them
            return newItem;
        });
    }, [layout, isMobile, widgetVisibility]);

    const throttledSetLayout = useCallback((newLayout) => {
        // DO NOT save layout changes when in mobile mode to prevent destroying desktop arrangement
        if (window.innerWidth < 768) return;

        pendingLayoutRef.current = newLayout;
        if (!layoutChangeTimerRef.current) {
            layoutChangeTimerRef.current = setTimeout(() => {
                if (pendingLayoutRef.current) {
                    setLayout(pendingLayoutRef.current);
                    pendingLayoutRef.current = null;
                }
                layoutChangeTimerRef.current = null;
            }, 50);
        }
    }, [setLayout]);

    // Handle window resize
    useEffect(() => {
        const updateGridWidth = () => {
            // Try explicit container first, else fallback to window width minus padding
            const container = document.querySelector('.dashboard-container') || document.querySelector('.terminal-workspace');
            if (container) {
                // Subtract padding (approx 32px for margins)
                setGridWidth(container.offsetWidth - 32);
            } else {
                setGridWidth(window.innerWidth - 32);
            }
        };

        // Initial calc
        updateGridWidth();

        // Add listener
        window.addEventListener('resize', updateGridWidth);

        // Cleanup
        return () => window.removeEventListener('resize', updateGridWidth);
    }, []);

    const handleWidgetMinimize = (widgetId) => {
        const isCurrentlyMinimized = widgetStates[widgetId]?.minimized;
        const currentLayoutItem = layout.find(item => item.i === widgetId);
        if (!isCurrentlyMinimized) {
            if (currentLayoutItem) {
                setWidgetStates(prev => ({
                    ...prev,
                    [widgetId]: { ...prev[widgetId], minimized: true, maximized: false, savedHeight: currentLayoutItem.h },
                }));
                setLayout(prev => prev.map(item => item.i === widgetId ? { ...item, h: 1, minH: 1 } : item));
            }
        } else {
            const savedHeight = widgetStates[widgetId]?.savedHeight;
            const defaultLayout = DEFAULT_LAYOUT.find(item => item.i === widgetId);
            const heightToRestore = savedHeight || defaultLayout?.h || 3;
            setWidgetStates(prev => ({ ...prev, [widgetId]: { ...prev[widgetId], minimized: false, maximized: false } }));
            setLayout(prev => prev.map(item => item.i === widgetId ? { ...item, h: heightToRestore, minH: defaultLayout?.minH || 2 } : item));
        }
    };

    const handleWidgetMaximize = (widgetId) => {
        const isCurrentlyMaximized = widgetStates[widgetId]?.maximized;
        const currentLayoutItem = layout.find(item => item.i === widgetId);
        if (!isCurrentlyMaximized) {
            setTimeout(() => {
                const widgetElement = document.querySelector(`[data-widget-id="${widgetId}"]`);
                if (widgetElement) {
                    const contentSection = widgetElement.querySelector('section');
                    if (contentSection) {
                        const contentHeight = contentSection.scrollHeight;
                        const requiredRows = Math.ceil((contentHeight + 28) / 60);
                        if (currentLayoutItem) {
                            setWidgetStates(prev => ({
                                ...prev,
                                [widgetId]: { ...prev[widgetId], maximized: true, minimized: false, savedBeforeMaximize: { ...currentLayoutItem } },
                            }));
                            setLayout(prev => prev.map(item => item.i === widgetId ? { ...item, x: 0, y: 0, h: Math.max(requiredRows, item.minH || 2), w: Math.min(Math.max(item.w, 6), item.maxW || 48) } : item));
                        }
                    }
                }
            }, 0);
        } else {
            const saved = widgetStates[widgetId]?.savedBeforeMaximize;
            if (saved) {
                setWidgetStates(prev => ({ ...prev, [widgetId]: { ...prev[widgetId], maximized: false } }));
                setLayout(prev => prev.map(item => item.i === widgetId ? { ...item, x: saved.x, y: saved.y, w: saved.w, h: saved.h } : item));
            }
        }
    };

    const handleWidgetClose = (widgetId) => {
        const currentLayoutItem = layout.find(item => item.i === widgetId);
        if (currentLayoutItem) {
            setWidgetStates(prev => ({ ...prev, [widgetId]: { ...prev[widgetId], lastLayout: { ...currentLayoutItem } } }));
        }
        setWidgetVisibility(prev => ({ ...prev, [widgetId]: false }));
    };

    const handleWidgetLock = (widgetId) => {
        setWidgetStates(prev => ({ ...prev, [widgetId]: { ...prev[widgetId], locked: !prev[widgetId]?.locked } }));
    };

    const handleLinkingGroupChange = (widgetId, group) => {
        setWidgetStates(prev => ({ ...prev, [widgetId]: { ...prev[widgetId], linkingGroup: group } }));
    };

    const handleMinimumFullView = (widgetId) => {
        const currentLayoutItem = layout.find(item => item.i === widgetId);
        if (!currentLayoutItem) return;
        setTimeout(() => {
            const widgetElement = document.querySelector(`[data-widget-id="${widgetId}"]`);
            if (!widgetElement) return;
            const contentSection = widgetElement.querySelector('section');
            if (!contentSection) return;
            const requiredHeight = contentSection.scrollHeight + 28;
            const requiredRows = Math.ceil(requiredHeight / 60);
            setLayout(prev => prev.map(item => item.i === widgetId ? { ...item, h: Math.max(item.minH || 2, requiredRows) } : item));
        }, 0);
    };

    return (
        <div className="dashboard-container relative">
            {/* METRICS TICKER BAR - Full Width Fluidity */}
            <div className="metrics-ticker-bar flex-shrink-0">
                <div 
                    className="metric-item glass-panel cursor-help"
                    data-tooltip="Aggregate market sentiment from 50+ data sources."
                >
                    <div className="metric-label">SENTIMENT</div>
                    <div className="metric-value">
                        <TrendingUp className="text-green-400" size={16} />
                        <span className="value-text">{marketPulse.sentiment}</span>
                    </div>
                </div>

                <div 
                    className="metric-item glass-panel cursor-help"
                    data-tooltip="CBOE Volatility Index. High values indicate market fear."
                >
                    <div className="metric-label">VOLATILITY VIX</div>
                    <div className="metric-value">
                        <Activity className="text-amber-400" size={16} />
                        <span className="value-text font-mono">13.42 <span className="text-[10px] text-green-400">(-2.1%)</span></span>
                    </div>
                </div>

                <div 
                    className="metric-item glass-panel cursor-help"
                    data-tooltip="System health indicator. Optimal state = peak performance."
                >
                    <div className="metric-label">HOMEOSTASIS</div>
                    <div className="metric-value">
                        <Zap className="text-fuchsia-400 animate-pulse" size={16} />
                        <span className="value-text">OPTIMAL</span>
                    </div>
                </div>

                <div 
                    className="metric-item glass-panel cursor-help"
                    data-tooltip="Number of AI agents currently scanning and analyzing data."
                >
                    <div className="metric-label">ACTIVE AGENTS</div>
                    <div className="metric-value">
                        <CpuIcon className="text-cyan-400" size={16} />
                        <span className="value-text">{marketPulse.activeAgents}</span>
                    </div>
                </div>
            </div>

            {/* Grid Scroll Wrapper - Full Bleed Layout */}
            <div className="grid-scroll-wrapper">
            <GridLayout
                className="layout"
                layout={displayLayout}
                onLayoutChange={throttledSetLayout}
                onDragStart={(layout, oldItem, newItem, placeholder, e, element) => {
                    if (globalLock) {
                        showToast('LAYOUT LOCKED: Enable editing via the Selection menu.', 'warning');
                        return false;
                    }
                }}
                cols={48}
                rowHeight={60}
                width={gridWidth}
                isDraggable={!globalLock}
                isResizable={!globalLock}
                draggableHandle=".widget-drag-handle"
                resizeHandles={['se', 'sw', 'ne', 'nw', 's', 'n', 'e', 'w']}
                margin={[8, 8]}
                containerPadding={[0, 0]}
                useCSSTransforms={true}
                compactType="vertical"
                preventCollision={false}
            >
                {widgetVisibility['monitor-view'] !== false && (
                    <div key="monitor-view" data-widget-id="monitor-view" className={`widget-wrapper ${widgetStates['monitor-view']?.minimized ? 'minimized' : ''} ${widgetStates['monitor-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['monitor-view']} onMinimize={() => handleWidgetMinimize('monitor-view')} onMaximize={() => handleWidgetMaximize('monitor-view')} onClose={() => handleWidgetClose('monitor-view')} onLock={() => handleWidgetLock('monitor-view')} onMinimumFullView={() => handleMinimumFullView('monitor-view')} onViewSource={() => handleViewSource('monitor-view')} isMaximized={widgetStates['monitor-view']?.maximized} isLocked={widgetStates['monitor-view']?.locked} linkingGroup={widgetStates['monitor-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('monitor-view', g)} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['monitor-view']?.minimized && <div className="window-content"><MonitorWidget /></div>}
                    </div>
                )}
                {widgetVisibility['command-view'] !== false && (
                    <div key="command-view" data-widget-id="command-view" className={`widget-wrapper ${widgetStates['command-view']?.minimized ? 'minimized' : ''} ${widgetStates['command-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['command-view']} onMinimize={() => handleWidgetMinimize('command-view')} onMaximize={() => handleWidgetMaximize('command-view')} onClose={() => handleWidgetClose('command-view')} onLock={() => handleWidgetLock('command-view')} onMinimumFullView={() => handleMinimumFullView('command-view')} onViewSource={() => handleViewSource('command-view')} isMaximized={widgetStates['command-view']?.maximized} isLocked={widgetStates['command-view']?.locked} linkingGroup={widgetStates['command-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('command-view', g)} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['command-view']?.minimized && <div className="window-content"><CommandWidget /></div>}
                    </div>
                )}
                {widgetVisibility['portfolio-view'] !== false && (
                    <div key="portfolio-view" data-widget-id="portfolio-view" className={`widget-wrapper ${widgetStates['portfolio-view']?.minimized ? 'minimized' : ''} ${widgetStates['portfolio-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['portfolio-view']} onMinimize={() => handleWidgetMinimize('portfolio-view')} onMaximize={() => handleWidgetMaximize('portfolio-view')} onClose={() => handleWidgetClose('portfolio-view')} onLock={() => handleWidgetLock('portfolio-view')} onMinimumFullView={() => handleMinimumFullView('portfolio-view')} onViewSource={() => handleViewSource('portfolio-view')} isMaximized={widgetStates['portfolio-view']?.maximized} isLocked={widgetStates['portfolio-view']?.locked} linkingGroup={widgetStates['portfolio-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('portfolio-view', g)} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['portfolio-view']?.minimized && <div className="window-content"><PortfolioWidget /></div>}
                    </div>
                )}
                {widgetVisibility['research-view'] !== false && (
                    <div key="research-view" data-widget-id="research-view" className={`widget-wrapper ${widgetStates['research-view']?.minimized ? 'minimized' : ''} ${widgetStates['research-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['research-view']} onMinimize={() => handleWidgetMinimize('research-view')} onMaximize={() => handleWidgetMaximize('research-view')} onClose={() => handleWidgetClose('research-view')} onLock={() => handleWidgetLock('research-view')} onMinimumFullView={() => handleMinimumFullView('research-view')} onViewSource={() => handleViewSource('research-view')} isMaximized={widgetStates['research-view']?.maximized} isLocked={widgetStates['research-view']?.locked} linkingGroup={widgetStates['research-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('research-view', g)} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['research-view']?.minimized && <div className="window-content"><ResearchWidget /></div>}
                    </div>
                )}
                {widgetVisibility['terminal-view'] !== false && (
                    <div key="terminal-view" data-widget-id="terminal-view" className={`widget-wrapper ${widgetStates['terminal-view']?.minimized ? 'minimized' : ''} ${widgetStates['terminal-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['terminal-view']} onMinimize={() => handleWidgetMinimize('terminal-view')} onMaximize={() => handleWidgetMaximize('terminal-view')} onClose={() => handleWidgetClose('terminal-view')} onLock={() => handleWidgetLock('terminal-view')} onMinimumFullView={() => handleMinimumFullView('terminal-view')} onViewSource={() => handleViewSource('terminal-view')} isMaximized={widgetStates['terminal-view']?.maximized} isLocked={widgetStates['terminal-view']?.locked} linkingGroup={widgetStates['terminal-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('terminal-view', g)} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['terminal-view']?.minimized && <div className="window-content"><TerminalWidget logs={logs} onClearHistory={handleClearLogs} /></div>}
                    </div>
                )}
                {/* Charts */}
                {widgetVisibility['bar-chart'] !== false && (
                    <div key="bar-chart" data-widget-id="bar-chart" className={`widget-wrapper ${widgetStates['bar-chart']?.minimized ? 'minimized' : ''} ${widgetStates['bar-chart']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['bar-chart']} onMinimize={() => handleWidgetMinimize('bar-chart')} onMaximize={() => handleWidgetMaximize('bar-chart')} onClose={() => handleWidgetClose('bar-chart')} onLock={() => handleWidgetLock('bar-chart')} onMinimumFullView={() => handleMinimumFullView('bar-chart')} onViewSource={() => handleViewSource('bar-chart')} isMaximized={widgetStates['bar-chart']?.maximized} isLocked={widgetStates['bar-chart']?.locked} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['bar-chart']?.minimized && <div className="window-content chart-card"><div style={{ flex: 1, minHeight: '300px' }}><SimpleBarChart data={barChartData} /></div></div>}
                    </div>
                )}
                {widgetVisibility['homeostasis-view'] !== false && (
                    <div key="homeostasis-view" data-widget-id="homeostasis-view" className={`widget-wrapper ${widgetStates['homeostasis-view']?.minimized ? 'minimized' : ''} ${widgetStates['homeostasis-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['homeostasis-view']} onMinimize={() => handleWidgetMinimize('homeostasis-view')} onMaximize={() => handleWidgetMaximize('homeostasis-view')} onClose={() => handleWidgetClose('homeostasis-view')} onLock={() => handleWidgetLock('homeostasis-view')} onMinimumFullView={() => handleMinimumFullView('homeostasis-view')} onViewSource={() => handleViewSource('homeostasis-view')} isMaximized={widgetStates['homeostasis-view']?.maximized} isLocked={widgetStates['homeostasis-view']?.locked} linkingGroup={widgetStates['homeostasis-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('homeostasis-view', g)} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['homeostasis-view']?.minimized && <div className="window-content"><HomeostasisWidget /></div>}
                    </div>
                )}
                {widgetVisibility['options-chain-view'] !== false && (
                    <div key="options-chain-view" data-widget-id="options-chain-view" className={`widget-wrapper ${widgetStates['options-chain-view']?.minimized ? 'minimized' : ''} ${widgetStates['options-chain-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['options-chain-view']} onMinimize={() => handleWidgetMinimize('options-chain-view')} onMaximize={() => handleWidgetMaximize('options-chain-view')} onClose={() => handleWidgetClose('options-chain-view')} onLock={() => handleWidgetLock('options-chain-view')} onMinimumFullView={() => handleMinimumFullView('options-chain-view')} onViewSource={() => handleViewSource('options-chain-view')} isMaximized={widgetStates['options-chain-view']?.maximized} isLocked={widgetStates['options-chain-view']?.locked} linkingGroup={widgetStates['options-chain-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('options-chain-view', g)} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['options-chain-view']?.minimized && <Suspense fallback={<div>Loading...</div>}><div className="window-content"><OptionsChainWidget linkingGroup={widgetStates['options-chain-view']?.linkingGroup || 'none'} /></div></Suspense>}
                    </div>
                )}
                {widgetVisibility['market-depth-view'] !== false && (
                    <div key="market-depth-view" data-widget-id="market-depth-view" className={`widget-wrapper ${widgetStates['market-depth-view']?.minimized ? 'minimized' : ''} ${widgetStates['market-depth-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['market-depth-view']} onMinimize={() => handleWidgetMinimize('market-depth-view')} onMaximize={() => handleWidgetMaximize('market-depth-view')} onClose={() => handleWidgetClose('market-depth-view')} onLock={() => handleWidgetLock('market-depth-view')} onMinimumFullView={() => handleMinimumFullView('market-depth-view')} onViewSource={() => handleViewSource('market-depth-view')} isMaximized={widgetStates['market-depth-view']?.maximized} isLocked={widgetStates['market-depth-view']?.locked} linkingGroup={widgetStates['market-depth-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('market-depth-view', g)} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['market-depth-view']?.minimized && <Suspense fallback={<div>Loading...</div>}><div className="window-content"><MarketDepthWidget linkingGroup={widgetStates['market-depth-view']?.linkingGroup || 'none'} /></div></Suspense>}
                    </div>
                )}
                {widgetVisibility['trade-tape-view'] !== false && (
                    <div key="trade-tape-view" data-widget-id="trade-tape-view" className={`widget-wrapper ${widgetStates['trade-tape-view']?.minimized ? 'minimized' : ''} ${widgetStates['trade-tape-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['trade-tape-view']} onMinimize={() => handleWidgetMinimize('trade-tape-view')} onMaximize={() => handleWidgetMaximize('trade-tape-view')} onClose={() => handleWidgetClose('trade-tape-view')} onLock={() => handleWidgetLock('trade-tape-view')} onMinimumFullView={() => handleMinimumFullView('trade-tape-view')} onViewSource={() => handleViewSource('trade-tape-view')} isMaximized={widgetStates['trade-tape-view']?.maximized} isLocked={widgetStates['trade-tape-view']?.locked} linkingGroup={widgetStates['trade-tape-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('trade-tape-view', g)} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['trade-tape-view']?.minimized && <Suspense fallback={<div>Loading...</div>}><div className="window-content"><TradeTapeWidget linkingGroup={widgetStates['trade-tape-view']?.linkingGroup || 'none'} /></div></Suspense>}
                    </div>
                )}
                {widgetVisibility['system-log-view'] !== false && (
                    <div key="system-log-view" data-widget-id="system-log-view" className={`widget-wrapper ${widgetStates['system-log-view']?.minimized ? 'minimized' : ''} ${widgetStates['system-log-view']?.maximized ? 'maximized' : ''}`}>
                        <WindowHeader title={WIDGET_TITLES['system-log-view']} onMinimize={() => handleWidgetMinimize('system-log-view')} onMaximize={() => handleWidgetMaximize('system-log-view')} onClose={() => handleWidgetClose('system-log-view')} onLock={() => handleWidgetLock('system-log-view')} onMinimumFullView={() => handleMinimumFullView('system-log-view')} onViewSource={() => handleViewSource('system-log-view')} isMaximized={widgetStates['system-log-view']?.maximized} isLocked={widgetStates['system-log-view']?.locked} />
                        <div className="widget-drag-handle" onMouseDown={handleDragAttempt}><span></span></div>
                        {!widgetStates['system-log-view']?.minimized && <div className="window-content"><SystemLogWidget /></div>}
                    </div>
                )}
                {/* Add more widgets as needed */}
            </GridLayout>
            {/* Bottom Buffer for grid scrolling */}
            <div style={{ height: '100px', width: '100%' }} />
            </div> {/* End grid-scroll-wrapper */}

            {/* Lock Overlay - Shows when locked and intercepts clicks */}
            {globalLock && (
                <div 
                    className="absolute inset-0 z-[100] cursor-not-allowed"
                    onMouseDown={(e) => {
                        e.preventDefault();
                        e.stopPropagation();
                        showToast('LAYOUT LOCKED: Enable editing via the Selection menu.', 'warning');
                    }}
                    style={{ pointerEvents: 'auto' }}
                />
            )}
        </div>
    );
};

export default Dashboard;
