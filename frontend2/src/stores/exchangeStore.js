/**
 * ==============================================================================
 * FILE: frontend2/src/stores/exchangeStore.js
 * ROLE: State Management
 * PURPOSE: Manages crypto ticker and order execution state.
 * ==============================================================================
 */

import { create } from 'zustand';

const useExchangeStore = create((set, get) => ({
    ticker: null,
    depth: null,
    loading: false,
    orderStatus: null,
    error: null,

    fetchTicker: async (symbol, mock = true) => {
        try {
            const response = await fetch(`/api/v1/exchange/binance/ticker/${symbol}?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch ticker');
            const data = await response.json();
            set({ ticker: data });
        } catch (error) {
            console.error('Fetch ticker failed:', error);
        }
    },

    fetchDepth: async (symbol, mock = true) => {
        try {
            const response = await fetch(`/api/v1/exchange/binance/depth/${symbol}?mock=${mock}&limit=5`);
            if (!response.ok) throw new Error('Failed to fetch depth');
            const data = await response.json();
            set({ depth: data });
        } catch (error) {
            console.error('Fetch depth failed:', error);
        }
    },

    placeOrder: async (orderParams, mock = true) => {
        set({ loading: true, orderStatus: null, error: null });
        try {
            const response = await fetch(`/api/v1/exchange/binance/order?mock=${mock}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(orderParams)
            });

            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Trade failed');
            
            set({ orderStatus: data, loading: false });
            return data;
        } catch (error) {
            console.error('Place order failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useExchangeStore;
