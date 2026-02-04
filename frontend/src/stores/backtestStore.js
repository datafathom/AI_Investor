/**
 * Backtest Store - Zustand State Management for Monte Carlo Backtesting
 * : Manages simulation parameters, paths, and risk metrics.
 */
import { create } from 'zustand';
import { workerManager } from '../services/workerManager';

const useBacktestStore = create((set, get) => ({
    // State
    simulationPaths: [],
    quantiles: { p5: [], p50: [], p95: [] },
    ruinProbability: 0,
    maxDrawdown: 0,
    recoveryDays: 0,
    params: { mu: 0.08, sigma: 0.15, paths: 10000, days: 252 },
    isSimulating: false,
    error: null,
    
    // Actions
    setParams: (params) => set((s) => ({ params: { ...s.params, ...params } })),
    setSimulationPaths: (paths, quantiles) => set({ simulationPaths: paths, quantiles }),
    setRuinProbability: (prob) => set({ ruinProbability: prob }),
    setMaxDrawdown: (dd) => set({ maxDrawdown: dd }),
    setRecoveryDays: (days) => set({ recoveryDays: days }),
    setSimulating: (simulating) => set({ isSimulating: simulating }),
    setError: (error) => set({ error }),
    
    // Async: Run simulation via Worker
    runSimulation: async () => {
        const { params, setSimulating, setError, setSimulationPaths, setRuinProbability } = get();
        setSimulating(true);
        setError(null);
        try {
            // Offload to Web Worker
            const data = await workerManager.runMonteCarlo({
                initialValue: 1000000,
                meanReturn: params.mu,
                volatility: params.sigma,
                timeHorizon: params.days,
                iterations: params.paths
            });
            
            setSimulationPaths(data.paths || [], data.quantiles || {});
            setRuinProbability(data.ruin_probability || 0);
        } catch (error) {
            console.error('Simulation error:', error);
            setError(error.message);
        } finally {
            setSimulating(false);
        }
    },
    
    reset: () => set({
        simulationPaths: [], quantiles: { p5: [], p50: [], p95: [] },
        ruinProbability: 0, maxDrawdown: 0, recoveryDays: 0, isSimulating: false, error: null
    })
}));

export default useBacktestStore;
