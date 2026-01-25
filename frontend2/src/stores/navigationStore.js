/**
 * ==============================================================================
 * FILE: frontend2/src/stores/navigationStore.js
 * ROLE: Navigation State Management
 * PURPOSE: Persists navigation history, active symbol, and route state using Zustand.
 *          Ensures seamless transitions and state recovery across reloads.
 * ==============================================================================
 */
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

const useNavigationStore = create(
  persist(
    (set, get) => ({
      currentRoute: '/workspace/terminal',
      previousRoute: null,
      history: [],
      activeSymbol: 'SPY', // Default symbol
      
      // Actions
      setCurrentRoute: (route) => set((state) => {
        if (route === state.currentRoute) return {};
        const newHistory = [...state.history, state.currentRoute].slice(-20); // Keep last 20
        return {
          currentRoute: route,
          previousRoute: state.currentRoute,
          history: newHistory
        };
      }),

      setSymbol: (symbol) => set({ activeSymbol: symbol }),
      
      goBack: () => {
        const { history } = get();
        if (history.length > 0) {
            const prev = history[history.length - 1];
            // In a real app, we'd sync with React Router's navigate here or assume Router updates store
            return prev; 
        }
        return null;
      },
      
      clearHistory: () => set({ history: [], previousRoute: null })
    }),
    {
      name: 'investor-navigation-storage', // unique name
      storage: createJSONStorage(() => localStorage),
    }
  )
);

export default useNavigationStore;
