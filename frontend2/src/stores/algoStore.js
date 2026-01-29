import { create } from 'zustand';

const API_BASE = '/api/v1/strategy';

const useAlgoStore = create((set, get) => ({
    // State
    strategies: [],
    selectedStrategy: null,
    performance: null,
    isLoading: false,
    error: null,

    // Actions
    fetchStrategies: async (userId) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`${API_BASE}/strategies?user_id=${userId}`);
            const result = await response.json();
            set({ strategies: result.data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    setSelectedStrategy: (strategy) => set({ selectedStrategy: strategy }),

    fetchPerformance: async (strategyId) => {
        try {
            const response = await fetch(`${API_BASE}/performance?strategy_id=${strategyId}`);
            const result = await response.json();
            set({ performance: result.data });
        } catch (error) {
            set({ error: error.message });
        }
    },

    createStrategy: async (userId, strategyData) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`${API_BASE}/create`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ user_id: userId, ...strategyData })
            });

            if (!response.ok) throw new Error('Failed to create strategy');
            
            await get().fetchStrategies(userId); // Refresh list
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    deployStrategy: async (strategyId, userId) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`${API_BASE}/deploy`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ strategy_id: strategyId })
            });
            await get().fetchStrategies(userId); // Refresh list
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    pauseStrategy: async (strategyId, userId) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`${API_BASE}/pause`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ strategy_id: strategyId })
            });
            await get().fetchStrategies(userId); // Refresh list
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    forkToShadow: async (strategyId, userId) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`${API_BASE}/fork`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    strategy_id: strategyId,
                    fork_type: 'shadow',
                    label: `Shadow Fork - ${new Date().toLocaleTimeString()}`
                })
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Failed to fork strategy');
            
            await get().fetchStrategies(userId); // Refresh list
            set({ selectedStrategy: result.data, isLoading: false });
            return result.data;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            return null;
        }
    }
}));

export default useAlgoStore;
