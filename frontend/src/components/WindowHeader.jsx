/**
 * WindowHeader Component
 * 
 * Mac-style window header with minimize, maximize, and close buttons.
 */

import React from 'react';
import './WindowHeader.css';
import SymbolLinkBadge from './SymbolLinkBadge';

export default function WindowHeader({
  title,
  onMinimize,
  onMaximize,
  onClose,
  onLock,
  onZoomIn,
  onZoomOut,
  onMinimumFullView,
  onViewSource,
  isMaximized = false,
  isLocked = false,
  linkingGroup = 'none', // none, red, blue, green
  onLinkingGroupChange
}) {
  const handleHeaderMouseDown = (e) => {
    // Make header draggable (except when clicking on buttons)
    // Don't prevent default on double-click to allow double-click handler to fire
    if (!e.target.closest('.window-control') && e.detail !== 2) {
      e.preventDefault();
      const widgetWrapper = e.currentTarget.closest('.widget-wrapper');
      if (widgetWrapper) {
        // Set the drag handle as the active drag element
        const dragHandle = widgetWrapper.querySelector('.widget-drag-handle');
        if (dragHandle) {
          // Make drag handle visible and trigger drag
          dragHandle.style.opacity = '1';
          dragHandle.style.pointerEvents = 'auto';
          // Create a synthetic mousedown event on the drag handle
          const syntheticEvent = new MouseEvent('mousedown', {
            bubbles: true,
            cancelable: true,
            view: window,
            clientX: e.clientX,
            clientY: e.clientY,
            button: 0,
          });
          dragHandle.dispatchEvent(syntheticEvent);
        }
      }
    }
  };

  const handleHeaderDoubleClick = (e) => {
    // Only trigger minimum full view if double-clicking on non-interactive space
    // Exclude control buttons (close, minimize, maximize, zoom, lock)
    if (!e.target.closest('.window-control') && !e.target.closest('.window-header-right')) {
      e.stopPropagation();
      if (onMinimumFullView) {
        onMinimumFullView();
      }
    }
  };

  const handleButtonClick = (e, handler) => {
    e.stopPropagation();
    if (handler) {
      handler(e);
    }
  };

  const handleButtonDoubleClick = (e) => {
    e.stopPropagation();
  };

  return (
    <div className="window-header" onMouseDown={handleHeaderMouseDown} onDoubleClick={handleHeaderDoubleClick}>
      <div className="window-header-left-group">
        <div className="window-controls">
          <button
            className="window-control window-control-close"
            onClick={(e) => handleButtonClick(e, onClose)}
            onDoubleClick={handleButtonDoubleClick}
            aria-label="Close window"
            title="Close"
          >
            <span className="window-control-icon"></span>
          </button>
          <button
            className="window-control window-control-minimize"
            onClick={(e) => handleButtonClick(e, onMinimize)}
            onDoubleClick={handleButtonDoubleClick}
            aria-label="Minimize window"
            title="Minimize"
          >
            <span className="window-control-icon"></span>
          </button>
          <button
            className="window-control window-control-maximize"
            onClick={(e) => handleButtonClick(e, onMaximize)}
            onDoubleClick={handleButtonDoubleClick}
            aria-label={isMaximized ? "Restore window" : "Maximize window"}
            title={isMaximized ? "Restore" : "Maximize"}
          >
            <span className="window-control-icon">{isMaximized ? '' : ''}</span>
          </button>
        </div>

        <SymbolLinkBadge 
          group={linkingGroup} 
          onGroupChange={onLinkingGroupChange} 
        />
      </div>
      <div className="window-title">{title}</div>
      <div className="window-header-right">
        {onZoomOut && (
          <button
            className="window-control window-control-zoom"
            onClick={(e) => handleButtonClick(e, onZoomOut)}
            onDoubleClick={handleButtonDoubleClick}
            aria-label="Zoom out widget"
            title="Zoom out"
          >
            <span className="window-control-icon"></span>
            <span className="window-zoom-symbol"></span>
          </button>
        )}
        {onZoomIn && (
          <button
            className="window-control window-control-zoom"
            onClick={(e) => handleButtonClick(e, onZoomIn)}
            onDoubleClick={handleButtonDoubleClick}
            aria-label="Zoom in widget"
            title="Zoom in"
          >
            <span className="window-control-icon"></span>
            <span className="window-zoom-symbol">+</span>
          </button>
        )}
        {onLock && (
          <button
            className="window-control window-control-lock"
            onClick={(e) => handleButtonClick(e, onLock)}
            onDoubleClick={handleButtonDoubleClick}
            aria-label={isLocked ? "Unlock widget" : "Lock widget"}
            title={isLocked ? "Unlock" : "Lock"}
          >
            <span className="window-control-icon">{isLocked ? '' : ''}</span>
          </button>
        )}
        {onViewSource && (
          <button
            className="window-control window-control-source"
            onClick={(e) => handleButtonClick(e, onViewSource)}
            onDoubleClick={handleButtonDoubleClick}
            aria-label="View source code"
            title="View Source"
          >
            <span className="window-control-icon">&lt; &gt;</span>
          </button>
        )}
      </div>
    </div>
  );
}

