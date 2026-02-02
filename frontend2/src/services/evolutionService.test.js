/**
 * ==============================================================================
 * FILE: frontend2/src/services/evolutionService.test.js
 * ROLE: Protocol Validator
 * PURPOSE:
 *   Verify that the evolutionService correctly handles API interactions
 *   and error scenarios.
 * ==============================================================================
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import apiClient from './apiClient';
import { evolutionService } from './evolutionService';

vi.mock('./apiClient');

describe('evolutionService', () => {
    beforeEach(() => {
        vi.resetAllMocks();
    });

    it('starts evolution successfully', async () => {
        const mockData = { status: 'success', current_generation: 5 };
        apiClient.post.mockResolvedValueOnce({ data: mockData });

        const result = await evolutionService.startEvolution();
        expect(result.status).toBe('success');
        expect(result.current_generation).toBe(5);
        expect(apiClient.post).toHaveBeenCalledWith('/evolution/start');
    });

    it('fetches status successfully', async () => {
        const mockStatus = { current_generation: 10, best_performer: { fitness: 0.95 } };
        apiClient.get.mockResolvedValueOnce({ data: mockStatus });

        const result = await evolutionService.getStatus();
        expect(result.current_generation).toBe(10);
        expect(result.best_performer.fitness).toBe(0.95);
        expect(apiClient.get).toHaveBeenCalledWith('/evolution/status');
    });

    it('handles errors gracefully', async () => {
        apiClient.get.mockRejectedValueOnce(new Error('Network Error'));

        await expect(evolutionService.getStatus()).rejects.toThrow('Network Error');
    });
});
