/**
 * Status Badge Component
 * 
 * Reusable status indicator component with color coding.
 * Similar to mobile app StatusBadge for consistency.
 */

import React from 'react';
import { useColorPalette } from '../hooks/useColorPalette';
import './StatusBadge.css';

/**
 * Status Badge Component
 * @param {Object} props - Component props
 * @param {string} props.status - Status text
 * @param {string} props.type - Status type: 'success' | 'warning' | 'error' | 'info' | 'default'
 * @param {string} props.size - Size: 'small' | 'medium' | 'large'
 */
export function StatusBadge({ status, type = 'default', size = 'medium' }) {
  const colors = useColorPalette();

  const getStatusColor = () => {
    switch (type) {
      case 'success':
        return '#4CAF50';
      case 'warning':
        return '#FF9800';
      case 'error':
        return '#F44336';
      case 'info':
        return '#2196F3';
      default:
        return colors.text?.secondary || '#666';
    }
  };

  const getSizeClass = () => {
    switch (size) {
      case 'small':
        return 'status-badge-small';
      case 'large':
        return 'status-badge-large';
      default:
        return 'status-badge-medium';
    }
  };

  const statusColor = getStatusColor();
  const sizeClass = getSizeClass();

  return (
    <span
      className={`status-badge ${sizeClass}`}
      style={{
        backgroundColor: `${statusColor}20`,
        color: statusColor,
      }}
    >
      {status}
    </span>
  );
}

export default StatusBadge;

