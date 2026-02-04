/**
 * dataWorker.js
 * 
 * Performs heavy data transformations and calculations off the main thread.
 */

self.onmessage = (e) => {
  const { type, payload } = e.data;

  switch (type) {
    case 'TRANSFORM_BROKERAGE_DATA':
      const { status, positions } = payload;
      
      // Intensive mapping and P&L calculations
      const transformed = {
        liquidity: status.total_buying_power / 4,
        buyingPower: status.total_buying_power,
        dailyPL: status.daily_pl_percentage || 0,
        equity: status.total_buying_power,
        positions: positions.map(pos => {
          const costBasis = (pos.avg_price || 0) * pos.qty;
          const pl = pos.unrealized_pl;
          const plPercent = costBasis !== 0 
            ? ((pl / costBasis) * 100).toFixed(2) + '%'
            : '0.00%';

          return {
            symbol: pos.symbol,
            qty: pos.qty,
            avgPrice: pos.avg_price || 0,
            currentPrice: pos.current_price || (pos.market_value / pos.qty),
            value: pos.market_value,
            pl: pl,
            plPercent: plPercent
          };
        })
      };

      self.postMessage({ type: 'TRANSFORM_BROKERAGE_DATA_COMPLETE', data: transformed });
      break;

    case 'TRANSFORM_MARKET_DATA':
      const { rawData, symbol } = payload;
      // Simulated complex transformation/normalization
      const marketData = {
        symbol: symbol,
        price: rawData.price || 0,
        change: rawData.change || 0,
        changePercent: rawData.change_percent || '0%',
        volume: rawData.volume || 0,
        lastUpdated: new Date().toLocaleTimeString(),
        performance: (rawData.price > rawData.previous_close ? 'positive' : 'negative')
      };
      self.postMessage({ type: 'TRANSFORM_MARKET_DATA_COMPLETE', data: marketData });
      break;

    case 'CALCULATE_ANALYTICS':
      // Future analytics calculations
      break;

    default:
      console.warn(`[Worker] Unknown message type: ${type}`);
  }
};
