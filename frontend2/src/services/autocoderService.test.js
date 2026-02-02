import { describe, it, expect, vi, beforeEach } from 'vitest';
import autocoderService from './autocoderService';
import apiClient from './apiClient';

vi.mock('./apiClient');

describe('autocoderService', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('generates code for a given task', async () => {
        const mockResponse = { data: { status: 'success', code: 'class MockAdapter {}' } };
        apiClient.post.mockResolvedValueOnce(mockResponse);

        const result = await autocoderService.generateCode('Test Task');
        expect(apiClient.post).toHaveBeenCalledWith('/dev/generate', { task: 'Test Task' });
        expect(result.code).toBe('class MockAdapter {}');
    });

    it('validates generated code', async () => {
        const mockResponse = { data: { status: 'success', is_valid: true } };
        apiClient.post.mockResolvedValueOnce(mockResponse);

        const result = await autocoderService.validateCode('class MyCode {}');
        const result = await autocoderService.validateCode('class MyCode {}');
        expect(apiClient.post).toHaveBeenCalledWith('/dev/validate', { code: 'class MyCode {}' });
        expect(result.is_valid).toBe(true);
    });

    it('deploys a module', async () => {
        const mockResponse = { data: { status: 'success', message: 'Deployed' } };
        apiClient.post.mockResolvedValueOnce(mockResponse);

        const result = await autocoderService.deployModule('test_mod', 'class X {}');
        const result = await autocoderService.deployModule('test_mod', 'class X {}');
        expect(apiClient.post).toHaveBeenCalledWith('/dev/deploy', { name: 'test_mod', code: 'class X {}' });
        expect(result.status).toBe('success');
    });

    it('handles API errors gracefully', async () => {
        apiClient.post.mockRejectedValueOnce(new Error('Network Error'));

        await expect(autocoderService.generateCode('fail')).rejects.toThrow('Network Error');
    });
});
