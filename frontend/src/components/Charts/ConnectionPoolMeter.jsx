import React from 'react';
import './ConnectionPoolMeter.css';

const ConnectionPoolMeter = ({ active = 0, max = 1000 }) => {
    const percentage = Math.min(100, (active / max) * 100);
    
    return (
        <div className="connection-pool-meter">
            <div className="meter-info">
                <span className="active-count">{active}</span>
                <span className="max-count">/ {max}</span>
                <label>ACTIVE_CONNS</label>
            </div>
            <div className="meter-track">
                <div 
                    className="meter-fill" 
                    style={{ width: `${percentage}%` }}
                ></div>
            </div>
        </div>
    );
};

export default ConnectionPoolMeter;
