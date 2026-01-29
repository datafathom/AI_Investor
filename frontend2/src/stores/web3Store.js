import { create } from 'zustand';

const API_BASE = '/api/v1/web3';

const useWeb3Store = create((set, get) => ({
  // State
  portfolio: null,
  walletBalances: {}, // { "chain:address": BalanceObj }
  lpPositions: [],
  gasMetrics: {}, // { "ethereum": MetricsObj }
  optimalWindow: null,
  queuedTransactions: [],
  activeWalletId: null, // "ledger" or "trezor" etc (mock)
  isLoading: false,
  error: null,

  // Actions
  fetchPortfolio: async (userId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await fetch(`${API_BASE}/portfolio/${userId}`);
      const result = await response.json();
      if (result.success) {
        set({ portfolio: result.data, isLoading: false });
      }
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchLPPositions: async (userId) => {
    try {
      const response = await fetch(`${API_BASE}/lp/${userId}`);
      const result = await response.json();
      if (result.success) {
        set({ lpPositions: result.data });
      }
    } catch (error) {
      console.error('LP fetch error:', error);
    }
  },

  fetchGasMetrics: async (chain = 'ethereum') => {
    try {
      const response = await fetch(`${API_BASE}/gas/${chain}`);
      const result = await response.json();
      if (result.success) {
        set(state => ({
          gasMetrics: {
            ...state.gasMetrics,
            [chain]: result.data
          }
        }));
      }
    } catch (error) {
      console.error('Gas fetch error:', error);
    }
  },

  fetchOptimalWindow: async () => {
    try {
      const response = await fetch(`${API_BASE}/gas/optimal-window`);
      const result = await response.json();
      if (result.success) {
        set({ optimalWindow: result.data });
      }
    } catch (error) {
      console.error('Window fetch error:', error);
    }
  },

  queueTransaction: async (chain, targetGas, ttlHours) => {
    set({ isLoading: true });
    try {
      const response = await fetch(`${API_BASE}/gas/queue`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chain, target_gas_gwei: targetGas, ttl_hours: ttlHours })
      });
      const result = await response.json();
      if (result.success) {
        set(state => ({
          queuedTransactions: [...state.queuedTransactions, result.data],
          isLoading: false
        }));
      }
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  setActiveWallet: (walletId) => set({ activeWalletId: walletId }),

  reset: () => set({
    portfolio: null,
    walletBalances: {},
    lpPositions: [],
    gasMetrics: {},
    optimalWindow: null,
    queuedTransactions: [],
    isLoading: false,
    error: null
  })
}));

export { useWeb3Store };
export default useWeb3Store;
