/**
 * brokerageService.js
 * 
 * Manages institutional brokerage connections and real-time execution.
 * Interfaces with backend brokerage_api.py.
 */

import apiClient from './apiClient';

class BrokerageService {
    constructor() {
        this.listeners = [];
        this.currentData = null;
        this.interval = null;
    }

    /**
     * Start a real-time polling loop for account updates.
     * In a production environment, this would ideally use the presenceService (Socket.io).
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
            const [status, positions] = await Promise.all([
                apiClient.get('/brokerage/status'),
                apiClient.get('/brokerage/positions')
            ]);

            // Transform backend data to frontend expected schema
            const transformedData = {
                liquidity: status.total_buying_power / 4, // Logic approximation
                buyingPower: status.total_buying_power,
                dailyPL: status.daily_pl_percentage || 0,
                equity: status.total_buying_power, // Placeholder if equity not in status
                positions: positions.map(pos => ({
                    symbol: pos.symbol,
                    qty: pos.qty,
                    avgPrice: pos.avg_price || 0,
                    currentPrice: pos.current_price || pos.market_value / pos.qty,
                    value: pos.market_value,
                    pl: pos.unrealized_pl,
                    plPercent: ((pos.unrealized_pl / (pos.market_value - pos.unrealized_pl)) * 100).toFixed(2) + '%'
                }))
            };

            this.currentData = transformedData;
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
