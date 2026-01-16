/**
 * Loading Spinner Component
 * 
 * Reusable loading indicator component.
 */

import React from 'react';
import { useColorPalette } from '../hooks/useColorPalette';
import './LoadingSpinner.css';

/**
 * Loading Spinner Component
 * @param {Object} props - Component props
 * @param {string} props.message - Optional message to display
 * @param {string} props.size - Size: 'small' | 'medium' | 'large'
 */
export function LoadingSpinner({ message, size = 'medium' }) {
  const colors = useColorPalette();
  const spinnerColor = colors.burgundy?.primary || '#8B1538';

  const getSizeClass = () => {
    switch (size) {
      case 'small':
        return 'loading-spinner-small';
      case 'large':
        return 'loading-spinner-large';
      default:
        return 'loading-spinner-medium';
    }
  };

  return (
    <div className="loading-spinner-container">
      <div
        className={`loading-spinner ${getSizeClass()}`}
        style={{
          borderColor: `${spinnerColor}20`,
          borderTopColor: spinnerColor,
        }}
      />
      {message && <div className="loading-spinner-message">{message}</div>}
    </div>
  );
}

export default LoadingSpinner;

