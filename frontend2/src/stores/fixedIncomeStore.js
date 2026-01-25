/**
 * Fixed Income Store - Zustand State Management
 * 
 * Phase 50: Manages bond ladder, yield curve, and rate shock state.
 * Provides real-time updates for fixed income analytics.
 */

import { create } from 'zustand';

const API_BASE = 'http://localhost:5050/api/v1/fixed-income';

const useFixedIncomeStore = create((set, get) => ({
  // State
  yieldCurve: null,
  historicalCurves: [],
  bondLadder: [],
  liquidityGaps: [],
  rateShockResult: null,
  weightedAverageLife: 0,
  isLoading: false,
  error: null,
  
  // Actions
  fetchYieldCurve: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/yield-curve`);
      const result = await response.json();
      
      if (result.success) {
        set({ yieldCurve: result.data, isLoading: false });
      }
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
  
  fetchHistoricalCurves: async (months = 12) => {
    try {
      const response = await fetch(`${API_BASE}/yield-curve/history?months=${months}`);
      const result = await response.json();
      
      if (result.success) {
        set({ historicalCurves: result.data });
      }
    } catch (error) {
      console.error('Historical curves fetch error:', error);
    }
  },
  
  simulateRateShock: async (portfolioId, basisPoints) => {
    set({ isLoading: true });
    try {
      const response = await fetch(`${API_BASE}/rate-shock`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ portfolio_id: portfolioId, basis_points: basisPoints })
      });
      const result = await response.json();
      
      if (result.success) {
        set({ rateShockResult: result.data, isLoading: false });
      }
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
  
  fetchLiquidityGaps: async (portfolioId) => {
    try {
      const response = await fetch(`${API_BASE}/gaps/${portfolioId}`);
      const result = await response.json();
      
      if (result.success) {
        set({ liquidityGaps: result.data });
      }
    } catch (error) {
      console.error('Gaps fetch error:', error);
    }
  },
  
  addBond: (bond) => {
    set(state => ({
      bondLadder: [...state.bondLadder, { id: Date.now(), ...bond }]
    }));
  },
  
  removeBond: (bondId) => {
    set(state => ({
      bondLadder: state.bondLadder.filter(b => b.id !== bondId)
    }));
  },
  
  updateBond: (bondId, updates) => {
    set(state => ({
      bondLadder: state.bondLadder.map(b => 
        b.id === bondId ? { ...b, ...updates } : b
      )
    }));
  },
  
  calculateWAL: async () => {
    const { bondLadder } = get();
    try {
      const response = await fetch(`${API_BASE}/wal`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          bonds: bondLadder.map(b => ({
            par_value: b.parValue,
            maturity_years: b.maturityYears
          }))
        })
      });
      const result = await response.json();
      
      if (result.success) {
        set({ weightedAverageLife: result.data.weighted_average_life });
      }
    } catch (error) {
      console.error('WAL calculation error:', error);
    }
  },
  
  reset: () => {
    set({
      yieldCurve: null,
      historicalCurves: [],
      bondLadder: [],
      liquidityGaps: [],
      rateShockResult: null,
      weightedAverageLife: 0,
      isLoading: false,
      error: null
    });
  }
}));

export { useFixedIncomeStore };
export default useFixedIncomeStore;
