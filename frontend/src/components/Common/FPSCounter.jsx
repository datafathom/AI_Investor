import React, { useState, useEffect, useRef } from 'react';

const FPSCounter = () => {
    const [fps, setFps] = useState(0);
    const framesRef = useRef(0);
    const lastTimeRef = useRef(performance.now());

    useEffect(() => {
        let requestRef;
        
        const loop = () => {
            framesRef.current++;
            const now = performance.now();
            
            if (now >= lastTimeRef.current + 1000) {
                setFps(Math.round((framesRef.current * 1000) / (now - lastTimeRef.current)));
                framesRef.current = 0;
                lastTimeRef.current = now;
            }
            
            requestRef = requestAnimationFrame(loop);
        };
        
        requestRef = requestAnimationFrame(loop);
        return () => cancelAnimationFrame(requestRef);
    }, []);

    const getColor = (fps) => {
        if (fps >= 55) return '#00ff88'; // Greenish
        if (fps >= 30) return '#ffc107'; // Yellowish
        return '#ff4757'; // Reddish
    };

    return (
        <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '2px 8px',
            borderRadius: '4px',
            background: 'rgba(0,0,0,0.3)',
            border: `1px solid ${getColor(fps)}44`,
            fontSize: '10px',
            fontFamily: 'monospace',
            color: getColor(fps),
            fontWeight: 'bold',
            minWidth: '50px',
            justifyContent: 'center'
        }} title="Frames Per Second">
            {fps} FPS
        </div>
    );
};

export default FPSCounter;
