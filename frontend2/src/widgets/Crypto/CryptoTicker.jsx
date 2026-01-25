/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Crypto/CryptoTicker.jsx
 * ROLE: Information Display Widget
 * PURPOSE: Displays a scrolling ticker of real-time crypto prices.
 *          
 * INTEGRATION POINTS:
 *     - api_cryptoStore: Zustand state management.
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-22
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import useCryptoStore from '../../stores/api_cryptoStore';
import './CryptoTicker.css';

const CryptoTicker = ({ symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'DOGE'], mock = false }) => {
    const { prices, fetchPrices, loading } = useCryptoStore();

    useEffect(() => {
        fetchPrices(symbols, ['USD'], mock);
        const interval = setInterval(() => {
            fetchPrices(symbols, ['USD'], mock);
        }, 10000); // Pulse every 10s
        return () => clearInterval(interval);
    }, [JSON.stringify(symbols), mock, fetchPrices]);

    const renderTickerItems = () => {
        return symbols.map(sym => {
            const data = prices[sym];
            const price = data ? data['USD'] : null;
            
            return (
                <div key={sym} className="ticker-item">
                    <span className="ticker-symbol">{sym}</span>
                    <span className="ticker-price">
                        {price ? `$${price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 4 })}` : '...'}
                    </span>
                    {/* Placeholder charge logic since basic endpoint doesn't return 24h change yet */}
                    <span className="ticker-change positive">+0.0%</span> 
                </div>
            );
        });
    };

    return (
        <div className="crypto-ticker">
            <div className="ticker-track">
                {renderTickerItems()}
                {/* Duplicate for seamless scrolling effect */}
                {renderTickerItems()}
            </div>
            {mock && <div className="ticker-mock-badge">SIMULATION</div>}
        </div>
    );
};

export default CryptoTicker;
