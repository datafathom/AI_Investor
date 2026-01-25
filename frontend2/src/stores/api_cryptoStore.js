/**
 * ==============================================================================
 * FILE: frontend2/src/stores/api_cryptoStore.js
 * ROLE: State Management
 * PURPOSE: Manages real-time crypto prices and volume data.
 * ==============================================================================
 */

import { create } from 'zustand';

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
            const url = `/api/v1/market/crypto/price?symbols=${symStr}&currencies=${curStr}${mock ? '&mock=true' : ''}`;
            
            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to fetch crypto prices');
            
            const data = await response.json();
            set({ 
                prices: data,
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
            const url = `/api/v1/market/crypto/volume/${symbol}${mock ? '?mock=true' : ''}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Failed to fetch volume for ${symbol}`);
            
            const data = await response.json();
            set((state) => ({
                volumes: { ...state.volumes, [symbol]: data },
                loading: { ...state.loading, volumes: false }
            }));
        } catch (error) {
            console.error(`Fetch volume ${symbol} failed:`, error);
            set({ error: error.message, loading: { ...get().loading, volumes: false } });
        }
    }
}));

export default useCryptoStore;
