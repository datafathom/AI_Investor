
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { marketService } from './marketService';

// Mock global fetch
global.fetch = vi.fn();

describe('marketService', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    });

    it('getMarketPrediction should return parsed data on success', async () => {
        const mockResponse = {
            prediction: "UP",
            probability_up: 0.85,
            symbol: "SPY"
        };

        fetch.mockResolvedValueOnce({
            ok: true,
            json: async () => mockResponse,
        });

        const result = await marketService.getMarketPrediction('SPY');

        expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/api/v1/market/predict?symbol=SPY'));
        expect(result).toEqual(mockResponse);
        expect(result.prediction).toBe("UP");
    });

    it('getMarketPrediction should handle errors gracefully', async () => {
        fetch.mockResolvedValueOnce({
            ok: false,
        });

        const result = await marketService.getMarketPrediction('SPY');

        expect(result).toHaveProperty('error');
        expect(result.prediction).toBe("UNKNOWN");
    });
});
