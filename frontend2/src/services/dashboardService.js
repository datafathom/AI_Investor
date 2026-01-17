
import { apiClient as api } from '../utils/apiClient';

export const dashboardService = {
    /**
     * Get current target allocation buckets (Alpha vs Shield).
     */
    getAllocation: async (fearIndex = 50) => {
        try {
            const response = await api.get(`/dashboard/allocation?fear_index=${fearIndex}`);
            return response.data;
        } catch (error) {
            console.error("Failed to fetch allocation", error);
            return null;
        }
    },

    /**
     * Get Risk metrics (VaR, Circuit Breaker).
     */
    getRiskStatus: async () => {
        try {
            const response = await api.get('/dashboard/risk');
            return response.data;
        } catch (error) {
            console.error("Failed to fetch risk status", error);
            return null;
        }
    },

    /**
     * Get Execution status (Cash, Positions).
     */
    getExecutionStatus: async () => {
        try {
            const response = await api.get('/dashboard/execution');
            return response.data;
        } catch (error) {
            console.error("Failed to fetch execution status", error);
            return null;
        }
    }
};
