/**
 * ==============================================================================
 * FILE: frontend2/src/services/evolutionService.js
 * ROLE: Genetic Conduit
 * PURPOSE: 
 *   Interface with the /api/v1/evolution endpoint to start and monitor 
 *   strategy discovery.
 * ==============================================================================
 */

import axios from 'axios';

const API_BASE_URL = '/api/v1/evolution';

export const evolutionService = {
    /**
     * Start a new evolution process.
     */
    async startEvolution() {
        try {
            const response = await axios.post(`${API_BASE_URL}/start`);
            return response.data;
        } catch (error) {
            console.error('Error starting evolution:', error);
            throw error;
        }
    },

    /**
     * Fetch the current status and history of the evolution.
     */
    async getStatus() {
        try {
            const response = await axios.get(`${API_BASE_URL}/status`);
            return response.data;
        } catch (error) {
            console.error('Error fetching evolution status:', error);
            throw error;
        }
    }
};

export default evolutionService;
