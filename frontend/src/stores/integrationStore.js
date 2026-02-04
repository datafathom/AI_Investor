/**
 * ==============================================================================
 * FILE: frontend2/src/stores/integrationStore.js
 * ROLE: State Management
 * PURPOSE: Manages Third-Party SaaS and App integrations (Slack, Discord, etc.)
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useIntegrationStore = create((set, get) => ({
    availableIntegrations: [],
    connectedIntegrations: [],
    syncHistory: [],
    loading: false,
    error: null,

    fetchAvailable: async () => {
        set({ loading: true, error: null });
        try {
            const res = await apiClient.get('/integrations/available');
            set({ availableIntegrations: res.data.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchConnected: async (userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            const res = await apiClient.get('/integrations/connected', { params: { user_id: userId } });
            set({ connectedIntegrations: res.data.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchSyncHistory: async (userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            const res = await apiClient.get('/integrations/sync-history', { params: { user_id: userId, limit: 20 } });
            set({ syncHistory: res.data.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    connectIntegration: async (integrationId, userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/integrations/connect', { user_id: userId, integration_id: integrationId });
            await get().fetchConnected(userId);
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    syncIntegration: async (integrationId, userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/integrations/sync', { integration_id: integrationId });
            await get().fetchSyncHistory(userId);
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    }
}));

export default useIntegrationStore;
