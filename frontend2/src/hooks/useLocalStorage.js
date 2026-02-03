/**
 * useLocalStorage Hook
 * 
 * Hook for managing localStorage with React state.
 */

import { useState, useEffect } from 'react';
import { StorageService } from '../utils/storageService';

/**
 * Local storage hook
 * @param {string} key - Storage key
 * @param {any} initialValue - Initial value
 * @returns {[any, Function]} Value and setter function
 */
export function useLocalStorage(key, initialValue) {
  // State to store our value
  const [storedValue, setStoredValue] = useState(() => {
    // Try synchronous get first (Memory/LocalStorage)
    const item = StorageService.getSync(key);
    return item !== null ? item : initialValue;
  });

  // Async hydration on mount (check IDB if missed in sync)
  useEffect(() => {
    async function hydrate() {
      const dbValue = await StorageService.get(key);
      if (dbValue !== null && JSON.stringify(dbValue) !== JSON.stringify(storedValue)) {
        setStoredValue(dbValue);
      }
    }
    hydrate();
  }, [key]);

  // Return a wrapped version of useState's setter function that
  // persists the new value to localStorage.
  const setValue = (value) => {
    try {
      // Allow value to be a function so we have the same API as useState
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      StorageService.set(key, valueToStore);
    } catch (error) {
      console.error(`Error setting key "${key}":`, error);
    }
  };

  return [storedValue, setValue];
}

export default useLocalStorage;

