/**
 * System Health Store - Zustand State Management for Infrastructure
 * Phase 62: Manages Kafka, Postgres, Neo4j health and agent load balancing.
 */
import { create } from 'zustand';
import apiClient from '../services/apiClient';

const useSystemHealthStore = create((set, get) => ({
    // State
    kafkaHealth: { messagesPerSecond: 0, lag: 0, topics: [], status: 'unknown' },
    postgresHealth: { connections: 0, queryTime: 0, diskUsage: 0, status: 'unknown' },
    neo4jHealth: { nodes: 0, relationships: 0, queryTime: 0, status: 'unknown' },
    agentLoad: [],
    auditStream: [],
    quotas: {},
    overallStatus: 'unknown',
    lastRefresh: null,
    error: null,
    
    // Actions
    setKafkaHealth: (health) => set({ kafkaHealth: health }),
    setPostgresHealth: (health) => set({ postgresHealth: health }),
    setNeo4jHealth: (health) => set({ neo4jHealth: health }),
    setAgentLoad: (load) => set({ agentLoad: load }),
    setOverallStatus: (status) => set({ overallStatus: status }),
    setError: (error) => set({ error }),
    
    // Async: Refresh all health
    refreshHealth: async () => {
        const { setKafkaHealth, setPostgresHealth, setNeo4jHealth, setAgentLoad, setOverallStatus, setError } = get();
        try {
            const response = await apiClient.get('/system/health');
            const data = response.data;
            if (data.kafka) setKafkaHealth(data.kafka);
            if (data.postgres) setPostgresHealth(data.postgres);
            if (data.neo4j) setNeo4jHealth(data.neo4j);
            if (data.agents) setAgentLoad(data.agents);
            setOverallStatus(data.overall_status || 'healthy');
            set({ lastRefresh: new Date().toISOString() });
        } catch (error) {
            console.error('Health refresh failed:', error);
            setError(error.message);
            setOverallStatus('error');
        }
    },
    
    // Async: Restart consumer
    restartConsumer: async (consumerId) => {
        try {
            await apiClient.post(`/system/kafka/restart/${consumerId}`);
        } catch (error) {
            console.error('Consumer restart failed:', error);
        }
    },

    fetchAuditStream: async () => {
        try {
            const response = await apiClient.get('/system/audit/stream');
            if (response.data.success) {
                set({ auditStream: response.data.data });
            }
        } catch (error) {
            console.error('Audit stream fetch failed:', error);
        }
    },

    fetchQuotas: async () => {
        try {
            const response = await apiClient.get('/system/quotas');
            if (response.data.success) {
                set({ quotas: response.data.data });
            }
        } catch (error) {
            console.error('Quotas fetch failed:', error);
        }
    },
    
    reset: () => set({
        kafkaHealth: { messagesPerSecond: 0, lag: 0, topics: [], status: 'unknown' },
        postgresHealth: { connections: 0, queryTime: 0, diskUsage: 0, status: 'unknown' },
        neo4jHealth: { nodes: 0, relationships: 0, queryTime: 0, status: 'unknown' },
        agentLoad: [], overallStatus: 'unknown', lastRefresh: null, error: null
    })
}));

export default useSystemHealthStore;
