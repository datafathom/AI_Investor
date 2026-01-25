/**
 * Assets Store - Zustand State Management for Illiquid Assets
 * Phase 67: Manages real estate, art, private equity entries and valuations.
 */
import { create } from 'zustand';

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
            const response = await fetch('/api/v1/assets/illiquid');
            const data = await response.json();
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
            const response = await fetch('/api/v1/assets/illiquid', {
                method: asset.id ? 'PUT' : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(asset)
            });
            const data = await response.json();
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
