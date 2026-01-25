/**
 * ==============================================================================
 * FILE: frontend2/src/stores/smsStore.js
 * ROLE: State Management
 * PURPOSE: Manages SMS alert preferences.
 * ==============================================================================
 */

import { create } from 'zustand';

const useSMSStore = create((set) => ({
    sending: false,
    lastResult: null,
    error: null,

    sendTestAlert: async (phoneNumber, mock = true) => {
        set({ sending: true, lastResult: null, error: null });
        try {
            const response = await fetch(`/api/v1/notifications/twilio/send?mock=${mock}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ to: phoneNumber, message: "Test alert from User Settings." })
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to send SMS');
            
            set({ lastResult: data, sending: false });
            return data;
        } catch (error) {
            console.error('SMS send failed:', error);
            set({ error: error.message, sending: false });
        }
    }
}));

export default useSMSStore;
