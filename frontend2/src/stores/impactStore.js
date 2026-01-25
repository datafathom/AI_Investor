/**
 * Impact Store - Zustand State Management for Philanthropy & ESG
 * Phase 61: Manages donation routing, ESG scores, and carbon tracking.
 */
import { create } from 'zustand';

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
            const response = await fetch('/api/v1/philanthropy/esg');
            const data = await response.json();
            set({ esgScores: data, isLoading: false });
        } catch (error) {
            set({ error: 'Failed to fetch ESG data', isLoading: false });
        }
    },

    fetchCarbonData: async () => {
        set({ isLoading: true });
        try {
            const val = get().currentNetWorth;
            const response = await fetch(`/api/v1/philanthropy/carbon?value=${val}`);
            const data = await response.json();
            set({ carbonData: data, isLoading: false });
        } catch (error) {
            console.error(error);
            set({ isLoading: false });
        }
    },

    fetchDonationHistory: async () => {
        try {
            const response = await fetch('/api/v1/philanthropy/history');
            const data = await response.json();
            set({ donationHistory: data });
        } catch (error) {
            console.error(error);
        }
    },

    triggerDonation: async (amount) => {
        set({ isLoading: true });
        try {
            const { allocations } = get();
            const response = await fetch('/api/v1/philanthropy/donate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ amount, allocations })
            });
            const result = await response.json();
            
            // Refresh history
            get().fetchDonationHistory();
            set({ isLoading: false });
            return result;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            return null;
        }
    }
}));

export default useImpactStore;
