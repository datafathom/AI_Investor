
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { marketService } from './marketService';

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { marketService } from './marketService';
import apiClient from './apiClient';

vi.mock('./apiClient');

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

        apiClient.get.mockResolvedValueOnce({
            data: mockResponse,
        });

        const result = await marketService.getMarketPrediction('SPY');

        expect(apiClient.get).toHaveBeenCalledWith(expect.stringContaining('/market/predict?symbol=SPY'));
        expect(result).toEqual(mockResponse);
        expect(result.prediction).toBe("UP");
    });

    it('getMarketPrediction should handle errors gracefully', async () => {
        apiClient.get.mockRejectedValueOnce(new Error('Network Error'));

        const result = await marketService.getMarketPrediction('SPY');

        expect(result).toHaveProperty('error');
        expect(result.prediction).toBe("UNKNOWN");
    });
});
