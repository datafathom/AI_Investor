/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Calendar/PortfolioCalendar.jsx
 * ROLE: Portfolio Calendar Widget
 * PURPOSE: Displays portfolio-related calendar events (earnings, dividends,
 *          rebalancing) in a calendar view with color coding.
 *          
 * INTEGRATION POINTS:
 *     - /api/v1/calendar/events: Calendar events API
 *     - /api/v1/calendar/sync/earnings: Earnings sync endpoint
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import './PortfolioCalendar.css';

const API_BASE = '/calendar';

const EVENT_COLORS = {
    earnings: '#4285f4',    // Blue
    dividend: '#34a853',    // Green
    rebalance: '#fbbc04',   // Yellow
    default: '#9aa0a6'      // Gray
};

const PortfolioCalendar = () => {
    const [events, setEvents] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [currentMonth, setCurrentMonth] = useState(new Date());
    const [syncing, setSyncing] = useState(false);

    useEffect(() => {
        loadEvents();
    }, [currentMonth]);

    const loadEvents = async () => {
        setLoading(true);
        try {
            const start = new Date(currentMonth.getFullYear(), currentMonth.getMonth(), 1);
            const end = new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1, 0);
            
            const response = await apiClient.get(`${API_BASE}/events`, {
                params: {
                    start_time: start.toISOString(),
                    end_time: end.toISOString()
                }
            });
            const data = response.data;
            setEvents(data.events || []);
        } catch (err) {
            console.error('Failed to load events:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleSyncEarnings = async () => {
        setSyncing(true);
        try {
            await apiClient.post(`${API_BASE}/sync/earnings`, {});
            await loadEvents(); // Reload events
        } catch (err) {
            console.error('Earnings sync failed:', err);
        } finally {
            setSyncing(false);
        }
    };

    const getEventsForDate = (date) => {
        const dateStr = date.toISOString().split('T')[0];
        return events.filter(event => {
            if (!event.start_time) return false;
            const eventDate = new Date(event.start_time).toISOString().split('T')[0];
            return eventDate === dateStr;
        });
    };

    const getEventType = (event) => {
        if (event.title?.toLowerCase().includes('earnings')) return 'earnings';
        if (event.title?.toLowerCase().includes('dividend')) return 'dividend';
        if (event.title?.toLowerCase().includes('rebalance')) return 'rebalance';
        return 'default';
    };

    const formatDate = (dateStr) => {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit'
        });
    };

    const renderCalendar = () => {
        const year = currentMonth.getFullYear();
        const month = currentMonth.getMonth();
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysInMonth = lastDay.getDate();
        const startingDayOfWeek = firstDay.getDay();

        const days = [];
        
        // Empty cells for days before month starts
        for (let i = 0; i < startingDayOfWeek; i++) {
            days.push(<div key={`empty-${i}`} className="calendar-day empty"></div>);
        }
        
        // Days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month, day);
            const dayEvents = getEventsForDate(date);
            
            days.push(
                <div
                    key={day}
                    className="calendar-day"
                    onClick={() => dayEvents.length > 0 && setSelectedEvent(dayEvents[0])}
                >
                    <div className="calendar-day-number">{day}</div>
                    <div className="calendar-day-events">
                        {dayEvents.slice(0, 3).map((event, idx) => {
                            const eventType = getEventType(event);
                            return (
                                <div
                                    key={idx}
                                    className="calendar-event-dot"
                                    style={{ backgroundColor: EVENT_COLORS[eventType] }}
                                    title={event.title}
                                />
                            );
                        })}
                        {dayEvents.length > 3 && (
                            <div className="calendar-event-more">+{dayEvents.length - 3}</div>
                        )}
                    </div>
                </div>
            );
        }
        
        return days;
    };

    return (
        <div className="portfolio-calendar">
            <div className="portfolio-calendar__header">
                <h3>📅 Portfolio Calendar</h3>
                <div className="portfolio-calendar__controls">
                    <button
                        className="sync-btn"
                        onClick={handleSyncEarnings}
                        disabled={syncing}
                    >
                        {syncing ? 'Syncing...' : '🔄 Sync Earnings'}
                    </button>
                    <button
                        className="nav-btn"
                        onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))}
                    >
                        ←
                    </button>
                    <span className="month-label">
                        {currentMonth.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })}
                    </span>
                    <button
                        className="nav-btn"
                        onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))}
                    >
                        →
                    </button>
                </div>
            </div>

            {/* Legend */}
            <div className="portfolio-calendar__legend">
                <div className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: EVENT_COLORS.earnings }}></div>
                    <span>Earnings</span>
                </div>
                <div className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: EVENT_COLORS.dividend }}></div>
                    <span>Dividends</span>
                </div>
                <div className="legend-item">
                    <div className="legend-color" style={{ backgroundColor: EVENT_COLORS.rebalance }}></div>
                    <span>Rebalancing</span>
                </div>
            </div>

            {/* Calendar Grid */}
            <div className="portfolio-calendar__grid">
                <div className="calendar-weekdays">
                    {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                        <div key={day} className="calendar-weekday">{day}</div>
                    ))}
                </div>
                <div className="calendar-days">
                    {loading ? (
                        <div className="calendar-loading">Loading events...</div>
                    ) : (
                        renderCalendar()
                    )}
                </div>
            </div>

            {/* Event Detail Modal */}
            {selectedEvent && (
                <div className="portfolio-calendar__modal-overlay" onClick={() => setSelectedEvent(null)}>
                    <div className="portfolio-calendar__modal" onClick={(e) => e.stopPropagation()}>
                        <h4>{selectedEvent.title}</h4>
                        {selectedEvent.description && (
                            <p className="event-description">{selectedEvent.description}</p>
                        )}
                        <div className="event-details">
                            <div className="event-detail-item">
                                <strong>Start:</strong> {formatDate(selectedEvent.start_time)}
                            </div>
                            {selectedEvent.end_time && (
                                <div className="event-detail-item">
                                    <strong>End:</strong> {formatDate(selectedEvent.end_time)}
                                </div>
                            )}
                            {selectedEvent.location && (
                                <div className="event-detail-item">
                                    <strong>Location:</strong> {selectedEvent.location}
                                </div>
                            )}
                        </div>
                        {selectedEvent.html_link && (
                            <a
                                href={selectedEvent.html_link}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="event-link"
                            >
                                Open in Google Calendar
                            </a>
                        )}
                        <button
                            className="close-btn"
                            onClick={() => setSelectedEvent(null)}
                        >
                            Close
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PortfolioCalendar;
