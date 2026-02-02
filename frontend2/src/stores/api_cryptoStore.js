/**
 * ==============================================================================
 * FILE: frontend2/src/stores/api_cryptoStore.js
 * ROLE: State Management
 * PURPOSE: Manages real-time crypto prices and volume data.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useCryptoStore = create((set, get) => ({
    // State
    prices: {}, // { "BTC": { "USD": 50000.0 } }
    volumes: {}, // { "BTC": [{ exchange, volume, share }] }
    
    loading: {
        prices: false,
        volumes: false
    },
    
    error: null,

    // Actions
    fetchPrices: async (symbols = ['BTC','ETH','SOL'], currencies = ['USD'], mock = false) => {
        set((state) => ({ loading: { ...state.loading, prices: true }, error: null }));
        try {
            const symStr = symbols.join(',');
            const curStr = currencies.join(',');
            const response = await apiClient.get('/market/crypto/price', { 
                params: { symbols: symStr, currencies: curStr, mock } 
            });
            
            set({ 
                prices: response.data,
                loading: { ...get().loading, prices: false }
            });
        } catch (error) {
            console.error('Fetch crypto prices failed:', error);
            set({ error: error.message, loading: { ...get().loading, prices: false } });
        }
    },

    fetchVolume: async (symbol, mock = false) => {
        set((state) => ({ loading: { ...state.loading, volumes: true }, error: null }));
        try {
            const response = await apiClient.get(`/market/crypto/volume/${symbol}`, { params: { mock } });
            
            set((state) => ({
                volumes: { ...state.volumes, [symbol]: response.data },
                loading: { ...state.loading, volumes: false }
            }));
        } catch (error) {
            console.error(`Fetch volume ${symbol} failed:`, error);
            set({ error: error.message, loading: { ...get().loading, volumes: false } });
        }
    }
}));

export default useCryptoStore;
