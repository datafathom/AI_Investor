/**
 * Political Alpha Service
 * Handles fetching congressional disclosures and political alpha scores.
 */

const API_BASE_URL = '/api/v1/politics';

export const politicsService = {
    /**
     * Fetch all recent congressional disclosures.
     */
    async getDisclosures() {
        try {
            const response = await fetch(`${API_BASE_URL}/disclosures`);
            if (!response.ok) throw new Error('Failed to fetch disclosures');
            return await response.json();
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
            const response = await fetch(`${API_BASE_URL}/alpha/${ticker}`);
            if (!response.ok) throw new Error(`Failed to fetch alpha for ${ticker}`);
            return await response.json();
        } catch (error) {
            console.error(`Error in politicsService.getAlphaScore for ${ticker}:`, error);
            throw error;
        }
    }
};
