import apiClient from './apiClient';
import { workerManager } from './workerManager';

class BrokerageService {
    constructor() {
        this.listeners = [];
        // Hydrate from LocalStorage for instant UI (Stale-while-revalidate)
        const cached = localStorage.getItem('last_brokerage_summary');
        this.currentData = cached ? JSON.parse(cached) : null;
        this.interval = null;
    }

    /**
     * Start a real-time polling loop for account updates.
     */
    startPolling(intervalMs = 5000) {
        if (this.interval) return;
        this.fetchUpdates();
        this.interval = setInterval(() => this.fetchUpdates(), intervalMs);
    }

    stopPolling() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }

    async fetchUpdates() {
        try {
            // Use apiClient with cache flag for the raw requests if appropriate
            // But for real-time brokerage, we usually want fresh data.
            // We use the worker to keep the UI thread smooth during transformation.
            const [status, positions] = await Promise.all([
                apiClient.get('/brokerage/status'),
                apiClient.get('/brokerage/positions')
            ]);

            // Offload transformation to Web Worker
            const transformedData = await workerManager.runTask('TRANSFORM_BROKERAGE_DATA', {
                status,
                positions
            });

            this.currentData = transformedData;
            
            // Persist for next session hydration
            localStorage.setItem('last_brokerage_summary', JSON.stringify(transformedData));
            
            this.notify({ type: 'MARKET_UPDATE', data: transformedData });
        } catch (error) {
            console.error('brokerageService poll error:', error);
        }
    }

    getAccountSummary() {
        // If data hasn't loaded yet, return skeleton
        return this.currentData || {
            liquidity: 0,
            buyingPower: 0,
            dailyPL: 0,
            equity: 0,
            positions: []
        };
    }

    async executeOrder(symbol, side, qty) {
        try {
            const result = await apiClient.post('/brokerage/order', { 
                symbol, side, qty, type: 'market' 
            });
            
            this.notify({ type: 'TRADE_FILL', data: { ...result, symbol, side, qty } });
            await this.fetchUpdates(); // Fast refresh
            return { success: true, ...result };
        } catch (error) {
            console.error('Order execution failed:', error);
            return { success: false, error: error.response?.data?.error || 'Execution rejected' };
        }
    }

    subscribe(callback) {
        this.listeners.push(callback);
        // If we have data, send initial trigger
        if (this.currentData) {
            callback({ type: 'INIT', data: this.currentData });
        }
        // Auto-start polling if this is the first listener
        if (this.listeners.length === 1) {
            this.startPolling();
        }
        return () => {
            this.listeners = this.listeners.filter(l => l !== callback);
            if (this.listeners.length === 0) {
                this.stopPolling();
            }
        };
    }

    notify(event) {
        this.listeners.forEach(cb => cb(event));
    }

    getTradeHistory() {
        // Future: Fetch from /api/v1/brokerage/history
        return [];
    }
}

export const brokerageService = new BrokerageService();
