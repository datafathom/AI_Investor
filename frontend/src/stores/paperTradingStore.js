import { create } from 'zustand';
import apiClient from '../services/apiClient';

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
      const response = await apiClient.get('/paper-trading/portfolio', { params: { user_id: userId } });
      set({ virtualPortfolio: response.data.data || null, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchPaperTrades: async (userId) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get('/paper-trading/trades', { params: { user_id: userId, limit: 20 } });
      set({ paperTrades: response.data.data || [], isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  placePaperTrade: async (userId, tradeData) => {
    set({ isLoading: true });
    try {
      await apiClient.post('/paper-trading/trade', { user_id: userId, ...tradeData });
      
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
      const response = await apiClient.post('/paper-trading/backtest', { user_id: userId, ...params });
      set({ backtestResults: response.data.data, isLoading: false });
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  }
}));

export default usePaperTradingStore;
