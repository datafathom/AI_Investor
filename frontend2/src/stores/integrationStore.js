/**
 * ==============================================================================
 * FILE: frontend2/src/stores/integrationStore.js
 * ROLE: State Management
 * PURPOSE: Manages Third-Party SaaS and App integrations (Slack, Discord, etc.)
 * ==============================================================================
 */

import { create } from 'zustand';

const useIntegrationStore = create((set, get) => ({
    availableIntegrations: [],
    connectedIntegrations: [],
    syncHistory: [],
    loading: false,
    error: null,

    fetchAvailable: async () => {
        set({ loading: true, error: null });
        try {
            const res = await fetch('/api/v1/integrations/available');
            const data = await res.json();
            set({ availableIntegrations: data.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchConnected: async (userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            const res = await fetch(`/api/v1/integrations/connected?user_id=${userId}`);
            const data = await res.json();
            set({ connectedIntegrations: data.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchSyncHistory: async (userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            const res = await fetch(`/api/v1/integrations/sync-history?user_id=${userId}&limit=20`);
            const data = await res.json();
            set({ syncHistory: data.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    connectIntegration: async (integrationId, userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            const res = await fetch('/api/v1/integrations/connect', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, integration_id: integrationId })
            });
            if (!res.ok) throw new Error('Failed to connect integration');
            await get().fetchConnected(userId);
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    syncIntegration: async (integrationId, userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            const res = await fetch('/api/v1/integrations/sync', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ integration_id: integrationId })
            });
            if (!res.ok) throw new Error('Failed to sync integration');
            await get().fetchSyncHistory(userId);
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    }
}));

export default useIntegrationStore;
