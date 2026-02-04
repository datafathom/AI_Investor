/**
 * ==============================================================================
 * FILE: frontend2/src/pages/TaxOptimizationDashboard.jsx
 * ROLE: Tax Optimization Dashboard
 * PURPOSE:  - Tax-Loss Harvesting & Optimization
 *          Displays tax-loss harvesting opportunities and optimization strategies.
 * 
 * INTEGRATION POINTS:
 *    - TaxOptimizationAPI: /api/v1/tax-optimization endpoints
 * 
 * FEATURES:
 *    - Tax-loss harvesting candidates
 *    - Wash-sale detection
 *    - Tax projections
 *    - Lot selection optimization
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';
import { analyticsService } from '../services/analyticsService';
import { GlassCard } from '../components/Common';
import './TaxOptimizationDashboard.css';

import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const TaxOptimizationDashboard = () => {
  const DEFAULT_LAYOUT = {
    lg: [
      { i: 'projection', x: 0, y: 0, w: 12, h: 4 },
      { i: 'candidates', x: 0, y: 4, w: 12, h: 8 }
    ]
  };
  const STORAGE_KEY = 'layout_tax_optimization_dashboard';

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

  const [harvestCandidates, setHarvestCandidates] = useState([]);
  const [taxProjection, setTaxProjection] = useState(null);
  const [loading, setLoading] = useState(false);
  const [portfolioId] = useState('portfolio_1');
  const [selectedYear] = useState(new Date().getFullYear());

  useEffect(() => {
    loadHarvestCandidates();
    loadTaxProjection();
  }, []);

  const loadHarvestCandidates = async () => {
    try {
      const data = await analyticsService.getTaxHarvestCandidates(portfolioId);
      setHarvestCandidates(data || []);
    } catch (error) {
      console.error('Error loading harvest candidates:', error);
    }
  };

  const loadTaxProjection = async () => {
    try {
      const data = await analyticsService.getTaxProjection(portfolioId, selectedYear);
      setTaxProjection(data);
    } catch (error) {
      console.error('Error loading tax projection:', error);
    }
  };

  const checkWashSale = async (symbol) => {
    try {
      const result = await analyticsService.checkWashSale(portfolioId, symbol);
      alert(`Wash Sale Check: ${result?.is_wash_sale ? 'WASH SALE DETECTED' : 'No wash sale'}`);
    } catch (error) {
      console.error('Error checking wash sale:', error);
    }
  };

  return (
    <div className="full-bleed-page tax-optimization-dashboard">
      <div className="dashboard-header">
        <h1>Tax Optimization & Harvesting</h1>
        <p className="subtitle">: Tax-Loss Harvesting & Optimization</p>
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
          draggableHandle="h2"
          margin={[16, 16]}
        >
          {/* Tax Projection */}
          <div key="projection">
            <GlassCard variant="elevated" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Tax Projection ({selectedYear})</h2>
              </div>
              {taxProjection ? (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                   <div className="p-4 bg-white/5 rounded-2xl">
                      <div className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Cap. Gains</div>
                      <div className="text-2xl font-black text-white">${(taxProjection?.estimated_capital_gains || 0).toLocaleString()}</div>
                   </div>
                   <div className="p-4 bg-rose-500/5 rounded-2xl border border-rose-500/10">
                      <div className="text-[10px] text-rose-500 uppercase font-bold mb-1">Liability</div>
                      <div className="text-2xl font-black text-rose-400">${(taxProjection?.estimated_tax_liability || 0).toLocaleString()}</div>
                   </div>
                   <div className="p-4 bg-emerald-500/5 rounded-2xl border border-emerald-500/10">
                      <div className="text-[10px] text-emerald-500 uppercase font-bold mb-1">Realized Loss</div>
                      <div className="text-2xl font-black text-emerald-400">${Math.abs(taxProjection?.realized_losses || 0).toLocaleString()}</div>
                   </div>
                   <div className="p-4 bg-cyan-500/10 rounded-2xl border border-cyan-500/20">
                      <div className="text-[10px] text-cyan-500 uppercase font-bold mb-1">Savings Potential</div>
                      <div className="text-2xl font-black text-cyan-400">${(taxProjection?.tax_savings_potential || 0).toLocaleString()}</div>
                   </div>
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-zinc-600">No tax projection data</div>
              )}
            </GlassCard>
          </div>

          <div key="candidates">
            <GlassCard variant="default" className="h-full">
              <div className="glass-card-drag-handle">
                <h2 className="text-xl font-bold mb-4">Harvesting Candidates</h2>
              </div>
              {harvestCandidates.length > 0 ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {harvestCandidates.map((candidate, idx) => (
                    <div key={idx} className="p-6 bg-zinc-900/40 rounded-2xl border border-white/5 hover:border-emerald-500/30 transition-all group">
                      <div className="flex justify-between items-start mb-6">
                         <div>
                            <div className="text-2xl font-black text-white italic uppercase">{candidate.symbol}</div>
                            <div className="text-[10px] text-zinc-500 uppercase font-bold tracking-widest">Candidate #{idx + 1}</div>
                         </div>
                         <div className="px-3 py-1 bg-emerald-500/10 rounded-full text-emerald-400 text-xs font-bold">
                            Loss: ${Math.abs(candidate.unrealized_loss).toLocaleString()}
                         </div>
                      </div>
                      <div className="space-y-3 mb-6">
                         <div className="flex justify-between text-sm">
                            <span className="text-zinc-500">Net Tax Benefit</span>
                            <span className="text-emerald-400 font-bold">${candidate.tax_benefit?.toLocaleString()}</span>
                         </div>
                         <div className="flex justify-between text-sm">
                            <span className="text-zinc-500">Replacement</span>
                            <span className="text-white font-medium italic">{candidate.replacement_suggestion || 'N/A'}</span>
                         </div>
                      </div>
                      <button onClick={() => checkWashSale(candidate.symbol)} className="w-full py-2 bg-white/5 border border-white/10 rounded-lg text-zinc-400 font-bold text-[10px] uppercase hover:bg-white/10 hover:text-white transition-all">
                         Validate Wash Sale Risk
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-zinc-600 italic">No candidates at this time</div>
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

export default TaxOptimizationDashboard;
