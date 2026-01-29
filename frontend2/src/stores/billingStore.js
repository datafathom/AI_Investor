/**
 * ==============================================================================
 * FILE: frontend2/src/stores/billingStore.js
 * ROLE: State Management
 * PURPOSE: Manages subscription state and checkout flows.
 * ==============================================================================
 */

import { create } from 'zustand';

const useBillingStore = create((set) => ({
    subscription: null,
    bills: [],
    upcomingBills: [],
    paymentHistory: [],
    loading: false,
    error: null,

    fetchSubscription: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            // Note: Reconciling endpoint to standardized path
            const response = await fetch(`/api/v1/billing/subscription?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch subscription');
            const data = await response.json();
            set({ subscription: data, loading: false });
        } catch (error) {
            console.error('Fetch subscription failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    fetchBills: async (userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            const [billsRes, upcomingRes, historyRes] = await Promise.all([
                fetch(`/api/v1/billing/bills?user_id=${userId}`),
                fetch(`/api/v1/billing/upcoming?user_id=${userId}`),
                fetch(`/api/v1/billing/history?user_id=${userId}&limit=20`)
            ]);

            const [billsData, upcomingData, historyData] = await Promise.all([
                billsRes.json(),
                upcomingRes.json(),
                historyRes.json()
            ]);

            set({ 
                bills: billsData.data || [], 
                upcomingBills: upcomingData.data || [], 
                paymentHistory: historyData.data || [],
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
            const response = await fetch('/api/v1/billing/bill/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(billData)
            });
            if (!response.ok) throw new Error('Failed to add bill');
            await get().fetchBills(billData.user_id);
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    schedulePayment: async (billId, userId = 'user_1') => {
        set({ loading: true, error: null });
        try {
            const response = await fetch('/api/v1/billing/payment/schedule', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    bill_id: billId,
                    payment_date: new Date().toISOString().split('T')[0]
                })
            });
            if (!response.ok) throw new Error('Failed to schedule payment');
            await get().fetchBills(userId);
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    createCheckout: async (planId, mock = true) => {
        set({ loading: true, error: null });
        try {
            const url = `/api/v1/billing/checkout?mock=${mock}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ plan_id: planId })
            });

            if (!response.ok) throw new Error('Checkout creation failed');

            const data = await response.json();
            // In a real app, we would redirect: window.location.href = data.url;
            return data.url; 

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
