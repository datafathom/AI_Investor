import apiClient from './apiClient';
import presenceService from './presenceService';

/**
 * Telemetry Service
 * Handles real-time system metrics, session timing, and activity history.
 */
class TelemetryService {
    constructor() {
        this.metrics = {
            quota: { used: 0, total: 1000, percentage: 0 },
            latency: {},
            systemLoad: [],
            cliHistory: []
        };
        this.listeners = new Set();
        this.pollingInterval = null;
    }

    /**
     * Starts polling for system metrics.
     */
    startPolling(interval = 5000) {
        if (this.pollingInterval) return;
        
        this.fetchMetrics();
        this.pollingInterval = setInterval(() => {
            this.fetchMetrics();
        }, interval);

        // Also listen for real-time events from presence service
        presenceService.on('system:log', (log) => {
            this.metrics.cliHistory.unshift(log);
            if (this.metrics.cliHistory.length > 50) this.metrics.cliHistory.pop();
            this.notify();
        });
    }

    /**
     * Stops polling.
     */
    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }

    /**
     * Fetches current metrics from the API.
     */
    async fetchMetrics() {
        try {
            // In a real app, these might be separate calls or a single telemetry endpoint
            const [quota, health, load] = await Promise.all([
                apiClient.get('/system/quota'),
                apiClient.get('/system/health'), // Latency usually comes from here
                apiClient.get('/system/load')
            ]);

            this.metrics.quota = quota.data || this.metrics.quota;
            this.metrics.latency = health.data?.latency || {};
            this.metrics.systemLoad = load.data || [];
            
            this.notify();
        } catch (error) {
            console.error('Failed to fetch telemetry metrics:', error);
        }
    }

    /**
     * Getters for components
     */
    getQuota() { return this.metrics.quota; }
    getLatency() { return this.metrics.latency; }
    getSystemLoad() { return this.metrics.systemLoad; }
    getCliHistory() { return this.metrics.cliHistory; }

    /**
     * Observer pattern
     */
    subscribe(callback) {
        this.listeners.add(callback);
        return () => this.listeners.delete(callback);
    }

    notify() {
        this.listeners.forEach(callback => callback(this.metrics));
    }
}

export const telemetryService = new TelemetryService();
export default telemetryService;
