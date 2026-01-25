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
    loading: false,
    error: null,

    fetchSubscription: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const url = `/api/v1/billing/subscription?mock=${mock}`;
            const response = await fetch(url);
            
            if (!response.ok) throw new Error('Failed to fetch subscription');
            
            const data = await response.json();
            set({ 
                subscription: data,
                loading: false 
            });
        } catch (error) {
            console.error('Fetch subscription failed:', error);
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
