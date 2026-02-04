/**
 * ==============================================================================
 * FILE: frontend2/src/pages/AdvancedPortfolioAnalytics.jsx
 * ROLE: Advanced Portfolio Analytics Dashboard
 * PURPOSE: Phase 1 - Portfolio Performance Attribution & Risk Decomposition
 *          Displays comprehensive portfolio analytics with performance attribution,
 *          risk decomposition, and holding contributions.
 * 
 * INTEGRATION POINTS:
 *    - AnalyticsAPI: /api/v1/analytics endpoints
 *    - PortfolioStore: Portfolio data
 *    - AnalyticsStore: Analytics state
 * 
 * FEATURES:
 *    - Performance attribution breakdown
 *    - Risk decomposition by factors
 *    - Holding contribution analysis
 *    - Factor exposure visualization
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { analyticsService } from '../services/analyticsService';
import { GlassCard } from '../components/Common';
import PageHeader from '../components/Navigation/PageHeader';
import './AdvancedPortfolioAnalytics.css';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const AdvancedPortfolioAnalytics = () => {
  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'attribution', x: 0, y: 0, w: 6, h: 8 },
      { i: 'risk', x: 6, y: 0, w: 6, h: 8 },
      { i: 'contributions', x: 0, y: 8, w: 12, h: 6 }
    ]
  };
  const STORAGE_KEY = 'layout_advanced_analytics';

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

  const [attribution, setAttribution] = useState(null);
  const [riskDecomp, setRiskDecomp] = useState(null);
  const [loading, setLoading] = useState(false);
  const [portfolioId] = useState('portfolio_1');

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    setLoading(true);
    try {
      const [attr, risk] = await Promise.all([
        analyticsService.getPerformanceAttribution(portfolioId),
        analyticsService.getRiskDecomposition(portfolioId)
      ]);
      setAttribution(attr);
      setRiskDecomp(risk);
    } catch (error) {
      console.error('Error loading analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="advanced-portfolio-analytics">
        <div className="loading">Loading analytics...</div>
      </div>
    );
  }

  return (
    <div className="full-bleed-page advanced-portfolio-analytics">
      <div className="analytics-header">
        <h1>Advanced Portfolio Analytics</h1>
        <p className="subtitle">Phase 1: Performance Attribution & Risk Decomposition</p>
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
          draggableHandle=".analytics-card h2"
          margin={[16, 16]}
        >
          {/* Performance Attribution */}
          <div key="attribution">
            <GlassCard variant="elevated" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Performance Attribution</h2>
              </div>
              {attribution ? (
                <div className="attribution-details">
                  <div className="metrics-row flex gap-4 mb-6">
                    <div className="flex-1 p-4 bg-white/5 rounded-xl border border-white/10">
                      <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Total Return</div>
                      <div className="text-2xl font-black text-white">{(attribution.total_return || 0).toFixed(2)}%</div>
                    </div>
                    <div className="flex-1 p-4 bg-white/5 rounded-xl border border-white/10">
                      <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Benchmark</div>
                      <div className="text-2xl font-black text-zinc-400">{(attribution.benchmark_return || 0).toFixed(2)}%</div>
                    </div>
                    <div className="flex-1 p-4 bg-cyan-500/10 rounded-xl border border-cyan-500/20">
                      <div className="text-[10px] text-cyan-500 uppercase font-bold mb-1">Alpha</div>
                      <div className="text-2xl font-black text-cyan-400">{(attribution.active_return || 0).toFixed(2)}%</div>
                    </div>
                  </div>
                  <div className="breakdown space-y-2">
                    <h3 className="text-xs font-black text-zinc-600 uppercase tracking-widest mb-4">Factor Contributions</h3>
                    {attribution.breakdown?.map((item, idx) => (
                      <div key={idx} className="flex justify-between items-center p-3 bg-zinc-900/50 rounded-lg border border-zinc-800">
                        <span className="text-zinc-400 font-medium">{item.factor}</span>
                        <span className={`font-bold ${(item.contribution || 0) >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                          {(item.contribution || 0) >= 0 ? '+' : ''}{(item.contribution || 0).toFixed(2)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-zinc-600">No attribution data available</div>
              )}
            </GlassCard>
          </div>

          {/* Risk Decomposition */}
          <div key="risk">
            <GlassCard variant="elevated" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Risk Decomposition</h2>
              </div>
              {riskDecomp ? (
                <div className="risk-details">
                  <div className="metrics-row flex gap-4 mb-6">
                     <div className="flex-1 p-4 bg-white/5 rounded-xl">
                        <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Total Vol</div>
                        <div className="text-2xl font-black text-white">{(riskDecomp.total_risk || 0).toFixed(2)}%</div>
                     </div>
                     <div className="flex-1 p-4 bg-white/5 rounded-xl">
                        <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Beta</div>
                        <div className="text-2xl font-black text-zinc-400">1.04</div>
                     </div>
                  </div>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-zinc-500">Systematic Risk</span>
                      <span className="text-white font-bold">{(riskDecomp.systematic_risk || 0).toFixed(2)}%</span>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-zinc-500">Idiosyncratic Risk</span>
                      <span className="text-white font-bold">{(riskDecomp.idiosyncratic_risk || 0).toFixed(2)}%</span>
                    </div>
                   
                    <div className="breakdown pt-4 border-t border-white/5">
                      <h3 className="text-xs font-black text-zinc-600 uppercase tracking-widest mb-4">Factor Exposures</h3>
                      <div className="grid grid-cols-2 gap-3">
                        {riskDecomp.factor_exposures?.map((factor, idx) => (
                           <div key={idx} className="p-3 bg-zinc-900/50 rounded-lg border border-zinc-800 flex justify-between items-center">
                             <span className="text-xs text-zinc-400">{factor.factor}</span>
                             <span className="text-xs font-bold text-white">{(factor.exposure || 0).toFixed(2)}</span>
                           </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-zinc-600">No risk data available</div>
              )}
            </GlassCard>
          </div>

          {/* Holding Contributions */}
          <div key="contributions">
            <GlassCard variant="default" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Holding Contributions</h2>
              </div>
              {attribution?.holding_contributions ? (
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                  {attribution.holding_contributions.slice(0, 10).map((holding, idx) => (
                     <div key={idx} className="p-4 bg-zinc-900/50 rounded-2xl border border-zinc-800 hover:border-cyan-500/30 transition-all group">
                       <div className="text-lg font-black text-white mb-1 group-hover:text-cyan-400 transition-colors uppercase italic">{holding.symbol}</div>
                       <div className={`text-sm font-bold ${(holding.contribution || 0) >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                         {(holding.contribution || 0) >= 0 ? '+' : ''}{(holding.contribution || 0).toFixed(2)}%
                       </div>
                     </div>
                  ))}
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-zinc-600">No contribution data available</div>
              )}
            </GlassCard>
          </div>
        </ResponsiveGridLayout>
        
        {/* Bottom Buffer for scrolling within the grid wrapper */}
        <div className="scroll-buffer-100" />
      </div>
    </div>
  );
};

export default AdvancedPortfolioAnalytics;
