/**
 * Zen Store - Zustand State Management for Homeostasis Mode
 * Phase 68: Manages "Enough" metric, retirement countdown, and autopilot override.
 */
import { create } from 'zustand';

const useZenStore = create((set, get) => ({
    // State
    freedomNumber: 0,
    currentProgress: 0,
    yearsOfExpenses: 0,
    retirementProbability: 0,
    autopilotEnabled: false,
    zenModeActive: false,
    enoughThreshold: 1.0,
    monthlyBurn: 0,
    error: null,
    
    // Actions
    setFreedomNumber: (number) => set({ freedomNumber: number }),
    setCurrentProgress: (progress) => set({ currentProgress: progress }),
    setYearsOfExpenses: (years) => set({ yearsOfExpenses: years }),
    setRetirementProbability: (prob) => set({ retirementProbability: prob }),
    setAutopilotEnabled: (enabled) => set({ autopilotEnabled: enabled }),
    setZenModeActive: (active) => set({ zenModeActive: active }),
    setEnoughThreshold: (threshold) => set({ enoughThreshold: threshold }),
    setMonthlyBurn: (burn) => set({ monthlyBurn: burn }),
    setError: (error) => set({ error }),
    
    // Computed
    isEnoughReached: () => {
        const { currentProgress, enoughThreshold } = get();
        return currentProgress >= enoughThreshold;
    },
    
    // Async: Calculate homeostasis
    calculateHomeostasis: async () => {
        const { setCurrentProgress, setYearsOfExpenses, setRetirementProbability, setError } = get();
        try {
            const response = await fetch('/api/v1/homeostasis/calculate');
            if (!response.ok) throw new Error('Homeostasis calc failed');
            const data = await response.json();
            setCurrentProgress(data.freedom_progress || 0);
            setYearsOfExpenses(data.years_covered || 0);
            setRetirementProbability(data.retirement_probability || 0);
        } catch (error) {
            console.error('Homeostasis calc error:', error);
            setError(error.message);
        }
    },
    
    // Async: Toggle autopilot
    toggleAutopilot: async (enabled) => {
        const { setAutopilotEnabled, setError } = get();
        try {
            await fetch('/api/v1/homeostasis/autopilot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ enabled })
            });
            setAutopilotEnabled(enabled);
        } catch (error) {
            console.error('Autopilot toggle error:', error);
            setError(error.message);
        }
    },
    
    // Async: Run retirement Monte Carlo
    runRetirementMonteCarlo: async (params) => {
        const { setRetirementProbability, setError } = get();
        try {
            const response = await fetch('/api/v1/homeostasis/retirement-sim', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params)
            });
            const data = await response.json();
            setRetirementProbability(data.success_probability || 0);
            return data;
        } catch (error) {
            console.error('Retirement sim error:', error);
            setError(error.message);
            throw error;
        }
    },
    
    reset: () => set({
        freedomNumber: 0, currentProgress: 0, yearsOfExpenses: 0, retirementProbability: 0,
        autopilotEnabled: false, zenModeActive: false, enoughThreshold: 1.0, monthlyBurn: 0, error: null
    })
}));

export default useZenStore;
