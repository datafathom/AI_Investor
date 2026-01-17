/**
 * debateService.js
 * 
 * Handles API calls to the Debate Chamber.
 */

import axios from 'axios';

const API_URL = '/api/v1/analysis/debate';

export const debateService = {
    /**
     * Triggers an AI committee debate for a ticker.
     * @param {string} ticker 
     * @param {string} summary 
     */
    triggerDebate: async (ticker, summary) => {
        try {
            const response = await axios.post(API_URL, { ticker, summary });
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
            const response = await axios.get(`${API_URL}/status`);
            return response.data;
        } catch (error) {
            console.error('Error getting debate status:', error);
            throw error;
        }
    }
};

export default debateService;
