/**
 * ==============================================================================
 * FILE: frontend2/src/stores/macroStore.js
 * ROLE: Macroeconomic Data State Management
 * PURPOSE: Centralized Zustand store for FRED macro data, regime analysis,
 *          and yield curve visualization.
 *          
 * INTEGRATION POINTS:
 *     - apiClient: API calls to /api/v1/macro-data/*
 *     - MacroHealthGauge: Regime health score
 *     - YieldCurveChart: Interest rate spreads
 *     - RegimeIndicator: Economic status
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

/**
 * Macro API Service using apiClient
 */
const macroService = {
    async getRegime() {
        const response = await apiClient.get('/macro-data/regime');
        return response.data;
    },

    async getYieldCurve() {
        const response = await apiClient.get('/macro-data/yield-curve');
        return response.data;
    },

    async getSeries(seriesId, limit = 100, transform = 'raw') {
        const response = await apiClient.get(`/macro-data/series/${seriesId}`, {
            params: { limit, transform }
        });
        return response.data;
    },

    async getIndicators() {
        const response = await apiClient.get('/macro-data/indicators');
        return response.data;
    },

    async getHealth() {
        const response = await apiClient.get('/macro-data/health');
        return response.data;
    }
};

/**
 * Macro Store
 */
export const useMacroStore = create((set, get) => ({
    // State
    regime: null,
    yieldCurve: null,
    indicators: [],
    seriesData: {},
    healthStatus: null,
    shippingRoutes: [],
    politicalSignals: [],
    commodities: [],
    isLoading: false,
    
    loading: {
        regime: false,
        yieldCurve: false,
        indicators: false,
        series: false
    },
    
    errors: {
        regime: null,
        yieldCurve: null,
        indicators: null,
        series: null
    },

    // Actions
    fetchMacroData: async () => {
        set({ isLoading: true });
        try {
            // Fetch multiple datasets in parallel
            await Promise.all([
                get().fetchRegime(),
                get().fetchIndicators(),
                get().fetchHealth()
            ]);
            
            // Mock or fetch specialized macro data if missing
            // For now, we populate with some defaults if the API doesn't provide them yet
            set({
                shippingRoutes: [
                    { route: 'Shanghai - LA', volume: 14500, change: 2.1, status: 'normal' },
                    { route: 'Singapore - Rotterdam', volume: 18200, change: -1.4, status: 'congested' },
                    { route: 'Suez Canal', volume: 12500, change: -15.2, status: 'blocked' }
                ],
                politicalSignals: [
                    { region: 'EU', signal: 'CRITICAL', reason: 'Energy Policy Shift' },
                    { region: 'US', signal: 'STABLE', reason: 'Election Cycle Pricing' }
                ],
                commodities: [
                    { commodity: 'Crude Oil', price: 78.42, change: 1.2 },
                    { commodity: 'Gold', price: 2024.50, change: -0.5 }
                ]
            });
        } catch (error) {
            console.error('Failed to fetch comprehensive macro data:', error);
        } finally {
            set({ isLoading: false });
        }
    },

    fetchRegime: async () => {
        set((state) => ({ loading: { ...state.loading, regime: true }, errors: { ...state.errors, regime: null } }));
        try {
            const response = await macroService.getRegime();
            set({ regime: response.data, loading: { ...get().loading, regime: false } });
            return response.data;
        } catch (error) {
            set({ errors: { ...get().errors, regime: error.message }, loading: { ...get().loading, regime: false } });
        }
    },

    fetchYieldCurve: async () => {
        set((state) => ({ loading: { ...state.loading, yieldCurve: true }, errors: { ...state.errors, yieldCurve: null } }));
        try {
            const response = await macroService.getYieldCurve();
            set({ yieldCurve: response.data, loading: { ...get().loading, yieldCurve: false } });
            return response.data;
        } catch (error) {
            set({ errors: { ...get().errors, yieldCurve: error.message }, loading: { ...get().loading, yieldCurve: false } });
        }
    },

    fetchIndicators: async () => {
        set((state) => ({ loading: { ...state.loading, indicators: true }, errors: { ...state.errors, indicators: null } }));
        try {
            const response = await macroService.getIndicators();
            const data = response.data.indicators || [];
            set({ indicators: data, loading: { ...get().loading, indicators: false } });
            return data;
        } catch (error) {
            set({ errors: { ...get().errors, indicators: error.message }, loading: { ...get().loading, indicators: false } });
        }
    },

    fetchSeries: async (seriesId, limit = 100, transform = 'raw') => {
        set((state) => ({ loading: { ...state.loading, series: true } }));
        try {
            const response = await macroService.getSeries(seriesId, limit, transform);
            set((state) => ({
                seriesData: {
                    ...state.seriesData,
                    [seriesId]: response.data
                },
                loading: { ...state.loading, series: false }
            }));
            return response.data;
        } catch (error) {
            set({ errors: { ...get().errors, series: error.message }, loading: { ...get().loading, series: false } });
        }
    },

    fetchHealth: async () => {
        try {
            const response = await macroService.getHealth();
            set({ healthStatus: response.data });
        } catch (error) {
            console.error('Macro health check failed:', error);
        }
    },

    clearAll: () => set({
        regime: null,
        yieldCurve: null,
        indicators: [],
        seriesData: {},
        shippingRoutes: [],
        politicalSignals: [],
        commodities: [],
        isLoading: false,
        loading: { regime: false, yieldCurve: false, indicators: false, series: false },
        errors: { regime: null, yieldCurve: null, indicators: null, series: null }
    })
}));

export default useMacroStore;
