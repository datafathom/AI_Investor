/**
 * Public API Store - Phase 25
 * Manages developer API keys and usage
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const usePublicApiStore = create((set, get) => ({
    // State
    apiKeys: [],
    usage: {},
    loading: false,
    error: null,

    // Actions
    fetchApiKeys: async (userId) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/public-api/keys', {
                params: { user_id: userId }
            });
            set({ apiKeys: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchUsage: async (userId) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/public-api/usage', {
                params: { user_id: userId }
            });
            set({ usage: response.data?.data || response.data || {}, loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    createApiKey: async (keyData) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/public-api/key/create', keyData);
            await get().fetchApiKeys(keyData.user_id);
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    },

    revokeApiKey: async (keyId, userId) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post(`/public-api/key/${keyId}/revoke`);
            await get().fetchApiKeys(userId);
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    }
}));

export default usePublicApiStore;
