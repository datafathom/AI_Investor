import React from 'react';
import './UptimeSparkline.css';

const UptimeSparkline = ({ data }) => {
    // A simple CSS-based sparkline for uptime
    return (
        <div className="uptime-sparkline">
            {data.map((day, i) => (
                <div 
                    key={i} 
                    className={`spark-bar ${day.uptime > 99.9 ? 'perfect' : day.uptime > 99 ? 'good' : 'degraded'}`}
                    style={{ height: `${Math.max(10, day.uptime - 80)}%` }}
                    title={`${day.date}: ${day.uptime.toFixed(2)}%`}
                ></div>
            ))}
        </div>
    );
};

export default UptimeSparkline;
