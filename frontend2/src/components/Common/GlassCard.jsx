import React from 'react';
import './GlassCard.css';

/**
 * A premium glassmorphism card component with configurable effects.
 * 
 * @param {string} variant - 'default' | 'elevated' | 'inset'
 * @param {string} status - 'success' | 'warning' | 'error' | null (adds left border accent)
 * @param {boolean} hoverable - Enable hover effects
 * @param {boolean} clickable - Show pointer cursor
 * @param {string} className - Additional classes
 */
const GlassCard = ({ 
  children, 
  variant = 'default', 
  status = null, 
  hoverable = true, 
  clickable = false,
  className = '',
  onClick,
  ...props 
}) => {
  const statusClass = status ? `glass-card--${status}` : '';
  const hoverClass = hoverable ? 'glass-card--hoverable' : '';
  const clickClass = clickable ? 'glass-card--clickable' : '';
  
  return (
    <div 
      className={`glass-card glass-card--${variant} ${statusClass} ${hoverClass} ${clickClass} ${className}`}
      onClick={onClick}
      role={clickable ? 'button' : undefined}
      tabIndex={clickable ? 0 : undefined}
      {...props}
    >
      {status && <div className="glass-card__status-bar" />}
      <div className="glass-card__content">
        {children}
      </div>
    </div>
  );
};

export default GlassCard;
