import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useAlgoStore = create((set, get) => ({
    // State
    strategies: [],
    selectedStrategy: null,
    performance: null,
    drift: null,
    isLoading: false,
    error: null,

    // Actions
    fetchStrategies: async (userId) => {
        set({ isLoading: true });
        try {
            const response = await apiClient.get('/strategy/strategies', { params: { user_id: userId } });
            set({ strategies: response.data.data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    setSelectedStrategy: (strategy) => set({ selectedStrategy: strategy }),

    fetchPerformance: async (strategyId) => {
        try {
            const response = await apiClient.get(`/strategy/${strategyId}/performance`);
            set({ performance: response.data.data });
        } catch (error) {
            set({ error: error.message });
        }
    },

    fetchDrift: async (strategyId) => {
        try {
            const response = await apiClient.get(`/strategy/${strategyId}/drift`);
            set({ drift: response.data.data });
        } catch (error) {
            set({ error: error.message });
        }
    },

    createStrategy: async (userId, strategyData) => {
        set({ isLoading: true });
        try {
            await apiClient.post('/strategy/create', { user_id: userId, ...strategyData });
            await get().fetchStrategies(userId); // Refresh list
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    deployStrategy: async (strategyId, userId) => {
        set({ isLoading: true });
        try {
            await apiClient.post('/strategy/deploy', { strategy_id: strategyId });
            await get().fetchStrategies(userId); // Refresh list
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    pauseStrategy: async (strategyId, userId) => {
        set({ isLoading: true });
        try {
            await apiClient.post('/strategy/pause', { strategy_id: strategyId });
            await get().fetchStrategies(userId); // Refresh list
            set({ isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
        }
    },

    forkToShadow: async (strategyId, userId) => {
        set({ isLoading: true });
        try {
            const response = await apiClient.post('/strategy/fork', { 
                strategy_id: strategyId,
                fork_type: 'shadow',
                label: `Shadow Fork - ${new Date().toLocaleTimeString()}`
            });
            
            const result = response.data;
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
