import React from 'react';
import './ProgressBar.css';

/**
 * Premium progress bar with animated fill.
 * 
 * @param {number} value - Current value (0-100)
 * @param {number} max - Maximum value (default 100)
 * @param {string} label - Label text
 * @param {string} variant - 'default' | 'success' | 'warning' | 'error'
 * @param {boolean} showValue - Show percentage/value text
 * @param {boolean} animated - Enable fill animation
 * @param {string} size - 'sm' | 'md' | 'lg'
 */
const ProgressBar = ({
  value = 0,
  max = 100,
  label,
  variant = 'default',
  showValue = true,
  animated = true,
  size = 'md',
  className = ''
}) => {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);

  return (
    <div className={`progress-bar progress-bar--${size} ${className}`}>
      {(label || showValue) && (
        <div className="progress-bar__header">
          {label && <span className="progress-bar__label">{label}</span>}
          {showValue && (
            <span className="progress-bar__value font-mono">
              {percentage.toFixed(0)}%
            </span>
          )}
        </div>
      )}
      
      <div className="progress-bar__track">
        <div 
          className={`progress-bar__fill progress-bar__fill--${variant} ${animated ? 'progress-bar__fill--animated' : ''}`}
          style={{ width: `${percentage}%` }}
        >
          <div className="progress-bar__glow" />
        </div>
      </div>
    </div>
  );
};

export default ProgressBar;
