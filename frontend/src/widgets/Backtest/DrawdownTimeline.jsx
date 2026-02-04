import React, { useState } from 'react';
import { Activity, AlertOctagon, ZoomIn, ZoomOut } from 'lucide-react';
import useBacktestStore from '../../stores/backtestStore';
import './DrawdownTimeline.css';

const DrawdownTimeline = () => {
    const { maxDrawdown, recoveryDays } = useBacktestStore();
    const [zoomLevel, setZoomLevel] = useState(1);
    
    // Mock drawdown events for visualization
    const drawdownEvents = [
        { id: 1, name: 'COVID Crash', date: 'Mar 2020', depth: -34.5, duration: '22 days' },
        { id: 2, name: 'Fed Rate Hike', date: 'Jun 2022', depth: -24.8, duration: '145 days' },
        { id: 3, name: 'Banking Crisis', date: 'Mar 2023', depth: -12.2, duration: '45 days' },
    ];

    return (
        <div className="drawdown-timeline-widget">
            <div className="widget-header">
                <h3><Activity size={18} /> Max Drawdown 'Stress Point' Timeline</h3>
                <div className="timeline-controls">
                    <button onClick={() => setZoomLevel(Math.max(0.5, zoomLevel - 0.1))}><ZoomOut size={14}/></button>
                    <button onClick={() => setZoomLevel(Math.min(2, zoomLevel + 0.1))}><ZoomIn size={14}/></button>
                </div>
            </div>

            <div className="timeline-container">
                <div className="timeline-track">
                    {drawdownEvents.map(event => (
                        <div key={event.id} className="drawdown-event" style={{ left: `${(event.id * 25)}%` }}>
                            <div className="event-marker"></div>
                            <div className="event-label">
                                <span className="event-name">{event.name}</span>
                                <span className="event-depth text-red-500">{event.depth}%</span>
                            </div>
                            <div className="event-tooltip">
                                <div>Duration: {event.duration}</div>
                                <div>Date: {event.date}</div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="underwater-chart-mock">
                <div className="chart-title">Underwater Equity Curve</div>
                <div className="underwater-area"></div>
            </div>

            <div className="risk-metrics">
                <div className="metric">
                    <span className="label">Max Drawdown</span>
                    <span className="value negative">{(maxDrawdown * 100).toFixed(1)}%</span>
                </div>
                <div className="metric">
                    <span className="label">Recovery Days</span>
                    <span className="value">{recoveryDays}d</span>
                </div>
                <div className="metric">
                    <span className="label">Recovery Factor</span>
                    <span className="value">{(1 / Math.max(maxDrawdown, 0.01)).toFixed(2)}x</span>
                </div>
            </div>
        </div>
    );
};

export default DrawdownTimeline;
