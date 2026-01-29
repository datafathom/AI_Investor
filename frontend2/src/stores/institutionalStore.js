import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useInstitutionalStore = create((set, get) => ({
    clients: [],
    analytics: {}, // client_id -> analytics
    revenueForecast: null,
    riskLevels: {}, // client_id -> risk data
    signatures: {}, // client_id -> signature data
    assetAllocation: {}, // client_id -> allocation data
    loading: false,
    error: null,
    onboardingStep: 1,

    fetchClients: async () => {
        set({ loading: true, error: null });
        try {
            const data = await apiClient.get('/institutional/clients');
            set({ clients: data.data, loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchClientAnalytics: async (clientId) => {
        set({ loading: true, error: null });
        try {
            const data = await apiClient.get(`/institutional/analytics/${clientId}`);
            set(state => ({
                analytics: { ...state.analytics, [clientId]: data.data },
                loading: false
            }));
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchRevenueForecast: async (clientId = null) => {
        set({ loading: true, error: null });
        try {
            const endpoint = clientId ? `/institutional/analytics/fees?client_id=${clientId}` : '/institutional/analytics/fees';
            const data = await apiClient.get(endpoint);
            set({ revenueForecast: data.data, loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchRiskLevels: async (clientId) => {
        set({ loading: true, error: null });
        try {
            const data = await apiClient.get(`/institutional/analytics/risk/${clientId}`);
            set(state => ({
                riskLevels: { ...state.riskLevels, [clientId]: data.data },
                loading: false
            }));
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchSignatures: async (clientId) => {
        set({ loading: true, error: null });
        try {
            const data = await apiClient.get(`/institutional/analytics/signatures/${clientId}`);
            set(state => ({
                signatures: { ...state.signatures, [clientId]: data.data },
                loading: false
            }));
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchAssetAllocation: async (clientId) => {
        set({ loading: true, error: null });
        try {
            const data = await apiClient.get(`/institutional/analytics/allocation/${clientId}`);
            set(state => ({
                assetAllocation: { ...state.assetAllocation, [clientId]: data.data },
                loading: false
            }));
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    createClient: async (clientData) => {
        set({ loading: true, error: null });
        try {
            const data = await apiClient.post('/institutional/client/create', clientData);
            set(state => ({
                clients: [...state.clients, data.data],
                loading: false
            }));
            return data.data;
        } catch (error) {
            set({ error: error.message, loading: false });
            return null;
        }
    },

    setOnboardingStep: (step) => set({ onboardingStep: step }),

    resetOnboarding: () => set({ onboardingStep: 1 })
}));

export default useInstitutionalStore;
