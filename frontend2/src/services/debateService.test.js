import { describe, it, expect, vi, beforeEach } from 'vitest';
import axios from 'axios';
import debateService from './debateService';

vi.mock('axios');

describe('debateService', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('triggers a debate and returns the committee consensus', async () => {
        const mockData = {
            ticker: 'TSLA',
            consensus: { decision: 'BUY', is_approved: true },
            responses: []
        };

        axios.post.mockResolvedValueOnce({ data: mockData });

        const result = await debateService.triggerDebate('TSLA', 'Testing');
        expect(result.ticker).toBe('TSLA');
        expect(result.consensus.decision).toBe('BUY');
        expect(axios.post).toHaveBeenCalledWith('/api/v1/analysis/debate', {
            ticker: 'TSLA',
            summary: 'Testing'
        });
    });

    it('handles API errors gracefully', async () => {
        axios.post.mockRejectedValueOnce(new Error('Network Error'));
        await expect(debateService.triggerDebate('AAPL', 'fail')).rejects.toThrow('Network Error');
    });
});
