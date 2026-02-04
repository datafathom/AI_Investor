/**
 * ==============================================================================
 * FILE: frontend2/src/stores/marketStore.js
 * ROLE: Market Data State Management
 * PURPOSE: Centralized Zustand store for all market data including quotes,
 *          historical data, intraday bars, and earnings calendar.
 *          
 * INTEGRATION POINTS:
 *     - apiClient: API calls to /api/v1/market/*
 *     - QuoteCard: Real-time quote display
 *     - PriceChart: Historical price visualization
 *     - EarningsCalendar: Upcoming earnings events
 *     
 * STATE SHAPE:
 *     quotes: { [symbol]: QuoteData }
 *     history: { [symbol]: { bars: [], count: number } }
 *     intraday: { [symbol]: { interval: string, bars: [], count: number } }
 *     earnings: { earnings: [], count: number }
 *     loading: { quotes: boolean, history: boolean, intraday: boolean, earnings: boolean }
 *     errors: { quotes: Error | null, history: Error | null, ... }
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

/**
 * Market Service - API calls to backend via apiClient
 */
const marketService = {
    async getQuote(symbol) {
        const response = await apiClient.get(`/market/quote/${symbol}`);
        return response.data;
    },

    async getHistory(symbol, period = 'compact', adjusted = true) {
        const response = await apiClient.get(`/market/history/${symbol}`, {
            params: { period, adjusted: adjusted.toString() }
        });
        return response.data;
    },

    async getShortInterest(symbol, mock = false) {
        const response = await apiClient.get(`/market/short-interest/${symbol}`, {
            params: mock ? { mock: 'true' } : {}
        });
        return response.data;
    },

    async getIntraday(symbol, interval = '5min', outputsize = 'compact') {
        const response = await apiClient.get(`/market/intraday/${symbol}`, {
            params: { interval, outputsize }
        });
        return response.data;
    },

    async getEarnings(symbol = null, horizon = '3month') {
        const params = { horizon };
        if (symbol) params.symbol = symbol;
        const response = await apiClient.get('/market/earnings', { params });
        return response.data;
    },

    async getHealth() {
        const response = await apiClient.get('/market/health');
        return response.data;
    }
};

/**
 * Market Store - Zustand state management
 */
