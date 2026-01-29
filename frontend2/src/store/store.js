/**
 * Global State Store
 * 
 * Centralized state management using Zustand.
 * Provides state persistence and synchronization.
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';

// Store configuration
const storeConfig = {
  name: 'app-store',
  storage: createJSONStorage(() => localStorage),
  partialize: (state) => ({
    // Only persist certain parts of state
    userPreferences: state.userPreferences,
    uiState: state.uiState,
  }),
};

// Create store
export const useStore = create(
  persist(
    (set, get) => ({
      // User state
      user: null,
      setUser: (user) => set({ user }),
      isAdmin: () => get().user?.role === 'admin' || get().user?.role === 'super_admin',
      isAdvisor: () => get().user?.role === 'advisor',

      // UI state
      uiState: {
        sidebarOpen: true,
        theme: 'light',
        notifications: [],
        isLoading: false,
      },
      setLoading: (isLoading) => set((state) => ({
        uiState: { ...state.uiState, isLoading }
      })),
      setUIState: (updates) => set((state) => ({
        uiState: { ...state.uiState, ...updates },
      })),

      // User preferences
      userPreferences: {
        theme: 'light',
        layout: null,
        notifications: {},
      },
      setUserPreferences: (preferences) => set({ userPreferences: preferences }),

      // Window state (synced with windowManager)
      windows: [],
      setWindows: (windows) => set({ windows }),

      // Widget state
      widgets: [],
      setWidgets: (widgets) => set({ widgets }),

      // Notification state
      notifications: [],
      addNotification: (notification) => set((state) => ({
        notifications: [...state.notifications, notification],
      })),
      removeNotification: (id) => set((state) => ({
        notifications: state.notifications.filter(n => n.id !== id),
      })),
      clearNotifications: () => set({ notifications: [] }),

      // State history for undo/redo
      history: [],
      historyIndex: -1,
      pushToHistory: (state) => {
        const currentHistory = get().history;
        const currentIndex = get().historyIndex;
        const newHistory = currentHistory.slice(0, currentIndex + 1);
        newHistory.push(state);
        set({
          history: newHistory,
          historyIndex: newHistory.length - 1,
        });
      },
      undo: () => {
        const index = get().historyIndex;
        if (index > 0) {
          set({ historyIndex: index - 1 });
          return get().history[index - 1];
        }
        return null;
      },
      redo: () => {
        const index = get().historyIndex;
        const history = get().history;
        if (index < history.length - 1) {
          set({ historyIndex: index + 1 });
          return history[index + 1];
        }
        return null;
      },

      // Clear all state
      reset: () => set({
        user: null,
        uiState: {
          sidebarOpen: true,
          theme: 'light',
          notifications: [],
          isLoading: false,
        },
        userPreferences: {
          theme: 'light',
          layout: null,
          notifications: {},
        },
        windows: [],
        widgets: [],
        notifications: [],
        history: [],
        historyIndex: -1,
      }),
    }),
    storeConfig
  )
);

// State synchronization across tabs
if (typeof window !== 'undefined') {
  window.addEventListener('storage', (e) => {
    if (e.key === 'app-store') {
      // Reload store from localStorage when another tab changes it
      useStore.persist.rehydrate();
    }
  });
}

export default useStore;

