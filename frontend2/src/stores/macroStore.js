/**
 * ==============================================================================
 * FILE: frontend2/src/stores/macroStore.js
 * ROLE: Macroeconomic Data State Management
 * PURPOSE: Centralized Zustand store for FRED macro data, regime analysis,
 *          and yield curve visualization.
 *          
 * INTEGRATION POINTS:
 *     - macroService: API calls to /api/v1/macro-data/*
 *     - MacroHealthGauge: Regime health score
 *     - YieldCurveChart: Interest rate spreads
 *     - RegimeIndicator: Economic status
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import { create } from 'zustand';

const API_BASE = '/api/v1/macro-data';

/**
 * Macro API Service
 */
const macroService = {
    async getRegime() {
        const response = await fetch(`${API_BASE}/regime`);
        if (!response.ok) throw new Error('Failed to fetch macro regime');
        return response.json();
    },

    async getYieldCurve() {
        const response = await fetch(`${API_BASE}/yield-curve`);
        if (!response.ok) throw new Error('Failed to fetch yield curve');
        return response.json();
    },

    async getSeries(seriesId, limit = 100, transform = 'raw') {
        const params = new URLSearchParams({ limit, transform });
        const response = await fetch(`${API_BASE}/series/${seriesId}?${params}`);
        if (!response.ok) throw new Error(`Failed to fetch series ${seriesId}`);
        return response.json();
    },

    async getIndicators() {
        const response = await fetch(`${API_BASE}/indicators`);
        if (!response.ok) throw new Error('Failed to fetch indicators');
        return response.json();
    },

    async getHealth() {
        const response = await fetch(`${API_BASE}/health`);
        if (!response.ok) throw new Error('Macro health check failed');
        return response.json();
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
