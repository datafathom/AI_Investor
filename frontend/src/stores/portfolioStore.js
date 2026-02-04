/**
 * Portfolio Store - Attribution State Management (Zustand)
 * 
 * This store manages portfolio attribution state for .
 * Provides real-time updates for Brinson-Fachler attribution analysis
 * with support for multiple benchmark comparisons.
 * 
 * Features:
 * - Fetch and cache attribution data
 * - Benchmark switching with <50ms state hydration
 * - Sector-level attribution filtering
 * - Regime shift event tracking
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

/**
 * @typedef {Object} SectorAttribution
 * @property {string} sector - GICS sector name
 * @property {number} allocation_effect - Basis points
 * @property {number} selection_effect - Basis points
 * @property {number} interaction_effect - Basis points
 * @property {number} portfolio_weight - Percentage
 * @property {number} benchmark_weight - Percentage
 * @property {number} portfolio_return - Percentage
 * @property {number} benchmark_return - Percentage
 */

/**
 * @typedef {Object} RegimeShift
 * @property {string} start_date
 * @property {string} end_date
 * @property {number} correlation_before
 * @property {number} correlation_during
 * @property {number} impact_basis_points
 * @property {string} description
 */

/**
 * @typedef {Object} AttributionData
 * @property {string} portfolio_id
 * @property {string} benchmark_id
 * @property {Object} period
 * @property {number} total_active_return
 * @property {number} total_allocation_effect
 * @property {number} total_selection_effect
 * @property {number} total_interaction_effect
 * @property {SectorAttribution[]} sector_attributions
 * @property {RegimeShift[]} regime_shifts
 */

const usePortfolioStore = create((set, get) => ({
  // State
  attribution: null,
  benchmarks: [],
  selectedBenchmark: 'sp500',
  selectedPortfolio: 'default-portfolio',
  isLoading: false,
  error: null,
  lastUpdated: null,

  // Demo Mode State
  is_demo: true,
  demo_balance: 100000.00,
  live_balance: 0.00,
  unrealized_pnl: 0.00,
  equity: 100000.00,
  
  // Computed getters
  getTotalActiveReturn: () => {
    const { attribution } = get();
    return attribution?.total_active_return ?? 0;
  },
  
  getSectorAttributions: () => {
    const { attribution } = get();
    return attribution?.sector_attributions ?? [];
  },
  
  getTopContributors: (n = 3) => {
    const sectors = get().getSectorAttributions();
    return [...sectors]
      .sort((a, b) => {
        const totalA = a.allocation_effect + a.selection_effect + a.interaction_effect;
        const totalB = b.allocation_effect + b.selection_effect + b.interaction_effect;
        return totalB - totalA;
      })
      .slice(0, n);
  },
  
  getTopDetractors: (n = 3) => {
    const sectors = get().getSectorAttributions();
    return [...sectors]
      .sort((a, b) => {
        const totalA = a.allocation_effect + a.selection_effect + a.interaction_effect;
        const totalB = b.allocation_effect + b.selection_effect + b.interaction_effect;
        return totalA - totalB;
      })
      .slice(0, n);
  },
  
  getRegimeShifts: () => {
    const { attribution } = get();
    return attribution?.regime_shifts ?? [];
  },

  // Demo Mode Getters
  getBalance: () => {
      const { is_demo, demo_balance, live_balance } = get();
      return is_demo ? demo_balance : live_balance;
  },

  getEquity: () => {
    return get().equity;
  },

  getUnrealizedPnL: () => {
    return get().unrealized_pnl;
  },
  
  // Actions
  toggleDemoMode: (confirm = false) => {
    const { is_demo } = get();
    if (!is_demo && !confirm) {
      console.error("Live mode requires explicit confirmation.");
      return;
    }
    const next_is_demo = !is_demo;
    set({ 
      is_demo: next_is_demo,
      equity: next_is_demo ? get().demo_balance + get().unrealized_pnl : get().live_balance + get().unrealized_pnl
    });
  },

  updateEquitySnapshot: (balance, pnl) => {
    set({
      demo_balance: get().is_demo ? balance : get().demo_balance,
      live_balance: !get().is_demo ? balance : get().live_balance,
      unrealized_pnl: pnl,
      equity: balance + pnl,
      lastUpdated: new Date().toISOString()
    });
  },

  fetchAttribution: async (portfolioId, benchmarkId, period) => {
    const startTime = performance.now();
    set({ isLoading: true, error: null });
    
    try {
      const response = await apiClient.get(`/attribution/${portfolioId || get().selectedPortfolio}`, {
        params: {
          benchmark: benchmarkId || get().selectedBenchmark,
          start: period?.start || '2025-01-01',
          end: period?.end || '2025-12-31'
        }
      });
      
      if (response.data.success) {
        const hydrationTime = performance.now() - startTime;
        console.log(`Attribution state hydrated in ${hydrationTime.toFixed(2)}ms`);
        
        set({
          attribution: response.data.data,
          isLoading: false,
          lastUpdated: new Date().toISOString()
        });
      } else {
        throw new Error(response.data.error);
      }
    } catch (error) {
      console.error('Attribution fetch error:', error);
      const errorMessage = error.response?.data?.error || error.response?.data?.detail || error.message || 'Failed to fetch attribution data';
      set({ error: errorMessage, isLoading: false });
    }
  },
  
  fetchBenchmarks: async () => {
    try {
      const response = await apiClient.get('/attribution/benchmarks');
      if (response.data.success) {
        set({ benchmarks: response.data.data });
      }
    } catch (error) {
      console.error('Benchmarks fetch error:', error);
    }
  },
  
  setBenchmark: async (benchmarkId) => {
    const startTime = performance.now();
    set({ selectedBenchmark: benchmarkId });
    
    // Trigger re-fetch with new benchmark
    await get().fetchAttribution(null, benchmarkId);
    
    const switchTime = performance.now() - startTime;
    console.log(`Benchmark switch completed in ${switchTime.toFixed(2)}ms`);
  },
  
  setPortfolio: (portfolioId) => {
    set({ selectedPortfolio: portfolioId });
  },
  
  // Clear state
  reset: () => {
    set({
      attribution: null,
      isLoading: false,
      error: null,
      lastUpdated: null
    });
  }
}));

export { usePortfolioStore };
export default usePortfolioStore;
