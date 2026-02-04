/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Market/QuoteCard.jsx
 * ROLE: Real-Time Quote Display Widget
 * PURPOSE: Displays real-time stock quote with price, volume, and change data.
 *          Supports auto-refresh during market hours and manual refresh.
 *          
 * INTEGRATION POINTS:
 *     - marketStore: Zustand state management for quote data
 *     - /api/v1/market/quote/{symbol}: Backend API endpoint
 *     
 * PROPS:
 *     - symbol (string, required): Stock ticker symbol
 *     - showVolume (boolean, default: true): Display volume indicator
 *     - autoRefresh (boolean, default: true): Enable auto-refresh
 *     - refreshInterval (number, default: 60000): Refresh interval in ms
 *     - compact (boolean, default: false): Compact display mode
 *     
 * USAGE:
 *     <QuoteCard symbol="AAPL" showVolume={true} autoRefresh={true} />
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect, useState, useCallback } from 'react';
import { useMarketStore } from '../../stores/marketStore';
import './Market.css';

/**
 * Check if market is currently open (9:30 AM - 4:00 PM ET, Mon-Fri)
 */
const isMarketOpen = () => {
    const now = new Date();
    const day = now.getDay();
    if (day === 0 || day === 6) return false; // Weekend
    
    const etOffset = -5; // EST offset
    const etHour = now.getUTCHours() + etOffset;
    const etMinute = now.getUTCMinutes();
    const totalMinutes = etHour * 60 + etMinute;
    
    // 9:30 AM = 570 minutes, 4:00 PM = 960 minutes
    return totalMinutes >= 570 && totalMinutes < 960;
};

/**
 * Format large numbers with abbreviations
 */
const formatVolume = (volume) => {
    if (!volume) return '0';
    if (volume >= 1e9) return (volume / 1e9).toFixed(2) + 'B';
    if (volume >= 1e6) return (volume / 1e6).toFixed(2) + 'M';
    if (volume >= 1e3) return (volume / 1e3).toFixed(1) + 'K';
    return volume.toString();
};

/**
 * Format relative time
 */
const formatRelativeTime = (date) => {
    if (!date) return 'Never';
    const seconds = Math.floor((new Date() - new Date(date)) / 1000);
    if (seconds < 60) return `${seconds}s ago`;
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
};

/**
 * Loading Skeleton
 */
const QuoteCardSkeleton = () => (
    <div className="quote-card quote-card--loading">
        <div className="quote-card__skeleton-header"></div>
        <div className="quote-card__skeleton-price"></div>
        <div className="quote-card__skeleton-change"></div>
    </div>
);

/**
 * Error State
 */
const QuoteCardError = ({ error, onRetry }) => (
    <div className="quote-card quote-card--error">
        <div className="quote-card__error-icon">⚠️</div>
        <div className="quote-card__error-message">{error}</div>
        <button className="quote-card__retry-btn" onClick={onRetry}>
            Retry
        </button>
    </div>
);

/**
 * QuoteCard Component
 */
const QuoteCard = ({ 
    symbol, 
    showVolume = true, 
    autoRefresh = true, 
    refreshInterval = 60000,
    compact = false
}) => {
    const { getQuote, fetchQuote, isLoading, getError } = useMarketStore();
    const [lastUpdated, setLastUpdated] = useState(null);
    
    const quote = getQuote(symbol);
    const loading = isLoading('quotes');
    const error = getError('quotes');

    const handleFetch = useCallback(async () => {
        try {
            await fetchQuote(symbol);
            setLastUpdated(new Date());
        } catch (e) {
            console.error(`Failed to fetch quote for ${symbol}:`, e);
        }
    }, [symbol, fetchQuote]);

    useEffect(() => {
        handleFetch();

        if (autoRefresh && isMarketOpen()) {
            const interval = setInterval(() => {
                handleFetch();
            }, refreshInterval);
            return () => clearInterval(interval);
        }
    }, [symbol, autoRefresh, refreshInterval, handleFetch]);

    if (loading && !quote) return <QuoteCardSkeleton />;
    if (error && !quote) return <QuoteCardError error={error} onRetry={handleFetch} />;
    if (!quote) return <QuoteCardSkeleton />;

    const isPositive = quote.change >= 0;
    const changeClass = isPositive ? 'positive' : 'negative';

    return (
        <div className={`quote-card ${compact ? 'quote-card--compact' : ''}`}>
            <div className="quote-card__header">
                <span className="quote-card__symbol">{quote.symbol}</span>
                {isMarketOpen() && (
                    <span className="quote-card__market-status quote-card__market-status--open">
                        LIVE
                    </span>
                )}
            </div>
            
            <div className="quote-card__price">
                ${quote.price?.toFixed(2) || '0.00'}
            </div>
            
            <div className={`quote-card__change ${changeClass}`}>
                <span className="quote-card__change-value">
                    {isPositive ? '+' : ''}{quote.change?.toFixed(2) || '0.00'}
                </span>
                <span className="quote-card__change-pct">
                    ({quote.change_percent || '0.00%'})
                </span>
            </div>

            {!compact && (
                <>
                    <div className="quote-card__details">
                        <div className="quote-card__detail-row">
                            <span className="quote-card__label">Open</span>
                            <span className="quote-card__value">${quote.open?.toFixed(2)}</span>
                        </div>
                        <div className="quote-card__detail-row">
                            <span className="quote-card__label">High</span>
                            <span className="quote-card__value">${quote.high?.toFixed(2)}</span>
                        </div>
                        <div className="quote-card__detail-row">
                            <span className="quote-card__label">Low</span>
                            <span className="quote-card__value">${quote.low?.toFixed(2)}</span>
                        </div>
                        <div className="quote-card__detail-row">
                            <span className="quote-card__label">Prev Close</span>
                            <span className="quote-card__value">${quote.previous_close?.toFixed(2)}</span>
                        </div>
                        {showVolume && (
                            <div className="quote-card__detail-row">
                                <span className="quote-card__label">Volume</span>
                                <span className="quote-card__value">{formatVolume(quote.volume)}</span>
                            </div>
                        )}
                    </div>
                </>
            )}

            <div className="quote-card__footer">
                <span className="quote-card__last-updated">
                    Updated: {formatRelativeTime(lastUpdated)}
                </span>
                <button 
                    className="quote-card__refresh-btn" 
                    onClick={handleFetch}
                    disabled={loading}
                >
                    {loading ? '...' : '↻'}
                </button>
            </div>
        </div>
    );
};

export default QuoteCard;
