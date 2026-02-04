import apiClient from './apiClient';

class PredictionService {
    /**
     * Fetches price prediction for a specific symbol.
     */
    async getPricePrediction(symbol, timeHorizon = '1m') {
        try {
            return await apiClient.post('/ai-predictions/price', { 
                symbol, time_horizon: timeHorizon 
            });
        } catch (error) {
            console.error('Prediction Service Error [getPrice]:', error);
            throw error;
        }
    }

    /**
     * Fetches trend prediction for a specific symbol.
     */
    async getTrendPrediction(symbol, timeHorizon = '1m') {
        try {
            return await apiClient.post('/ai-predictions/trend', { 
                symbol, time_horizon: timeHorizon 
            });
        } catch (error) {
            console.error('Prediction Service Error [getTrend]:', error);
            throw error;
        }
    }

    /**
     * Fetches market regime detection for an index.
     */
    async getMarketRegime(marketIndex = 'SPY') {
        try {
            return await apiClient.get('/ai-predictions/regime', {
                params: { market_index: marketIndex }
            });
        } catch (error) {
            console.error('Prediction Service Error [getRegime]:', error);
            throw error;
        }
    }
}

export const predictionService = new PredictionService();
export default predictionService;
