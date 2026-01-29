/**
 * scannerService.js
 * 
 * Interfaces with the backend scanner_api.py for real-time asset discovery.
 */
import apiClient from './apiClient';

class ScannerService {
    async getLatestMatches() {
        try {
            return await apiClient.get('/scanner/matches');
        } catch (error) {
            console.error('Failed to fetch scanner matches:', error);
            return [];
        }
    }

    async getGalaxyData() {
        try {
            return await apiClient.get('/scanner/galaxy');
        } catch (error) {
            console.error('Failed to fetch galaxy data:', error);
            return [];
        }
    }

    async getMarketPulse() {
        try {
            return await apiClient.get('/scanner/pulse');
        } catch (error) {
            console.error('Failed to fetch market pulse:', error);
            return [];
        }
    }
}

export const scannerService = new ScannerService();
