/**
 * Metric Card Component
 * 
 * Reusable metric display component with icon and label.
 * Similar to mobile app MetricCard for consistency.
 */

import React from 'react';
import { useColorPalette } from '../hooks/useColorPalette';
import './MetricCard.css';

/**
 * Metric Card Component
 * @param {Object} props - Component props
 * @param {string|number} props.value - Metric value
 * @param {string} props.label - Label text
 * @param {string} props.icon - Optional emoji icon
 * @param {string} props.color - Optional custom color
 */
export function MetricCard({ value, label, icon, color }) {
  const colors = useColorPalette();
  const displayColor = color || colors.burgundy?.primary || '#8B1538';

  return (
    <div className="metric-card">
      {icon && <div className="metric-card-icon">{icon}</div>}
      <div className="metric-card-value" style={{ color: displayColor }}>
        {value}
      </div>
      <div className="metric-card-label">{label}</div>
    </div>
  );
}

export default MetricCard;

