import React, { useState, useEffect } from 'react';

const TaskbarClock = () => {
    const [time, setTime] = useState(new Date());

    useEffect(() => {
        const timer = setInterval(() => setTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    return (
        <div className="taskbar-tray">
            <div className="tray-date">
                <span>{time.toLocaleDateString([], { month: 'short', day: 'numeric' })}</span>
                <span className="tray-clock">{time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
            </div>
        </div>
    );
};

export default React.memo(TaskbarClock);
