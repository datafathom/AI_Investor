/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Corporate/IPOCalendar.jsx
 * ROLE: Corporate Events Widget
 * PURPOSE: Displays upcoming IPOs with success probability and risk metrics.
 *          
 * INTEGRATION POINTS:
 *     - corporateStore: Zustand state management for IPO data
 *     - /api/v1/corporate/ipo/upcoming: Backend API endpoint
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect } from 'react';
import useCorporateStore from '../../stores/corporateStore';
import './IPOCalendar.css';

const IPOCalendar = ({ days = 30, mock = false }) => {
    const { upcomingIPOs, fetchUpcomingIPOs, loading, error } = useCorporateStore();

    useEffect(() => {
        fetchUpcomingIPOs(days, mock);
    }, [fetchUpcomingIPOs, days, mock]);

    if (loading.ipos && upcomingIPOs.length === 0) {
        return (
            <div className="ipo-calendar ipo-calendar--loading">
                <div className="ipo-calendar__skeleton-header"></div>
                <div className="ipo-calendar__skeleton-list">
                    {[1, 2, 3].map(i => <div key={i} className="ipo-calendar__skeleton-item"></div>)}
                </div>
            </div>
        );
    }

    if (error && upcomingIPOs.length === 0) {
        return (
            <div className="ipo-calendar ipo-calendar--error">
                <div className="ipo-calendar__error-message">{error}</div>
                <button onClick={() => fetchUpcomingIPOs(days, mock)}>Retry</button>
            </div>
        );
    }

    const getSignalClass = (signal) => {
        switch (signal) {
            case 'BULLISH': return 'signal--bullish';
            case 'BEARISH': return 'signal--bearish';
            default: return 'signal--neutral';
        }
    };

    return (
        <div className="ipo-calendar">
            <div className="ipo-calendar__header">
                <div className="ipo-calendar__title">Upcoming IPOs</div>
                <div className="ipo-calendar__refresh">
                    <button onClick={() => fetchUpcomingIPOs(days, mock)} disabled={loading.ipos}>
                        {loading.ipos ? '...' : '↻'}
                    </button>
                </div>
            </div>

            <div className="ipo-calendar__list">
                {upcomingIPOs.length === 0 ? (
                    <div className="ipo-calendar__empty">No upcoming IPOs found.</div>
                ) : (
                    upcomingIPOs.map((ipo) => (
                        <div key={ipo.symbol} className="ipo-item">
                            <div className="ipo-item__main">
                                <div className="ipo-item__symbol-box">
                                    <span className="ipo-item__symbol">{ipo.symbol}</span>
                                    <span className={`ipo-item__signal ${getSignalClass(ipo.sentiment_signal)}`}>
                                        {ipo.sentiment_signal}
                                    </span>
                                </div>
                                <div className="ipo-item__info">
                                    <div className="ipo-item__company">{ipo.company}</div>
                                    <div className="ipo-item__date">Expected: {ipo.date}</div>
                                </div>
                            </div>

                            <div className="ipo-item__stats">
                                <div className="ipo-stat">
                                    <div className="ipo-stat__label">Success Prob.</div>
                                    <div className="ipo-stat__value-bar">
                                        <div 
                                            className="ipo-stat__fill" 
                                            style={{ width: `${ipo.success_probability}%` }}
                                        ></div>
                                        <span className="ipo-stat__text">{Math.round(ipo.success_probability)}%</span>
                                    </div>
                                </div>
                                <div className="ipo-stat">
                                    <div className="ipo-stat__label">Valuation</div>
                                    <div className="ipo-stat__value">{ipo.estimated_valuation || 'N/A'}</div>
                                </div>
                            </div>
                        </div>
                    ))
                )}
            </div>

            <div className="ipo-calendar__footer">
                <div className="ipo-source">Data via Finnhub Events</div>
                {mock && <div className="ipo-mock-tag">Simulation Mode</div>}
            </div>
        </div>
    );
};

export default IPOCalendar;
