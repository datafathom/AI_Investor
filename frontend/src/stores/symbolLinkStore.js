import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import { storageAdapter } from '../utils/storageAdapter';

/**
 * Symbol Link Store
 * Manages synchronized tickers across windows using color-coded groups.
 * Groups: 'red', 'blue', 'green', 'none'
 */
const useSymbolLinkStore = create(
  persist(
    (set, get) => ({
      links: {
        red: 'AAPL',
        blue: 'TSLA',
        green: 'BTC/USD',
      },

      /**
       * Update the symbol for a specific color group
       * @param {string} group - 'red' | 'blue' | 'green'
       * @param {string} symbol - e.g. 'NVDA'
       */
      updateSymbol: (group, symbol) => {
        if (group === 'none') return;
        set((state) => ({
          links: {
            ...state.links,
            [group]: symbol.toUpperCase()
          }
        }));
      },

      /**
       * Get current symbol for a group
       */
      getSymbol: (group) => {
        if (group === 'none') return null;
        return get().links[group];
      }
    }),
    {
      name: 'ai-investor-symbol-links',
      storage: createJSONStorage(() => storageAdapter),
    }
  )
);

export default useSymbolLinkStore;
