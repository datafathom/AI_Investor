/**
 * ML Training Service
 * : API integration for ML Model Training Pipeline
 */
import apiClient from './apiClient';

const BASE_URL = '/ml-training';

export const mlService = {
    /**
     * Get all training jobs
     * @param {string} userId
     */
    getTrainingJobs: async (userId) => {
        const response = await apiClient.get(`${BASE_URL}/jobs`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Get all model versions
     * @param {string} userId
     */
    getModelVersions: async (userId) => {
        const response = await apiClient.get(`${BASE_URL}/models`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Get active deployments
     * @param {string} userId
     */
    getDeployments: async (userId) => {
        const response = await apiClient.get(`${BASE_URL}/deployments`, {
            params: { user_id: userId }
        });
        return response.data;
    },

    /**
     * Start a new training job
     * @param {Object} data { user_id, model_type, dataset }
     */
    startTrainingJob: async (data) => {
        const response = await apiClient.post(`${BASE_URL}/job/start`, data);
        return response.data;
    },

    /**
     * Deploy a model version
     * @param {Object} data { model_id }
     */
    deployModel: async (data) => {
        const response = await apiClient.post(`${BASE_URL}/deploy`, data);
        return response.data;
    }
};

export default mlService;
