/**
 * ==============================================================================
 * FILE: frontend2/src/stores/merchantStore.js
 * ROLE: State Management
 * PURPOSE: Manages merchant stats and catalog data.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useMerchantStore = create((set) => ({
    stats: null,
    catalog: [],
    loading: false,
    error: null,

    fetchStats: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/merchant/square/stats', { params: { mock } });
            set({ stats: response.data, loading: false });
        } catch (error) {
            console.error('Fetch stats failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    fetchCatalog: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/merchant/square/catalog', { params: { mock } });
            set({ catalog: response.data, loading: false });
        } catch (error) {
            console.error('Fetch catalog failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useMerchantStore;
