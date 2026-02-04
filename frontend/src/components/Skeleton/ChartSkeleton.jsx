import React from 'react';
import './Skeleton.css';

/**
 * Chart skeleton with animated wave effect.
 * @param {string} type - 'line' | 'bar' | 'pie' | 'area'
 * @param {number} height - Chart height in pixels
 */
const ChartSkeleton = ({ type = 'area', height = 200 }) => {
  return (
    <div className="chart-skeleton" style={{ height }}>
      <div className="chart-skeleton__background">
        {/* Grid Lines */}
        <div className="chart-skeleton__grid">
          {[1, 2, 3, 4].map(i => (
            <div key={i} className="chart-skeleton__grid-line" />
          ))}
        </div>
        
        {/* Animated Wave */}
        {type === 'area' || type === 'line' ? (
          <svg className="chart-skeleton__wave" viewBox="0 0 400 100" preserveAspectRatio="none">
            <path
              className="chart-skeleton__wave-path shimmer-path"
              d="M0,80 C50,60 100,90 150,50 C200,10 250,70 300,40 C350,10 400,60 400,80 L400,100 L0,100 Z"
              fill="url(#skeleton-gradient)"
            />
            <defs>
              <linearGradient id="skeleton-gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="rgba(6, 182, 212, 0.1)" />
                <stop offset="50%" stopColor="rgba(6, 182, 212, 0.2)" />
                <stop offset="100%" stopColor="rgba(6, 182, 212, 0.1)" />
              </linearGradient>
            </defs>
          </svg>
        ) : type === 'bar' ? (
          <div className="chart-skeleton__bars">
            {[40, 70, 55, 85, 60, 45, 75].map((h, i) => (
              <div 
                key={i} 
                className="chart-skeleton__bar shimmer" 
                style={{ height: `${h}%`, animationDelay: `${i * 0.1}s` }} 
              />
            ))}
          </div>
        ) : (
          <div className="chart-skeleton__pie shimmer" />
        )}
      </div>
      
      {/* Axis Labels */}
      <div className="chart-skeleton__x-axis">
        {[1, 2, 3, 4, 5].map(i => (
          <div key={i} className="skeleton skeleton--axis-label shimmer" />
        ))}
      </div>
    </div>
  );
};

export default ChartSkeleton;
