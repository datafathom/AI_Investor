/**
 * Split Pane Component
 * 
 * Resizable split-pane layout component.
 * Supports horizontal and vertical splits with multiple panes.
 */

import React, { useState, useRef, useEffect } from 'react';
import './SplitPane.css';

export default function SplitPane({
  direction = 'horizontal', // 'horizontal' | 'vertical'
  children,
  defaultSizes = [50, 50], // Percentage sizes
  minSize = 10, // Minimum size in percentage
  onResize,
}) {
  const [sizes, setSizes] = useState(defaultSizes);
  const [isResizing, setIsResizing] = useState(false);
  const [resizeIndex, setResizeIndex] = useState(null);
  const containerRef = useRef(null);
  const startPosRef = useRef(null);
  const startSizesRef = useRef(null);

  const handleMouseDown = (index, e) => {
    e.preventDefault();
    setIsResizing(true);
    setResizeIndex(index);
    startPosRef.current = direction === 'horizontal' ? e.clientX : e.clientY;
    startSizesRef.current = [...sizes];
  };

  useEffect(() => {
    if (!isResizing) return;

    const handleMouseMove = (e) => {
      if (!containerRef.current || startPosRef.current === null) return;

      const containerSize = direction === 'horizontal'
        ? containerRef.current.offsetWidth
        : containerRef.current.offsetHeight;

      const currentPos = direction === 'horizontal' ? e.clientX : e.clientY;
      const delta = currentPos - startPosRef.current;
      const deltaPercent = (delta / containerSize) * 100;

      const newSizes = [...startSizesRef.current];
      const leftSize = newSizes[resizeIndex];
      const rightSize = newSizes[resizeIndex + 1];

      // Calculate new sizes
      let newLeftSize = leftSize + deltaPercent;
      let newRightSize = rightSize - deltaPercent;

      // Enforce minimum sizes
      if (newLeftSize < minSize) {
        newLeftSize = minSize;
        newRightSize = leftSize + rightSize - minSize;
      } else if (newRightSize < minSize) {
        newRightSize = minSize;
        newLeftSize = leftSize + rightSize - minSize;
      }

      newSizes[resizeIndex] = newLeftSize;
      newSizes[resizeIndex + 1] = newRightSize;

      setSizes(newSizes);

      if (onResize) {
        onResize(newSizes);
      }
    };

    const handleMouseUp = () => {
      setIsResizing(false);
      setResizeIndex(null);
      startPosRef.current = null;
      startSizesRef.current = null;
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isResizing, resizeIndex, direction, minSize, onResize]);

  const childrenArray = React.Children.toArray(children);

  return (
    <div
      ref={containerRef}
      className={`split-pane split-pane-${direction} ${isResizing ? 'split-pane-resizing' : ''}`}
    >
      {childrenArray.map((child, index) => (
        <React.Fragment key={index}>
          <div
            className="split-pane-pane"
            style={{
              [direction === 'horizontal' ? 'width' : 'height']: `${sizes[index]}%`,
            }}
          >
            {child}
          </div>
          {index < childrenArray.length - 1 && (
            <div
              className={`split-pane-divider split-pane-divider-${direction}`}
              onMouseDown={(e) => handleMouseDown(index, e)}
            >
              <div className="split-pane-divider-handle" />
            </div>
          )}
        </React.Fragment>
      ))}
    </div>
  );
}

