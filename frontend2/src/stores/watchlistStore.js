import { create } from 'zustand';

const API_WATCHLIST = '/api/v1/watchlist';
const API_ALERT = '/api/v1/alert';

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
            const response = await fetch(`${API_WATCHLIST}/user/${userId}`);
            const result = await response.json();
            set({ watchlists: result.data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    fetchAlerts: async (userId) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`${API_ALERT}/user/${userId}`);
            const result = await response.json();
            set({ alerts: result.data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    createWatchlist: async (userId, watchlistName) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`${API_WATCHLIST}/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, watchlist_name: watchlistName })
            });
            await get().fetchWatchlists(userId);
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    addSymbolToWatchlist: async (watchlistId, symbol, userId) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`${API_WATCHLIST}/${watchlistId}/add`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symbol })
            });
            await get().fetchWatchlists(userId);
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    createAlert: async (userId, alertData) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`${API_ALERT}/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, ...alertData })
            });
            await get().fetchAlerts(userId);
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    setSelectedWatchlist: (watchlist) => set({ selectedWatchlist: watchlist })
}));

export default useWatchlistStore;
