/**
 * Scenario Store - Zustand State Management for What-If Simulator
 * : Manages macro shock scenarios and portfolio impact simulation.
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useScenarioStore = create((set, get) => ({
    // State
    scenarios: [],
    activeScenario: null,
    impactResults: null,
    hedgeSufficiency: 0,
    recoveryProjection: null,
    isSimulating: false,
    error: null,
    
    // Preset scenarios
    presetScenarios: [
        { id: 'recession', name: '2008-style Recession', equityDrop: -50, bondDrop: -10, goldChange: 25 },
        { id: 'inflation', name: 'Stagflation Shock', equityDrop: -30, bondDrop: -20, goldChange: 40 },
        { id: 'bankrun', name: 'Bank Run / Liquidity Crisis', equityDrop: -40, bondDrop: 5, goldChange: 15 },
        { id: 'war', name: 'Geopolitical Conflict', equityDrop: -25, bondDrop: 0, goldChange: 20 },
    ],
    
    // Actions
    setScenarios: (scenarios) => set({ scenarios }),
    setActiveScenario: (scenario) => set({ activeScenario: scenario }),
    setImpactResults: (results) => set({ impactResults: results }),
    setHedgeSufficiency: (sufficiency) => set({ hedgeSufficiency: sufficiency }),
    setRecoveryProjection: (projection) => set({ recoveryProjection: projection }),
    setSimulating: (simulating) => set({ isSimulating: simulating }),
    setError: (error) => set({ error }),
    
    // Async: Run scenario
    runScenario: async (scenarioId) => {
        const { setSimulating, setError, setImpactResults, setHedgeSufficiency, setRecoveryProjection, presetScenarios } = get();
        setSimulating(true);
        setError(null);
        try {
            const scenario = presetScenarios.find(s => s.id === scenarioId) || { id: scenarioId };
            const response = await apiClient.post('/scenario/simulate', scenario);
            const data = response.data;
            setImpactResults(data.impact);
            setHedgeSufficiency(data.hedge_sufficiency || 0);
            setRecoveryProjection(data.recovery);
        } catch (error) {
            console.error('Scenario simulation error:', error);
            setError(error.message);
        } finally {
            setSimulating(false);
        }
    },

    runRefinedMonteCarlo: async (scenarioId, initialValue) => {
        set({ isSimulating: true });
        try {
            const response = await apiClient.get('/scenario/monte-carlo-refined', {
                params: { scenario_id: scenarioId, initial_value: initialValue }
            });
            set({ recoveryProjection: { ...get().recoveryProjection, mcPaths: response.data }, isSimulating: false });
        } catch (error) {
            set({ error: 'Refined Monte Carlo failed', isSimulating: false });
        }
    },

    fetchBankRunDetails: async (stressLevel = 1.0) => {
        set({ isSimulating: true });
        try {
            const response = await apiClient.get('/scenario/bank-run', { params: { stress_level: stressLevel } });
            set({ impactResults: { ...(get().impactResults || {}), bankRun: response.data }, isSimulating: false });
        } catch (error) {
            set({ error: 'Bank run simulation failed', isSimulating: false });
        }
    },

    runShadowRun: async (initialValue, baselineParams, shadowParams, horizonDays = 30) => {
        set({ isSimulating: true });
        try {
            const response = await apiClient.post('/scenario/shadow-fork', {
                initial_value: initialValue,
                baseline_params: baselineParams,
                shadow_params: shadowParams,
                horizon_days: horizonDays
            });
            set({ 
                impactResults: { 
                    ...(get().impactResults || {}), 
                    shadowRun: response.data 
                }, 
                isSimulating: false 
            });
            return response.data;
        } catch (error) {
            set({ error: 'Shadow run failed', isSimulating: false });
        }
    },
    
    reset: () => set({
        scenarios: [], activeScenario: null, impactResults: null, hedgeSufficiency: 0,
        recoveryProjection: null, isSimulating: false, error: null
    })
}));

export default useScenarioStore;
