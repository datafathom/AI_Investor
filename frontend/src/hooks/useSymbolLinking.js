
import { create } from 'zustand';

/**
 * useSymbolLinking Hook (via Zustand)
 * Manages ticker synchronization across color groups.
 */
export const useSymbolLinking = create((set) => ({
    // groups: { [groupId]: ticker }
    groups: {
        red: 'SPY',
        blue: 'AAPL',
        green: 'BTC',
        none: ''
    },

    setGroupTicker: (group, ticker) => set((state) => ({
        groups: { ...state.groups, [group]: ticker }
    })),

    getTickerForGroup: (group) => {
        // This is a selector-style helper if needed outside of component hooks
    }
}));
