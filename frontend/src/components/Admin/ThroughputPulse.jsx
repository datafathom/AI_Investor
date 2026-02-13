import React, { useState, useEffect, useMemo, useRef } from 'react';

/**
 * ThroughputPulse - A dynamic SVG Sparkline visualizing events per second.
 * @param {Object} props
 * @param {Object} props.stats - The current stats object from EventBus
 */
const ThroughputPulse = ({ stats }) => {
  const [dataPoints, setDataPoints] = useState(new Array(30).fill(0));

  // Track total system activity (EPS approximation)
  const totalActivity = useMemo(() => {
    return Object.values(stats).reduce((acc, curr) => acc + (curr.publish_count || 0), 0);
  }, [stats]);

  // Use refs to track activity values without triggering interval restarts
  const activityRef = useRef(totalActivity);
  const lastActivityRef = useRef(totalActivity);

  useEffect(() => {
    activityRef.current = totalActivity;
  }, [totalActivity]);

  useEffect(() => {
    const interval = setInterval(() => {
      const current = activityRef.current;
      const delta = current - lastActivityRef.current;
      
      setDataPoints(prev => [...prev.slice(1), delta >= 0 ? delta : 0]);
      lastActivityRef.current = current;
    }, 1000);
    
    return () => clearInterval(interval);
  }, []); // Run once on mount

  const viewBoxWidth = 300;
  const viewBoxHeight = 60;

  const pathData = useMemo(() => {
    const max = Math.max(...dataPoints, 5); // Minimum 5 to avoid flat lines
    const points = dataPoints.map((val, i) => {
      const x = (i / (dataPoints.length - 1)) * viewBoxWidth;
      const y = viewBoxHeight - (val / max) * viewBoxHeight;
      return `${x},${y}`;
    });
    return `M ${points.join(' L ')}`;
  }, [dataPoints]);

  const currentEPS = dataPoints[dataPoints.length - 1];

  return (
    <div className="throughput-pulse-container">
      <div className="pulse-header">
        <span className="pulse-title">NEURAL_LOAD_PULSE</span>
        <span className={`pulse-value ${currentEPS > 50 ? 'high-load' : ''}`}>
          {currentEPS} EPS
        </span>
      </div>
      <svg 
        viewBox={`0 0 ${viewBoxWidth} ${viewBoxHeight}`} 
        className="pulse-svg"
        preserveAspectRatio="none"
      >
        <defs>
          <linearGradient id="pulseGradient" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="#00f2ff" stopOpacity="0.2" />
            <stop offset="100%" stopColor="#00f2ff" stopOpacity="0" />
          </linearGradient>
        </defs>
        <path
          d={`${pathData} L ${viewBoxWidth},${viewBoxHeight} L 0,${viewBoxHeight} Z`}
          fill="url(#pulseGradient)"
        />
        <path
          d={pathData}
          fill="none"
          stroke="#00f2ff"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="pulse-path"
        />
      </svg>
      <div className="pulse-footer">
        <div className="pulse-timeline">
            <span className="time-label">-30S</span>
            <span className="time-label">-15S</span>
            <span className="time-label">NOW</span>
        </div>
        <div className="pulse-grid">
            {[...Array(7)].map((_, i) => <div key={i} className="grid-tick" />)}
        </div>
      </div>
      
      <style jsx="true">{`
        .throughput-pulse-container {
          background: rgba(0, 242, 255, 0.03);
          border: 1px solid rgba(0, 242, 255, 0.1);
          border-radius: 4px;
          padding: 12px;
          height: 100%;
          display: flex;
          flex-direction: column;
        }
        .pulse-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 8px;
        }
        .pulse-title {
          font-size: 0.65rem;
          color: #00f2ff;
          letter-spacing: 0.1em;
          font-weight: 800;
        }
        .pulse-value {
          font-size: 0.8rem;
          color: #fff;
          font-weight: 900;
        }
        .high-load {
          color: #ff4757;
          text-shadow: 0 0 5px #ff4757;
        }
        .pulse-svg {
          flex: 1;
          width: 100%;
          filter: drop-shadow(0 0 4px rgba(0, 242, 255, 0.4));
        }
        .pulse-path {
            stroke-dasharray: 1000;
            stroke-dashoffset: 0;
        }
        .pulse-footer {
          margin-top: auto;
        }
        .pulse-timeline {
          display: flex;
          justify-content: space-between;
          padding: 0 2px;
          margin-bottom: 2px;
        }
        .time-label {
          font-size: 0.5rem;
          color: #555;
          font-weight: 800;
          letter-spacing: 0.05em;
        }
        .pulse-grid {
          display: flex;
          justify-content: space-between;
          height: 3px;
          border-top: 1px solid rgba(0, 242, 255, 0.1);
        }
        .grid-tick {
          width: 1px;
          height: 100%;
          background: rgba(0, 242, 255, 0.2);
        }
      `}</style>
    </div>
  );
};

export default ThroughputPulse;
