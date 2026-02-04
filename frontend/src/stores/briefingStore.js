/**
 * ==============================================================================
 * FILE: frontend2/src/stores/briefingStore.js
 * ROLE: State Management
 * PURPOSE: Manages fetching and storing daily market briefings.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useBriefingStore = create((set) => ({
    briefing: null,
    loading: false,
    error: null,

    fetchBriefing: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/ai/briefing/daily', { params: { mock } });
            
            set({ 
                briefing: response.data,
                loading: false 
            });
        } catch (error) {
            console.error('Fetch briefing failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useBriefingStore;
