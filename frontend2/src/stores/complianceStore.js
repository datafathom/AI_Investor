/**
 * Compliance Store - Zustand State Management for Audit & SAR
 * Phase 59: Manages audit logs, SAR workflow, and compliance monitoring.
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

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
            const response = await apiClient.get('/compliance/audit', { params: { limit } });
            set({ auditLogs: response.data || [], isLoading: false });
        } catch (error) {
            set({ error: 'Failed to fetch audit logs', isLoading: false });
        }
    },

    fetchSarAlerts: async () => {
        set({ isLoading: true });
        try {
            const response = await apiClient.get('/compliance/sar');
            set({ 
                sarAlerts: response.data || [], 
                isLoading: false 
            });
        } catch (error) {
            set({ error: 'Failed to fetch SAR alerts', isLoading: false });
        }
    },

    fetchOverview: async () => {
        try {
            const response = await apiClient.get('/compliance/overview');
            set({ complianceOverview: response.data });
        } catch (error) {
            console.error('Failed to fetch overview:', error);
        }
    },

    updateSarStatus: async (id, status) => {
        try {
            await apiClient.post(`/compliance/sar/${id}/status`, null, { params: { status } });
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
            const response = await apiClient.get('/compliance/verify');
            set({ verificationStatus: response.data, isLoading: false });
            return response.data;
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
