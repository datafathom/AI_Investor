import React, { useState, useEffect, useRef } from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import './StatCard.css';

/**
 * Premium stat card with animated counter and optional sparkline.
 * 
 * @param {string} label - Stat label
 * @param {number} value - Numeric value to display
 * @param {string} prefix - Value prefix (e.g., '$')
 * @param {string} suffix - Value suffix (e.g., '%')
 * @param {number} change - Change value for trend
 * @param {string} changeLabel - Label for change (e.g., 'vs yesterday')
 * @param {number[]} sparklineData - Array of values for mini chart
 * @param {string} status - 'positive' | 'negative' | 'neutral'
 */
const StatCard = ({ 
  label, 
  value, 
  prefix = '', 
  suffix = '', 
  change, 
  changeLabel = '',
  sparklineData = [],
  status = 'neutral',
  formatValue = (v) => v.toLocaleString()
}) => {
  const [displayValue, setDisplayValue] = useState(0);
  const [hasAnimated, setHasAnimated] = useState(false);
  const cardRef = useRef(null);

  // Animate counter on visibility
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasAnimated) {
          animateValue(0, value, 1000);
          setHasAnimated(true);
        }
      },
      { threshold: 0.1 }
    );

    if (cardRef.current) observer.observe(cardRef.current);
    return () => observer.disconnect();
  }, [value, hasAnimated]);

  const animateValue = (start, end, duration) => {
    const numericEnd = typeof end === 'number' ? end : parseFloat(end);
    if (isNaN(numericEnd)) {
      setDisplayValue(end);
      return;
    }

    const startTime = performance.now();
    
    const update = (currentTime) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const current = start + (numericEnd - start) * easeOut;
      
      setDisplayValue(current);
      
      if (progress < 1) {
        requestAnimationFrame(update);
      } else {
        setDisplayValue(numericEnd);
      }
    };
    
    requestAnimationFrame(update);
  };

  const TrendIcon = change > 0 ? TrendingUp : change < 0 ? TrendingDown : Minus;
  const trendClass = change > 0 ? 'positive' : change < 0 ? 'negative' : 'neutral';

  // Render sparkline
  const renderSparkline = () => {
    if (!sparklineData.length) return null;
    const max = Math.max(...sparklineData);
    const min = Math.min(...sparklineData);
    const range = max - min || 1;
    const height = 32;
    const width = 80;
    const points = sparklineData.map((v, i) => {
      const x = (i / (sparklineData.length - 1)) * width;
      const y = height - ((v - min) / range) * height;
      return `${x},${y}`;
    }).join(' ');

    return (
      <svg className="stat-card__sparkline" viewBox={`0 0 ${width} ${height}`}>
        <polyline
          points={points}
          fill="none"
          stroke={status === 'positive' ? 'var(--neon-green)' : status === 'negative' ? 'var(--neon-red)' : 'var(--neon-cyan)'}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    );
  };

  return (
    <div ref={cardRef} className={`stat-card stat-card--${status}`}>
      <div className="stat-card__header">
        <span className="stat-card__label">{label}</span>
        {renderSparkline()}
      </div>
      
      <div className="stat-card__value">
        <span className="stat-card__prefix">{prefix}</span>
        <span className="stat-card__number">{formatValue(displayValue)}</span>
        <span className="stat-card__suffix">{suffix}</span>
      </div>

      {change !== undefined && (
        <div className={`stat-card__trend stat-card__trend--${trendClass}`}>
          <TrendIcon size={14} />
          <span>{change > 0 ? '+' : ''}{change}{suffix}</span>
          {changeLabel && <span className="stat-card__trend-label">{changeLabel}</span>}
        </div>
      )}
    </div>
  );
};

export default StatCard;
