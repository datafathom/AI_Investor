/**
 * ==============================================================================
 * FILE: frontend2/src/stores/debateStore.js
 * ROLE: State Management
 * PURPOSE: Manages debate progress, messages, and consensus state.
 * ==============================================================================
 */

import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useDebateStore = create((set) => ({
    debateResult: null,
    loading: false,
    error: null,

    runDebate: async (ticker, mock = true) => {
        set({ loading: true, error: null, debateResult: null });
        try {
            const response = await apiClient.post(`/ai/debate/run/${ticker}`, null, {
                params: { mock }
            });
            
            set({ 
                debateResult: response.data,
                loading: false 
            });
        } catch (error) {
            console.error('Debate simulation failed:', error);
            set({ error: error.message, loading: false });
        }
    },
    
    resetDebate: () => set({ debateResult: null, error: null })
}));

export default useDebateStore;
