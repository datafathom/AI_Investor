/**
 * Marketplace Store Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import useMarketplaceStore from '../marketplaceStore';
import apiClient from '../../services/apiClient';

// Mock apiClient
vi.mock('../../services/apiClient', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
  },
}));

describe('marketplaceStore', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    useMarketplaceStore.setState({
      extensions: [],
      installedExtensions: [],
      loading: false,
      error: null,
      searchQuery: '',
    });
  });

  it('should fetch extensions successfully', async () => {
    const mockExtensions = [{ id: 'ext1', name: 'Algotrader' }];
    apiClient.get.mockResolvedValueOnce({ data: { data: mockExtensions } });

    await useMarketplaceStore.getState().fetchExtensions('algo');

    expect(apiClient.get).toHaveBeenCalledWith('/marketplace/extensions', { params: { search: 'algo' } });
    expect(useMarketplaceStore.getState().extensions).toEqual(mockExtensions);
  });

  it('should fetch installed extensions', async () => {
    const mockInstalled = [{ id: 'ext1', name: 'Algotrader' }];
    apiClient.get.mockResolvedValueOnce({ data: { data: mockInstalled } });

    await useMarketplaceStore.getState().fetchInstalledExtensions('user123');

    expect(apiClient.get).toHaveBeenCalledWith('/marketplace/installed', { params: { user_id: 'user123' } });
    expect(useMarketplaceStore.getState().installedExtensions).toEqual(mockInstalled);
  });

  it('should handle extension installation', async () => {
    apiClient.post.mockResolvedValueOnce({ data: { success: true } });
    apiClient.get.mockResolvedValueOnce({ data: { data: [] } }); // Refresh installed list

    const success = await useMarketplaceStore.getState().installExtension('user123', 'ext1');

    expect(apiClient.post).toHaveBeenCalledWith('/marketplace/install', { user_id: 'user123', extension_id: 'ext1' });
    expect(success).toBe(true);
  });

  it('should handle extension uninstallation', async () => {
    apiClient.post.mockResolvedValueOnce({ data: { success: true } });
    apiClient.get.mockResolvedValueOnce({ data: { data: [] } }); // Refresh installed list

    const success = await useMarketplaceStore.getState().uninstallExtension('user123', 'ext1');

    expect(apiClient.post).toHaveBeenCalledWith('/marketplace/uninstall', { extension_id: 'ext1' });
    expect(success).toBe(true);
  });
});
