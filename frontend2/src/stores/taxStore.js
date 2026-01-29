/**
 * ==============================================================================
 * FILE: frontend2/src/stores/taxStore.js
 * ROLE: State Management
 * PURPOSE: Manages tax analysis and harvesting data.
 * ==============================================================================
 */

import { create } from 'zustand';

export const useTaxStore = create((set) => ({
    report: null,
    loading: false,
    error: null,

    fetchOpportunities: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await fetch(`/api/v1/tax/harvesting/opportunities?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch tax opportunities');
            const data = await response.json();
            set({ report: data, loading: false });
        } catch (error) {
            console.error('Fetch tax ops failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useTaxStore;
