import React from 'react';
import useWindowStore from '../../stores/windowStore';
import TaskbarIcon from './TaskbarIcon';
import './Taskbar.css';

const Taskbar = () => {
    const windows = useWindowStore((state) => state.windows);
    
    // Sort logic? Creation order or manual? For now, creation order (array order).
    
    return (
        <div className="taskbar-container">
            <div className="taskbar-start-button">
                {/* Placeholder for Start Menu / Launcher */}
                <div className="start-icon">🐺</div> 
            </div>
            
            <div className="taskbar-apps">
                {windows.map((window) => (
                    <TaskbarIcon key={window.id} window={window} />
                ))}
            </div>
            
            <div className="taskbar-tray">
                {/* Placeholder for System Tray (Clock, Network, Heartbeat status summary) */}
                <span className="tray-clock">{new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</span>
            </div>
        </div>
    );
};

export default Taskbar;
