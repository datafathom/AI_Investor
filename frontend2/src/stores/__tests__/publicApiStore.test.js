/**
 * Public API Store Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import usePublicApiStore from '../publicApiStore';
import apiClient from '../../services/apiClient';

// Mock apiClient
vi.mock('../../services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('publicApiStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    usePublicApiStore.setState({
      apiKeys: [],
      usage: {},
      loading: false,
      error: null,
    });
  });

  it('should fetch API keys successfully', async () => {
    const mockKeys = [{ id: 'key1', name: 'Production Key' }];
    apiClient.get.mockResolvedValueOnce({ data: { data: mockKeys } });

    await usePublicApiStore.getState().fetchApiKeys('user123');

    expect(apiClient.get).toHaveBeenCalledWith('/public-api/keys', expect.any(Object));
    expect(usePublicApiStore.getState().apiKeys).toEqual(mockKeys);
  });

  it('should fetch usage data', async () => {
    const mockUsage = { totalCalls: 100, remaining: 900 };
    apiClient.get.mockResolvedValueOnce({ data: { data: mockUsage } });

    await usePublicApiStore.getState().fetchUsage('user123');

    expect(apiClient.get).toHaveBeenCalledWith('/public-api/usage', expect.any(Object));
    expect(usePublicApiStore.getState().usage).toEqual(mockUsage);
  });

  it('should create API key and refresh list', async () => {
    apiClient.post.mockResolvedValueOnce({ data: { success: true } });
    apiClient.get.mockResolvedValueOnce({ data: { data: [] } }); // Refresh fetchApiKeys

    const success = await usePublicApiStore.getState().createApiKey({ user_id: 'user123', name: 'New Key' });

    expect(apiClient.post).toHaveBeenCalledWith('/public-api/key/create', expect.any(Object));
    expect(success).toBe(true);
  });

  it('should revoke API key', async () => {
    apiClient.post.mockResolvedValueOnce({ data: { success: true } });
    apiClient.get.mockResolvedValueOnce({ data: { data: [] } }); // Refresh fetchApiKeys

    const success = await usePublicApiStore.getState().revokeApiKey('key1', 'user123');

    expect(apiClient.post).toHaveBeenCalledWith(`/public-api/key/key1/revoke`);
    expect(success).toBe(true);
  });
});
