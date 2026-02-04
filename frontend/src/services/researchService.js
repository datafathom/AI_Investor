/**
 * Research Service
 * : Research Reports & Analysis
 */
import apiClient from './apiClient';

const BASE_URL = '/research';

export const researchService = {
    /**
     * Get generated reports
     * @param {string} userId
     */
    getReports: async (userId) => {
        const response = await apiClient.get(`${BASE_URL}/reports`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Get available templates
     */
    getTemplates: async () => {
        const response = await apiClient.get(`${BASE_URL}/templates`);
        return response.data;
    },

    /**
     * Generate a new research report
     * @param {Object} data { user_id, template_id, report_title, format }
     */
    generateReport: async (data) => {
        const response = await apiClient.post(`${BASE_URL}/generate`, data);
        return response.data;
    },

    /**
     * Ask an AI research question
     * @param {string} query
     * @param {boolean} mock
     */
    askQuestion: async (query, mock = true) => {
        // NOTE: The original store used /api/v1/ai/research/ask. 
        // We should normalize this if possible, but for now we'll match the existing endpoint.
        const response = await apiClient.post(`/ai/research/ask`, { query }, {
            params: { mock }
        });
        return response.data;
    }
};

export default researchService;
