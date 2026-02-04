/**
 * Marketplace Store - 
 * Manages extension marketplace state following User Rule 6 pattern
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useMarketplaceStore = create((set, get) => ({
    // State
    extensions: [],
    installedExtensions: [],
    loading: false,
    error: null,
    searchQuery: '',

    // Actions
    setSearchQuery: (query) => set({ searchQuery: query }),

    fetchExtensions: async (search = '') => {
        set({ loading: true, error: null });
        try {
            const params = search ? { search } : {};
            const response = await apiClient.get('/marketplace/extensions', { params });
            set({ extensions: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchInstalledExtensions: async (userId) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/marketplace/installed', {
                params: { user_id: userId }
            });
            set({ installedExtensions: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    installExtension: async (userId, extensionId) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/marketplace/install', {
                user_id: userId,
                extension_id: extensionId
            });
            // Refresh installed list
            await get().fetchInstalledExtensions(userId);
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    },

    uninstallExtension: async (userId, extensionId) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/marketplace/uninstall', {
                extension_id: extensionId
            });
            await get().fetchInstalledExtensions(userId);
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    }
}));

export default useMarketplaceStore;
