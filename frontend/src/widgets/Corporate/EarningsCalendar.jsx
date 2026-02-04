import React, { useEffect } from 'react';
import { Calendar, DollarSign, Mic, Clock } from 'lucide-react';
import useCorporateStore from '../../stores/corporateStore';
import './EarningsCalendar.css';

const EarningsCalendar = () => {
    const { earningsCalendar, fetchEarnings } = useCorporateStore();

    useEffect(() => {
        fetchEarnings(7); // Show 7 days for the "Week" view
    }, []);

    // Group earnings by date
    const groupedEarnings = earningsCalendar.reduce((acc, curr) => {
        if (!acc[curr.date]) acc[curr.date] = [];
        acc[curr.date].push(curr);
        return acc;
    }, {});

    const sortedDates = Object.keys(groupedEarnings).sort();

    return (
        <div className="earnings-calendar-widget">
            <div className="widget-header">
                <h3><Calendar size={18} className="text-cyan-400" /> Interactive Earnings Calendar</h3>
                <div className="view-toggle">
                    <button className="active">Week</button>
                    <button onClick={() => fetchEarnings(30)}>Month</button>
                </div>
            </div>

            <div className="calendar-grid">
                {sortedDates.length === 0 ? (
                    <div className="empty-state">No earnings events found for this period.</div>
                ) : (
                    sortedDates.map(date => (
                        <div key={date} className="day-col">
                            <div className="day-header">
                                {new Date(date).toLocaleDateString(undefined, { weekday: 'short', month: 'numeric', day: 'numeric' })}
                            </div>
                            {groupedEarnings[date].map((event, idx) => (
                                <div key={idx} className={`event-card ${event.time.toLowerCase()}`}>
                                    <div className="event-top">
                                        <span className="ticker">{event.ticker}</span>
                                        <span className="time">{event.time}</span>
                                    </div>
                                    <div className="event-details">
                                        <div className="est">Est: ${event.estimated_eps.toFixed(2)}</div>
                                        <div className="rev">Rev: {event.estimated_revenue}</div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    ))
                )}
            </div>

            <div className="debate-link">
                <Mic size={14} />
                <span>AI Debate Chamber: </span>
                <a href="#">Discuss Upcoming Earnings Strategy</a>
            </div>
        </div>
    );
};

export default EarningsCalendar;
