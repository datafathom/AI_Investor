/**
 * Cash Store - Zustand State Management for Multi-Currency Cash
 * 
 * : Manages global cash balances, FX rates, and
 * interest-bearing cash optimization.
 * 
 * State slices:
 * - balances: Cash balances by currency
 * - fxRates: Real-time FX rates
 * - baseCurrency: Selected base currency for display
 * - sweepSuggestions: Cash optimization suggestions
 * 
 * Usage:
 *   const { balances, setBaseCurrency, triggerSweep } = useCashStore();
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useCashStore = create((set, get) => ({
    // ─────────────────────────────────────────────────────────────────────────
    // State
    // ─────────────────────────────────────────────────────────────────────────
    
    /** @type {string} */
    baseCurrency: 'USD',
    
    /** @type {CurrencyBalance[]} */
    balances: [],
    
    /** @type {Object.<string, FXRate>} */
    fxRates: {},
    
    /** @type {SweepSuggestion[]} */
    sweepSuggestions: [],
    
    /** @type {RepoRate[]} */
    repoRates: [],
    
    /** @type {number} */
    totalValueUSD: 0,
    
    /** @type {boolean} */
    isLoading: false,
    
    /** @type {string|null} */
    error: null,
    
    /** @type {string|null} */
    lastUpdated: null,
    
    // Supported currencies
    supportedCurrencies: ['USD', 'EUR', 'GBP', 'JPY', 'CHF', 'CAD'],
    
    // ─────────────────────────────────────────────────────────────────────────
    // Actions
    // ─────────────────────────────────────────────────────────────────────────
    
    /**
     * Sets the base currency for display
     * @param {string} currency 
     */
    setBaseCurrency: (currency) => set({ baseCurrency: currency }),
    
    /**
     * Updates all balances
     * @param {CurrencyBalance[]} balances 
     */
    setBalances: (balances) => {
        const totalUSD = balances.reduce((sum, b) => sum + b.amountUSD, 0);
        set({ 
            balances, 
            totalValueUSD: totalUSD,
            lastUpdated: new Date().toISOString()
        });
    },
    
    /**
     * Updates a single balance
     * @param {string} currency 
     * @param {number} amount 
     */
    updateBalance: (currency, amount) => set((state) => {
        const rate = state.fxRates[`${currency}/USD`]?.rate || 1;
        const amountUSD = currency === 'USD' ? amount : amount * rate;
        
        const existing = state.balances.find(b => b.currency === currency);
        if (existing) {
            return {
                balances: state.balances.map(b => 
                    b.currency === currency ? { ...b, amount, amountUSD } : b
                ),
                totalValueUSD: state.balances.reduce((sum, b) => 
                    sum + (b.currency === currency ? amountUSD : b.amountUSD), 0
                )
            };
        }
        const newBalances = [...state.balances, { currency, amount, amountUSD, interestRate: 0 }];
        return {
            balances: newBalances,
            totalValueUSD: newBalances.reduce((sum, b) => sum + b.amountUSD, 0)
        };
    }),
    
    /**
     * Updates FX rates
     * @param {FXRate[]} rates 
     */
    setFxRates: (rates) => {
        const ratesMap = {};
        rates.forEach(r => {
            ratesMap[r.pair] = r;
        });
        set({ 
            fxRates: ratesMap,
            lastUpdated: new Date().toISOString()
        });
    },
    
    /**
     * Updates a single FX rate
     * @param {FXRate} rate 
     */
    updateFxRate: (rate) => set((state) => ({
        fxRates: {
            ...state.fxRates,
            [rate.pair]: rate
        }
    })),
    
    /**
     * Sets sweep suggestions
     * @param {SweepSuggestion[]} suggestions 
     */
    setSweepSuggestions: (suggestions) => set({ sweepSuggestions: suggestions }),
    
    /**
     * Sets repo rates
     * @param {RepoRate[]} rates 
     */
    setRepoRates: (rates) => set({ repoRates: rates }),
    
    /**
     * Sets loading state
     * @param {boolean} loading 
     */
    setLoading: (loading) => set({ isLoading: loading }),
    
    /**
     * Sets error message
     * @param {string|null} error 
     */
    setError: (error) => set({ error }),
    
    /**
     * Clears error state
     */
    clearError: () => set({ error: null }),
    
    // ─────────────────────────────────────────────────────────────────────────
    // Computed / Selectors
    // ─────────────────────────────────────────────────────────────────────────
    
    /**
     * Gets total value in base currency
     * @returns {number}
     */
    getTotalInBaseCurrency: () => {
        const state = get();
        if (state.baseCurrency === 'USD') return state.totalValueUSD;
        
        const rate = state.fxRates[`USD/${state.baseCurrency}`]?.rate;
        if (!rate) return state.totalValueUSD;
        return state.totalValueUSD * rate;
    },
    
    /**
     * Gets balances sorted by value
     * @returns {CurrencyBalance[]}
     */
    getBalancesSortedByValue: () => {
        const state = get();
        return [...state.balances].sort((a, b) => b.amountUSD - a.amountUSD);
    },
    
    /**
     * Gets currencies with high overnight rates (>4%)
     * @returns {CurrencyBalance[]}
     */
    getHighYieldCurrencies: () => {
        const state = get();
        return state.balances.filter(b => b.interestRate > 4);
    },
    
    /**
     * Checks if currency exposure exceeds limit (15%)
     * @param {string} currency 
     * @returns {boolean}
     */
    isExposureExceeded: (currency) => {
        const state = get();
        const balance = state.balances.find(b => b.currency === currency);
        if (!balance || state.totalValueUSD === 0) return false;
        return (balance.amountUSD / state.totalValueUSD) > 0.15;
    },
    
    /**
     * Gets the best repo rate
     * @returns {RepoRate|null}
     */
    getBestRepoRate: () => {
        const state = get();
        if (state.repoRates.length === 0) return null;
        return state.repoRates.reduce((best, r) => 
            r.rate > best.rate ? r : best, state.repoRates[0]
        );
    },
    
    /**
     * Gets idle cash amount (USD balance)
     * @returns {number}
     */
    getIdleCash: () => {
        const state = get();
        const usdBalance = state.balances.find(b => b.currency === 'USD');
        return usdBalance?.amount || 0;
    },
    
    // ─────────────────────────────────────────────────────────────────────────
    // Async Actions (API Integration)
    // ─────────────────────────────────────────────────────────────────────────
    
    /**
     * Fetches all cash data from API
     */
    fetchCashData: async () => {
        const { setLoading, setError, setBalances, setFxRates, setSweepSuggestions, setRepoRates } = get();
        
        setLoading(true);
        setError(null);
        
        try {
            const response = await apiClient.get('/cash/dashboard');
            const data = response.data?.data || response.data || {};
            
            if (data.balances) setBalances(data.balances);
            if (data.fx_rates) setFxRates(data.fx_rates);
            if (data.sweep_suggestions) setSweepSuggestions(data.sweep_suggestions);
            if (data.repo_rates) setRepoRates(data.repo_rates);
            
        } catch (error) {
            console.error('Error fetching cash data:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    },
    
    /**
     * Fetches real-time FX rates
     */
    fetchFxRates: async () => {
        const { setFxRates, setError } = get();
        
        try {
            const response = await apiClient.get('/cash/fx/rates');
            const data = response.data?.data || response.data || {};
            setFxRates(data.rates || []);
        } catch (error) {
            console.error('Error fetching FX rates:', error);
            setError(error.message);
        }
    },
    
    /**
     * Executes a cash sweep
     * @param {string} suggestionId 
     */
    executeSweep: async (suggestionId) => {
        const { setLoading, setError, fetchCashData } = get();
        
        setLoading(true);
        setError(null);
        
        try {
            await apiClient.post('/cash/sweep/execute', { suggestion_id: suggestionId });
            
            // Refresh data after sweep
            await fetchCashData();
            
        } catch (error) {
            console.error('Error executing sweep:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    },
    
    /**
     * Executes an FX conversion
     * @param {string} fromCurrency 
     * @param {string} toCurrency 
     * @param {number} amount 
     */
    executeFxConversion: async (fromCurrency, toCurrency, amount) => {
        const { setLoading, setError, fetchCashData } = get();
        
        setLoading(true);
        setError(null);
        
        try {
            const response = await apiClient.post('/cash/fx/convert', { 
                from_currency: fromCurrency,
                to_currency: toCurrency,
                amount
            });
            
            const result = response.data?.data || response.data || {};
            
            // Refresh data after conversion
            await fetchCashData();
            
            return result;
            
        } catch (error) {
            console.error('Error executing FX conversion:', error);
            setError(error.message);
            throw error;
        } finally {
            setLoading(false);
        }
    },
    
    /**
     * Resets store to initial state
     */
    reset: () => set({
        baseCurrency: 'USD',
        balances: [],
        fxRates: {},
        sweepSuggestions: [],
        repoRates: [],
        totalValueUSD: 0,
        isLoading: false,
        error: null,
        lastUpdated: null
    })
}));

export default useCashStore;
