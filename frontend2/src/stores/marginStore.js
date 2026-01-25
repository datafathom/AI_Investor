/**
 * Margin Store - Zustand State Management for Margin & Collateral
 * Phase 64: Manages margin buffer, liquidation distance, and de-leveraging.
 */
import { create } from 'zustand';

const useMarginStore = create((set, get) => ({
    // State
    marginBuffer: 0,
    marginUsed: 0,
    marginAvailable: 0,
    liquidationDistance: 100,
    positions: [],
    collateralPriority: [],
    dangerZone: false,
    deleveragePlan: null,
    error: null,
    
    // Actions
    setMarginBuffer: (buffer) => set({ marginBuffer: buffer, dangerZone: buffer < 20 }),
    setMarginStats: (stats) => set({ marginUsed: stats.used, marginAvailable: stats.available }),
    setLiquidationDistance: (distance) => set({ liquidationDistance: distance }),
    setPositions: (positions) => set({ positions }),
    setCollateralPriority: (priority) => set({ collateralPriority: priority }),
    setDeleveragePlan: (plan) => set({ deleveragePlan: plan }),
    setError: (error) => set({ error }),
    
    // Async: Fetch margin data
    fetchMarginData: async () => {
        try {
            const response = await fetch('/api/v1/margin/status');
            const data = await response.json();
            set({
                marginBuffer: data.buffer || 0,
                marginUsed: data.used || 0,
                marginAvailable: data.available || 0,
                liquidationDistance: data.liquidation_distance || 100,
                dangerZone: (data.buffer || 0) < 20
            });
        } catch (error) {
            console.error('Fetch margin failed:', error);
        }
    },
    
    // Async: Generate deleverage plan
    generateDeleveragePlan: async (targetBuffer) => {
        const { setDeleveragePlan, setError } = get();
        try {
            const response = await fetch('/api/v1/margin/deleverage', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ target_buffer: targetBuffer })
            });
            const data = await response.json();
            setDeleveragePlan(data.plan);
        } catch (error) {
            console.error('Deleverage plan failed:', error);
            setError(error.message);
        }
    },
    
    reset: () => set({
        marginBuffer: 0, marginUsed: 0, marginAvailable: 0, liquidationDistance: 100,
        positions: [], collateralPriority: [], dangerZone: false, deleveragePlan: null, error: null
    })
}));

export default useMarginStore;
