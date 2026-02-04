/**
 * Charting Store - 
 * Manages advanced charting data and indicators
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useChartingStore = create((set) => ({
    // State
    chartData: [],
    indicators: [],
    patterns: [],
    loading: false,
    error: null,

    // Actions
    fetchChartData: async (params) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/charting/data', { params });
            set({ chartData: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchIndicators: async (params) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/charting/indicators', { params });
            set({ indicators: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchPatterns: async (params) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/charting/patterns', { params });
            set({ patterns: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    }
}));

export default useChartingStore;
