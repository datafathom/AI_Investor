
import React, { useEffect, useMemo, useState, useRef, useCallback, Suspense, lazy } from 'react';
import GridLayout from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import { useColorPalette } from '../hooks/useColorPalette';
import { useWidgetLayout } from '../hooks/useWidgetLayout';
import WindowHeader from '../components/WindowHeader';
import { SimpleBarChart, SimplePieChart, SimpleLineChart, SimpleAreaChart } from '../components/Charts/SimpleCharts';
import { authService } from '../utils/authService';
import io from 'socket.io-client';

// AI Investor Widgets
import MonitorWidget from '../components/AI_Investor/Views/MonitorWidget';
import CommandWidget from '../components/AI_Investor/Views/CommandWidget';
import ResearchWidget from '../components/AI_Investor/Views/ResearchWidget';
import PortfolioWidget from '../components/AI_Investor/Views/PortfolioWidget';
import DockerWidget from '../components/DockerWidget';
import WindowManagerWidget from '../components/WindowManager/WindowManagerWidget';
import HomeostasisWidget from '../components/AI_Investor/Views/HomeostasisWidget';
const OptionsChainWidget = lazy(() => import('../components/AI_Investor/Views/OptionsChainWidget'));
const MarketDepthWidget = lazy(() => import('../components/AI_Investor/Views/MarketDepthWidget'));
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
  'trade-tape-view': 'Live Trade Tape (Time & Sales)'
};

