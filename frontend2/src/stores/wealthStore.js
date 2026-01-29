import { create } from 'zustand';

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
      const response = await fetch('/api/v1/assets/');
      if (!response.ok) throw new Error('Failed to fetch assets');
      const data = await response.json();
      set({ assets: data, isLoading: false });
    } catch (err) {
      console.error(err);
      set({ error: err.message, isLoading: false });
    }
  },

  addAsset: async (asset) => {
    try {
        const response = await fetch('/api/v1/assets/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(asset)
        });
        if (!response.ok) throw new Error('Failed to add asset');
        const newAsset = await response.json();
        
        set((state) => ({ 
            assets: [...state.assets, newAsset] 
        }));
        return newAsset;
    } catch (err) {
        console.error(err);
    }
  },
  
  updateAsset: async (id, updates) => {
    try {
        const response = await fetch(`/api/v1/assets/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updates)
        });
        if (!response.ok) throw new Error('Failed to update asset');
        const updatedAsset = await response.json();
        
        set((state) => ({
            assets: state.assets.map((a) => (a.id === id ? updatedAsset : a))
        }));
    } catch (err) {
        console.error(err);
    }
  },
  
  removeAsset: async (id) => {
    try {
        await fetch(`/api/v1/assets/${id}`, { method: 'DELETE' });
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
        const response = await fetch(`/api/v1/financial-planning/goals?user_id=${userId}`);
        const result = await response.json();
        set({ goals: result.data || [], isLoading: false });
    } catch (err) {
        set({ error: err.message, isLoading: false });
    }
  },

  createGoal: async (userId, goalData) => {
    set({ isLoading: true });
    try {
        const response = await fetch('/api/v1/financial-planning/goals/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, ...goalData })
        });
        if (!response.ok) throw new Error('Failed to create goal');
        
        // Refresh goals
        await get().fetchGoals(userId);
        set({ isLoading: false });
    } catch (err) {
        set({ error: err.message, isLoading: false });
    }
  },

  fetchRecommendations: async (userId) => {
    try {
        const response = await fetch(`/api/v1/financial-planning/recommendations?user_id=${userId}`);
        const result = await response.json();
        set({ recommendations: result.data || [] });
    } catch (err) {
        console.error(err);
    }
  },

  // Retirement Actions
  runRetirementProjection: async (userId, params) => {
      set({ isLoading: true });
      try {
          const response = await fetch('/api/v1/retirement/projection', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ user_id: userId, ...params })
          });
          const result = await response.json();
          set({ retirementProjection: result.data, isLoading: false });
      } catch (err) {
          set({ error: err.message, isLoading: false });
      }
  },

  fetchWithdrawalStrategy: async (userId) => {
      try {
          const response = await fetch(`/api/v1/retirement/withdrawal-strategy?user_id=${userId}`);
          const result = await response.json();
          set({ withdrawalStrategy: result.data });
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
