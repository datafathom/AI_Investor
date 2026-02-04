import React, { useState, useRef, useEffect } from 'react';
import useWindowStore from '../../stores/windowStore';
import { X } from 'lucide-react';
import './Taskbar.css'; 

/**
 * TaskbarIcon - Simplified for Performance
 * 
 * NOTE: Hover preview logic has been commented out due to performance issues.
 * The preview popup was causing significant frame drops.
 * TODO: Re-enable once performance optimization is complete (TechDebt2).
 */
const TaskbarIcon = ({ window, isActive }) => {
    // Select stable action references
    const focusWindow = useWindowStore((state) => state.focusWindow);
    const restoreWindow = useWindowStore((state) => state.restoreWindow);
    const minimizeWindow = useWindowStore((state) => state.minimizeWindow);
    const closeWindow = useWindowStore((state) => state.closeWindow);
    
    // PERFORMANCE: Hover preview disabled - uncomment to re-enable
    const [showPreview, setShowPreview] = useState(false);
    const hoverTimer = useRef(null);
    
    const handleClick = () => {
        if (window.isMinimized) {
            restoreWindow(window.id);
        } else if (isActive) {
            minimizeWindow(window.id);
        } else {
            focusWindow(window.id);
        }
    };
    
    // PERFORMANCE: Hover handlers disabled - uncomment to re-enable
    // const handleMouseEnter = () => {
    //     hoverTimer.current = setTimeout(() => {
    //         setShowPreview(true);
    //     }, 400); // 400ms debounce to avoid accidental triggers
    // };

    // const handleMouseLeave = () => {
    //     if (hoverTimer.current) clearTimeout(hoverTimer.current);
    //     setShowPreview(false);
    // };

    const handleCloseWindow = (e) => {
        e.stopPropagation();
        closeWindow(window.id);
    };

    // PERFORMANCE: Cleanup disabled since hover is disabled
    useEffect(() => {
        return () => {
            if (hoverTimer.current) clearTimeout(hoverTimer.current);
        };
    }, []);
    
    // Risk color based on window state
    const riskColor = window.risk === 'high' ? '#ff4757' : window.risk === 'medium' ? '#ffc107' : '#00ff88';
    const riskClass = window.risk || 'low';
    
    // Badge count from window props (e.g., notifications, alerts)
    const badgeCount = window.badgeCount || 0;

    return (
        <div 
            className={`taskbar-icon ${isActive ? 'active' : ''} ${window.isMinimized ? 'minimized' : ''}`}
            onClick={handleClick}
            // PERFORMANCE: Hover handlers disabled
            // onMouseEnter={handleMouseEnter}
            // onMouseLeave={handleMouseLeave}
        >
            <div className="icon-indicator" style={{ backgroundColor: riskColor }}></div>
            <span className="icon-label">{window.title.substring(0, 2).toUpperCase()}</span>
            
            {badgeCount > 0 && (
                <div className="taskbar-badge">{badgeCount > 9 ? '9+' : badgeCount}</div>
            )}
            
            {/* PERFORMANCE: Hover preview disabled - heavy DOM causing frame drops
             * TODO: Re-enable after implementing virtualization or lazy loading
             * See: TechDebt2.txt
             */}
            {/* {showPreview && (
                <div className="hover-preview glass-premium">
                    <div className="preview-header">
                        <span className="preview-title">{window.title}</span>
                        <button 
                            className="preview-close-btn"
                            onClick={handleCloseWindow}
                        >
                            <X size={12} />
                        </button>
                    </div>
                    <div className="preview-snapshot">
                        {window.snapshot ? (
                            <img 
                                src={window.snapshot} 
                                alt={window.title} 
                                className="snapshot-img"
                                style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '4px' }}
                            />
                        ) : (
                            <div className="fake-window-content">
                                <div className="fake-sidebar">
                                    <div className="fake-nav-item"></div>
                                    <div className="fake-nav-item"></div>
                                    <div className="fake-nav-item active"></div>
                                </div>
                                <div className="fake-main">
                                    <div className="fake-row"></div>
                                    <div className="fake-row short"></div>
                                    <div className="fake-chart">
                                        <div className="chart-glow"></div>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>
                    <div className="preview-footer">
                        <span className={`status-badge ${riskClass}`}>
                            {window.isMinimized ? 'Minimized' : 'Active'}
                        </span>
                    </div>
                </div>
            )} */}
        </div>
    );
};

export default React.memo(TaskbarIcon);
