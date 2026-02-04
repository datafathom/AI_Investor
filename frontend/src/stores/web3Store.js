import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useWeb3Store = create((set, get) => ({
  // State
  portfolio: null,
  walletBalances: {}, // { "chain:address": BalanceObj }
  lpPositions: [],
  gasMetrics: {}, // { "ethereum": MetricsObj }
  optimalWindow: null,
  queuedTransactions: [],
  liquidityDepth: {}, // { poolAddress: depthData }
  activeWalletId: null, // "ledger" or "trezor" etc (mock)
  isLoading: false,
  error: null,

  // Actions
  fetchPortfolio: async (userId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await apiClient.get(`/web3/portfolio/${userId}`);
      if (response.data.success) {
        set({ portfolio: response.data.data, isLoading: false });
      }
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchLPPositions: async (userId) => {
    try {
      const response = await apiClient.get(`/web3/lp/${userId}`);
      if (response.data.success) {
        set({ lpPositions: response.data.data });
      }
    } catch (error) {
      console.error('LP fetch error:', error);
    }
  },

  fetchGasMetrics: async (chain = 'ethereum') => {
    try {
      const response = await apiClient.get(`/web3/gas/${chain}`);
      if (response.data.success) {
        set(state => ({
          gasMetrics: {
            ...state.gasMetrics,
            [chain]: response.data.data
          }
        }));
      }
    } catch (error) {
      console.error('Gas fetch error:', error);
    }
  },

  fetchOptimalWindow: async () => {
    try {
      const response = await apiClient.get('/web3/gas/optimal-window');
      if (response.data.success) {
        set({ optimalWindow: response.data.data });
      }
    } catch (error) {
      console.error('Window fetch error:', error);
    }
  },

  queueTransaction: async (chain, targetGas, ttlHours) => {
    set({ isLoading: true });
    try {
      const response = await apiClient.post('/web3/gas/queue', {
        chain,
        target_gas_gwei: targetGas,
        ttl_hours: ttlHours
      });
      if (response.data.success) {
        set(state => ({
          queuedTransactions: [...state.queuedTransactions, response.data.data],
          isLoading: false
        }));
      }
    } catch (error) {
      set({ error: error.message, isLoading: false });
    }
  },

  fetchLiquidityDepth: async (poolAddress) => {
    try {
      const response = await apiClient.get(`/web3/liquidity/depth/${poolAddress}`);
      if (response.data.success) {
        set(state => ({
          liquidityDepth: {
            ...state.liquidityDepth,
            [poolAddress]: response.data.data
          }
        }));
      }
    } catch (error) {
      console.error('Liquidity depth fetch failed:', error);
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
