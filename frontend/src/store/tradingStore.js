
import { create } from 'zustand';

export const useTradingStore = create((set) => ({
    optionsChain: {
        ticker: 'SPY',
        expirations: ['2026-01-16', '2026-01-23', '2026-02-20'],
        selectedExpiration: '2026-01-16',
        strikes: []
    },
    marketDepth: {
        ticker: 'SPY',
        bids: [],
        asks: [],
        lastPrice: 0
    },
    tradeTape: [],
    setOptionsExpiration: (expiration) => set((state) => ({
        optionsChain: { ...state.optionsChain, selectedExpiration: expiration }
    })),
    updateOptionsStrikes: (strikes) => set((state) => ({
        optionsChain: { ...state.optionsChain, strikes }
    })),
    updateMarketDepth: (depth) => set((state) => ({
        marketDepth: { ...state.marketDepth, ...depth }
    })),
    addTrade: (trade) => set((state) => ({
        tradeTape: [trade, ...state.tradeTape].slice(0, 100)
    })),
    clearTape: () => set({ tradeTape: [] })
}));
