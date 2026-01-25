/**
 * ==============================================================================
 * FILE: frontend2/src/stores/merchantStore.js
 * ROLE: State Management
 * PURPOSE: Manages merchant stats and catalog data.
 * ==============================================================================
 */

import { create } from 'zustand';

const useMerchantStore = create((set) => ({
    stats: null,
    catalog: [],
    loading: false,
    error: null,

    fetchStats: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await fetch(`/api/v1/merchant/square/stats?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch merchant stats');
            const data = await response.json();
            set({ stats: data, loading: false });
        } catch (error) {
            console.error('Fetch stats failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    fetchCatalog: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await fetch(`/api/v1/merchant/square/catalog?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch catalog');
            const data = await response.json();
            set({ catalog: data, loading: false });
        } catch (error) {
            console.error('Fetch catalog failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useMerchantStore;
