/**
 * debateService.js
 * 
 * Handles API calls to the Debate Chamber.
 */

import apiClient from './apiClient';

export const debateService = {
    /**
     * Triggers an AI committee debate for a ticker.
     * @param {string} ticker 
     * @param {string} summary 
     */
    triggerDebate: async (ticker, summary) => {
        try {
            const response = await apiClient.post('/analysis/debate', { ticker, summary });
            return response.data;
        } catch (error) {
            console.error('Error triggering debate:', error);
            throw error;
        }
    },

    /**
     * Gets the status of the debate chamber.
     */
    getStatus: async () => {
        try {
            const response = await apiClient.get('/analysis/debate/status');
            return response.data;
        } catch (error) {
            console.error('Error getting debate status:', error);
            throw error;
        }
    }
};

export default debateService;
