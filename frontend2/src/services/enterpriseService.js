/**
 * Enterprise Service
 * Phase 31: API integration for Enterprise Features & Multi-User Support
 */
import apiClient from './apiClient';

const BASE_URL = '/enterprise';

export const enterpriseService = {
    /**
     * Get user's teams
     * @param {string} userId
     */
    getTeams: async (userId) => {
        const response = await apiClient.get(`${BASE_URL}/teams`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Get user's organizations
     * @param {string} userId
     */
    getOrganizations: async (userId) => {
        const response = await apiClient.get(`${BASE_URL}/organizations`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Get shared portfolios
     * @param {string} userId
     */
    getSharedPortfolios: async (userId) => {
        const response = await apiClient.get(`${BASE_URL}/shared-portfolios`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Create a new team
     * @param {Object} data { user_id, team_name, description }
     */
    createTeam: async (data) => {
        const response = await apiClient.post(`${BASE_URL}/team/create`, data);
        return response.data;
    },

    /**
     * Share a portfolio with a team
     * @param {Object} data { portfolio_id, team_id }
     */
    sharePortfolio: async (data) => {
        const response = await apiClient.post(`${BASE_URL}/portfolio/share`, data);
        return response.data;
    }
};

export default enterpriseService;
