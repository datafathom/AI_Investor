
import React, { useEffect } from 'react';
import { useTradingStore } from '../../../store/tradingStore';
import { Activity, Layers } from 'lucide-react';
import './MarketDepthWidget.css';

import { useSymbolLinking } from '../../../hooks/useSymbolLinking';

const MarketDepthWidget = ({ linkingGroup = 'none' }) => {
    const { marketDepth, updateMarketDepth } = useTradingStore();
    const { groups, setGroupTicker } = useSymbolLinking();

    const currentTicker = linkingGroup !== 'none' ? groups[linkingGroup] : marketDepth.ticker;

    // Simulated Depth Update
    useEffect(() => {
        const generateDepth = () => {
            const basePrice = 480.00;
            const bids = Array.from({ length: 10 }, (_, i) => ({
                price: (basePrice - 0.05 - i * 0.01).toFixed(2),
                size: Math.floor(Math.random() * 500) + 100,
                cumulative: 0
            }));

            const asks = Array.from({ length: 10 }, (_, i) => ({
                price: (basePrice + 0.05 + i * 0.01).toFixed(2),
                size: Math.floor(Math.random() * 500) + 100,
                cumulative: 0
            })).reverse();

            // Calculate cumulative
            let cumBid = 0;
            bids.forEach(b => { cumBid += b.size; b.cumulative = cumBid; });
            let cumAsk = 0;
            asks.slice().reverse().forEach(a => { cumAsk += a.size; a.cumulative = cumAsk; });

            updateMarketDepth({ bids, asks, lastPrice: basePrice });
        };

        generateDepth();
        const interval = setInterval(generateDepth, 500);
        return () => clearInterval(interval);
    }, [updateMarketDepth, currentTicker]);

    const maxSideSize = 2500; // For normalization of histogram bars

    return (
        <div className="market-depth-widget glass">
            <div className="depth-header">
                <Layers size={16} />
                <span>Level 2 / DOM</span>
                <div
                    className={`ticker-badge group-${linkingGroup}`}
                    onClick={() => {
                        const newTicker = prompt('Enter new symbol:', currentTicker);
                        if (newTicker) {
                            if (linkingGroup !== 'none') {
                                setGroupTicker(linkingGroup, newTicker.toUpperCase());
                            }
                        }
                    }}
                >
                    {currentTicker}
                </div>
            </div>

            <div className="depth-container">
                <div className="depth-side asks">
                    {marketDepth.asks.map((a, i) => (
                        <div key={a.price} className="depth-row">
                            <div className="depth-bar ask-bar" style={{ width: `${(a.size / 1000) * 100}%` }}></div>
                            <span className="depth-price sell">{a.price}</span>
                            <span className="depth-size">{a.size}</span>
                            <span className="depth-cum">{a.cumulative}</span>
                        </div>
                    ))}
                </div>

                <div className="price-spread">
                    <span className="last-price">480.00</span>
                    <span className="spread-label">Spread: 0.03</span>
                </div>

                <div className="depth-side bids">
                    {marketDepth.bids.map((b, i) => (
                        <div key={b.price} className="depth-row">
                            <div className="depth-bar bid-bar" style={{ width: `${(b.size / 1000) * 100}%` }}></div>
                            <span className="depth-price buy">{b.price}</span>
                            <span className="depth-size">{b.size}</span>
                            <span className="depth-cum">{b.cumulative}</span>
                        </div>
                    ))}
                </div>
            </div>
        </div >
    );
};

export default MarketDepthWidget;
