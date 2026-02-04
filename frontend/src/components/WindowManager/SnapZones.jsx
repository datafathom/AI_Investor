/**
 * Snap Zones Component
 * 
 * Visual overlay showing snap zones for window snapping.
 * Appears when dragging a window near screen edges.
 */

import React, { useState, useEffect } from 'react';
import './SnapZones.css';

const SNAP_ZONES = [
  { id: 'left', label: 'Left Half', position: { left: 0, top: 0, width: '50%', height: '100%' } },
  { id: 'right', label: 'Right Half', position: { right: 0, top: 0, width: '50%', height: '100%' } },
  { id: 'top', label: 'Top Half', position: { left: 0, top: 0, width: '100%', height: '50%' } },
  { id: 'bottom', label: 'Bottom Half', position: { left: 0, bottom: 0, width: '100%', height: '50%' } },
  { id: 'topLeft', label: 'Top Left', position: { left: 0, top: 0, width: '50%', height: '50%' } },
  { id: 'topRight', label: 'Top Right', position: { right: 0, top: 0, width: '50%', height: '50%' } },
  { id: 'bottomLeft', label: 'Bottom Left', position: { left: 0, bottom: 0, width: '50%', height: '50%' } },
  { id: 'bottomRight', label: 'Bottom Right', position: { right: 0, bottom: 0, width: '50%', height: '50%' } },
];

const SNAP_THRESHOLD = 50; // pixels from edge to trigger snap zone

export default function SnapZones({ 
  isDragging, 
  dragPosition, 
  onSnap, 
  enabled = true 
}) {
  const [activeZone, setActiveZone] = useState(null);
  const [showZones, setShowZones] = useState(false);

  useEffect(() => {
    if (!isDragging || !enabled || !dragPosition) {
      setActiveZone(null);
      setShowZones(false);
      return;
    }

    // Check if we're near any edge
    const { x, y } = dragPosition;
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    let detectedZone = null;

    // Check proximity to edges
    const nearLeft = x < SNAP_THRESHOLD;
    const nearRight = x > viewportWidth - SNAP_THRESHOLD;
    const nearTop = y < SNAP_THRESHOLD + 30; // Account for menu bar
    const nearBottom = y > viewportHeight - SNAP_THRESHOLD;

    // Determine which zone based on proximity
    if (nearTop && nearLeft) {
      detectedZone = 'topLeft';
    } else if (nearTop && nearRight) {
      detectedZone = 'topRight';
    } else if (nearBottom && nearLeft) {
      detectedZone = 'bottomLeft';
    } else if (nearBottom && nearRight) {
      detectedZone = 'bottomRight';
    } else if (nearLeft) {
      detectedZone = 'left';
    } else if (nearRight) {
      detectedZone = 'right';
    } else if (nearTop) {
      detectedZone = 'top';
    } else if (nearBottom) {
      detectedZone = 'bottom';
    }

    setActiveZone(detectedZone);
    setShowZones(detectedZone !== null);

    // Auto-snap if we're very close to an edge
    if (detectedZone) {
      const zone = SNAP_ZONES.find(z => z.id === detectedZone);
      if (zone) {
        // Check if we're within auto-snap distance (smaller threshold)
        const autoSnapThreshold = SNAP_THRESHOLD / 2;
        const shouldAutoSnap = 
          (nearLeft && x < autoSnapThreshold) ||
          (nearRight && x > viewportWidth - autoSnapThreshold) ||
          (nearTop && y < autoSnapThreshold + 30) ||
          (nearBottom && y > viewportHeight - autoSnapThreshold);

        if (shouldAutoSnap && onSnap) {
          onSnap(detectedZone);
        }
      }
    }
  }, [isDragging, dragPosition, enabled, onSnap]);

  if (!showZones || !enabled) {
    return null;
  }

  return (
    <div className="snap-zones-overlay">
      {SNAP_ZONES.map(zone => {
        const isActive = activeZone === zone.id;
        return (
          <div
            key={zone.id}
            className={`snap-zone ${isActive ? 'snap-zone-active' : ''}`}
            style={zone.position}
            onClick={() => {
              if (isActive && onSnap) {
                onSnap(zone.id);
              }
            }}
          >
            {isActive && (
              <div className="snap-zone-label">
                {zone.label}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

/**
 * Hook to detect snap zones during drag
 */
export function useSnapZones(isDragging, dragPosition, onSnap) {
  const [snapZone, setSnapZone] = useState(null);

  useEffect(() => {
    if (!isDragging || !dragPosition) {
      setSnapZone(null);
      return;
    }

    const { x, y } = dragPosition;
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;

    const nearLeft = x < SNAP_THRESHOLD;
    const nearRight = x > viewportWidth - SNAP_THRESHOLD;
    const nearTop = y < SNAP_THRESHOLD + 30;
    const nearBottom = y > viewportHeight - SNAP_THRESHOLD;

    let detectedZone = null;

    if (nearTop && nearLeft) detectedZone = 'topLeft';
    else if (nearTop && nearRight) detectedZone = 'topRight';
    else if (nearBottom && nearLeft) detectedZone = 'bottomLeft';
    else if (nearBottom && nearRight) detectedZone = 'bottomRight';
    else if (nearLeft) detectedZone = 'left';
    else if (nearRight) detectedZone = 'right';
    else if (nearTop) detectedZone = 'top';
    else if (nearBottom) detectedZone = 'bottom';

    setSnapZone(detectedZone);

    if (detectedZone && onSnap) {
      const autoSnapThreshold = SNAP_THRESHOLD / 2;
      const shouldAutoSnap = 
        (nearLeft && x < autoSnapThreshold) ||
        (nearRight && x > viewportWidth - autoSnapThreshold) ||
        (nearTop && y < autoSnapThreshold + 30) ||
        (nearBottom && y > viewportHeight - autoSnapThreshold);

      if (shouldAutoSnap) {
        onSnap(detectedZone);
      }
    }
  }, [isDragging, dragPosition, onSnap]);

  return snapZone;
}

