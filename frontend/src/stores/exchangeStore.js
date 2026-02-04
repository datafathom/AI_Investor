/**
 * ==============================================================================
 * FILE: frontend2/src/stores/exchangeStore.js
 * ROLE: State Management
 * PURPOSE: Manages crypto ticker and order execution state.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useExchangeStore = create((set, get) => ({
    ticker: null,
    depth: null,
    loading: false,
    orderStatus: null,
    error: null,

    fetchTicker: async (symbol, mock = true) => {
        try {
            const response = await apiClient.get(`/exchange/binance/ticker/${symbol}`, { params: { mock } });
            set({ ticker: response.data });
        } catch (error) {
            console.error('Fetch ticker failed:', error);
        }
    },

    fetchDepth: async (symbol, mock = true) => {
        try {
            const response = await apiClient.get(`/exchange/binance/depth/${symbol}`, { 
                params: { mock, limit: 5 } 
            });
            set({ depth: response.data });
        } catch (error) {
            console.error('Fetch depth failed:', error);
        }
    },

    placeOrder: async (orderParams, mock = true) => {
        set({ loading: true, orderStatus: null, error: null });
        try {
            const response = await apiClient.post('/exchange/binance/order', orderParams, {
                params: { mock }
            });

            set({ orderStatus: response.data, loading: false });
            return response.data;
        } catch (error) {
            console.error('Place order failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useExchangeStore;
