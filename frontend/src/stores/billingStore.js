/**
 * ==============================================================================
 * FILE: frontend2/src/stores/billingStore.js
 * ROLE: State Management
 * PURPOSE: Manages subscription state and checkout flows.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useBillingStore = create((set, get) => ({
    subscription: null,
    bills: [],
    upcomingBills: [],
    paymentHistory: [],
    loading: false,
    error: null,

    fetchSubscription: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/billing/subscription', { params: { mock } });
            set({ subscription: response.data, loading: false });
        } catch (error) {
            console.error('Fetch subscription failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    fetchBills: async (userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            const [billsRes, upcomingRes, historyRes] = await Promise.all([
                apiClient.get('/billing/bills', { params: { user_id: userId } }),
                apiClient.get('/billing/upcoming', { params: { user_id: userId } }),
                apiClient.get('/billing/history', { params: { user_id: userId, limit: 20 } })
            ]);

            set({ 
                bills: billsRes.data.data || [], 
                upcomingBills: upcomingRes.data.data || [], 
                paymentHistory: historyRes.data.data || [],
                loading: false 
            });
        } catch (error) {
            console.error('Fetch bills failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    addBill: async (billData) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/billing/bill/add', billData);
            await get().fetchBills(billData.user_id);
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    schedulePayment: async (billId, userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/billing/payment/schedule', { 
                bill_id: billId,
                payment_date: new Date().toISOString().split('T')[0]
            });
            await get().fetchBills(userId);
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    createCheckout: async (planId, mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.post('/billing/checkout', 
                { plan_id: planId },
                { params: { mock } }
            );

            return response.data.url; 

        } catch (error) {
            console.error('Checkout failed:', error);
            set({ error: error.message, loading: false });
            return null;
        } finally {
             set({ loading: false });
        }
    }
}));

export default useBillingStore;
