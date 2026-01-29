/**
 * ==============================================================================
 * FILE: frontend2/src/services/evolutionService.js
 * ROLE: Genetic Conduit
 * PURPOSE: 
 *   Interface with the /api/v1/evolution endpoint to start and monitor 
 *   strategy discovery.
 * ==============================================================================
 */

import apiClient from './apiClient';

export const evolutionService = {
    /**
     * Start a new evolution process.
     */
    async startEvolution() {
        try {
            return await apiClient.post('/evolution/start');
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
            return await apiClient.get('/evolution/status');
        } catch (error) {
            console.error('Error fetching evolution status:', error);
            throw error;
        }
    }
};

export default evolutionService;
