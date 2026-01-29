import { create } from 'zustand';
import enterpriseService from '../services/enterpriseService';

const useEnterpriseStore = create((set, get) => ({
    // State
    teams: [],
    organizations: [],
    sharedPortfolios: [],
    isLoading: false,
    error: null,
    
    // Actions
    
    fetchTeams: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const data = await enterpriseService.getTeams(userId);
            set({ teams: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch teams:', error);
        }
    },

    fetchOrganizations: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const data = await enterpriseService.getOrganizations(userId);
            set({ organizations: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch organizations:', error);
        }
    },

    fetchSharedPortfolios: async (userId) => {
        set({ isLoading: true, error: null });
        try {
            const data = await enterpriseService.getSharedPortfolios(userId);
            set({ sharedPortfolios: data || [], isLoading: false });
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to fetch shared portfolios:', error);
        }
    },

    createTeam: async (userId, teamName, description) => {
        set({ isLoading: true, error: null });
        try {
            await enterpriseService.createTeam({
                user_id: userId,
                team_name: teamName,
                description
            });
            // Refresh list
            await get().fetchTeams(userId);
            set({ isLoading: false });
            return true;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to create team:', error);
            return false;
        }
    },

    sharePortfolio: async (userId, portfolioId, teamId) => {
        set({ isLoading: true, error: null });
        try {
            await enterpriseService.sharePortfolio({
                portfolio_id: portfolioId,
                team_id: teamId
            });
            // Refresh list
            await get().fetchSharedPortfolios(userId);
            set({ isLoading: false });
            return true;
        } catch (error) {
            set({ error: error.message, isLoading: false });
            console.error('Failed to share portfolio:', error);
            return false;
        }
    },

    clearError: () => set({ error: null })
}));

export default useEnterpriseStore;
