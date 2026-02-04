/**
 * IndexedDB Provider
 * Wraps the 'idb' library to provide a clean Promise-based API for storage.
 * Handles database versioning and migration.
 */
import { openDB } from 'idb';

const DB_NAME = 'AI_Investor_DB';
const DB_VERSION = 1;
const STORES = {
  KEY_VALUE: 'key_value_store', // Replacement for simple localStorage items
  CACHE: 'api_cache_store',     // For API response caching
  DATA: 'large_data_store'      // For heavy datasets like charts/portfolio
};

/**
 * Initialize the database
 */
const initDB = async () => {
  return openDB(DB_NAME, DB_VERSION, {
    upgrade(db) {
      // Key-Value Store (like localStorage)
      if (!db.objectStoreNames.contains(STORES.KEY_VALUE)) {
        db.createObjectStore(STORES.KEY_VALUE);
      }
      
      // Cache Store
      if (!db.objectStoreNames.contains(STORES.CACHE)) {
        db.createObjectStore(STORES.CACHE);
      }
      
      // Data Store
      if (!db.objectStoreNames.contains(STORES.DATA)) {
        db.createObjectStore(STORES.DATA);
      }
    },
  });
};

// Singleton promise to ensure we don't open multiple connections
let dbPromise = initDB();

export const IndexedDBProvider = {
  /**
   * Get a value from the store
   * @param {string} key 
   * @param {string} storeName 
   */
  async get(key, storeName = STORES.KEY_VALUE) {
    const db = await dbPromise;
    return db.get(storeName, key);
  },

  /**
   * Set a value in the store
   * @param {string} key 
   * @param {any} value 
   * @param {string} storeName 
   */
  async set(key, value, storeName = STORES.KEY_VALUE) {
    const db = await dbPromise;
    return db.put(storeName, value, key);
  },

  /**
   * Delete a value
   * @param {string} key 
   * @param {string} storeName 
   */
  async delete(key, storeName = STORES.KEY_VALUE) {
    const db = await dbPromise;
    return db.delete(storeName, key);
  },

  /**
   * Clear an entire store
   * @param {string} storeName 
   */
  async clear(storeName = STORES.KEY_VALUE) {
    const db = await dbPromise;
    return db.clear(storeName);
  },

  /**
   * Get all keys from a store
   * @param {string} storeName 
   */
  async keys(storeName = STORES.KEY_VALUE) {
    const db = await dbPromise;
    return db.getAllKeys(storeName);
  },
  
  // Expose store names constants
  STORES
};
