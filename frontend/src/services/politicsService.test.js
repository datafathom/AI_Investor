import { describe, it, expect, vi, beforeEach } from 'vitest';
import { politicsService } from './politicsService';

describe('politicsService', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('fetches disclosures successfully', async () => {
        const mockData = { data: [{ member: 'Nancy Pelosi', ticker: 'NVDA' }] };
        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: () => Promise.resolve(mockData),
        });

        const result = await politicsService.getDisclosures();
        expect(result).toEqual(mockData);
        expect(global.fetch).toHaveBeenCalledWith('/api/v1/politics/disclosures');
    });

    it('handles fetch errors', async () => {
        global.fetch = vi.fn().mockResolvedValue({
            ok: false,
        });

        await expect(politicsService.getDisclosures()).rejects.toThrow('Failed to fetch disclosures');
    });

    it('fetches alpha score for a ticker', async () => {
        const mockData = { ticker: 'NVDA', alpha_score: 0.59 };
        global.fetch = vi.fn().mockResolvedValue({
            ok: true,
            json: () => Promise.resolve(mockData),
        });

        const result = await politicsService.getAlphaScore('NVDA');
        expect(result).toEqual(mockData);
        expect(global.fetch).toHaveBeenCalledWith('/api/v1/politics/alpha/NVDA');
    });
});
