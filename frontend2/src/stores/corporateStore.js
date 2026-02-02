/**
 * Corporate Store - Zustand State Management for Corporate Actions
 * Phase 63: Manages earnings calendar, DRIP, and corporate actions.
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useCorporateStore = create((set, get) => ({
    // State
    earningsCalendar: [],
    corporateActions: [],
    upcomingIPOs: [],
    dripSettings: { enabled: false, reinvestDividends: true, reinvestCapGains: true },
    upcomingDividends: [],
    loading: { earnings: false, actions: false, ipos: false },
    error: null,
    
    // Actions
    setEarningsCalendar: (calendar) => set({ earningsCalendar: calendar }),
    setCorporateActions: (actions) => set({ corporateActions: actions }),
    setDripSettings: (settings) => set((s) => ({ dripSettings: { ...s.dripSettings, ...settings } })),
    setUpcomingDividends: (dividends) => set({ upcomingDividends: dividends }),
    setError: (error) => set({ error }),
    
    // Async: Fetch earnings
    fetchEarnings: async (days = 30) => {
        set((s) => ({ loading: { ...s.loading, earnings: true } }));
        try {
            const response = await apiClient.get('/corporate/earnings', { params: { days } });
            set({ earningsCalendar: response.data || [], loading: { ...get().loading, earnings: false } });
        } catch (error) {
            console.error('Fetch earnings failed:', error);
            set({ error: error.message, loading: { ...get().loading, earnings: false } });
        }
    },

    // Async: Fetch Upcoming IPOs
    fetchUpcomingIPOs: async (days = 30, mock = false) => {
        set((s) => ({ loading: { ...s.loading, ipos: true } }));
        try {
            const params = { days };
            if (mock) params.mock = 'true';
            
            const response = await apiClient.get('/corporate/ipo/upcoming', { params });
            set({ upcomingIPOs: response.data || [], loading: { ...get().loading, ipos: false } });
        } catch (error) {
            console.error('Fetch IPOs failed:', error);
            set({ error: error.message, loading: { ...get().loading, ipos: false } });
        }
    },
    
    // Async: Toggle DRIP
    toggleDrip: async (enabled) => {
        try {
            await apiClient.post('/corporate/drip', { enabled });
            set((s) => ({ dripSettings: { ...s.dripSettings, enabled } }));
        } catch (error) {
            console.error('Toggle DRIP failed:', error);
        }
    },
    
    reset: () => set({
        earningsCalendar: [], corporateActions: [],
        dripSettings: { enabled: false, reinvestDividends: true, reinvestCapGains: true },
        upcomingDividends: [], error: null
    })
}));

export default useCorporateStore;
