/**
 * Storage Service
 * Tiered storage solution:
 * 1. Memory Cache (Fastest)
 * 2. IndexedDB (Persistent, Async, Large Data)
 * 3. LocalStorage (Fallback, Sync, Small Data)
 */
import { IndexedDBProvider } from './indexedDBProvider';

// Memory cache for sub-millisecond access
const memoryCache = new Map();

export const StorageService = {
  /**
   * Get item from storage
   * Priority: Memory -> IDB -> LocalStorage
   * @param {string} key 
   */
  async get(key) {
    console.log(`[Storage Debug] get(${key}) started`);
    // 1. Check Memory
    if (memoryCache.has(key)) {
      return memoryCache.get(key);
    }

    try {
      // 2. Check IndexedDB with 250ms Timeout
      const idbPromise = IndexedDBProvider.get(key);
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('IDB timeout')), 250)
      );
      
      const idbValue = await Promise.race([idbPromise, timeoutPromise]);
      if (idbValue !== undefined) {
        memoryCache.set(key, idbValue);
        return idbValue;
      }
    } catch (e) {
      if (e.message === 'IDB timeout') {
        console.warn(`[StorageService] IDB Read TIMEOUT for ${key}. Falling back to LocalStorage.`);
      } else {
        console.warn(`[StorageService] IDB Read Error for ${key}:`, e);
      }
    }

    // 3. Check LocalStorage (Fallback)
    try {
      const localValue = localStorage.getItem(key);
      if (localValue) {
        try {
          const parsed = JSON.parse(localValue);
          memoryCache.set(key, parsed);
          // Auto-migrate to IDB? Maybe later.
          return parsed;
        } catch (err) {
          memoryCache.set(key, localValue);
          return localValue;
        }
      }
    } catch (e) {
      console.error('LocalStorage unavailable:', e);
    }

    return null;
  },

  /**
   * Synchronous Get (Memory -> LocalStorage only)
   * Skips IndexedDB. Use for critical initial render paths (like Auth).
   * @param {string} key 
   */
  getSync(key) {
    // 1. Check Memory
    if (memoryCache.has(key)) {
      return memoryCache.get(key);
    }

    // 2. Check LocalStorage
    try {
      const localValue = localStorage.getItem(key);
      if (localValue) {
        try {
          const parsed = JSON.parse(localValue);
          memoryCache.set(key, parsed);
          return parsed;
        } catch (err) {
          memoryCache.set(key, localValue);
          return localValue;
        }
      }
    } catch (e) {
      console.error('LocalStorage unavailable:', e);
    }

    return null;
  },

  /**
   * Set item in storage
   * Writes to: Memory, IDB, and LocalStorage (if small)
   * @param {string} key 
   * @param {any} value 
   */
  async set(key, value) {
    // 1. Update Memory
    memoryCache.set(key, value);

    try {
      // 2. Update IndexedDB (Always) with 250ms Timeout
      const idbPromise = IndexedDBProvider.set(key, value);
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('IDB timeout')), 250)
      );
      await Promise.race([idbPromise, timeoutPromise]);
    } catch (e) {
      if (e.message === 'IDB timeout') {
        console.warn(`[StorageService] IDB Write TIMEOUT for ${key}.`);
      } else {
        console.warn(`[StorageService] IDB Write Error for ${key}:`, e);
      }
    }

    // 3. Update LocalStorage (Only if small keys/values to avoid quota limits)
    // We treat LocalStorage as a sync backup for critical small data
    try {
      const serialized = JSON.stringify(value);
      if (serialized.length < 500000) { // ~500KB limit for LS backup
         localStorage.setItem(key, serialized);
      }
    } catch (e) {
      // Quota exceeded or serialization error
      // console.warn('LocalStorage skip/error:', e);
    }
  },

  /**
   * Remove item
   * @param {string} key 
   */
  async remove(key) {
    memoryCache.delete(key);
    try {
      const idbPromise = IndexedDBProvider.delete(key);
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('IDB timeout')), 250)
      );
      await Promise.race([idbPromise, timeoutPromise]);
    } catch (e) {
      console.warn(`[StorageService] IDB Delete Error/Timeout for ${key}:`, e);
    }
    localStorage.removeItem(key);
  },

  /**
   * Clear all storage
   */
  async clear() {
    memoryCache.clear();
    await IndexedDBProvider.clear();
    localStorage.clear();
  },

  // Constants
  STORES: IndexedDBProvider.STORES
};
