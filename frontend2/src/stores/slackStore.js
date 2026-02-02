/**
 * ==============================================================================
 * FILE: frontend2/src/stores/slackStore.js
 * ROLE: State Management
 * PURPOSE: Manages Slack channels and messaging.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useSlackStore = create((set) => ({
    channels: [],
    loading: false,
    posting: false,
    error: null,
    lastMessage: null,

    fetchChannels: async (mock = true) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/team/slack/channels', { params: { mock } });
            set({ channels: response.data, loading: false });
        } catch (error) {
            console.error('Fetch channels failed:', error);
            set({ error: error.message, loading: false });
        }
    },

    postMessage: async (channel, text, mock = true) => {
        set({ posting: true, error: null });
        try {
            const response = await apiClient.post('/team/slack/message', { channel, text }, { params: { mock } });
            set({ lastMessage: response.data, posting: false });
            return response.data;
        } catch (error) {
            console.error('Post message failed:', error);
            set({ error: error.message, posting: false });
        }
    }
}));

export default useSlackStore;
