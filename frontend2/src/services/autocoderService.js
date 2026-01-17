/**
 * autocoderService.js
 * 
 * Client-side service for AI code generation and deployment.
 */

import axios from 'axios';

const API_BASE = '/api/v1/dev';

export const autocoderService = {
    generateCode: async (task) => {
        try {
            const response = await axios.post(`${API_BASE}/generate`, { task });
            return response.data;
        } catch (error) {
            console.error('Error generating code:', error);
            throw error;
        }
    },

    validateCode: async (code) => {
        try {
            const response = await axios.post(`${API_BASE}/validate`, { code });
            return response.data;
        } catch (error) {
            console.error('Error validating code:', error);
            throw error;
        }
    },

    deployModule: async (name, code) => {
        try {
            const response = await axios.post(`${API_BASE}/deploy`, { name, code });
            return response.data;
        } catch (error) {
            console.error('Error deploying module:', error);
            throw error;
        }
    },

    getStatus: async () => {
        try {
            const response = await axios.get(`${API_BASE}/status`);
            return response.data;
        } catch (error) {
            console.error('Error fetching status:', error);
            throw error;
        }
    }
};

export default autocoderService;
