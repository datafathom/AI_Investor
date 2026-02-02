/**
 * ==============================================================================
 * FILE: frontend2/src/stores/emailStore.js
 * ROLE: State Management
 * PURPOSE: Manages Email alert preferences and test sends.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useEmailStore = create((set) => ({
    sending: false,
    lastResult: null,
    error: null,
    preferences: {
        dailyBriefing: true,
        weeklySummary: true,
        monthlyPerformance: true,
        securityAlerts: true
    },

    sendTestEmail: async (email, mock = true) => {
        set({ sending: true, lastResult: null, error: null });
        try {
            const response = await apiClient.post('/notifications/email/send', 
                { 
                    to: email, 
                    subject: "AI Investor: Test Email",
                    content: "This is a test email sent from the Settings dashboard."
                },
                { params: { mock } }
            );
            
            set({ lastResult: response.data, sending: false });
            return response.data;
        } catch (error) {
            console.error('Email send failed:', error);
            set({ error: error.message, sending: false });
        }
    },

    updatePreferences: async (email, prefs, mock = true) => {
        try {
            await apiClient.post('/notifications/email/subscribe', 
                { email, preferences: prefs },
                { params: { mock } }
            );
            set({ preferences: prefs });
        } catch (error) {
            console.error('Update preferences failed:', error);
        }
    }
}));

export default useEmailStore;