const DEFAULT_LAYOUT = [
  { i: 'monitor-view', x: 0, y: 0, w: 24, h: 20, minW: 16, minH: 10, maxW: 48 },
  { i: 'command-view', x: 24, y: 0, w: 24, h: 10, minW: 16, minH: 8, maxW: 48 },
  { i: 'portfolio-view', x: 24, y: 10, w: 24, h: 10, minW: 16, minH: 8, maxW: 48 },
  { i: 'research-view', x: 0, y: 20, w: 24, h: 12, minW: 16, minH: 8, maxW: 48 },
  { i: 'homeostasis-view', x: 24, y: 20, w: 24, h: 12, minW: 16, minH: 8, maxW: 48 },
  { i: 'options-chain-view', x: 0, y: 32, w: 24, h: 15, minW: 16, minH: 10, maxW: 48 },
  { i: 'market-depth-view', x: 24, y: 32, w: 12, h: 15, minW: 8, minH: 10, maxW: 24 },
  { i: 'trade-tape-view', x: 36, y: 32, w: 12, h: 15, minW: 8, minH: 10, maxW: 24 },
  { i: 'socketio', x: 0, y: 47, w: 24, h: 7, minW: 16, minH: 4, maxW: 48 },
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
  const [gridWidth, setGridWidth] = useState(1200);

  // Throttle layout changes
  const layoutChangeTimerRef = useRef(null);
  const pendingLayoutRef = useRef(null);

  const throttledSetLayout = useCallback((newLayout) => {
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
      const container = document.querySelector('.widget-grid-container');
      if (container) {
        setGridWidth(container.offsetWidth - 32);
      }
    };
    updateGridWidth();
    window.addEventListener('resize', updateGridWidth);
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
    <GridLayout
      className="layout"
      layout={layout.filter(item => widgetVisibility[item.i] !== false)}
      onLayoutChange={throttledSetLayout}
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
          <div className="widget-drag-handle"><span></span></div>
          {!widgetStates['monitor-view']?.minimized && <section className="glass card"><MonitorWidget /></section>}
        </div>
      )}
      {widgetVisibility['command-view'] !== false && (
        <div key="command-view" data-widget-id="command-view" className={`widget-wrapper ${widgetStates['command-view']?.minimized ? 'minimized' : ''} ${widgetStates['command-view']?.maximized ? 'maximized' : ''}`}>
          <WindowHeader title={WIDGET_TITLES['command-view']} onMinimize={() => handleWidgetMinimize('command-view')} onMaximize={() => handleWidgetMaximize('command-view')} onClose={() => handleWidgetClose('command-view')} onLock={() => handleWidgetLock('command-view')} onMinimumFullView={() => handleMinimumFullView('command-view')} onViewSource={() => handleViewSource('command-view')} isMaximized={widgetStates['command-view']?.maximized} isLocked={widgetStates['command-view']?.locked} linkingGroup={widgetStates['command-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('command-view', g)} />
          <div className="widget-drag-handle"><span></span></div>
          {!widgetStates['command-view']?.minimized && <section className="glass card"><CommandWidget /></section>}
        </div>
      )}
      {widgetVisibility['portfolio-view'] !== false && (
        <div key="portfolio-view" data-widget-id="portfolio-view" className={`widget-wrapper ${widgetStates['portfolio-view']?.minimized ? 'minimized' : ''} ${widgetStates['portfolio-view']?.maximized ? 'maximized' : ''}`}>
          <WindowHeader title={WIDGET_TITLES['portfolio-view']} onMinimize={() => handleWidgetMinimize('portfolio-view')} onMaximize={() => handleWidgetMaximize('portfolio-view')} onClose={() => handleWidgetClose('portfolio-view')} onLock={() => handleWidgetLock('portfolio-view')} onMinimumFullView={() => handleMinimumFullView('portfolio-view')} onViewSource={() => handleViewSource('portfolio-view')} isMaximized={widgetStates['portfolio-view']?.maximized} isLocked={widgetStates['portfolio-view']?.locked} linkingGroup={widgetStates['portfolio-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('portfolio-view', g)} />
          <div className="widget-drag-handle"><span></span></div>
          {!widgetStates['portfolio-view']?.minimized && <section className="glass card"><PortfolioWidget /></section>}
        </div>
      )}
      {widgetVisibility['research-view'] !== false && (
        <div key="research-view" data-widget-id="research-view" className={`widget-wrapper ${widgetStates['research-view']?.minimized ? 'minimized' : ''} ${widgetStates['research-view']?.maximized ? 'maximized' : ''}`}>
          <WindowHeader title={WIDGET_TITLES['research-view']} onMinimize={() => handleWidgetMinimize('research-view')} onMaximize={() => handleWidgetMaximize('research-view')} onClose={() => handleWidgetClose('research-view')} onLock={() => handleWidgetLock('research-view')} onMinimumFullView={() => handleMinimumFullView('research-view')} onViewSource={() => handleViewSource('research-view')} isMaximized={widgetStates['research-view']?.maximized} isLocked={widgetStates['research-view']?.locked} linkingGroup={widgetStates['research-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('research-view', g)} />
          <div className="widget-drag-handle"><span></span></div>
          {!widgetStates['research-view']?.minimized && <section className="glass card"><ResearchWidget /></section>}
        </div>
      )}
      {/* Charts */}
      {widgetVisibility['bar-chart'] !== false && (
        <div key="bar-chart" data-widget-id="bar-chart" className={`widget-wrapper ${widgetStates['bar-chart']?.minimized ? 'minimized' : ''} ${widgetStates['bar-chart']?.maximized ? 'maximized' : ''}`}>
          <WindowHeader title={WIDGET_TITLES['bar-chart']} onMinimize={() => handleWidgetMinimize('bar-chart')} onMaximize={() => handleWidgetMaximize('bar-chart')} onClose={() => handleWidgetClose('bar-chart')} onLock={() => handleWidgetLock('bar-chart')} onMinimumFullView={() => handleMinimumFullView('bar-chart')} onViewSource={() => handleViewSource('bar-chart')} isMaximized={widgetStates['bar-chart']?.maximized} isLocked={widgetStates['bar-chart']?.locked} />
          <div className="widget-drag-handle"><span></span></div>
          {!widgetStates['bar-chart']?.minimized && <section className="glass card chart-card"><div style={{ flex: 1 }}><SimpleBarChart /></div></section>}
        </div>
      )}
      {widgetVisibility['homeostasis-view'] !== false && (
        <div key="homeostasis-view" data-widget-id="homeostasis-view" className={`widget-wrapper ${widgetStates['homeostasis-view']?.minimized ? 'minimized' : ''} ${widgetStates['homeostasis-view']?.maximized ? 'maximized' : ''}`}>
          <WindowHeader title={WIDGET_TITLES['homeostasis-view']} onMinimize={() => handleWidgetMinimize('homeostasis-view')} onMaximize={() => handleWidgetMaximize('homeostasis-view')} onClose={() => handleWidgetClose('homeostasis-view')} onLock={() => handleWidgetLock('homeostasis-view')} onMinimumFullView={() => handleMinimumFullView('homeostasis-view')} onViewSource={() => handleViewSource('homeostasis-view')} isMaximized={widgetStates['homeostasis-view']?.maximized} isLocked={widgetStates['homeostasis-view']?.locked} linkingGroup={widgetStates['homeostasis-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('homeostasis-view', g)} />
          <div className="widget-drag-handle"><span></span></div>
          {!widgetStates['homeostasis-view']?.minimized && <section className="glass card"><HomeostasisWidget /></section>}
        </div>
      )}
      {widgetVisibility['options-chain-view'] !== false && (
        <div key="options-chain-view" data-widget-id="options-chain-view" className={`widget-wrapper ${widgetStates['options-chain-view']?.minimized ? 'minimized' : ''} ${widgetStates['options-chain-view']?.maximized ? 'maximized' : ''}`}>
          <WindowHeader title={WIDGET_TITLES['options-chain-view']} onMinimize={() => handleWidgetMinimize('options-chain-view')} onMaximize={() => handleWidgetMaximize('options-chain-view')} onClose={() => handleWidgetClose('options-chain-view')} onLock={() => handleWidgetLock('options-chain-view')} onMinimumFullView={() => handleMinimumFullView('options-chain-view')} onViewSource={() => handleViewSource('options-chain-view')} isMaximized={widgetStates['options-chain-view']?.maximized} isLocked={widgetStates['options-chain-view']?.locked} linkingGroup={widgetStates['options-chain-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('options-chain-view', g)} />
          <div className="widget-drag-handle"><span></span></div>
          {!widgetStates['options-chain-view']?.minimized && <Suspense fallback={<div>Loading...</div>}><section className="glass card"><OptionsChainWidget linkingGroup={widgetStates['options-chain-view']?.linkingGroup || 'none'} /></section></Suspense>}
        </div>
      )}
      {widgetVisibility['market-depth-view'] !== false && (
        <div key="market-depth-view" data-widget-id="market-depth-view" className={`widget-wrapper ${widgetStates['market-depth-view']?.minimized ? 'minimized' : ''} ${widgetStates['market-depth-view']?.maximized ? 'maximized' : ''}`}>
          <WindowHeader title={WIDGET_TITLES['market-depth-view']} onMinimize={() => handleWidgetMinimize('market-depth-view')} onMaximize={() => handleWidgetMaximize('market-depth-view')} onClose={() => handleWidgetClose('market-depth-view')} onLock={() => handleWidgetLock('market-depth-view')} onMinimumFullView={() => handleMinimumFullView('market-depth-view')} onViewSource={() => handleViewSource('market-depth-view')} isMaximized={widgetStates['market-depth-view']?.maximized} isLocked={widgetStates['market-depth-view']?.locked} linkingGroup={widgetStates['market-depth-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('market-depth-view', g)} />
          <div className="widget-drag-handle"><span></span></div>
          {!widgetStates['market-depth-view']?.minimized && <Suspense fallback={<div>Loading...</div>}><section className="glass card"><MarketDepthWidget linkingGroup={widgetStates['market-depth-view']?.linkingGroup || 'none'} /></section></Suspense>}
        </div>
      )}
      {widgetVisibility['trade-tape-view'] !== false && (
        <div key="trade-tape-view" data-widget-id="trade-tape-view" className={`widget-wrapper ${widgetStates['trade-tape-view']?.minimized ? 'minimized' : ''} ${widgetStates['trade-tape-view']?.maximized ? 'maximized' : ''}`}>
          <WindowHeader title={WIDGET_TITLES['trade-tape-view']} onMinimize={() => handleWidgetMinimize('trade-tape-view')} onMaximize={() => handleWidgetMaximize('trade-tape-view')} onClose={() => handleWidgetClose('trade-tape-view')} onLock={() => handleWidgetLock('trade-tape-view')} onMinimumFullView={() => handleMinimumFullView('trade-tape-view')} onViewSource={() => handleViewSource('trade-tape-view')} isMaximized={widgetStates['trade-tape-view']?.maximized} isLocked={widgetStates['trade-tape-view']?.locked} linkingGroup={widgetStates['trade-tape-view']?.linkingGroup || 'none'} onLinkingGroupChange={(g) => handleLinkingGroupChange('trade-tape-view', g)} />
          <div className="widget-drag-handle"><span></span></div>
          {!widgetStates['trade-tape-view']?.minimized && <Suspense fallback={<div>Loading...</div>}><section className="glass card"><TradeTapeWidget linkingGroup={widgetStates['trade-tape-view']?.linkingGroup || 'none'} /></section></Suspense>}
        </div>
      )}
      {/* Add more widgets as needed */}
    </GridLayout>
  );
};

export default Dashboard;
