/**
 * ==============================================================================
 * FILE: frontend2/src/stores/smsStore.js
 * ROLE: State Management
 * PURPOSE: Manages SMS alert preferences.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useSMSStore = create((set) => ({
    sending: false,
    lastResult: null,
    error: null,
    preferences: {
        priceSpikes: true,
        tradeExecutions: true,
        systemHealth: false
    },

    sendTestAlert: async (phoneNumber, mock = true) => {
        set({ sending: true, lastResult: null, error: null });
        try {
            const response = await apiClient.post('/notifications/twilio/send', 
                { to: phoneNumber, message: "Test alert from User Settings." },
                { params: { mock } }
            );
            set({ lastResult: response.data, sending: false });
            return response.data;
        } catch (error) {
            console.error('SMS send failed:', error);
            set({ error: error.message, sending: false });
        }
    },

    updatePreferences: async (phoneNumber, prefs, mock = true) => {
        try {
            await apiClient.post('/notifications/twilio/subscribe', 
                { phone: phoneNumber, preferences: prefs },
                { params: { mock } }
            );
            set({ preferences: prefs });
        } catch (error) {
            console.error('Update SMS preferences failed:', error);
        }
    }
}));

export default useSMSStore;
