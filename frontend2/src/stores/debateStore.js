/**
 * ==============================================================================
 * FILE: frontend2/src/stores/debateStore.js
 * ROLE: State Management
 * PURPOSE: Manages debate progress, messages, and consensus state.
 * ==============================================================================
 */

import { create } from 'zustand';

const useDebateStore = create((set) => ({
    debateResult: null,
    loading: false,
    error: null,

    runDebate: async (ticker, mock = true) => {
        set({ loading: true, error: null, debateResult: null });
        try {
            const url = `/api/v1/ai/debate/run/${ticker}?mock=${mock}`;
            const response = await fetch(url, { method: 'POST' });
            
            if (!response.ok) throw new Error('Failed to run debate simulation');
            
            const data = await response.json();
            set({ 
                debateResult: data,
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
