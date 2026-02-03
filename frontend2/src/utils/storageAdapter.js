import { StorageService } from './storageService';

/**
 * Adapter for Zustand persist middleware.
 * Maps StorageService (Async IDB/Sync Fallback) to Zustand's storage API.
 */
export const storageAdapter = {
  getItem: async (name) => {
    // We use async get (IDB) for hydration to ensure we get the latest persistent data
    // Zustand handles async hydration automatically
    const value = await StorageService.get(name);
    return value;
  },
  setItem: async (name, value) => {
    // Fire and forget (or await if critical, but Zustand setItem is typically void)
    await StorageService.set(name, value);
  },
  removeItem: async (name) => {
    await StorageService.remove(name);
  },
};
