/**
 * MarketService
 * Handles API calls for market-related data.
 */
import apiClient from './apiClient';

class MarketService {
    constructor() {
        this.baseUrl = '/market';
    }

    /**
     * Fetches the Fear & Greed Index.
     * @param {string[]} symbols - Optional list of symbols to analyze.
     * @returns {Promise<Object>} - The fear and greed index data.
     */
    async getFearGreedIndex(symbols = []) {
        try {
            const queryParams = new URLSearchParams();
            if (symbols.length > 0) {
                queryParams.append('symbols', symbols.join(','));
            }

            // Default to mock=true for now as per backend default
            queryParams.append('mock', 'true');

            const response = await apiClient.get(`${this.baseUrl}/fear-greed?${queryParams.toString()}`);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch Fear & Greed Index:', error);
            throw error;
        }
    }

    /**
     * Fetches the Market Direction Prediction.
     * @param {string} symbol - Symbol to predict (default SPY).
     * @returns {Promise<Object>} - Prediction result { prediction: "UP"|"DOWN", ... }.
     */
    async getMarketPrediction(symbol = 'SPY') {
        try {
            const queryParams = new URLSearchParams();
            queryParams.append('symbol', symbol);

            const response = await apiClient.get(`${this.baseUrl}/predict?${queryParams.toString()}`);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch Market Prediction:', error);
            return {
                prediction: "UNKNOWN",
                probability_up: 0.5,
                error: error.message
            };
        }
    }
}

export const marketService = new MarketService();
