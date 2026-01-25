/**
 * ==============================================================================
 * FILE: frontend2/src/stores/researchStore.js
 * ROLE: State Management
 * PURPOSE: Manages research query history and active answers.
 * ==============================================================================
 */

import { create } from 'zustand';

const useResearchStore = create((set, _get) => ({
    history: [],
    loading: false,
    error: null,

    askQuestion: async (query, mock = true) => {
        set({ loading: true, error: null });
        
        try {
            const url = `/api/v1/ai/research/ask?mock=${mock}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });
            
            if (!response.ok) throw new Error('Research query failed');
            
            const data = await response.json();
            
            // Add to history
            const newEntry = {
                id: Date.now(),
                query: query,
                answer: data.answer,
                citations: data.citations || [],
                timestamp: new Date().toLocaleTimeString()
            };
            
            set((state) => ({ 
                history: [newEntry, ...state.history],
                loading: false 
            }));
            
        } catch (error) {
            console.error('Research failed:', error);
            set({ error: error.message, loading: false });
        }
    },
    
    clearHistory: () => set({ history: [] })
}));

export default useResearchStore;
