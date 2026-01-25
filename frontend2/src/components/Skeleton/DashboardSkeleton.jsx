import React from 'react';
import './Skeleton.css';

/**
 * Full page skeleton for dashboard loading states.
 */
const DashboardSkeleton = () => {
  return (
    <div className="dashboard-skeleton animate-fade-in">
      {/* Header Skeleton */}
      <div className="skeleton-header">
        <div className="skeleton skeleton--title shimmer" />
        <div className="skeleton skeleton--subtitle shimmer" />
      </div>

      {/* Stats Row Skeleton */}
      <div className="skeleton-stats-row">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="skeleton-stat-card">
            <div className="skeleton skeleton--label shimmer" />
            <div className="skeleton skeleton--value shimmer" />
          </div>
        ))}
      </div>

      {/* Content Grid Skeleton */}
      <div className="skeleton-grid">
        <div className="skeleton-card skeleton-card--large">
          <div className="skeleton skeleton--chart shimmer" />
        </div>
        <div className="skeleton-card">
          <div className="skeleton skeleton--line shimmer" />
          <div className="skeleton skeleton--line shimmer" />
          <div className="skeleton skeleton--line shimmer" />
        </div>
        <div className="skeleton-card">
          <div className="skeleton skeleton--line shimmer" />
          <div className="skeleton skeleton--line shimmer" />
        </div>
      </div>
    </div>
  );
};

export default DashboardSkeleton;