export const useMarketStore = create((set, get) => ({
    // State
    quotes: {},
    history: {},
    intraday: {},
    shortInterest: {},
    earnings: { earnings: [], count: 0 },
    health: null,
    
    loading: {
        quotes: false,
        history: false,
        intraday: false,
        shortInterest: false,
        earnings: false,
        health: false
    },
    
    errors: {
        quotes: null,
        history: null,
        intraday: null,
        shortInterest: null,
        earnings: null,
        health: null
    },

    // Actions
    fetchShortInterest: async (symbol, mock = false) => {
        const upperSymbol = symbol.toUpperCase();
        set((state) => ({
            loading: { ...state.loading, shortInterest: true },
            errors: { ...state.errors, shortInterest: null }
        }));

        try {
            const data = await marketService.getShortInterest(upperSymbol, mock);
            set((state) => ({
                shortInterest: { ...state.shortInterest, [upperSymbol]: data.data || data },
                loading: { ...state.loading, shortInterest: false }
            }));
            return data.data || data;
        } catch (error) {
            set((state) => ({
                errors: { ...state.errors, shortInterest: error.message },
                loading: { ...state.loading, shortInterest: false }
            }));
            throw error;
        }
    },

    fetchQuote: async (symbol) => {
        const upperSymbol = symbol.toUpperCase();
        set((state) => ({
            loading: { ...state.loading, quotes: true },
            errors: { ...state.errors, quotes: null }
        }));

        try {
            const data = await marketService.getQuote(upperSymbol);
            set((state) => ({
                quotes: { ...state.quotes, [upperSymbol]: data.data || data },
                loading: { ...state.loading, quotes: false }
            }));
            return data.data || data;
        } catch (error) {
            set((state) => ({
                errors: { ...state.errors, quotes: error.message },
                loading: { ...state.loading, quotes: false }
            }));
            throw error;
        }
    },

    fetchHistory: async (symbol, period = 'compact', adjusted = true) => {
        const upperSymbol = symbol.toUpperCase();
        set((state) => ({
            loading: { ...state.loading, history: true },
            errors: { ...state.errors, history: null }
        }));

        try {
            const data = await marketService.getHistory(upperSymbol, period, adjusted);
            const bars = data.data?.bars || data.bars || [];
            const count = data.data?.count || data.count || 0;
            set((state) => ({
                history: { 
                    ...state.history, 
                    [upperSymbol]: {
                        bars,
                        count,
                        lastUpdated: new Date().toISOString()
                    }
                },
                loading: { ...state.loading, history: false }
            }));
            return data.data || data;
        } catch (error) {
            set((state) => ({
                errors: { ...state.errors, history: error.message },
                loading: { ...state.loading, history: false }
            }));
            throw error;
        }
    },

    fetchIntraday: async (symbol, interval = '5min', outputsize = 'compact') => {
        const upperSymbol = symbol.toUpperCase();
        set((state) => ({
            loading: { ...state.loading, intraday: true },
            errors: { ...state.errors, intraday: null }
        }));

        try {
            const data = await marketService.getIntraday(upperSymbol, interval, outputsize);
            const result = data.data || data;
            set((state) => ({
                intraday: { 
                    ...state.intraday, 
                    [upperSymbol]: {
                        interval: result.interval,
                        bars: result.bars,
                        count: result.count,
                        lastUpdated: new Date().toISOString()
                    }
                },
                loading: { ...state.loading, intraday: false }
            }));
            return result;
        } catch (error) {
            set((state) => ({
                errors: { ...state.errors, intraday: error.message },
                loading: { ...state.loading, intraday: false }
            }));
            throw error;
        }
    },

    fetchEarnings: async (symbol = null, horizon = '3month') => {
        set((state) => ({
            loading: { ...state.loading, earnings: true },
            errors: { ...state.errors, earnings: null }
        }));

        try {
            const data = await marketService.getEarnings(symbol, horizon);
            const result = data.data || data;
            set((state) => ({
                earnings: {
                    earnings: result.earnings || [],
                    count: result.count || 0,
                    lastUpdated: new Date().toISOString()
                },
                loading: { ...state.loading, earnings: false }
            }));
            return result;
        } catch (error) {
            set((state) => ({
                errors: { ...state.errors, earnings: error.message },
                loading: { ...state.loading, earnings: false }
            }));
            throw error;
        }
    },

    fetchHealth: async () => {
        set((state) => ({
            loading: { ...state.loading, health: true },
            errors: { ...state.errors, health: null }
        }));

        try {
            const data = await marketService.getHealth();
            const result = data.data || data;
            set((state) => ({
                health: result,
                loading: { ...state.loading, health: false }
            }));
            return result;
        } catch (error) {
            set((state) => ({
                errors: { ...state.errors, health: error.message },
                loading: { ...state.loading, health: false }
            }));
            throw error;
        }
    },

    // Selectors
    getQuote: (symbol) => get().quotes[symbol?.toUpperCase()],
    getHistory: (symbol) => get().history[symbol?.toUpperCase()],
    getIntraday: (symbol) => get().intraday[symbol?.toUpperCase()],
    getShortInterest: (symbol) => get().shortInterest[symbol?.toUpperCase()],
    isLoading: (dataType) => get().loading[dataType],
    getError: (dataType) => get().errors[dataType],

    // Clear state
    clearQuote: (symbol) => {
        set((state) => {
            const { [symbol.toUpperCase()]: _, ...rest } = state.quotes;
            return { quotes: rest };
        });
    },

    clearAll: () => {
        set({
            quotes: {},
            history: {},
            intraday: {},
            earnings: { earnings: [], count: 0 },
            health: null,
            loading: { quotes: false, history: false, intraday: false, earnings: false, health: false },
            errors: { quotes: null, history: null, intraday: null, earnings: null, health: null }
        });
    }
}));

export default useMarketStore;
