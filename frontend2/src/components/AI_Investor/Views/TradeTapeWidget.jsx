
import React, { useEffect } from 'react';
import { useTradingStore } from '../../../store/tradingStore';
import { History, Zap } from 'lucide-react';
import './TradeTapeWidget.css';

import { useSymbolLinking } from '../../../hooks/useSymbolLinking';

const TradeTapeWidget = ({ linkingGroup = 'none' }) => {
    const { tradeTape, addTrade } = useTradingStore();
    const { groups, setGroupTicker } = useSymbolLinking();

    const currentTicker = linkingGroup !== 'none' ? groups[linkingGroup] : 'SPY';

    // Simulated Trade Feed
    useEffect(() => {
        const interval = setInterval(() => {
            const side = Math.random() > 0.5 ? 'buy' : 'sell';
            const size = Math.floor(Math.random() * 500) + 1;
            const isBlock = size > 450;

            const newTrade = {
                id: Date.now(),
                time: new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }),
                price: (480.00 + (Math.random() * 0.1 - 0.05)).toFixed(2),
                size,
                side,
                isBlock
            };

            addTrade(newTrade);
        }, Math.random() * 1000 + 200);

        return () => clearInterval(interval);
    }, [addTrade, currentTicker]);

    return (
        <div className="trade-tape-widget glass">
            <div className="tape-header">
                <History size={16} />
                <span>Time & Sales</span>
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
                <div className="tape-controls">
                    <Zap size={14} className="text-yellow-500" />
                    <span className="text-[0.65rem] opacity-50 uppercase tracking-widest">Live</span>
                </div>
            </div>

            <div className="tape-container">
                <table className="tape-table">
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>Price</th>
                            <th>Size</th>
                        </tr>
                    </thead>
                    <tbody>
                        {tradeTape.map((trade) => (
                            <tr key={trade.id} className={`${trade.side} ${trade.isBlock ? 'block-trade' : ''}`}>
                                <td className="time-col">{trade.time}</td>
                                <td className="price-col">{trade.price}</td>
                                <td className="size-col">
                                    {trade.size}
                                    {trade.isBlock && <span className="block-tag">BLOCK</span>}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div >
    );
};

export default TradeTapeWidget;
