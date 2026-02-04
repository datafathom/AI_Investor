/**
 * ==============================================================================
 * FILE: frontend2/src/stores/walletStore.js
 * ROLE: State Management
 * PURPOSE: Manages crypto wallet connection and assets.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useWalletStore = create((set, get) => ({
    balance: null,
    transactions: [],
    loading: false,
    error: null,
    isConnected: false,

    connectWallet: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/wallet/coinbase/connect', null, { params: { mock } });
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
            const response = await apiClient.get('/wallet/coinbase/balance', { params: { mock } });
            set({ balance: response.data, loading: false });
        } catch (error) {
            console.error('Fetch balance failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    fetchTransactions: async (mock = true) => {
        try {
            const response = await apiClient.get('/wallet/coinbase/transactions', { params: { mock } });
            set({ transactions: response.data });
        } catch (error) {
            console.error('Fetch transactions failed:', error);
        }
    }
}));

export default useWalletStore;
