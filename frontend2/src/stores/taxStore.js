/**
 * ==============================================================================
 * FILE: frontend2/src/stores/taxStore.js
 * ROLE: State Management
 * PURPOSE: Manages tax analysis and harvesting data.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

export const useTaxStore = create((set) => ({
    report: null,
    opportunities: [],
    loading: false,
    error: null,

    fetchHarvestOpportunities: async (portfolioId = 'default') => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get(`/tax/harvest/opportunities/${portfolioId}`);
            set({ 
                opportunities: response.data, 
                loading: false 
            });
        } catch (error) {
            console.error('Fetch tax harvest opportunities failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    executeHarvest: async (portfolioId, opportunity, replacementSymbol) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post(`/tax/harvest/execute/${portfolioId}`, {
                opportunity,
                replacement_symbol: replacementSymbol,
                approved: true
            });
            // Refresh opportunities
            const updated = await apiClient.get(`/tax/harvest/opportunities/${portfolioId}`);
            set({ opportunities: updated.data, loading: false });
        } catch (error) {
            console.error('Execute harvest failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useTaxStore;
