/**
 * ==============================================================================
 * FILE: frontend2/src/pages/PortfolioOptimizationDashboard.jsx
 * ROLE: Portfolio Optimization & Rebalancing Dashboard
 * PURPOSE: Phase 2 - Portfolio Optimization & Automated Rebalancing
 *          Displays portfolio optimization results and rebalancing recommendations.
 * 
 * INTEGRATION POINTS:
 *    - OptimizationAPI: /api/v1/optimization endpoints
 *    - PortfolioStore: Portfolio data
 * 
 * FEATURES:
 *    - Portfolio optimization (MVO, Risk Parity, etc.)
 *    - Rebalancing recommendations
 *    - Rebalancing history
 *    - Optimization constraints
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import apiClient from '../services/apiClient';
import { analyticsService } from '../services/analyticsService';
import { GlassCard } from '../components/Common';
import './PortfolioOptimizationDashboard.css';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const PortfolioOptimizationDashboard = () => {
  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'results', x: 0, y: 0, w: 12, h: 6 },
      { i: 'recs', x: 0, y: 6, w: 6, h: 8 },
      { i: 'history', x: 6, y: 6, w: 6, h: 8 }
    ]
  };
  const STORAGE_KEY = 'layout_optimization_dashboard';

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
      localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
  };

  const [optimizationResult, setOptimizationResult] = useState(null);
  const [rebalancingRecs, setRebalancingRecs] = useState([]);
  const [rebalancingHistory, setRebalancingHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [portfolioId] = useState('portfolio_1');
  const [optimizationType, setOptimizationType] = useState('mean_variance');

  useEffect(() => {
    loadRebalancingRecs();
    loadRebalancingHistory();
  }, []);

  const loadRebalancingRecs = async () => {
    try {
      const data = await analyticsService.getRebalancingRecommendations(portfolioId);
      setRebalancingRecs(data || []);
    } catch (error) {
      console.error('Error loading rebalancing recommendations:', error);
    }
  };

  const loadRebalancingHistory = async () => {
    try {
      // Note: Rebalancing history endpoint might need adding to analyticsService if used frequently
      // For now, using a generic fetch or adding to service
      const res = await apiClient.get('/optimization/rebalancing-history', {
        params: { portfolio_id: portfolioId }
      });
      const data = res.data;
      setRebalancingHistory(data.history || []);
    } catch (error) {
      console.error('Error loading rebalancing history:', error);
    }
  };

  const runOptimization = async () => {
    setLoading(true);
    try {
      const data = await analyticsService.optimizePortfolio({
        portfolio_id: portfolioId,
        optimization_type: optimizationType,
        objective: 'maximize_sharpe',
        constraints: []
      });
      setOptimizationResult(data);
    } catch (error) {
      console.error('Error running optimization:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-bleed-page portfolio-optimization-dashboard">
      <div className="dashboard-header">
        <h1>Portfolio Optimization & Rebalancing</h1>
        <p className="subtitle">Phase 2: Portfolio Optimization & Automated Rebalancing</p>
      </div>

      <div className="scrollable-content-wrapper">
        <div className="optimization-controls">
          <div className="form-group" style={{ minWidth: '300px' }}>
            <span className="form-label">Optimization Strategy</span>
            <select
              value={optimizationType}
              onChange={(e) => setOptimizationType(e.target.value)}
              className="form-input"
            >
              <option value="mean_variance">Mean-Variance Optimization</option>
              <option value="risk_parity">Risk Parity</option>
              <option value="minimum_variance">Minimum Variance</option>
              <option value="black_litterman">Black-Litterman</option>
            </select>
          </div>
          <button onClick={runOptimization} disabled={loading} className="optimize-button">
            {loading ? 'Optimizing...' : 'Run Optimization'}
          </button>
        </div>

        <ResponsiveGridLayout
          className="layout"
          layouts={layouts}
          onLayoutChange={onLayoutChange}
          breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
          cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
          rowHeight={80}
          isDraggable={true}
          isResizable={true}
          draggableHandle="h2"
          margin={[16, 16]}
        >
          {/* Optimization Results */}
          <div key="results">
            <GlassCard variant="elevated" className="h-full">
               <div className="glass-card-drag-handle">
                  <h2 className="text-xl font-bold mb-4">Optimization Results</h2>
               </div>
               {optimizationResult ? (
                 <div className="optimization-details">
                    <div className="metrics-row flex gap-4 mb-6">
                      <div className="flex-1 p-4 bg-white/5 rounded-xl border border-white/10">
                        <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Expected Return</div>
                        <div className="text-2xl font-black text-white">{(optimizationResult.expected_return * 100).toFixed(2)}%</div>
                      </div>
                      <div className="flex-1 p-4 bg-white/5 rounded-xl border border-white/10">
                        <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Expected Risk</div>
                        <div className="text-2xl font-black text-white">{(optimizationResult.expected_risk * 100).toFixed(2)}%</div>
                      </div>
                      <div className="flex-1 p-4 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
                        <div className="text-[10px] text-emerald-500 uppercase font-bold mb-1">Sharpe Ratio</div>
                        <div className="text-2xl font-black text-emerald-400">{optimizationResult.sharpe_ratio?.toFixed(2)}</div>
                      </div>
                    </div>
                    <div className="allocations space-y-2">
                       <h3 className="text-xs font-black text-zinc-600 uppercase tracking-widest mb-4">Optimal Allocations</h3>
                       <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                         {optimizationResult.allocations?.map((alloc, idx) => (
                           <div key={idx} className="p-3 bg-zinc-900/50 rounded-lg border border-zinc-800 flex justify-between items-center">
                             <span className="text-sm font-bold text-white uppercase italic">{alloc.symbol}</span>
                             <span className="text-sm font-black text-zinc-400">{(alloc.allocation * 100).toFixed(1)}%</span>
                           </div>
                         ))}
                       </div>
                    </div>
                 </div>
               ) : (
                 <div className="flex flex-col items-center justify-center h-[200px] text-zinc-600">
                    <p className="mb-2 italic">Ready for simulation run</p>
                    <button onClick={runOptimization} disabled={loading} className="px-6 py-2 bg-emerald-500/10 border border-emerald-500/20 rounded-full text-emerald-400 font-bold uppercase text-xs hover:bg-emerald-500/20 transition-all">
                       Trigger Solver
                    </button>
                 </div>
               )}
            </GlassCard>
          </div>

          {/* Rebalancing Recommendations */}
          <div key="recs">
            <GlassCard variant="default" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Rebalancing Recommendations</h2>
              </div>
              {rebalancingRecs.length > 0 ? (
                <div className="space-y-3">
                  {rebalancingRecs.map((rec, idx) => (
                    <div key={idx} className="p-4 bg-zinc-900/40 rounded-xl border border-white/5 flex items-center justify-between">
                      <div className="flex items-center gap-4">
                         <div className={`w-2 h-8 rounded-full ${rec.action === 'buy' ? 'bg-emerald-500' : 'bg-rose-500'}`} />
                         <div>
                            <div className="text-lg font-black text-white uppercase italic">{rec.symbol}</div>
                            <div className="text-[10px] text-zinc-500 uppercase font-bold">{rec.action} execution required</div>
                         </div>
                      </div>
                      <div className="text-right">
                         <div className="text-sm font-bold text-white">${rec.trade_amount?.toLocaleString()}</div>
                         <div className="text-[10px] text-zinc-500">Target: {(rec.target_allocation * 100).toFixed(1)}%</div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-zinc-600">No rebalancing recommendations</div>
              )}
            </GlassCard>
          </div>

          {/* Rebalancing History */}
          <div key="history">
            <GlassCard variant="default" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Rebalancing History</h2>
              </div>
              {rebalancingHistory.length > 0 ? (
                <div className="space-y-2">
                  {rebalancingHistory.slice(0, 10).map((entry, idx) => (
                    <div key={idx} className="flex justify-between items-center p-3 bg-zinc-900/20 rounded-lg border border-white/5">
                      <div>
                        <div className="text-sm text-white font-medium">{new Date(entry.rebalancing_date).toLocaleDateString()}</div>
                        <div className="text-[10px] text-zinc-600 uppercase font-black">{entry.trades_executed} trades executed</div>
                      </div>
                      <div className={`px-2 py-1 rounded text-[10px] font-bold uppercase ${entry.status === 'completed' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'}`}>
                        {entry.status}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-zinc-600">No rebalancing history</div>
              )}
            </GlassCard>
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default PortfolioOptimizationDashboard;
