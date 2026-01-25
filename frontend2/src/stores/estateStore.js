/**
 * Estate Store - Zustand State Management for Estate Planning
 * Phase 58: Manages beneficiaries, dead man's switch, and succession planning.
 */
import { create } from 'zustand';

const useEstateStore = create((set, get) => ({
    // State
    beneficiaries: [],
    heartbeatStatus: { lastCheck: null, isAlive: true, daysUntilTrigger: 30, triggerDate: null },
    entityGraph: { nodes: [], edges: [] },
    successionPlan: null,
    isHeartbeatEnabled: false,
    isLoading: false,
    error: null,
    
    // Actions
    setBeneficiaries: (beneficiaries) => set({ beneficiaries }),
    addBeneficiary: (b) => set((s) => ({ beneficiaries: [...s.beneficiaries, b] })),
    removeBeneficiary: (id) => set((s) => ({ beneficiaries: s.beneficiaries.filter(b => b.id !== id) })),
    setHeartbeatStatus: (status) => set({ heartbeatStatus: status }),
    setEntityGraph: (graph) => set({ entityGraph: graph }),
    toggleHeartbeat: (enabled) => set({ isHeartbeatEnabled: enabled }),
    setError: (error) => set({ error }),
    
    // Async: Fetch all estate data
    fetchEstateData: async () => {
        set({ isLoading: true });
        try {
            const [bRes, hRes, gRes] = await Promise.all([
                fetch('/api/v1/estate/beneficiaries'),
                fetch('/api/v1/estate/heartbeat'),
                fetch('/api/v1/estate/graph')
            ]);
            
            const [beneficiaries, heartbeatStatus, entityGraph] = await Promise.all([
                bRes.json(),
                hRes.json(),
                gRes.json()
            ]);
            
            set({ beneficiaries, heartbeatStatus, entityGraph, isLoading: false });
        } catch (error) {
            console.error('Failed to fetch estate data:', error);
            set({ error: 'Failed to synchronize estate protocol', isLoading: false });
        }
    },
    
    // Async: Confirm alive
    confirmAlive: async () => {
        try {
            const response = await fetch('/api/v1/estate/heartbeat/confirm', { method: 'POST' });
            if (response.ok) {
                const hRes = await fetch('/api/v1/estate/heartbeat');
                const heartbeatStatus = await hRes.json();
                set({ heartbeatStatus });
            }
        } catch (error) {
            console.error('Confirm alive failed:', error);
        }
    },

    // Async: Update allocation
    updateAllocation: async (beneficiaryId, percent) => {
        try {
            const response = await fetch('/api/v1/estate/beneficiaries/allocation', {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ beneficiary_id: beneficiaryId, percent })
            });
            if (response.ok) {
                set((s) => ({
                    beneficiaries: s.beneficiaries.map(b => 
                        b.id === beneficiaryId ? { ...b, allocation_percent: percent } : b
                    )
                }));
            }
        } catch (error) {
            console.error('Allocation update failed:', error);
        }
    },
    
    reset: () => set({
        beneficiaries: [], 
        heartbeatStatus: { lastCheck: null, isAlive: true, daysUntilTrigger: 30, triggerDate: null },
        entityGraph: { nodes: [], edges: [] },
        successionPlan: null, 
        isHeartbeatEnabled: false, 
        isLoading: false,
        error: null
    })
}));

export default useEstateStore;
