/**
 * ==============================================================================
 * FILE: frontend2/src/pages/OptionsStrategyDashboard.jsx
 * ROLE: Options Strategy Builder & Analyzer Dashboard
 * PURPOSE: Phase 6 - Options Strategy Builder & Analyzer
 *          Displays options strategies, Greeks analysis, and P&L visualization.
 * 
 * INTEGRATION POINTS:
 *    - OptionsAPI: /api/v1/options endpoints
 * 
 * FEATURES:
 *    - Options strategy builder
 *    - Greeks analysis (Delta, Gamma, Theta, Vega, Rho)
 *    - P&L visualization
 *    - Options chain data
 * 
 * FIXES (2026-01-25):
 *    - Fixed 'Controls' panel not being draggable (missing handle)
 *    - Fixed resizing/rearranging issues by standardizing drag handles
 *    - Fixed "cut off at bottom" by increasing scroll container padding
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */


import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import useOptionsStore from '../stores/optionsStore';
import { Responsive, WidthProvider } from 'react-grid-layout';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';
import './OptionsStrategyDashboard.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

const OptionsStrategyDashboard = () => {
  const {
      strategy,
      greeks,
      optionsChain,
      isLoading,
      selectedSymbol,
      strategyType,
      setSelectedSymbol,
      setStrategyType,
      fetchOptionsChain,
      buildStrategy
  } = useOptionsStore();

  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'controls', x: 0, y: 0, w: 12, h: 2 },
      { i: 'details', x: 0, y: 2, w: 6, h: 6 },
      { i: 'greeks', x: 6, y: 2, w: 6, h: 6 },
      { i: 'chain', x: 0, y: 8, w: 12, h: 10 }
    ]
  };
  // Bump version to force reset for users with corrupted/legacy layouts
  const STORAGE_KEY = 'layout_options_strategy_v3';

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

  const resetLayout = () => {
    localStorage.removeItem(STORAGE_KEY);
    setLayouts(DEFAULT_LAYOUT);
    window.location.reload();
  };

  useEffect(() => {
    fetchOptionsChain(selectedSymbol);
  }, [fetchOptionsChain, selectedSymbol]);

  const handleBuildStrategy = async () => {
    await buildStrategy(selectedSymbol, strategyType, []);
  };

  return (
    <div className="full-bleed-page options-strategy-dashboard">
      <div className="dashboard-header">
        <div className="header-titles">
          <h1>Options Strategy Builder</h1>
          <p className="subtitle">Phase 6: Options Strategy Builder & Analyzer</p>
        </div>
        <div className="header-actions">
          <button onClick={resetLayout} className="btn-utility ripple">
            Reset Layout
          </button>
        </div>
      </div>

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
          {/* Controls */}
          <div key="controls" className="overflow-hidden rounded-xl">
             <div className="glass-panel glass-premium h-full flex flex-col">
                <div className="glass-panel-header p-4 border-b border-white/10 flex justify-between items-center cursor-move">
                   <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Strategy Controls</h3>
                   <div className="flex items-center gap-2">
                       <span className="w-2 h-2 rounded-full bg-cyan-500 animate-pulse"></span>
                       <span className="text-cyan-500 text-[10px] font-mono uppercase">Interactive</span>
                   </div>
                </div>
                <div className="flex-1 p-6 overflow-y-auto">
                    <div className="flex flex-wrap gap-6 items-end">
                        <div className="flex-1 min-w-[180px]">
                            <label className="form-label">Symbol</label>
                            <input
                                type="text"
                                value={selectedSymbol}
                                onChange={(e) => setSelectedSymbol(e.target.value.toUpperCase())}
                                placeholder="e.g. TSLA"
                                className="form-input w-full"
                            />
                        </div>
                        <div className="flex-1 min-w-[180px]">
                            <label className="form-label">Strategy Type</label>
                            <select
                                value={strategyType}
                                onChange={(e) => setStrategyType(e.target.value)}
                                className="form-input w-full"
                            >
                                <option value="covered_call">Covered Call</option>
                                <option value="protective_put">Protective Put</option>
                                <option value="straddle">Straddle</option>
                                <option value="strangle">Strangle</option>
                                <option value="iron_condor">Iron Condor</option>
                                <option value="butterfly">Butterfly</option>
                            </select>
                        </div>
                        <button onClick={handleBuildStrategy} disabled={isLoading} className="p-2 px-6 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-lg transition-all active:scale-95 disabled:opacity-50">
                            {isLoading ? 'Building...' : 'Build Strategy'}
                        </button>
                    </div>
                </div>
             </div>
          </div>

          {/* Strategy Details */}
          <div key="details" className="overflow-hidden rounded-xl">
             <div className="glass-panel glass-premium h-full flex flex-col">
                <div className="glass-panel-header p-4 border-b border-white/10 flex justify-between items-center cursor-move">
                   <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Strategy Details</h3>
                </div>
                <div className="flex-1 p-6 overflow-y-auto">
                    {strategy ? (
                        <div className="space-y-4">
                            {[
                                { label: 'Type', val: strategy.strategy_type },
                                { label: 'Net Cost', val: `$${strategy.net_cost?.toFixed(2)}` },
                                { label: 'Max Profit', val: `$${strategy.max_profit?.toFixed(2)}`, color: 'text-green-400' },
                                { label: 'Max Loss', val: `$${strategy.max_loss?.toFixed(2)}`, color: 'text-red-400' },
                                { label: 'Breakeven', val: `$${strategy.breakeven?.toFixed(2)}` }
                            ].map((item, idx) => (
                                <div key={idx} className="flex justify-between items-center py-2 border-b border-white/5">
                                    <span className="text-sm text-slate-500">{item.label}</span>
                                    <span className={`text-sm font-bold ${item.color || 'text-white'}`}>{item.val}</span>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="h-full flex items-center justify-center text-slate-600 italic text-sm">
                            Build a strategy to see details
                        </div>
                    )}
                </div>
             </div>
          </div>

          {/* Greeks Analysis */}
          <div key="greeks" className="overflow-hidden rounded-xl">
            <div className="glass-panel glass-premium h-full flex flex-col">
                <div className="glass-panel-header p-4 border-b border-white/10 flex justify-between items-center cursor-move">
                   <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Greeks Analysis</h3>
                </div>
                <div className="flex-1 p-6 overflow-y-auto">
                    {greeks ? (
                        <div className="grid grid-cols-2 gap-4">
                            {[
                                { label: 'Delta', val: greeks.delta?.toFixed(4) },
                                { label: 'Gamma', val: greeks.gamma?.toFixed(4) },
                                { label: 'Theta', val: greeks.theta?.toFixed(4), color: 'text-red-400' },
                                { label: 'Vega', val: greeks.vega?.toFixed(4) },
                                { label: 'Rho', val: greeks.rho?.toFixed(4) }
                            ].map((greek, idx) => (
                                <div key={idx} className="p-4 bg-white/5 rounded-lg border border-white/5 text-center">
                                    <div className="text-[10px] text-slate-500 uppercase font-bold">{greek.label}</div>
                                    <div className={`text-lg font-black ${greek.color || 'text-cyan-400'}`}>{greek.val}</div>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="h-full flex items-center justify-center text-slate-600 italic text-sm">
                            Analyze a strategy to see Greeks
                        </div>
                    )}
                </div>
            </div>
          </div>

          {/* Options Chain */}
          <div key="chain" className="overflow-hidden rounded-xl">
             <div className="glass-panel glass-premium h-full flex flex-col">
                <div className="glass-panel-header p-4 border-b border-white/10 flex justify-between items-center cursor-move">
                   <h3 className="text-xs font-bold text-slate-400 uppercase tracking-widest">Options Chain - {selectedSymbol}</h3>
                </div>
                <div className="flex-1 overflow-y-auto">
                    {optionsChain.length > 0 ? (
                        <table className="w-full text-left border-collapse">
                            <thead className="sticky top-0 bg-slate-900/90 backdrop-blur-sm shadow-xl z-10">
                                <tr>
                                    <th className="p-4 text-[10px] font-bold text-cyan-500 uppercase tracking-widest">Strike</th>
                                    <th className="p-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Call Bid</th>
                                    <th className="p-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Call Ask</th>
                                    <th className="p-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Put Bid</th>
                                    <th className="p-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Put Ask</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {optionsChain.slice(0, 50).map((option, idx) => (
                                    <tr key={idx} className="hover:bg-cyan-500/5 transition-colors">
                                        <td className="p-4 text-cyan-400 font-mono font-bold">${option.strike}</td>
                                        <td className="p-4 text-slate-300 font-mono text-sm">${option.call_bid?.toFixed(2)}</td>
                                        <td className="p-4 text-slate-300 font-mono text-sm">${option.call_ask?.toFixed(2)}</td>
                                        <td className="p-4 text-slate-300 font-mono text-sm">${option.put_bid?.toFixed(2)}</td>
                                        <td className="p-4 text-slate-300 font-mono text-sm">${option.put_ask?.toFixed(2)}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    ) : (
                        <div className="h-full flex items-center justify-center text-slate-600 italic text-sm">
                            No options data available
                        </div>
                    )}
                </div>
             </div>
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer - Increased to prevent cutoff */}
        <div className="scroll-buffer-200" />
      </div>
    </div>
  );
};

export default OptionsStrategyDashboard;
