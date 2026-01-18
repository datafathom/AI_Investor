/**
 * brokerageService.js
 * 
 * Simulates a high-frequency trading brokerage connection.
 * Provides real-time updates for Liquidity, P&L, and Positions.
 */

const STARTING_CAPITAL = 100000;
const ASSETS = ['NVDA', 'TSLA', 'SPY', 'AMD', 'AAPL', 'MSFT', 'COIN'];

class BrokerageService {
    constructor() {
        this.currentLiquidity = STARTING_CAPITAL;
        this.startingLiquidity = STARTING_CAPITAL; // Reference for Daily P&L
        this.listeners = [];
        this.history = [];

        // Initialize dynamic positions
        this.positions = {
            'NVDA': { symbol: 'NVDA', qty: 50, avgPrice: 480.00, currentPrice: 485.20 },
            'SPY': { symbol: 'SPY', qty: 100, avgPrice: 450.00, currentPrice: 452.10 },
            'TSLA': { symbol: 'TSLA', qty: -20, avgPrice: 220.00, currentPrice: 218.50 },
        };

        // Initialize market prices
        this.marketPrices = {};
        ASSETS.forEach(asset => {
            // Default to some price if not in initial positions
            this.marketPrices[asset] = this.positions[asset] ? this.positions[asset].currentPrice : (100 + Math.random() * 400);
        });

        // Start simulation loop
        setInterval(() => this.simulateMarketMove(), 1000);
        setInterval(() => this.simulateTrade(), 5000);
    }

    getAccountSummary() {
        const positionsArray = Object.values(this.positions).map(pos => {
            const marketValue = pos.qty * pos.currentPrice;
            const costBasis = pos.qty * pos.avgPrice;
            const pl = pos.qty > 0 ? (marketValue - costBasis) : (costBasis - marketValue); // Short logic approximation
            const plPercent = (pl / Math.abs(costBasis)) * 100;

            return {
                ...pos,
                value: marketValue,
                pl,
                plPercent: plPercent.toFixed(2) + '%'
            };
        });

        const totalEquity = this.currentLiquidity + positionsArray.reduce((acc, pos) => acc + (pos.qty * pos.currentPrice), 0);
        const dailyPL = totalEquity - this.startingLiquidity;

        return {
            liquidity: this.currentLiquidity,
            buyingPower: this.currentLiquidity * 4, // 4x Margin
            dailyPL: dailyPL,
            equity: totalEquity,
            positions: positionsArray
        };
    }

    simulateMarketMove() {
        // Update random prices
        ASSETS.forEach(asset => {
            const move = (Math.random() - 0.48) * 2; // Slight upward drift bias
            let price = this.marketPrices[asset] || (100 + Math.random() * 100);
            price += move;
            if (price < 1) price = 1;
            this.marketPrices[asset] = price;

            // Update position current price
            if (this.positions[asset]) {
                this.positions[asset].currentPrice = price;
            }
        });

        this.notify({
            type: 'MARKET_UPDATE',
            data: this.getAccountSummary()
        });
    }

    simulateTrade() {
        if (Math.random() > 0.7) return; // Not every tick is a trade

        const symbol = ASSETS[Math.floor(Math.random() * ASSETS.length)];
        const side = Math.random() > 0.5 ? 'BUY' : 'SELL';
        const qty = Math.floor(Math.random() * 50) + 1;
        const price = this.marketPrices[symbol];
        const cost = qty * price;

        // Validation (Simple)
        if (side === 'BUY' && this.currentLiquidity < cost) return; // Not enough cash

        // Execute
        if (side === 'BUY') {
            this.currentLiquidity -= cost;
            if (!this.positions[symbol]) {
                this.positions[symbol] = { symbol, qty: 0, avgPrice: 0, currentPrice: price };
            }
            // Update Avg Price
            const pos = this.positions[symbol];
            const oldCost = pos.qty * pos.avgPrice;
            pos.qty += qty;
            pos.avgPrice = (oldCost + cost) / pos.qty;
        } else {
            // SELL
            this.currentLiquidity += cost;
            if (!this.positions[symbol]) {
                // Open Short
                this.positions[symbol] = { symbol, qty: 0, avgPrice: price, currentPrice: price };
            }
            const pos = this.positions[symbol];
            // If reducing long position, avg price stays same. If flipping to short, it's complex.
            // Simplified: Just reduce qty.
            pos.qty -= qty;
            if (pos.qty === 0) delete this.positions[symbol];
        }

        const trade = {
            id: Date.now(),
            time: new Date().toLocaleTimeString(),
            symbol,
            side,
            qty,
            price: price.toFixed(2),
            total: (qty * price).toFixed(2),
            reason: this.generateAIReason(symbol, side)
        };

        this.history.unshift(trade);
        if (this.history.length > 50) this.history.pop();

        this.notify({
            type: 'TRADE_FILL',
            data: trade
        });

        // Also trigger update for balances
        this.notify({
            type: 'MARKET_UPDATE',
            data: this.getAccountSummary()
        });
    }

    generateAIReason(symbol, side) {
        const reasons = [
            `MACD Crossover confirmed on 5m timeframe for ${symbol}.`,
            `Sentiment scores for ${symbol} sector turned ${side === 'BUY' ? 'Bullish' : 'Bearish'}.`,
            `Delta divergence detected in options chain.`,
            `Mean reversion setup triggered at ${side === 'BUY' ? 'Support' : 'Resistance'}.`,
            `Political Alpha: Senator transaction correlated with price action.`,
            `RSI Divergence detected on 15m chart.`,
            `Volume spike detected > 300% relative volume.`
        ];
        return reasons[Math.floor(Math.random() * reasons.length)];
    }

    subscribe(callback) {
        this.listeners.push(callback);
        // Initial callback
        callback({ type: 'INIT', data: this.getAccountSummary() });
        return () => {
            this.listeners = this.listeners.filter(l => l !== callback);
        };
    }

    notify(event) {
        this.listeners.forEach(cb => cb(event));
    }

    getTradeHistory() {
        return this.history;
    }
}

export const brokerageService = new BrokerageService();
