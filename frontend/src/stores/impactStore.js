/**
 * Impact Store - Zustand State Management for Philanthropy & ESG
 * Phase 61: Manages donation routing, ESG scores, and carbon tracking.
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useImpactStore = create((set, get) => ({
    // State
    esgScores: null,
    carbonData: null,
    donationHistory: [],
    enoughThreshold: 3000000,
    currentNetWorth: 3247500, // Mocked for now, should come from portfolio store
    allocations: [
        { category: 'Climate', percentage: 40 },
        { category: 'Education', percentage: 35 },
        { category: 'Health', percentage: 25 }
    ],
    isLoading: false,
    error: null,

    // Actions
    setThreshold: (val) => set({ enoughThreshold: val }),
    setAllocations: (allocs) => set({ allocations: allocs }),
    
    // Async Actions
    fetchESGData: async () => {
        set({ isLoading: true });
        try {
            const response = await apiClient.get('/philanthropy/esg');
            set({ esgScores: response.data, isLoading: false });
        } catch (error) {
            set({ error: 'Failed to fetch ESG data', isLoading: false });
        }
    },

    fetchCarbonData: async () => {
        set({ isLoading: true });
        try {
            const val = get().currentNetWorth;
            const response = await apiClient.get('/philanthropy/carbon', { params: { value: val } });
            set({ carbonData: response.data, isLoading: false });
        } catch (error) {
            console.error(error);
            set({ isLoading: false });
        }
    },

    fetchDonationHistory: async () => {
        try {
            const response = await apiClient.get('/philanthropy/history');
            set({ donationHistory: response.data });
        } catch (error) {
            console.error(error);
        }
    },

    triggerDonation: async (amount) => {
        set({ isLoading: true });
        try {
            const { allocations } = get();
            const response = await apiClient.post('/philanthropy/donate', { amount, allocations });
            
            // Refresh history
            get().fetchDonationHistory();
            set({ isLoading: false });
            return response.data;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            return null;
        }
    }
}));

export default useImpactStore;
