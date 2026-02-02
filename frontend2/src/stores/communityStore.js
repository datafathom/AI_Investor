/**
 * Community Store - Phase 22
 * Manages community forums and expert Q&A
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useCommunityStore = create((set, get) => ({
    // State
    threads: [],
    expertQuestions: [],
    loading: false,
    error: null,

    // Actions
    fetchThreads: async (category = '') => {
        set({ loading: true, error: null });
        try {
            const params = category ? { category } : {};
            const response = await apiClient.get('/community/threads', { params });
            set({ threads: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    fetchExpertQuestions: async (userId) => {
        set({ loading: true, error: null });
        try {
            const response = await apiClient.get('/community/expert/questions', {
                params: { user_id: userId }
            });
            set({ expertQuestions: response.data?.data || response.data || [], loading: false });
        } catch (error) {
            set({ error: error.message, loading: false });
        }
    },

    createThread: async (threadData) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post('/community/thread/create', threadData);
            await get().fetchThreads();
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    },

    replyToThread: async (threadId, replyData) => {
        set({ loading: true, error: null });
        try {
            await apiClient.post(`/community/thread/${threadId}/reply`, replyData);
            set({ loading: false });
            return true;
        } catch (error) {
            set({ error: error.message, loading: false });
            return false;
        }
    },

    upvoteThread: async (threadId, userId) => {
        try {
            await apiClient.post(`/community/thread/${threadId}/upvote`, { user_id: userId });
            return true;
        } catch (error) {
            set({ error: error.message });
            return false;
        }
    }
}));

export default useCommunityStore;
