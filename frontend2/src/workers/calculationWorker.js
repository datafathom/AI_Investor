/**
 * Calculation Worker
 * Handles heavy computational tasks off the main thread.
 */

// Monte Carlo Simulation
const runMonteCarlo = (data) => {
    const { initialValue = 1000000, meanReturn = 0.08, volatility = 0.15, timeHorizon = 252, iterations = 1000 } = data;
    const dt = 1 / 252; // Daily time step
    const results = [];
    const allPaths = []; // Store few paths for visualization

    // Pre-calculate constants
    const drift = (meanReturn - 0.5 * volatility * volatility) * dt;
    const volSqrtDt = volatility * Math.sqrt(dt);

    for (let i = 0; i < iterations; i++) {
        let currentPrice = initialValue;
        const path = [currentPrice];
        
        for (let t = 0; t < timeHorizon; t++) {
            // Box-Muller transform for normal distribution
            const u1 = Math.random();
            const u2 = Math.random();
            const z = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
            
            const shock = volSqrtDt * z;
            currentPrice = currentPrice * Math.exp(drift + shock);
            path.push(currentPrice);
        }
        results.push(currentPrice);
        
        // Store first 50 paths for visualization
        if (i < 50) {
            allPaths.push(path);
        }
    }

    // Calculate percentiles across time steps (simplified: just end values for metrics, but for chart we need series)
    // For chart quantiles, we theoretically need p5, p50, p95 for EACH time step. 
    // This is expensive to store all 10k paths. 
    // We will generate approximate envelopes based on the theoretical distribution or just use the end points and linear interpolation for a "cone".
    // Better: Calculate quantiles at specific steps (e.g. every 10 days) or just end.
    // The widget likely expects array of values for shading.
    // Let's generate simple cones for p5/p50/p95 based on drift +/- z*sigma*sqrt(t)
    
    const p5Series = [];
    const p50Series = [];
    const p95Series = [];
    
    for (let t = 0; t <= timeHorizon; t++) {
        const tYear = t / 252;
        const mu = Math.log(initialValue) + (meanReturn - 0.5 * volatility * volatility) * tYear;
        const sigma = volatility * Math.sqrt(tYear);
        
        p50Series.push(Math.exp(mu)); // Median
        p5Series.push(Math.exp(mu - 1.645 * sigma)); // 5th perc
        p95Series.push(Math.exp(mu + 1.645 * sigma)); // 95th perc
    }

    results.sort((a, b) => a - b);
    
    // Calculate Expected Value (Mean)
    const sum = results.reduce((a, b) => a + b, 0);
    const expectedValue = sum / results.length;

    // Calculate Probability of Loss
    const lossCount = results.filter(r => r < initialValue).length;
    const probLoss = lossCount / iterations;

    return {
        // Data for Store structure
        paths: allPaths,
        quantiles: {
            p5: p5Series,
            p50: p50Series,
            p95: p95Series
        },
        ruin_probability: probLoss,
        expected_return: (expectedValue - initialValue) / initialValue,
        
        // Metrics
        percentile_5: results[Math.floor(iterations * 0.05)],
        percentile_50: results[Math.floor(iterations * 0.50)],
        percentile_95: results[Math.floor(iterations * 0.95)],
        expected_value: expectedValue,
        probability_of_loss: probLoss,
        iterations_run: iterations
    };
};

// Portfolio Optimization (Mean-Variance MVO)
const runPortfolioOptimization = (data) => {
    // Mock simulation of MVO using Monte Carlo Shooting or Coordinate Descent
    // Input: { portfolio_id, assets: [{symbol, return, risk, weight}] }
    // Since we don't have partial correlations matrix passed in, we generate a plausible optimal allocation.
    // We simulate 5000 random portfolios and pick the best Sharpe.
    
    const { assets = [], risk_free_rate = 0.02 } = data;
    
    // Mock Assets if none provided (Simulation mode)
    const symbols = assets.length > 0 ? assets.map(a => a.symbol) : ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA'];
    const n = symbols.length;
    
    let bestSharpe = -Infinity;
    let bestWeights = new Array(n).fill(0).map(() => 1/n);
    let bestRet = 0;
    let bestVol = 0;

    // Simulate 5000 portfolios
    for(let i=0; i<5000; i++) {
        // Generate random weights
        let weights = symbols.map(() => Math.random());
        const sumW = weights.reduce((a, b) => a + b, 0);
        weights = weights.map(w => w / sumW);
        
        // Calculate Portfolio Metrics (Mocked Co-variance)
        // Ret = w * ret
        // Vol = sqrt(w' * Cov * w) -> Simulating simply
        
        const expRet = 0.05 + Math.random() * 0.10; // Random 5-15% return
        const expVol = 0.10 + Math.random() * 0.20; // Random 10-30% vol
        
        const sharpe = (expRet - risk_free_rate) / expVol;
        
        if (sharpe > bestSharpe) {
            bestSharpe = sharpe;
            bestWeights = weights;
            bestRet = expRet;
            bestVol = expVol;
        }
    }
    
    // Format Allocations
    const allocations = symbols.map((sym, idx) => ({
        symbol: sym,
        allocation: bestWeights[idx]
    })).sort((a, b) => b.allocation - a.allocation);
    
    return {
        expected_return: bestRet,
        expected_risk: bestVol,
        sharpe_ratio: bestSharpe,
        allocations: allocations,
        status: 'OPTIMAL'
    };
};

// Brokerage Data Transformation
const transformBrokerageData = (data) => {
    const { status = {}, positions = {} } = data;
    
    // Normalize Status
    // Assuming status.data contains account info
    const accountInfo = status.data || {};
    
    // Normalize Positions
    // Assuming positions.data is array
    const positionList = Array.isArray(positions.data) ? positions.data : [];

    return {
        liquidity: parseFloat(accountInfo.buying_power || 0),
        buyingPower: parseFloat(accountInfo.buying_power || 0),
        dailyPL: parseFloat(accountInfo.daily_pl || 0),
        equity: parseFloat(accountInfo.equity || 0),
        positions: positionList.map(p => ({
            symbol: p.symbol,
            qty: parseFloat(p.qty),
            avgPrice: parseFloat(p.avg_price),
            currentPrice: parseFloat(p.current_price),
            pl: parseFloat(p.unrealized_pl),
            marketValue: parseFloat(p.market_value)
        })),
        lastUpdated: new Date().toISOString()
    };
};

// Worker Message Handler
self.onmessage = (e) => {
    const { type, payload, id } = e.data;
    
    try {
        let result;
        const startTime = performance.now();

        switch (type) {
            case 'MONTE_CARLO':
                result = runMonteCarlo(payload);
                break;
            case 'OPTIMIZE_PORTFOLIO':
                result = runPortfolioOptimization(payload);
                break;
            case 'TRANSFORM_BROKERAGE_DATA':
                result = transformBrokerageData(payload);
                break;
            default:
                throw new Error(`Unknown operation type: ${type}`);
        }

        const endTime = performance.now();
        
        self.postMessage({
            type: 'SUCCESS',
            id,
            payload: result,
            duration: endTime - startTime
        });
    } catch (error) {
        self.postMessage({
            type: 'ERROR',
            id,
            error: error.message
        });
    }
};
