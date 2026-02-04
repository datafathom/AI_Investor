/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AdvancedRiskDashboard.jsx
 * ROLE: Advanced Risk Management Dashboard
 * PURPOSE:  - Advanced Risk Management & Stress Testing
 *          Displays risk metrics, stress test results, and Monte Carlo simulations.
 * 
 * INTEGRATION POINTS:
 *    - AdvancedRiskAPI: /api/v1/advanced-risk endpoints
 * 
 * FEATURES:
 *    - VaR and CVaR calculations
 *    - Stress testing scenarios
 *    - Monte Carlo simulations
 *    - Risk-adjusted ratios
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { analyticsService } from '../services/analyticsService';
import { workerManager } from '../services/workerManager';
import { StorageService } from '../utils/storageService';
import { GlassCard } from '../components/Common';
import './AdvancedRiskDashboard.css';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const AdvancedRiskDashboard = () => {
  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'metrics', x: 0, y: 0, w: 12, h: 10 },
      { i: 'stress', x: 0, y: 10, w: 6, h: 14 },
      { i: 'monte_carlo', x: 6, y: 10, w: 6, h: 14 }
    ]
  };
  const STORAGE_KEY = 'layout_advanced_risk_dashboard_v2';

  const [layouts, setLayouts] = useState(DEFAULT_LAYOUT);

  // Async load layout
  useEffect(() => {
      const loadLayout = async () => {
          const saved = await StorageService.get(STORAGE_KEY);
          if (saved) setLayouts(saved);
      };
      loadLayout();
  }, []);

  const onLayoutChange = (currentLayout, allLayouts) => {
      setLayouts(allLayouts);
      StorageService.set(STORAGE_KEY, allLayouts);
  };

  const [riskMetrics, setRiskMetrics] = useState(null);
  const [stressTestResult, setStressTestResult] = useState(null);
  const [monteCarloResult, setMonteCarloResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [portfolioId] = useState('portfolio_1');
  const [selectedScenario, setSelectedScenario] = useState('market_crash_2008');

  useEffect(() => {
    loadRiskMetrics();
  }, []);

  const loadRiskMetrics = async () => {
    setLoading(true);
    try {
      const data = await analyticsService.getRiskMetrics(portfolioId);
      setRiskMetrics(data);
    } catch (error) {
      console.error('Error loading risk metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  const runStressTest = async () => {
    setLoading(true);
    try {
      const data = await analyticsService.runStressTest(portfolioId, selectedScenario);
      setStressTestResult(data);
    } catch (error) {
      console.error('Error running stress test:', error);
    } finally {
      setLoading(false);
    }
  };

  const runMonteCarlo = async () => {
    setLoading(true);
    try {
      // Use Client-Side Worker for immediate interaction
      const data = await workerManager.runMonteCarlo({
        initialValue: 1000000, // Example Portfolio Value
        meanReturn: 0.08,      // Example 8% Annual Return
        volatility: 0.15,      // Example 15% Volatility
        timeHorizon: 30,       // 30 Days
        iterations: 10000      // 10k simulations
      });
      
      // Map worker result to state structure if needed (worker returns snake_case mostly, matching prop names)
      setMonteCarloResult(data);
    } catch (error) {
      console.error('Error running Monte Carlo:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page advanced-risk-dashboard">
      <div className="dashboard-header">
        <h1>Advanced Risk Management</h1>
        <p className="subtitle">: Advanced Risk Management & Stress Testing</p>
      </div>

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
          draggableHandle="h2"
          margin={[10, 10]}
        >
          {/* ... (widgets remain the same) ... */}
          <div key="metrics">
            <GlassCard variant="elevated" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Risk Metrics</h2>
              </div>
              {riskMetrics ? (
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  <div className="p-4 bg-rose-500/5 rounded-2xl border border-rose-500/10">
                    <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Value at Risk (VaR)</div>
                    <div className="text-2xl font-black text-rose-400">${Math.abs(riskMetrics.var?.toFixed(2))}</div>
                    <div className="text-[10px] text-zinc-600 font-bold mt-1">95% CONFIDENCE</div>
                  </div>
                  <div className="p-4 bg-orange-500/5 rounded-2xl border border-orange-500/10">
                    <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Expected Tail Loss</div>
                    <div className="text-2xl font-black text-orange-400">${Math.abs(riskMetrics.cvar?.toFixed(2))}</div>
                  </div>
                  <div className="p-4 bg-rose-500/5 rounded-2xl border border-rose-500/10">
                    <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Max Drawdown</div>
                    <div className="text-2xl font-black text-rose-400">{(riskMetrics.max_drawdown * 100).toFixed(2)}%</div>
                  </div>
                  <div className="p-4 bg-emerald-500/5 rounded-2xl border border-emerald-500/10">
                    <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Sharpe Ratio</div>
                    <div className="text-2xl font-black text-emerald-400">{riskMetrics.sharpe_ratio?.toFixed(2)}</div>
                  </div>
                  <div className="p-4 bg-emerald-500/5 rounded-2xl border border-emerald-500/10">
                    <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Sortino Ratio</div>
                    <div className="text-2xl font-black text-emerald-400">{riskMetrics.sortino_ratio?.toFixed(2)}</div>
                  </div>
                  <div className="p-4 bg-cyan-500/5 rounded-2xl border border-cyan-500/10">
                    <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Vol / Drawdown</div>
                    <div className="text-2xl font-black text-cyan-400">{riskMetrics.calmar_ratio?.toFixed(2)}</div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-zinc-600">No risk metrics available</div>
              )}
            </GlassCard>
          </div>

          <div key="stress">
            <GlassCard variant="default" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Stress Testing</h2>
              </div>
              <div className="flex gap-2 mb-6">
                <select
                  value={selectedScenario}
                  onChange={(e) => setSelectedScenario(e.target.value)}
                  className="flex-1 bg-zinc-900 border border-zinc-800 rounded-lg px-4 py-2 text-sm text-white focus:outline-none focus:border-cyan-500/50"
                >
                  <option value="market_crash_2008">2008 Financial Crisis</option>
                  <option value="covid_2020">2020 COVID-19 Crash</option>
                  <option value="inflation_2022">2022 Inflation Spike</option>
                  <option value="sector_shock_tech">Tech Sector Shock</option>
                </select>
                <button onClick={runStressTest} disabled={loading} className="px-4 py-2 bg-cyan-500/10 border border-cyan-500/20 rounded-lg text-cyan-400 font-bold text-xs hover:bg-cyan-500/20 transition-all">
                  RUN
                </button>
              </div>
              {stressTestResult ? (
                <div className="space-y-4">
                  <div className="p-4 bg-zinc-900/50 rounded-xl border border-white/5 flex justify-between items-center">
                    <span className="text-zinc-500 text-sm">Portfolio Impact</span>
                    <span className={`text-xl font-black ${stressTestResult.portfolio_impact < 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                      {(stressTestResult.portfolio_impact * 100).toFixed(2)}%
                    </span>
                  </div>
                  <div className="scenario-details space-y-2">
                    {stressTestResult.scenario_impacts?.slice(0, 5).map((impact, idx) => (
                      <div key={idx} className="flex justify-between text-xs">
                        <span className="text-zinc-600 font-bold uppercase italic">{impact.symbol}</span>
                        <span className={impact.impact < 0 ? 'text-rose-500' : 'text-emerald-500'}>{(impact.impact * 100).toFixed(2)}%</span>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-24 text-zinc-700 italic text-sm">Select scenario to simulate impact</div>
              )}
            </GlassCard>
          </div>

          <div key="monte_carlo">
            <GlassCard variant="default" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Monte Carlo Simulation</h2>
              </div>
              <div className="mb-6">
                <button onClick={runMonteCarlo} disabled={loading} className="w-full py-3 bg-zinc-900 border border-zinc-800 rounded-xl text-zinc-400 font-bold text-xs hover:border-cyan-500/50 hover:text-white transition-all uppercase tracking-widest">
                  {loading ? 'CALCULATING...' : 'GENERATE 10K PATHS'}
                </button>
              </div>
              {monteCarloResult ? (
                <div className="space-y-4">
                  <div className="grid grid-cols-2 gap-4">
                    <div className="p-3 bg-white/5 rounded-lg">
                      <div className="text-[10px] text-zinc-600 uppercase font-black">Exp. Value</div>
                      <div className="text-lg font-bold text-white">${monteCarloResult.expected_value?.toLocaleString()}</div>
                    </div>
                    <div className="p-3 bg-rose-500/5 rounded-lg border border-rose-500/10">
                      <div className="text-[10px] text-rose-500 uppercase font-black">Prob. Loss</div>
                      <div className="text-lg font-bold text-rose-400">{(monteCarloResult.probability_of_loss * 100).toFixed(1)}%</div>
                    </div>
                  </div>
                  <div className="pt-4 border-t border-white/5">
                    <div className="flex justify-between text-xs mb-2">
                       <span className="text-zinc-500">5th Percentile (Tail)</span>
                       <span className="text-rose-400 font-bold">${monteCarloResult.percentile_5?.toLocaleString()}</span>
                    </div>
                    <div className="flex justify-between text-xs">
                       <span className="text-zinc-500">95th Percentile (Peak)</span>
                       <span className="text-emerald-400 font-bold">${monteCarloResult.percentile_95?.toLocaleString()}</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-24 text-zinc-700 italic text-sm">Initiate paths for probability analysis</div>
              )}
            </GlassCard>
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};;

export default AdvancedRiskDashboard;
