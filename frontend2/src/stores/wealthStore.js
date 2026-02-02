import { create } from 'zustand';
import apiClient from '../services/apiClient';

// No persistence middleware - we fetch from backend
export const useWealthStore = create((set, get) => ({
  assets: [],
  currency: 'USD',
  isLoading: false,
  error: null,

  // Actions
  fetchAssets: async () => {
    set({ isLoading: true });
    try {
      const response = await apiClient.get('/assets/');
      set({ assets: response.data, isLoading: false });
    } catch (err) {
      console.error(err);
      set({ error: err.message, isLoading: false });
    }
  },

  addAsset: async (asset) => {
    try {
        const response = await apiClient.post('/assets/', asset);
        set((state) => ({ 
            assets: [...state.assets, response.data] 
        }));
        return response.data;
    } catch (err) {
        console.error(err);
    }
  },
  
  updateAsset: async (id, updates) => {
    try {
        const response = await apiClient.put(`/assets/${id}`, updates);
        set((state) => ({
            assets: state.assets.map((a) => (a.id === id ? response.data : a))
        }));
    } catch (err) {
        console.error(err);
    }
  },
  
  removeAsset: async (id) => {
    try {
        await apiClient.delete(`/assets/${id}`);
        set((state) => ({
            assets: state.assets.filter((a) => a.id !== id)
        }));
    } catch (err) {
        console.error(err);
    }
  },
  
  // Financial Planning State
  goals: [],
  recommendations: [],
  retirementProjection: null,
  withdrawalStrategy: null,

  // Financial Planning Actions
  fetchGoals: async (userId) => {
    set({ isLoading: true });
    try {
        const response = await apiClient.get('/financial-planning/goals', { params: { user_id: userId } });
        set({ goals: response.data.data || [], isLoading: false });
    } catch (err) {
        set({ error: err.message, isLoading: false });
    }
  },

  createGoal: async (userId, goalData) => {
    set({ isLoading: true });
    try {
        await apiClient.post('/financial-planning/goals/create', { user_id: userId, ...goalData });
        // Refresh goals
        await get().fetchGoals(userId);
        set({ isLoading: false });
    } catch (err) {
        set({ error: err.message, isLoading: false });
    }
  },

  fetchRecommendations: async (userId) => {
    try {
        const response = await apiClient.get('/financial-planning/recommendations', { params: { user_id: userId } });
        set({ recommendations: response.data.data || [] });
    } catch (err) {
        console.error(err);
    }
  },

  // Retirement Actions
  runRetirementProjection: async (userId, params) => {
      set({ isLoading: true });
      try {
          const response = await apiClient.post('/retirement/projection', { user_id: userId, ...params });
          set({ retirementProjection: response.data.data, isLoading: false });
      } catch (err) {
          set({ error: err.message, isLoading: false });
      }
  },

  fetchWithdrawalStrategy: async (userId) => {
      try {
          const response = await apiClient.get('/retirement/withdrawal-strategy', { params: { user_id: userId } });
          set({ withdrawalStrategy: response.data.data });
      } catch (err) {
          console.error(err);
      }
  },

  // Computed Getters
  getTotalWealth: () => {
    const state = get();
    return state.assets.reduce((sum, asset) => sum + (parseFloat(asset.value) || 0), 0);
  },
  
  getAssetsByCategory: (category) => {
    const state = get();
    return state.assets.filter(a => a.category === category);
  },

  getIlliquidTotal: () => {
    const state = get();
    return state.assets
      .filter(a => ['Real Estate', 'Art', 'Private Equity', 'Vehicles', 'Collectibles'].includes(a.category))
      .reduce((sum, asset) => sum + (parseFloat(asset.value) || 0), 0);
  }
}));
