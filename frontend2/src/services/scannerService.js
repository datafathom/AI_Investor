/**
 * scannerService.js
 * 
 * Interfaces with the backend scanner_api.py for real-time asset discovery.
 */
import apiClient from './apiClient';

class ScannerService {
    async getLatestMatches() {
        try {
            const response = await apiClient.get('/scanner/matches');
            return response.data || [];
        } catch (error) {
            console.error('Failed to fetch scanner matches:', error);
            return [];
        }
    }

    async getGalaxyData() {
        try {
            const response = await apiClient.get('/scanner/galaxy');
            return response.data || [];
        } catch (error) {
            console.error('Failed to fetch galaxy data:', error);
            return [];
        }
    }

    async getMarketPulse() {
        try {
            const response = await apiClient.get('/scanner/pulse');
            return response.data || [];
        } catch (error) {
            console.error('Failed to fetch market pulse:', error);
            return [];
        }
    }
}

export const scannerService = new ScannerService();
