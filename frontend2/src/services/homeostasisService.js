
import apiClient from './apiClient';

const API_PATH = '/homeostasis';

export const homeostasisService = {
    /**
     * Get current homeostasis status.
     */
    getStatus: async () => {
        try {
            return await apiClient.get(`${API_PATH}/status`);
        } catch (error) {
            console.error("Failed to fetch homeostasis status", error);
            return null;
        }
    },

    /**
     * Update net worth and check autopilot pulse.
     */
    updateMetrics: async (netWorth) => {
        try {
            return await apiClient.post(`${API_PATH}/update`, { net_worth: net_worth });
        } catch (error) {
            console.error("Failed to update homeostasis metrics", error);
            return null;
        }
    },

    /**
     * Manually trigger a philanthropy donation.
     */
    donate: async (amount) => {
        try {
            return await apiClient.post(`${API_PATH}/donate`, { amount });
        } catch (error) {
            console.error("Failed to trigger donation", error);
            return null;
        }
    }
};
