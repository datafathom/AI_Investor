import React, { useState, useEffect, useRef } from 'react';
import './GlobalTooltip.css';

/**
 * GlobalTooltip Component
 * Listens for hover on elements with 'data-tooltip' attribute
 * Displays tooltip after 3 seconds of continuous hover.
 */
const GlobalTooltip = () => {
    const [tooltip, setTooltip] = useState({ visible: false, text: '', x: 0, y: 0 });
    const timerRef = useRef(null);

    useEffect(() => {
        const handleMouseOver = (e) => {
            const target = e.target.closest('[data-tooltip]');
            if (target) {
                const text = target.getAttribute('data-tooltip');
                const rect = target.getBoundingClientRect();
                
                timerRef.current = setTimeout(() => {
                    setTooltip({
                        visible: true,
                        text,
                        x: rect.left + rect.width / 2,
                        y: rect.top - 10
                    });
                }, 3000); // 3 second delay
            }
        };

        const handleMouseOut = () => {
            clearTimeout(timerRef.current);
            setTooltip(prev => ({ ...prev, visible: false }));
        };

        window.addEventListener('mouseover', handleMouseOver);
        window.addEventListener('mouseout', handleMouseOut);
        window.addEventListener('scroll', handleMouseOut);

        return () => {
            window.removeEventListener('mouseover', handleMouseOver);
            window.removeEventListener('mouseout', handleMouseOut);
            window.removeEventListener('scroll', handleMouseOut);
        };
    }, []);

    if (!tooltip.visible) return null;

    return (
        <div 
            className="global-tooltip-container"
            style={{ left: tooltip.x, top: tooltip.y }}
        >
            <div className="tooltip-arrow" />
            <div className="tooltip-content">
                {tooltip.text}
            </div>
        </div>
    );
};

export default GlobalTooltip;
