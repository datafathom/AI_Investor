/**
 * ==============================================================================
 * FILE: frontend2/src/stores/slackStore.js
 * ROLE: State Management
 * PURPOSE: Manages Slack channels and messaging.
 * ==============================================================================
 */

import { create } from 'zustand';

const useSlackStore = create((set) => ({
    channels: [],
    loading: false,
    posting: false,
    error: null,
    lastMessage: null,

    fetchChannels: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await fetch(`/api/v1/team/slack/channels?mock=${mock}`);
            if (!response.ok) throw new Error('Failed to fetch channels');
            const data = await response.json();
            set({ channels: data, loading: false });
        } catch (error) {
            console.error('Fetch channels failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    postMessage: async (channel, text, mock = true) => {
        set({ posting: true, error: null });
        try {
            const response = await fetch(`/api/v1/team/slack/message?mock=${mock}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ channel, text })
            });
            
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to post message');
            
            set({ lastMessage: data, posting: false });
            return data;
        } catch (error) {
            console.error('Post message failed:', error);
            set({ error: error.message, posting: false });
        }
    }
}));

export default useSlackStore;
