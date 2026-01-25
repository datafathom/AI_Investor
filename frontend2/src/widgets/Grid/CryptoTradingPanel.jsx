/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Grid/CryptoTradingPanel.jsx
 * ROLE: Trading Interface
 * PURPOSE: Ticker view, Order Book, and Order Execution form.
 * ==============================================================================
 */

import React, { useEffect, useState } from 'react';
import useExchangeStore from '../../stores/exchangeStore';
import './CryptoTradingPanel.css';

const CryptoTradingPanel = ({ symbol = 'BTCUSDT', mock = true }) => {
    const { ticker, depth, fetchTicker, fetchDepth, placeOrder, loading, orderStatus, error } = useExchangeStore();
    const [side, setSide] = useState('BUY');
    const [quantity, setQuantity] = useState(0.01);
    const [autoRefresh, setAutoRefresh] = useState(true);

    useEffect(() => {
        fetchTicker(symbol, mock);
        fetchDepth(symbol, mock);

        let interval;
        if (autoRefresh) {
            interval = setInterval(() => {
                fetchTicker(symbol, mock);
                fetchDepth(symbol, mock);
            }, 3000);
        }
        return () => clearInterval(interval);
    }, [symbol, mock, autoRefresh, fetchTicker, fetchDepth]);

    const handleTrade = async () => {
        await placeOrder({ symbol, side, quantity }, mock);
    };

    const priceChangeColor = (ticker?.priceChangePercent || 0) >= 0 ? 'green' : 'red';

    return (
        <div className="crypto-trading-panel">
            <header className="panel-header">
                <div className="ticker-info">
                    <h3>{symbol}</h3>
                    {ticker && (
                         <span className={`price ${priceChangeColor}`}>
                             ${parseFloat(ticker.lastPrice).toLocaleString()} 
                             <small>({ticker.priceChangePercent}%)</small>
                         </span>
                    )}
                </div>
                <div className="controls">
                     <label className="toggle-switch">
                         <input 
                            type="checkbox" 
                            checked={autoRefresh} 
                            onChange={(e) => setAutoRefresh(e.target.checked)} 
                         />
                         <span className="slider"></span>
                     </label>
                     <span className="live-tag">LIVE</span>
                </div>
            </header>

            <div className="panel-content">
                {/* Order Book */}
                <div className="order-book">
                    <div className="ob-header"><span>Price</span><span>Amount</span></div>
                    <div className="asks">
                        {depth?.asks?.slice().reverse().map((ask, i) => (
                            <div key={`ask-${i}`} className="ob-row ask">
                                <span>{ask[0]}</span>
                                <span>{parseFloat(ask[1]).toFixed(4)}</span>
                            </div>
                        ))}
                    </div>
                    <div className="spread">
                         Spread: {ticker ? (parseFloat(depth?.asks[0][0]) - parseFloat(depth?.bids[0][0])).toFixed(2) : '-'}
                    </div>
                    <div className="bids">
                        {depth?.bids?.map((bid, i) => (
                            <div key={`bid-${i}`} className="ob-row bid">
                                <span>{bid[0]}</span>
                                <span>{parseFloat(bid[1]).toFixed(4)}</span>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Trade Form */}
                <div className="trade-form">
                    <div className="trade-tabs">
                        <button 
                            className={`tab buy ${side === 'BUY' ? 'active' : ''}`}
                            onClick={() => setSide('BUY')}
                        >
                            BUY
                        </button>
                        <button 
                            className={`tab sell ${side === 'SELL' ? 'active' : ''}`}
                            onClick={() => setSide('SELL')}
                        >
                            SELL
                        </button>
                    </div>
                    
                    <div className="form-group">
                        <label>Price</label>
                        <input type="text" value={ticker?.lastPrice || 'Market'} disabled />
                    </div>

                    <div className="form-group">
                        <label>Amount</label>
                        <input 
                            type="number" 
                            step="0.001" 
                            value={quantity} 
                            onChange={(e) => setQuantity(e.target.value)} 
                        />
                    </div>

                    <button 
                        className={`execute-btn ${side.toLowerCase()}`}
                        onClick={handleTrade}
                        disabled={loading}
                    >
                        {loading ? 'Processing...' : `${side} ${symbol}`}
                    </button>

                    {/* Feedback */}
                    {error && <div className="trade-msg error">{error}</div>}
                    {orderStatus && (
                        <div className="trade-msg success">
                            Order Filled! <br/>
                            ID: {orderStatus.orderId} <br/>
                            Avg: ${orderStatus.price}
                        </div>
                    )}
                </div>
            </div>
            
            <div className="footer">
                <span>Binance Integration {mock && '(Mock)'}</span>
            </div>
        </div>
    );
};

export default CryptoTradingPanel;
