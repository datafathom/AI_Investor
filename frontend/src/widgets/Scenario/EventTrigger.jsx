import React, { useState } from 'react';
import { Bolt, Zap, Globe, AlertTriangle } from 'lucide-react';
import './EventTrigger.css';

const EventTrigger = () => {
    const [dragging, setDragging] = useState(false);
    
    // Pre-built events
    const events = [
        { id: 1, name: 'Oil Shock ($150/bbl)', impact: 'High', type: 'Commodity' },
        { id: 2, name: 'Fed Rates +200bps', impact: 'Critical', type: 'Monetary' },
        { id: 3, name: 'Geopolitics: Taiwan', impact: 'Extreme', type: 'Geopolitical' },
        { id: 4, name: 'AI Bubble Burst', impact: 'High', type: 'Sector' },
    ];

    return (
        <div className="event-trigger-widget">
            <div className="widget-header">
                <h3><Bolt size={18} className="text-yellow-400" /> Drag-and-Drop Macro Event Trigger</h3>
            </div>

            <div className="scene-drop-zone">
                <div className={`drop-target ${dragging ? 'active' : ''}`}>
                    <Zap size={32} />
                    <span>Drag Event Here to Simulate</span>
                </div>
            </div>

            <div className="event-library">
                <h4>Event Library</h4>
                <div className="event-grid">
                    {events.map(event => (
                        <div 
                            key={event.id} 
                            className="event-card" 
                            draggable
                            onDragStart={() => setDragging(true)}
                            onDragEnd={() => setDragging(false)}
                        >
                            <div className="event-icon">
                                <Globe size={16} />
                            </div>
                            <div className="event-info">
                                <span className="event-name">{event.name}</span>
                                <span className={`event-impact ${event.impact.toLowerCase()}`}>{event.impact} Impact</span>
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            <div className="active-simulation-banner">
                <AlertTriangle size={16} />
                <span>Correlation Graph Propagation: Ready</span>
            </div>
        </div>
    );
};

export default EventTrigger;
