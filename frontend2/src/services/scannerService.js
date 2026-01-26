/**
 * scannerService.js
 * 
 * Interfaces with the backend scanner_api.py for real-time asset discovery.
 */

class ScannerService {
    constructor() {
        this.baseUrl = '/api/v1/scanner';
    }

    async getLatestMatches() {
        try {
            const response = await fetch(`${this.baseUrl}/matches`);
            const result = await response.json();
            return result.success ? result.data : [];
        } catch (error) {
            console.error('Failed to fetch scanner matches:', error);
            return [];
        }
    }

    async getGalaxyData() {
        try {
            const response = await fetch(`${this.baseUrl}/galaxy`);
            const result = await response.json();
            return result.success ? result.data : [];
        } catch (error) {
            console.error('Failed to fetch galaxy data:', error);
            return [];
        }
    }

    async getMarketPulse() {
        try {
            const response = await fetch(`${this.baseUrl}/pulse`);
            const result = await response.json();
            return result.success ? result.data : [];
        } catch (error) {
            console.error('Failed to fetch market pulse:', error);
            return [];
        }
    }
}

export const scannerService = new ScannerService();
