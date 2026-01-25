/**
 * Philanthropy Store - Zustand State Management for ESG & Donations
 * Phase 61: Manages ESG scores, donation routing, and carbon footprint.
 */
import { create } from 'zustand';

const usePhilanthropyStore = create((set, get) => ({
    // State
    esgScore: { e: 0, s: 0, g: 0, total: 0 },
    carbonFootprint: { tons: 0, percentile: 0, offset: 0 },
    donationHistory: [],
    excessAlpha: 0,
    charities: [],
    autoRouteEnabled: false,
    error: null,
    
    // Actions
    setEsgScore: (score) => set({ esgScore: score }),
    setCarbonFootprint: (footprint) => set({ carbonFootprint: footprint }),
    setDonationHistory: (history) => set({ donationHistory: history }),
    addDonation: (donation) => set((s) => ({ donationHistory: [donation, ...s.donationHistory] })),
    setExcessAlpha: (alpha) => set({ excessAlpha: alpha }),
    setCharities: (charities) => set({ charities: charities }),
    toggleAutoRoute: (enabled) => set({ autoRouteEnabled: enabled }),
    setError: (error) => set({ error }),
    
    // Async: Donate
    executeDonation: async (charityId, amount) => {
        try {
            const response = await fetch('/api/v1/philanthropy/donate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ charity_id: charityId, amount })
            });
            if (!response.ok) throw new Error('Donation failed');
            const data = await response.json();
            set((s) => ({ donationHistory: [data.receipt, ...s.donationHistory], excessAlpha: s.excessAlpha - amount }));
            return data;
        } catch (error) {
            console.error('Donation error:', error);
            set({ error: error.message });
            throw error;
        }
    },
    
    reset: () => set({
        esgScore: { e: 0, s: 0, g: 0, total: 0 }, carbonFootprint: { tons: 0, percentile: 0, offset: 0 },
        donationHistory: [], excessAlpha: 0, charities: [], autoRouteEnabled: false, error: null
    })
}));

export default usePhilanthropyStore;
