import React from 'react';
import useWindowStore from '../../stores/windowStore';
import './Taskbar.css'; // Shared CSS

const TaskbarIcon = ({ window }) => {
    const focusWindow = useWindowStore((state) => state.focusWindow);
    const restoreWindow = useWindowStore((state) => state.restoreWindow);
    const minimizeWindow = useWindowStore((state) => state.minimizeWindow);
    const activeWindowId = useWindowStore((state) => state.activeWindowId);
    
    const isActive = activeWindowId === window.id && !window.isMinimized;
    
    const handleClick = () => {
        if (window.isMinimized) {
            restoreWindow(window.id);
        } else if (isActive) {
            minimizeWindow(window.id);
        } else {
            focusWindow(window.id);
        }
    };
    
    // Mock risk color - should come from window props or store
    const riskColor = window.risk === 'high' ? '#ff4757' : window.risk === 'medium' ? '#ffc107' : '#00ff88';

    return (
        <div 
            className={`taskbar-icon ${isActive ? 'active' : ''} ${window.isMinimized ? 'minimized' : ''}`}
            onClick={handleClick}
            title={window.title}
        >
            <div className="icon-indicator" style={{ backgroundColor: riskColor }}></div>
            <span className="icon-label">{window.title.substring(0, 2).toUpperCase()}</span>
            {/* Full title on hover via tooltip would be nice */}
            <div className="icon-tooltip">{window.title}</div>
        </div>
    );
};

export default TaskbarIcon;
