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
            set({ indicators: response.data.indicators, loading: { ...get().loading, indicators: false } });
            return response.data.indicators;
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
        loading: { regime: false, yieldCurve: false, indicators: false, series: false },
        errors: { regime: null, yieldCurve: null, indicators: null, series: null }
    })
}));

export default useMacroStore;
