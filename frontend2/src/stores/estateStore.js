/**
 * Estate Store - Zustand State Management for Estate Planning
 * Phase 58: Manages beneficiaries, estate plans, and inheritance simulations.
 * Updated to use apiClient per User Rule 6.
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useEstateStore = create((set, get) => ({
    // State
    estatePlan: null,
    beneficiaries: [],
    inheritanceSim: null,
    heartbeatStatus: { lastCheck: null, isAlive: true, daysUntilTrigger: 30, triggerDate: null },
    entityGraph: { nodes: [], edges: [] },
    isLoading: false,
    error: null,
    
    // Actions - Estate Plan
    fetchEstatePlan: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const response = await apiClient.get('/estate/plan', { params: { user_id: userId } });
            set({ estatePlan: response.data?.data || response.data, isLoading: false });
        } catch (error) {
            console.error('Failed to fetch estate plan:', error);
            set({ error: error.message, isLoading: false });
        }
    },

    // Actions - Beneficiaries
    fetchBeneficiaries: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const response = await apiClient.get('/estate/beneficiaries', { params: { user_id: userId } });
            set({ beneficiaries: response.data?.data || response.data || [], isLoading: false });
        } catch (error) {
            console.error('Failed to fetch beneficiaries:', error);
            set({ error: error.message, isLoading: false });
        }
    },

    addBeneficiary: async (beneficiaryData) => {
        set({ isLoading: true, error: null });
        try {
            await apiClient.post('/estate/beneficiary/add', beneficiaryData);
            await get().fetchBeneficiaries(beneficiaryData.user_id);
            set({ isLoading: false });
            return true;
        } catch (error) {
            console.error('Failed to add beneficiary:', error);
            set({ error: error.message, isLoading: false });
            return false;
        }
    },

    removeBeneficiary: async (beneficiaryId, userId) => {
        set({ isLoading: true, error: null });
        try {
            await apiClient.delete(`/estate/beneficiary/${beneficiaryId}`);
            await get().fetchBeneficiaries(userId);
            set({ isLoading: false });
            return true;
        } catch (error) {
            console.error('Failed to remove beneficiary:', error);
            set({ error: error.message, isLoading: false });
            return false;
        }
    },

    // Actions - Inheritance Simulation
    runInheritanceSimulation: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const response = await apiClient.post('/estate/inheritance/simulate', { user_id: userId });
            set({ inheritanceSim: response.data?.data || response.data, isLoading: false });
            return true;
        } catch (error) {
            console.error('Failed to run simulation:', error);
            set({ error: error.message, isLoading: false });
            return false;
        }
    },

    // Actions - Heartbeat / Dead Man's Switch
    confirmAlive: async () => {
        try {
            await apiClient.post('/estate/heartbeat/confirm');
            const response = await apiClient.get('/estate/heartbeat');
            set({ heartbeatStatus: response.data?.data || response.data });
        } catch (error) {
            console.error('Confirm alive failed:', error);
        }
    },

    // Actions - Entity Graph
    fetchEntityGraph: async () => {
        try {
            const response = await apiClient.get('/estate/graph');
            set({ entityGraph: response.data?.data || response.data || { nodes: [], edges: [] } });
        } catch (error) {
            console.error('Failed to fetch entity graph:', error);
        }
    },

    reset: () => set({
        estatePlan: null,
        beneficiaries: [], 
        inheritanceSim: null,
        heartbeatStatus: { lastCheck: null, isAlive: true, daysUntilTrigger: 30, triggerDate: null },
        entityGraph: { nodes: [], edges: [] },
        isLoading: false,
        error: null
    })
}));

export default useEstateStore;
