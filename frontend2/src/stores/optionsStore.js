import { create } from 'zustand';
import apiClient from '../services/apiClient';

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
            const response = await apiClient.get('/options/chain', { params: { symbol } });
            set({ optionsChain: response.data.data || [], isLoading: false });
        } catch (err) {
            set({ error: err.message, isLoading: false });
        }
    },

    buildStrategy: async (symbol, strategyType, legs = []) => {
        set({ isLoading: true, error: null });
        try {
            const response = await apiClient.post('/options/strategy/build', {
                symbol,
                strategy_type: strategyType,
                legs
            });
            
            set({ strategy: response.data.data });
            
            // Auto analyze if strategy created
            if (response.data.data?.strategy_id) {
                await get().analyzeStrategy(response.data.data.strategy_id);
            }
            
            set({ isLoading: false });
        } catch (err) {
            set({ error: err.message, isLoading: false });
        }
    },

    analyzeStrategy: async (strategyId) => {
        try {
            const response = await apiClient.post('/options/strategy/analyze', { strategy_id: strategyId });
            set({ greeks: response.data.data });
        } catch (err) {
            console.error('Analysis error:', err);
        }
    }
}));

export default useOptionsStore;
