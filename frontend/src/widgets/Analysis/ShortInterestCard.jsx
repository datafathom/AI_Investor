/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Analysis/ShortInterestCard.jsx
 * ROLE: Short Interest Analysis Widget
 * PURPOSE: Displays short interest metrics including ratio, days-to-cover,
 *          and squeeze probability.
 *          
 * INTEGRATION POINTS:
 *     - marketStore: Zustand state management for short interest data
 *     - /api/v1/market/short-interest/{symbol}: Backend API endpoint
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect, useCallback } from 'react';
import PropTypes from 'prop-types';
import { useMarketStore } from '../../stores/marketStore';
import './ShortInterestCard.css';

const ShortInterestCard = ({ symbol, mock = false }) => {
    const { getShortInterest, fetchShortInterest, isLoading, getError } = useMarketStore();
    
    const data = getShortInterest(symbol);
    const loading = isLoading('shortInterest');
    const error = getError('shortInterest');

    const handleFetch = useCallback(async () => {
        try {
            await fetchShortInterest(symbol, mock);
        } catch (e) {
            console.error(`Failed to fetch short interest for ${symbol}:`, e);
        }
    }, [symbol, mock, fetchShortInterest]);

    useEffect(() => {
        handleFetch();
    }, [handleFetch]);

    if (loading && !data) {
        return (
            <div className="short-interest-card short-interest-card--loading">
                <div className="short-interest-card__skeleton-header"></div>
                <div className="short-interest-card__skeleton-content"></div>
            </div>
        );
    }

    if (error && !data) {
        return (
            <div className="short-interest-card short-interest-card--error">
                <div className="short-interest-card__error-message">{error}</div>
                <button onClick={handleFetch}>Retry</button>
            </div>
        );
    }

    if (!data) return null;

    const getProbColor = (prob) => {
        if (prob > 80) return 'extreme';
        if (prob > 60) return 'high';
        if (prob > 30) return 'medium';
        return 'low';
    };

    const probClass = getProbColor(data.squeeze_probability);

    return (
        <div className={`short-interest-card short-interest-card--${probClass}`}>
            <div className="short-interest-card__header">
                <span className="short-interest-card__title">Short Interest Analysis</span>
                <span className="short-interest-card__symbol">{symbol}</span>
            </div>

            <div className="short-interest-card__main">
                <div className="short-interest-card__gauge-container">
                    <div className="short-interest-card__gauge">
                        <svg viewBox="0 0 100 100">
                            <circle className="gauge-bg" cx="50" cy="50" r="45" />
                            <circle 
                                className="gauge-fill" 
                                cx="50" cy="50" r="45" 
                                style={{ strokeDasharray: `${data.squeeze_probability * 2.82} 282` }}
                            />
                        </svg>
                        <div className="gauge-text">
                            <span className="gauge-value">{Math.round(data.squeeze_probability)}%</span>
                            <span className="gauge-label">Squeeze Prob.</span>
                        </div>
                    </div>
                </div>

                <div className="short-interest-card__metrics">
                    <div className="metric-row">
                        <span className="metric-label">Short Ratio</span>
                        <span className="metric-value">{(data.short_ratio * 100).toFixed(2)}%</span>
                    </div>
                    <div className="metric-row">
                        <span className="metric-label">Days to Cover</span>
                        <span className="metric-value">{data.days_to_cover.toFixed(2)}</span>
                    </div>
                    <div className="metric-row">
                        <span className="metric-label">Risk Level</span>
                        <span className={`metric-value risk-${probClass}`}>{data.risk_level}</span>
                    </div>
                </div>
            </div>

            <div className="short-interest-card__footer">
                <span className="source-tag">Source: Quandl/FINRA</span>
                <button className="refresh-btn" onClick={handleFetch} disabled={loading}>
                    {loading ? '...' : '↻'}
                </button>
            </div>
        </div>
    );
};

ShortInterestCard.propTypes = {
    symbol: PropTypes.string.isRequired,
    mock: PropTypes.bool
};

export default ShortInterestCard;
