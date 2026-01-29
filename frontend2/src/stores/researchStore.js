import { create } from 'zustand';
import researchService from '../services/researchService';

const useResearchStore = create((set, get) => ({
    // Shared State
    isLoading: false,
    error: null,

    // Research Reports State (Phase 18)
    reports: [],
    templates: [],

    // AI Research State (Existing)
    history: [],
    
    // Actions - Research Reports
    fetchReports: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const data = await researchService.getReports(userId);
            set({ reports: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch reports:', error);
        }
    },

    fetchTemplates: async () => {
        set({ isLoading: true, error: null });
        try {
            const data = await researchService.getTemplates();
            set({ templates: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch templates:', error);
        }
    },

    generateReport: async (userId, templateId, title, format) => {
        set({ isLoading: true, error: null });
        try {
            await researchService.generateReport({
                user_id: userId,
                template_id: templateId,
                report_title: title,
                format
            });
            // Refresh list
            await get().fetchReports(userId);
            set({ isLoading: false });
            return true;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to generate report:', error);
            return false;
        }
    },

    // Actions - AI Research
    askQuestion: async (query, mock = true) => {
        set({ isLoading: true, error: null });
        try {
            const data = await researchService.askQuestion(query, mock);
            
            const newEntry = {
                id: Date.now(),
                query: query,
                answer: data.answer,
                citations: data.citations || [],
                timestamp: new Date().toLocaleTimeString()
            };
            
            set((state) => ({ 
                history: [newEntry, ...state.history],
                isLoading: false 
            }));
        } catch (error) {
            console.error('Research query failed:', error);
            set({ error: error.message, isLoading: false });
        }
    },

    clearHistory: () => set({ history: [] })
}));

export default useResearchStore;
