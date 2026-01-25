/**
 * ==============================================================================
 * FILE: frontend2/src/stores/socialStore.js
 * ROLE: State Management
 * PURPOSE: Manages Reddit posts and sentiment data.
 * ==============================================================================
 */

import { create } from 'zustand';

const useSocialStore = create((set, get) => ({
    posts: [],
    sentimentData: {}, // { "NVDA": { score, label, hype } }
    loading: {
        posts: false,
        sentiment: false
    },
    error: null,

    fetchPosts: async (subreddit = 'wallstreetbets', limit = 10, mock = true) => {
        set((state) => ({ loading: { ...state.loading, posts: true }, error: null }));
        try {
            const url = `/api/v1/social/reddit/posts?subreddit=${subreddit}&limit=${limit}&mock=${mock}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error('Failed to fetch reddit posts');
            
            const data = await response.json();
            set({ 
                posts: data,
                loading: { ...get().loading, posts: false }
            });
        } catch (error) {
            console.error('Fetch reddit posts failed:', error);
            set({ error: error.message, loading: { ...get().loading, posts: false } });
        }
    },

    analyzeSentiment: async (ticker, mock = true) => {
        set((state) => ({ loading: { ...state.loading, sentiment: true }, error: null }));
        try {
            const url = `/api/v1/social/reddit/analyze/${ticker}?mock=${mock}`;
            const response = await fetch(url);
            if (!response.ok) throw new Error(`Failed to analyze sentiment for ${ticker}`);
            
            const data = await response.json();
            set((state) => ({
                sentimentData: { ...state.sentimentData, [ticker]: data },
                loading: { ...state.loading, sentiment: false }
            }));
        } catch (error) {
            console.error(`Analyze sentiment ${ticker} failed:`, error);
            set({ error: error.message, loading: { ...get().loading, sentiment: false } });
        }
    }
}));

export default useSocialStore;
