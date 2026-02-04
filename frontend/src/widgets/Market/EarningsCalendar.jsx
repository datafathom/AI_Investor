/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Market/EarningsCalendar.jsx
 * ROLE: Earnings Calendar Widget
 * PURPOSE: Displays upcoming earnings dates with date, EPS estimate, and fiscal quarter.
 *          
 * INTEGRATION POINTS:
 *     - marketStore: Zustand state management for earnings data
 *     - /api/v1/market/earnings: Backend API endpoint
 *     
 * PROPS:
 *     - symbols (array, optional): Filter by specific symbols
 *     - horizon (string, default: '3month'): '3month', '6month', '12month'
 *     - limit (number, default: 10): Maximum entries to display
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import { useMarketStore } from '../../stores/marketStore';
import './Market.css';

/**
 * Format date for display
 */
const formatDate = (dateStr) => {
    if (!dateStr) return 'TBD';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
        month: 'short', 
        day: 'numeric',
        year: '2-digit'
    });
};

/**
 * Calculate days until earnings
 */
const getDaysUntil = (dateStr) => {
    if (!dateStr) return null;
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const reportDate = new Date(dateStr);
    const diffTime = reportDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
};

/**
 * EarningsCalendar Component
 */
const EarningsCalendar = ({ 
    symbols = null, 
    horizon = '3month',
    limit = 10 
}) => {
    const { earnings, fetchEarnings, isLoading, getError } = useMarketStore();
    const loading = isLoading('earnings');
    const error = getError('earnings');

    useEffect(() => {
        fetchEarnings(symbols?.[0] || null, horizon);
    }, [symbols, horizon, fetchEarnings]);

    if (loading && !earnings?.earnings?.length) {
        return (
            <div className="earnings-calendar earnings-calendar--loading">
                <div className="earnings-calendar__skeleton"></div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="earnings-calendar earnings-calendar--error">
                <span>⚠️ {error}</span>
            </div>
        );
    }

    const filteredEarnings = earnings?.earnings
        ?.filter(e => !symbols || symbols.includes(e.symbol))
        ?.slice(0, limit) || [];

    if (filteredEarnings.length === 0) {
        return (
            <div className="earnings-calendar earnings-calendar--empty">
                <span>No upcoming earnings</span>
            </div>
        );
    }

    return (
        <div className="earnings-calendar">
            <div className="earnings-calendar__header">
                <h3 className="earnings-calendar__title">📅 Upcoming Earnings</h3>
                <span className="earnings-calendar__count">
                    {earnings?.count || 0} total
                </span>
            </div>
            
            <div className="earnings-calendar__list">
                {filteredEarnings.map((entry, idx) => {
                    const daysUntil = getDaysUntil(entry.report_date);
                    let urgencyClass = '';
                    if (daysUntil !== null) {
                        if (daysUntil <= 1) urgencyClass = 'urgent';
                        else if (daysUntil <= 7) urgencyClass = 'soon';
                    }

                    return (
                        <div 
                            key={`${entry.symbol}-${idx}`} 
                            className={`earnings-calendar__item ${urgencyClass}`}
                        >
                            <div className="earnings-calendar__item-left">
                                <span className="earnings-calendar__symbol">
                                    {entry.symbol}
                                </span>
                                {entry.name && (
                                    <span className="earnings-calendar__name">
                                        {entry.name}
                                    </span>
                                )}
                            </div>
                            
                            <div className="earnings-calendar__item-center">
                                <span className="earnings-calendar__date">
                                    {formatDate(entry.report_date)}
                                </span>
                                {daysUntil !== null && (
                                    <span className="earnings-calendar__days">
                                        {daysUntil === 0 ? 'Today' : 
                                         daysUntil === 1 ? 'Tomorrow' : 
                                         `${daysUntil} days`}
                                    </span>
                                )}
                            </div>
                            
                            <div className="earnings-calendar__item-right">
                                {entry.estimate && (
                                    <span className="earnings-calendar__estimate">
                                        Est: ${entry.estimate.toFixed(2)}
                                    </span>
                                )}
                                {entry.fiscal_date_ending && (
                                    <span className="earnings-calendar__fiscal">
                                        FY: {entry.fiscal_date_ending}
                                    </span>
                                )}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default EarningsCalendar;
