import apiClient from './apiClient';

export const politicsService = {
    /**
     * Fetch all recent congressional disclosures.
     */
    async getDisclosures() {
        try {
            const response = await apiClient.get('/politics/disclosures');
            return response.data || [];
        } catch (error) {
            console.error('Error in politicsService.getDisclosures:', error);
            throw error;
        }
    },

    /**
     * Fetch political alpha score for a specific ticker.
     * @param {string} ticker 
     */
    async getAlphaScore(ticker) {
        try {
            const response = await apiClient.get(`/politics/alpha/${ticker}`);
            return response.data || null;
        } catch (error) {
            console.error(`Error in politicsService.getAlphaScore for ${ticker}:`, error);
            throw error;
        }
    }
};
