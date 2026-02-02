/**
 * Advanced Orders Store - Phase 13
 * Manages advanced order types and smart execution
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useAdvancedOrdersStore = create((set, get) => ({
    // State
    orders: [],
    templates: [],
    loading: false,
    error: null,

    // Actions
    fetchOrders: async (userId) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/advanced-orders/orders', {
                params: { user_id: userId }
            });
            set({ orders: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchTemplates: async () => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/advanced-orders/templates');
            set({ templates: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    placeOrder: async (orderData) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/advanced-orders/place', orderData);
            await get().fetchOrders(orderData.user_id);
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    },

    executeTWAP: async (params) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/advanced-orders/execute/twap', params);
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    },

    executeVWAP: async (params) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/advanced-orders/execute/vwap', params);
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    }
}));

export default useAdvancedOrdersStore;
