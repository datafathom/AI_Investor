/**
 * MemoizedWidget Component
 * 
 * Wraps widget content in React.memo to prevent unnecessary re-renders
 * when other widgets in the grid are dragged or resized.
 */
import React from 'react';

export const MemoizedWidget = React.memo(({ children, widgetId }) => {
  return <>{children}</>;
}, (prevProps, nextProps) => {
  // Only re-render if the children actually change
  // This prevents re-renders when other widgets move in the grid
  return prevProps.children === nextProps.children && 
         prevProps.widgetId === nextProps.widgetId;
});

MemoizedWidget.displayName = 'MemoizedWidget';

