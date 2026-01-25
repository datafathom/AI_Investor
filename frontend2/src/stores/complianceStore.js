/**
 * Compliance Store - Zustand State Management for Audit & SAR
 * Phase 59: Manages audit logs, SAR workflow, and compliance monitoring.
 */
import { create } from 'zustand';

const useComplianceStore = create((set, get) => ({
    // State
    auditLogs: [],
    sarAlerts: [],
    complianceOverview: {
        compliance_score: 100,
        pending_alerts: 0,
        total_logs: 0
    },
    isMonitoring: true,
    verificationStatus: null, // { is_valid, errors, timestamp }
    isLoading: false,
    error: null,
    
    // Actions
    fetchAuditLogs: async (limit = 100) => {
        set({ isLoading: true });
        try {
            const response = await fetch(`/api/v1/compliance/audit?limit=${limit}`);
            const data = await response.json();
            set({ auditLogs: data || [], isLoading: false });
        } catch (error) {
            set({ error: 'Failed to fetch audit logs', isLoading: false });
        }
    },

    fetchSarAlerts: async () => {
        set({ isLoading: true });
        try {
            const response = await fetch('/api/v1/compliance/sar');
            const data = await response.json();
            set({ 
                sarAlerts: data || [], 
                isLoading: false 
            });
        } catch (error) {
            set({ error: 'Failed to fetch SAR alerts', isLoading: false });
        }
    },

    fetchOverview: async () => {
        try {
            const response = await fetch('/api/v1/compliance/overview');
            const data = await response.json();
            set({ complianceOverview: data });
        } catch (error) {
            console.error('Failed to fetch overview:', error);
        }
    },

    updateSarStatus: async (id, status) => {
        try {
            await fetch(`/api/v1/compliance/sar/${id}/status?status=${status}`, { method: 'POST' });
            set((s) => ({
                sarAlerts: s.sarAlerts.map(a => a.id === id ? { ...a, status } : a)
            }));
            get().fetchOverview();
        } catch (error) {
            set({ error: 'Failed to update SAR status' });
        }
    },

    verifyIntegrity: async () => {
        set({ isLoading: true });
        try {
            const response = await fetch('/api/v1/compliance/verify');
            const data = await response.json();
            set({ verificationStatus: data, isLoading: false });
            return data;
        } catch (error) {
            set({ error: 'Integrity verification failed', isLoading: false });
        }
    },

    pauseAgent: (agentId) => {
        // Mock pause action
        console.log(`Agent ${agentId} paused by compliance monitor.`);
        set((s) => ({
            auditLogs: [{
                id: `SYS-${Date.now()}`,
                timestamp: new Date().toISOString(),
                action: 'AGENT_PAUSE',
                resource: agentId,
                status: 'success',
                severity: 'warning',
                details: { reason: 'Compliance trigger' }
            }, ...s.auditLogs]
        }));
    },
    
    reset: () => set({
        auditLogs: [], sarAlerts: [], complianceOverview: { compliance_score: 100, pending_alerts: 0, total_logs: 0 },
        isMonitoring: true, verificationStatus: null, error: null
    })
}));

export default useComplianceStore;
