/**
 * MarketService
 * Handles API calls for market-related data.
 */
import apiClient from './apiClient';
import { workerManager } from './workerManager';

class MarketService {
    constructor() {
        this.baseUrl = '/market';
    }

    /**
     * Fetches the Fear & Greed Index.
     */
    async getFearGreedIndex(symbols = []) {
        try {
            const queryParams = new URLSearchParams();
            if (symbols.length > 0) {
                queryParams.append('symbols', symbols.join(','));
            }
            queryParams.append('mock', 'true');

            // ENABLE CACHING: Result is valid for 5 mins
            const response = await apiClient.get(`${this.baseUrl}/fear-greed?${queryParams.toString()}`, {
                useCache: true,
                cacheTTL: 5 * 60 * 1000
            });
            return response;
        } catch (error) {
            console.error('Failed to fetch Fear & Greed Index:', error);
            throw error;
        }
    }

    /**
     * Fetches the Market Direction Prediction.
     */
    async getMarketPrediction(symbol = 'SPY') {
        try {
            const queryParams = new URLSearchParams();
            queryParams.append('symbol', symbol);

            const rawData = await apiClient.get(`${this.baseUrl}/predict?${queryParams.toString()}`);
            
            // Offload complex transformation to worker
            const transformed = await workerManager.runTask('TRANSFORM_MARKET_DATA', {
                rawData,
                symbol
            });
            
            return transformed;
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
