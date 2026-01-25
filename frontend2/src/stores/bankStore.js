/**
 * ==============================================================================
 * FILE: frontend2/src/stores/bankStore.js
 * ROLE: State Management
 * PURPOSE: Manages linked bank accounts and Plaid Link flow.
 * ==============================================================================
 */

import { create } from 'zustand';

const useBankStore = create((set, get) => ({
    accounts: [],
    linkToken: null,
    loading: false,
    error: null,
    isLinked: false,

    fetchLinkToken: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await fetch(`/api/v1/bank/plaid/link-token?mock=${mock}`, { method: 'POST' });
            if (!response.ok) throw new Error('Failed to create link token');
            const data = await response.json();
            set({ linkToken: data.link_token, loading: false });
        } catch (error) {
            console.error('Fetch link token failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    exchangePublicToken: async (publicToken, mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await fetch(`/api/v1/bank/plaid/exchange-token?mock=${mock}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ public_token: publicToken })
            });

            if (!response.ok) throw new Error('Failed to exchange token');
            
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
            const response = await fetch(`/api/v1/bank/accounts?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch accounts');
            const data = await response.json();
            set({ accounts: data, loading: false });
        } catch (error) {
            console.error('Fetch accounts failed:', error);
            set({ error: error.message, loading: false });
        }
    }
}));

export default useBankStore;
