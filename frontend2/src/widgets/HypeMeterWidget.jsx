/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/HypeMeterWidget.jsx
 * ROLE: Social Hype Ticker Widget
 * PURPOSE: Displays a scrolling tape of social sentiment analysis (HypeMeter).
 *          Aggregates signals from Reddit/Twitter/News for high-velocity trends.
 * ==============================================================================
 */
import React, { useEffect, useState } from 'react';
import ViralAlertBadge from '../components/ViralAlertBadge';
import './HypeMeterWidget.css';

const HypeMeterWidget = () => {
    const [feed, setFeed] = useState([]);
    
    useEffect(() => {
        const fetchFeed = async () => {
             // Mock for now, would stick endpoint
             const symbols = ['AAPL', 'TSLA', 'NVDA', 'GME', 'AMC', 'SPY'];
             const newItems = Array.from({length: 5}).map((_, i) => ({
                 id: Date.now() + i,
                 symbol: symbols[Math.floor(Math.random() * symbols.length)],
                 source: Math.random() > 0.5 ? 'Reddit' : 'Twitter',
                 text: Math.random() > 0.5 ? 'Huge breakout imminent! 🚀' : 'Support failing, get out now.',
                 sentiment: Math.random() * 2 - 1
             }));
             setFeed(newItems);
        };
        
        fetchFeed();
        const interval = setInterval(fetchFeed, 10000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="hypemeter-widget">
            <header className="hm-header">
                <h3>Social HypeMeter</h3>
                <span className="live-tag">LIVE</span>
            </header>
            
            <div className="tape-container">
                {feed.map(item => (
                    <div key={item.id} className={`tape-card ${item.viral ? 'is-viral' : ''}`}>
                        <div className="tc-top">
                            <div className="tc-identity">
                                <span className="tc-symbol">{item.symbol}</span>
                                {item.viral && <ViralAlertBadge />}
                            </div>
                            <span className={`tc-sent ${item.sentiment > 0 ? 'pos' : 'neg'}`}>
                                {item.sentiment > 0 ? 'bullish' : 'bearish'}
                            </span>
                        </div>
                        <p className="tc-text">{item.text}</p>
                        
                        {/* Keyword Chips */}
                        {item.keywords && item.keywords.length > 0 && (
                            <div className="tc-keywords">
                                {item.keywords.map((kw, idx) => (
                                    <span key={idx} className="keyword-chip">{kw}</span>
                                ))}
                            </div>
                        )}
                        
                        <span className="tc-source">{item.source}</span>
                    </div>
                ))}
            </div>
            {/* Real scrolling tape implementation would need CSS animation or a library */}
        </div>
    );
};

export default HypeMeterWidget;
