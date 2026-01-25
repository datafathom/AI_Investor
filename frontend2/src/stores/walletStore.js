/**
 * ==============================================================================
 * FILE: frontend2/src/stores/walletStore.js
 * ROLE: State Management
 * PURPOSE: Manages crypto wallet connection and assets.
 * ==============================================================================
 */

import { create } from 'zustand';

const useWalletStore = create((set, get) => ({
    balance: null,
    transactions: [],
    loading: false,
    error: null,
    isConnected: false,

    connectWallet: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await fetch(`/api/v1/wallet/coinbase/connect?mock=${mock}`, { method: 'POST' });
            if (!response.ok) throw new Error('Failed to connect wallet');
            await response.json();
            
            set({ isConnected: true });
            await get().fetchBalance(mock);
            await get().fetchTransactions(mock);

        } catch (error) {
            console.error('Wallet connect failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    fetchBalance: async (mock = true) => {
        set({ loading: true });
        try {
            const response = await fetch(`/api/v1/wallet/coinbase/balance?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch balance');
            const data = await response.json();
            set({ balance: data, loading: false });
        } catch (error) {
            console.error('Fetch balance failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    fetchTransactions: async (mock = true) => {
        try {
            const response = await fetch(`/api/v1/wallet/coinbase/transactions?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch transactions');
            const data = await response.json();
            set({ transactions: data });
        } catch (error) {
            console.error('Fetch transactions failed:', error);
        }
    }
}));

export default useWalletStore;
