import { create } from 'zustand';

const API_BASE = '/api/v1/options';

const useOptionsStore = create((set, get) => ({
    // State
    strategy: null,
    greeks: null,
    optionsChain: [],
    isLoading: false,
    error: null,
    selectedSymbol: 'AAPL',
    strategyType: 'covered_call',

    // Actions
    setSelectedSymbol: (symbol) => set({ selectedSymbol: symbol }),
    setStrategyType: (type) => set({ strategyType: type }),

    fetchOptionsChain: async (symbol) => {
        set({ isLoading: true, error: null });
        try {
            const response = await fetch(`${API_BASE}/chain?symbol=${symbol}`);
            const result = await response.json();
            set({ optionsChain: result.data || [], isLoading: false });
        } catch (err) {
            set({ error: err.message, isLoading: false });
        }
    },

    buildStrategy: async (symbol, strategyType, legs = []) => {
        set({ isLoading: true, error: null });
        try {
            const response = await fetch(`${API_BASE}/strategy/build`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ symbol, strategy_type: strategyType, legs })
            });
            const result = await response.json();
            
            if (!response.ok) throw new Error(result.error || 'Failed to build strategy');
            
            set({ strategy: result.data });
            
            // Auto analyze if strategy created
            if (result.data?.strategy_id) {
                await get().analyzeStrategy(result.data.strategy_id);
            }
            
            set({ isLoading: false });
        } catch (err) {
            set({ error: err.message, isLoading: false });
        }
    },

    analyzeStrategy: async (strategyId) => {
        try {
            const response = await fetch(`${API_BASE}/strategy/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ strategy_id: strategyId })
            });
            const result = await response.json();
            set({ greeks: result.data });
        } catch (err) {
            console.error('Analysis error:', err);
        }
    }
}));

export default useOptionsStore;
