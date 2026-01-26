import { authService } from './authService';

class PredictionService {
    constructor() {
        this.baseUrl = '/api/ai-predictions';
    }

    /**
     * Fetches price prediction for a specific symbol.
     */
    async getPricePrediction(symbol, timeHorizon = '1m') {
        try {
            const response = await authService.authenticatedFetch(`${this.baseUrl}/price`, {
                method: 'POST',
                body: JSON.stringify({ symbol, time_horizon: timeHorizon })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Price prediction failed');
            return data.data;
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
            const response = await authService.authenticatedFetch(`${this.baseUrl}/trend`, {
                method: 'POST',
                body: JSON.stringify({ symbol, time_horizon: timeHorizon })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Trend prediction failed');
            return data.data;
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
            const response = await authService.authenticatedFetch(`${this.baseUrl}/regime?market_index=${marketIndex}`);
            const data = await response.json();
            if (!response.ok) throw new Error(data.message || 'Regime detection failed');
            return data.data;
        } catch (error) {
            console.error('Prediction Service Error [getRegime]:', error);
            throw error;
        }
    }
}

export const predictionService = new PredictionService();
export default predictionService;
