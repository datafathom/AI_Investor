/**
 * ==============================================================================
 * FILE: frontend2/src/stores/taxStore.js
 * ROLE: State Management
 * PURPOSE: Manages tax analysis and harvesting data.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

export const useTaxStore = create((set, get) => ({
    report: null,
    opportunities: [],
    harvestCandidates: [],
    totalPotentialSavings: 0,
    autoHarvestEnabled: false,
    loading: false,
    isLoading: false,
    gainsProjection: null,
    error: null,

    fetchHarvestCandidates: async (portfolioId = 'default_portfolio', minLoss = 100) => {
        set({ isLoading: true, error: null });
        try {
            const response = await apiClient.get('/tax-optimization/harvest-candidates', {
                params: { portfolio_id: portfolioId, min_loss: minLoss }
            });
            const candidates = Array.isArray(response.data) ? response.data : (response.data?.candidates || []);
            const savings = candidates.reduce((sum, c) => sum + (c.tax_savings || 0), 0);
            set({ 
                harvestCandidates: candidates,
                totalPotentialSavings: savings,
                isLoading: false 
            });
        } catch (error) {
            console.error('Fetch harvest candidates failed:', error);
            set({ harvestCandidates: [], totalPotentialSavings: 0, error: error.message, isLoading: false });
        }
    },

    toggleAutoHarvest: (enabled) => {
        set({ autoHarvestEnabled: enabled });
    },

    fetchHarvestOpportunities: async (portfolioId = 'default') => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get(`/tax/harvest/opportunities/${portfolioId}`);
            set({ 
                opportunities: response.data || [], 
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
            set({ opportunities: updated.data || [], loading: false });
        } catch (error) {
            console.error('Execute harvest failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    projectGains: async (portfolioId, scenario) => {
        set({ isLoading: true });
        try {
            const response = await apiClient.post('/tax-optimization/tax-projection', {
                portfolio_id: portfolioId,
                scenario: scenario
            });
            set({ gainsProjection: response.data, isLoading: false });
        } catch (error) {
            console.error('Project gains failed:', error);
            set({ error: error.message, isLoading: false });
        }
    }
}));

export default useTaxStore;

