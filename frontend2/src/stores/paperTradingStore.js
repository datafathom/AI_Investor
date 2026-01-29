import { create } from 'zustand';

const API_BASE = '/api/v1/paper-trading';

const usePaperTradingStore = create((set, get) => ({
  // State
  virtualPortfolio: null,
  paperTrades: [],
  backtestResults: null,
  isLoading: false,
  error: null,

  // Actions
  fetchVirtualPortfolio: async (userId) => {
    set({ isLoading: true });
    try {
      const response = await fetch(`${API_BASE}/portfolio?user_id=${userId}`);
      const result = await response.json();
      set({ virtualPortfolio: result.data || null, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchPaperTrades: async (userId) => {
    set({ isLoading: true });
    try {
      const response = await fetch(`${API_BASE}/trades?user_id=${userId}&limit=20`);
      const result = await response.json();
      set({ paperTrades: result.data || [], isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  placePaperTrade: async (userId, tradeData) => {
    set({ isLoading: true });
    try {
      const response = await fetch(`${API_BASE}/trade`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, ...tradeData })
      });
      
      if (!response.ok) throw new Error('Trade failed');
      
      // Refresh data
      await Promise.all([
          get().fetchVirtualPortfolio(userId),
          get().fetchPaperTrades(userId)
      ]);
      
      set({ isLoading: false });
      return true;
    } catch (error) {
      set({ error: error.message, isLoading: false });
      return false;
    }
  },

  runBacktest: async (userId, params) => {
    set({ isLoading: true });
    try {
      const response = await fetch(`${API_BASE}/backtest`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: userId, ...params })
      });
      const result = await response.json();
      set({ backtestResults: result.data, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  }
}));

export default usePaperTradingStore;
