/**
 * ==============================================================================
 * FILE: frontend2/src/stores/emailStore.js
 * ROLE: State Management
 * PURPOSE: Manages Email alert preferences and test sends.
 * ==============================================================================
 */

import { create } from 'zustand';

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
            const response = await fetch(`/api/v1/notifications/email/send?mock=${mock}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    to: email, 
                    subject: "AI Investor: Test Email",
                    content: "This is a test email sent from the Settings dashboard."
                })
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to send email');
            
            set({ lastResult: data, sending: false });
            return data;
        } catch (error) {
            console.error('Email send failed:', error);
            set({ error: error.message, sending: false });
        }
    },

    updatePreferences: async (email, prefs, mock = true) => {
        try {
             await fetch(`/api/v1/notifications/email/subscribe?mock=${mock}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, preferences: prefs })
            });
            set({ preferences: prefs });
        } catch (error) {
            console.error('Update preferences failed:', error);
        }
    }
}));

export default useEmailStore;
