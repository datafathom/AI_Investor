/**
 * Portfolio Store - Attribution State Management (Zustand)
 * 
 * This store manages portfolio attribution state for Phase 49.
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

const API_BASE = 'http://localhost:5050/api/v1/attribution';

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
  
  // Actions
  fetchAttribution: async (portfolioId, benchmarkId, period) => {
    const startTime = performance.now();
    set({ isLoading: true, error: null });
    
    try {
      const params = new URLSearchParams({
        benchmark: benchmarkId || get().selectedBenchmark,
        start: period?.start || '2025-01-01',
        end: period?.end || '2025-12-31'
      });
      
      const response = await fetch(
        `${API_BASE}/${portfolioId || get().selectedPortfolio}?${params}`
      );
      
      if (!response.ok) {
        throw new Error(`Failed to fetch attribution: ${response.status}`);
      }
      
      const result = await response.json();
      
      if (result.success) {
        const hydrationTime = performance.now() - startTime;
        console.log(`Attribution state hydrated in ${hydrationTime.toFixed(2)}ms`);
        
        set({
          attribution: result.data,
          isLoading: false,
          lastUpdated: new Date().toISOString()
        });
      } else {
        throw new Error(result.error);
      }
    } catch (error) {
      console.error('Attribution fetch error:', error);
      set({ error: error.message, isLoading: false });
    }
  },
  
  fetchBenchmarks: async () => {
    try {
      const response = await fetch(`${API_BASE}/benchmarks`);
      const result = await response.json();
      
      if (result.success) {
        set({ benchmarks: result.data });
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
