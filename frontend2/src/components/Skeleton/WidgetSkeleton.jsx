import React from 'react';
import './Skeleton.css';

/**
 * Skeleton loader for individual widgets.
 * @param {number} lines - Number of skeleton lines to show
 * @param {boolean} showHeader - Show header skeleton
 * @param {boolean} showChart - Show chart placeholder
 */
const WidgetSkeleton = ({ lines = 3, showHeader = true, showChart = false }) => {
  return (
    <div className="widget-skeleton">
      {showHeader && (
        <div className="skeleton-widget-header">
          <div className="skeleton skeleton--icon shimmer" />
          <div className="skeleton skeleton--widget-title shimmer" />
        </div>
      )}
      
      {showChart ? (
        <div className="skeleton skeleton--chart shimmer" />
      ) : (
        <div className="skeleton-lines">
          {Array.from({ length: lines }).map((_, i) => (
            <div 
              key={i} 
              className="skeleton skeleton--line shimmer" 
              style={{ width: `${85 - (i * 10)}%`, animationDelay: `${i * 0.1}s` }}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default WidgetSkeleton;
