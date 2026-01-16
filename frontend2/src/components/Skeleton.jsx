/**
 * Skeleton Loading Component
 * 
 * Shimmer effect skeleton loader for content placeholders.
 */

import React from 'react';
import { useColorPalette } from '../hooks/useColorPalette';
import '../App.css';

function Skeleton({ width, height, borderRadius = '4px', style = {} }) {
  const { palette } = useColorPalette();

  return (
    <div
      className="skeleton shimmer"
      style={{
        width: width || '100%',
        height: height || '1.2em',
        backgroundColor: palette?.backgrounds?.hover || '#faf5d8',
        borderRadius,
        overflow: 'hidden',
        position: 'relative',
        ...style,
      }}
    >
      <div
        style={{
          position: 'absolute',
          inset: 0,
          background: `linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent
          )`,
          animation: 'shimmer 1.5s infinite',
        }}
      />
    </div>
  );
}

export function SkeletonCard() {
  return (
    <div className="glass card" style={{ padding: '1.5rem' }}>
      <Skeleton width="60%" height="1.5rem" borderRadius="var(--radius-chip)" style={{ marginBottom: '1rem' }} />
      <Skeleton height="1rem" style={{ marginBottom: '0.5rem' }} />
      <Skeleton height="1rem" style={{ marginBottom: '0.5rem' }} />
      <Skeleton width="80%" height="1rem" />
    </div>
  );
}

export function SkeletonTable({ rows = 5, cols = 4 }) {
  return (
    <div className="glass card" style={{ padding: '1.5rem', overflow: 'hidden' }}>
      {/* Table Header */}
      <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem', paddingBottom: '0.75rem', borderBottom: '1px solid rgba(0,0,0,0.1)' }}>
        {Array.from({ length: cols }).map((_, i) => (
          <Skeleton key={i} width="100%" height="1.25rem" />
        ))}
      </div>
      {/* Table Rows */}
      {Array.from({ length: rows }).map((_, rowIdx) => (
        <div key={rowIdx} style={{ display: 'flex', gap: '1rem', marginBottom: '0.75rem' }}>
          {Array.from({ length: cols }).map((_, colIdx) => (
            <Skeleton key={colIdx} width="100%" height="1rem" />
          ))}
        </div>
      ))}
    </div>
  );
}

export default Skeleton;

