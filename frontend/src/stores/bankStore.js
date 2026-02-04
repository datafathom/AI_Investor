/**
 * ==============================================================================
 * FILE: frontend2/src/stores/bankStore.js
 * ROLE: State Management
 * PURPOSE: Manages linked bank accounts and Plaid Link flow.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useBankStore = create((set, get) => ({
    accounts: [],
    linkToken: null,
    loading: false,
    error: null,
    isLinked: false,

    fetchLinkToken: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.post('/bank/plaid/link-token', null, { params: { mock } });
            set({ linkToken: response.data.link_token, loading: false });
        } catch (error) {
            console.error('Fetch link token failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    exchangePublicToken: async (publicToken, mock = true) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/bank/plaid/exchange-token', 
                { public_token: publicToken },
                { params: { mock } }
            );
            
            // On success, fetch accounts
            await get().fetchAccounts(mock);
            set({ isLinked: true, loading: false });

        } catch (error) {
            console.error('Exchange token failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    fetchAccounts: async (mock = true) => {
        set({ loading: true });
        try {
            const response = await apiClient.get('/bank/accounts', { params: { mock } });
            set({ accounts: response.data, loading: false });
        } catch (error) {
            console.error('Fetch accounts failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useBankStore;
