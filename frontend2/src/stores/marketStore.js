/**
 * ==============================================================================
 * FILE: frontend2/src/stores/marketStore.js
 * ROLE: Market Data State Management
 * PURPOSE: Centralized Zustand store for all market data including quotes,
 *          historical data, intraday bars, and earnings calendar.
 *          
 * INTEGRATION POINTS:
 *     - marketService: API calls to /api/v1/market/*
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

const API_BASE = '/api/v1/market';

/**
 * Market Service - API calls to backend
 */
const marketService = {
    async getQuote(symbol) {
        const response = await fetch(`${API_BASE}/quote/${symbol}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.errors?.[0]?.message || 'Failed to fetch quote');
        }
        return response.json();
    },

    async getHistory(symbol, period = 'compact', adjusted = true) {
        const params = new URLSearchParams({ period, adjusted: adjusted.toString() });
        const response = await fetch(`${API_BASE}/history/${symbol}?${params}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.errors?.[0]?.message || 'Failed to fetch history');
        }
        return response.json();
    },

    async getShortInterest(symbol, mock = false) {
        const params = new URLSearchParams();
        if (mock) params.set('mock', 'true');
        const response = await fetch(`${API_BASE}/short-interest/${symbol}?${params}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.errors?.[0]?.message || 'Failed to fetch short interest');
        }
        return response.json();
    },

    async getIntraday(symbol, interval = '5min', outputsize = 'compact') {
        const params = new URLSearchParams({ interval, outputsize });
        const response = await fetch(`${API_BASE}/intraday/${symbol}?${params}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.errors?.[0]?.message || 'Failed to fetch intraday');
        }
        return response.json();
    },

    async getEarnings(symbol = null, horizon = '3month') {
        const params = new URLSearchParams({ horizon });
        if (symbol) params.set('symbol', symbol);
        const response = await fetch(`${API_BASE}/earnings?${params}`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.errors?.[0]?.message || 'Failed to fetch earnings');
        }
        return response.json();
    },

    async getHealth() {
        const response = await fetch(`${API_BASE}/health`);
        if (!response.ok) throw new Error('Health check failed');
        return response.json();
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
            const response = await marketService.getShortInterest(upperSymbol, mock);
            set((state) => ({
                shortInterest: { ...state.shortInterest, [upperSymbol]: response.data },
                loading: { ...state.loading, shortInterest: false }
            }));
            return response.data;
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
            const response = await marketService.getQuote(upperSymbol);
            set((state) => ({
                quotes: { ...state.quotes, [upperSymbol]: response.data },
                loading: { ...state.loading, quotes: false }
            }));
            return response.data;
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
            const response = await marketService.getHistory(upperSymbol, period, adjusted);
            set((state) => ({
                history: { 
                    ...state.history, 
                    [upperSymbol]: {
                        bars: response.data.bars,
                        count: response.data.count,
                        lastUpdated: new Date().toISOString()
                    }
                },
                loading: { ...state.loading, history: false }
            }));
            return response.data;
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
            const response = await marketService.getIntraday(upperSymbol, interval, outputsize);
            set((state) => ({
                intraday: { 
                    ...state.intraday, 
                    [upperSymbol]: {
                        interval: response.data.interval,
                        bars: response.data.bars,
                        count: response.data.count,
                        lastUpdated: new Date().toISOString()
                    }
                },
                loading: { ...state.loading, intraday: false }
            }));
            return response.data;
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
            const response = await marketService.getEarnings(symbol, horizon);
            set((state) => ({
                earnings: {
                    earnings: response.data.earnings,
                    count: response.data.count,
                    lastUpdated: new Date().toISOString()
                },
                loading: { ...state.loading, earnings: false }
            }));
            return response.data;
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
            const response = await marketService.getHealth();
            set((state) => ({
                health: response.data,
                loading: { ...state.loading, health: false }
            }));
            return response.data;
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
