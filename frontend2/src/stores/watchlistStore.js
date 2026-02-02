import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useWatchlistStore = create((set, get) => ({
    // State
    watchlists: [],
    alerts: [],
    selectedWatchlist: null,
    isLoading: false,
    error: null,

    // Actions
    fetchWatchlists: async (userId) => {
        set({ isLoading: true });
        try {
            const response = await apiClient.get(`/watchlist/user/${userId}`);
            set({ watchlists: response.data.data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    fetchAlerts: async (userId) => {
        set({ isLoading: true });
        try {
            const response = await apiClient.get(`/alert/user/${userId}`);
            set({ alerts: response.data.data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    createWatchlist: async (userId, watchlistName) => {
        set({ isLoading: true });
        try {
            await apiClient.post('/watchlist/create', { user_id: userId, watchlist_name: watchlistName });
            await get().fetchWatchlists(userId);
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    addSymbolToWatchlist: async (watchlistId, symbol, userId) => {
        set({ isLoading: true });
        try {
            await apiClient.post(`/watchlist/${watchlistId}/add`, { symbol });
            await get().fetchWatchlists(userId);
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    createAlert: async (userId, alertData) => {
        set({ isLoading: true });
        try {
            await apiClient.post('/alert/create', { user_id: userId, ...alertData });
            await get().fetchAlerts(userId);
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    setSelectedWatchlist: (watchlist) => set({ selectedWatchlist: watchlist })
}));

export default useWatchlistStore;
