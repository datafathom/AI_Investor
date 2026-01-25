/**
 * ==============================================================================
 * FILE: frontend2/src/stores/briefingStore.js
 * ROLE: State Management
 * PURPOSE: Manages fetching and storing daily market briefings.
 * ==============================================================================
 */

import { create } from 'zustand';

const useBriefingStore = create((set) => ({
    briefing: null,
    loading: false,
    error: null,

    fetchBriefing: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const url = `/api/v1/ai/briefing/daily?mock=${mock}`;
            const response = await fetch(url);
            
            if (!response.ok) throw new Error('Failed to fetch daily briefing');
            
            const data = await response.json();
            set({ 
                briefing: data,
                loading: false 
            });
        } catch (error) {
            console.error('Fetch briefing failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useBriefingStore;
