/**
 * Risk Store - Institutional Safety Monitoring (Zustand)
 * 
 * Manages the state of the risk Sentinels and compliance gates.
 * Provides real-time alerts for stop-loss triggers and risk violations.
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useRiskStore = create((set, get) => ({
  // State
  sentinelActive: true,
  healthStatus: 'HEALTHY', // HEALTHY, WARNING, CRITICAL
  recentViolations: [],
  orderImpact: null,
  lastSentinelCheck: new Date().toISOString(),
  
  // Stats
  triggerCount: 0,
  blockedRemovals: 0,

  // Getters
  isSentinelHealthy: () => get().healthStatus === 'HEALTHY',
  
  // Actions
  recordViolation: (violation) => {
    set((state) => ({
      recentViolations: [violation, ...state.recentViolations].slice(0, 20),
      healthStatus: 'WARNING',
      lastSentinelCheck: new Date().toISOString()
    }));
  },

  incrementTriggers: () => {
    set((state) => ({ triggerCount: state.triggerCount + 1 }));
  },

  setStatus: (status) => {
    set({ healthStatus: status });
  },

  fetchOrderImpact: async (tradeDetails) => {
    try {
      const response = await apiClient.post('/risk/impact', tradeDetails);
      if (response.data.success) {
        set({ orderImpact: response.data.data });
      }
    } catch (error) {
      console.error('Order impact fetch failed:', error);
    }
  },

  reset: () => {
    set({
      sentinelActive: true,
      healthStatus: 'HEALTHY',
      recentViolations: [],
      triggerCount: 0,
      blockedRemovals: 0,
      lastSentinelCheck: new Date().toISOString()
    });
  }
}));

export { useRiskStore };
export default useRiskStore;
