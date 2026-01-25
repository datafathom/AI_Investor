import React from 'react';
import './Badge.css';

/**
 * Notification badge for counts and status indicators.
 * 
 * @param {number|string} count - Badge content (number or text)
 * @param {string} variant - 'default' | 'success' | 'warning' | 'error' | 'info'
 * @param {boolean} dot - Show as dot (no content)
 * @param {boolean} pulse - Enable pulse animation
 * @param {string} position - 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left'
 */
const Badge = ({
  count,
  variant = 'default',
  dot = false,
  pulse = false,
  position = 'top-right',
  children,
  max = 99,
  className = ''
}) => {
  const displayCount = typeof count === 'number' && count > max ? `${max}+` : count;
  const showBadge = dot || (count !== undefined && count !== 0);

  if (!children) {
    // Standalone badge
    return (
      <span className={`badge badge--${variant} ${pulse ? 'badge--pulse' : ''} ${className}`}>
        {!dot && displayCount}
      </span>
    );
  }

  // Badge with children (positioned)
  return (
    <div className="badge-wrapper">
      {children}
      {showBadge && (
        <span 
          className={`badge badge--${variant} badge--${position} ${dot ? 'badge--dot' : ''} ${pulse ? 'badge--pulse' : ''} ${className}`}
        >
          {!dot && displayCount}
        </span>
      )}
    </div>
  );
};

export default Badge;
