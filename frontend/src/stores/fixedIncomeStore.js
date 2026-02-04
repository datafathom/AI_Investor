/**
 * Fixed Income Store - Zustand State Management
 * 
 * Phase 50: Manages bond ladder, yield curve, and rate shock state.
 * Provides real-time updates for fixed income analytics.
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

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
      const response = await apiClient.get('/fixed-income/yield-curve');
      if (response.data.success) {
        set({ yieldCurve: response.data.data, isLoading: false });
      }
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
  
  fetchHistoricalCurves: async (months = 12) => {
    try {
      const response = await apiClient.get('/fixed-income/yield-curve/history', { params: { months } });
      if (response.data.success) {
        set({ historicalCurves: response.data.data });
      }
    } catch (error) {
      console.error('Historical curves fetch error:', error);
    }
  },
  
  simulateRateShock: async (portfolioId, basisPoints) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.post('/fixed-income/rate-shock', { portfolio_id: portfolioId, basis_points: basisPoints });
      if (response.data.success) {
        set({ rateShockResult: response.data.data, isLoading: false });
      }
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },
  
  fetchLiquidityGaps: async (portfolioId) => {
    try {
      const response = await apiClient.get(`/fixed-income/gaps/${portfolioId}`);
      if (response.data.success) {
        set({ liquidityGaps: response.data.data });
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
      const response = await apiClient.post('/fixed-income/wal', { 
        bonds: bondLadder.map(b => ({
          par_value: b.parValue,
          maturity_years: b.maturityYears
        }))
      });
      
      if (response.data.success) {
        set({ weightedAverageLife: response.data.data.weighted_average_life });
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
