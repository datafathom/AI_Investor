/**
 * ==============================================================================
 * FILE: frontend2/src/stores/newsStore.js
 * ROLE: State Management
 * PURPOSE: Manages global news state, including headlines, analyzed topics,
 *          and sentiment indicators.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/news/headlines: Market sentiment endpoint
 *     - /api/v1/news/analyze/{topic}: Keyword sentiment endpoint
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useNewsStore = create((set, get) => ({
    // State
    headlines: [],
    marketSentiment: { average_score: 0, label: 'NEUTRAL', count: 0 },
    sectorSentiment: [],
    analyzedTopics: {}, // keyed by topic
    
    loading: {
        headlines: false,
        topics: false
    },
    
    error: null,

    // Actions
    fetchHeadlines: async (mock = false) => {
        set((state) => ({ loading: { ...state.loading, headlines: true }, error: null }));
        try {
            const response = await apiClient.get('/news/headlines', { params: mock ? { mock: true } : {} });
            const data = response.data;
            set({ 
                headlines: data.top_news || [],
                marketSentiment: {
                    average_score: data.average_score,
                    label: data.label,
                    count: data.count
                },
                loading: { ...get().loading, headlines: false }
            });
        } catch (error) {
            console.error('Fetch headlines failed:', error);
            set({ error: error.message, loading: { ...get().loading, headlines: false } });
        }
    },

    analyzeTopic: async (topic, mock = false) => {
        const lowerTopic = topic.toLowerCase();
        set((state) => ({ loading: { ...state.loading, topics: true }, error: null }));
        try {
            const response = await apiClient.get(`/news/analyze/${topic}`, { params: mock ? { mock: true } : {} });
            set((state) => ({
                analyzedTopics: { ...state.analyzedTopics, [lowerTopic]: response.data },
                loading: { ...state.loading, topics: false }
            }));
        } catch (error) {
            console.error(`Analyze topic ${topic} failed:`, error);
            set({ error: error.message, loading: { ...get().loading, topics: false } });
        }
    },

    fetchSectorSentiment: async () => {
        set((state) => ({ loading: { ...state.loading, sectors: true }, error: null }));
        try {
            const response = await apiClient.get('/news/sectors');
            set({ 
                sectorSentiment: response.data,
                loading: { ...get().loading, sectors: false }
            });
        } catch (error) {
            console.error('Fetch sector sentiment failed:', error);
            set({ error: error.message, loading: { ...get().loading, sectors: false } });
        }
    },

    clearHistory: () => set({ analyzedTopics: {}, error: null })
}));

export default useNewsStore;
