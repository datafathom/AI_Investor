/**
 * Assets Store - Zustand State Management for Illiquid Assets
 * : Manages real estate, art, private equity entries and valuations.
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useAssetsStore = create((set, get) => ({
    // State
    illiquidAssets: [],
    appreciationRates: {},
    totalIlliquidValue: 0,
    unifiedNetWorth: 0,
    categories: ['real_estate', 'art', 'private_equity', 'collectibles', 'other'],
    error: null,
    
    // Actions
    setIlliquidAssets: (assets) => {
        const total = assets.reduce((sum, a) => sum + (a.currentValue || 0), 0);
        set({ illiquidAssets: assets, totalIlliquidValue: total });
    },
    addAsset: (asset) => set((s) => {
        const assets = [...s.illiquidAssets, { ...asset, id: `asset-${Date.now()}` }];
        return { illiquidAssets: assets, totalIlliquidValue: assets.reduce((sum, a) => sum + (a.currentValue || 0), 0) };
    }),
    updateAsset: (id, updates) => set((s) => {
        const assets = s.illiquidAssets.map(a => a.id === id ? { ...a, ...updates } : a);
        return { illiquidAssets: assets, totalIlliquidValue: assets.reduce((sum, a) => sum + (a.currentValue || 0), 0) };
    }),
    removeAsset: (id) => set((s) => {
        const assets = s.illiquidAssets.filter(a => a.id !== id);
        return { illiquidAssets: assets, totalIlliquidValue: assets.reduce((sum, a) => sum + (a.currentValue || 0), 0) };
    }),
    setAppreciationRate: (assetId, rate) => set((s) => ({ appreciationRates: { ...s.appreciationRates, [assetId]: rate } })),
    setUnifiedNetWorth: (worth) => set({ unifiedNetWorth: worth }),
    setError: (error) => set({ error }),
    
    // Async: Fetch assets
    fetchAssets: async () => {
        try {
            const response = await apiClient.get('/assets/illiquid');
            const data = response.data;
            const total = (data.assets || []).reduce((sum, a) => sum + (a.currentValue || 0), 0);
            set({ illiquidAssets: data.assets || [], totalIlliquidValue: total });
        } catch (error) {
            console.error('Fetch assets failed:', error);
        }
    },
    
    // Async: Save asset
    saveAsset: async (asset) => {
        const { addAsset, updateAsset, setError } = get();
        try {
            let response;
            if (asset.id) {
                response = await apiClient.put('/assets/illiquid', asset); // Assuming PUT for update if supported, typically would use POST or specific ID endpoint
            } else {
                response = await apiClient.post('/assets/illiquid', asset);
            }
            
            // Note: The original code used POST/PUT to same endpoint based on logic, but apiClient handles methods.
            // If the backend expects PUT for updates, we use put. 
            // However, typical REST would be PUT /assets/illiquid/:id. 
            // The previous code did: method: asset.id ? 'PUT' : 'POST' to /api/v1/assets/illiquid
            
            const data = response.data;
            if (asset.id) updateAsset(asset.id, data.asset);
            else addAsset(data.asset);
        } catch (error) {
            console.error('Save asset failed:', error);
            setError(error.message);
        }
    },
    
    reset: () => set({
        illiquidAssets: [], appreciationRates: {}, totalIlliquidValue: 0,
        unifiedNetWorth: 0, error: null
    })
}));

export default useAssetsStore;
