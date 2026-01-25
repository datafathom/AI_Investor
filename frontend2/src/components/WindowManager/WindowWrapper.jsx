import React, { useRef, useEffect } from 'react';
import { motion, useDragControls } from 'framer-motion';
import useWindowStore from '../../stores/windowStore';
import ResizeHandles from './ResizeHandles';
import './WindowWrapper.css';

const WindowWrapper = ({ id }) => {
  const windowState = useWindowStore((state) => state.windows.find((w) => w.id === id));
  const focusWindow = useWindowStore((state) => state.focusWindow);
  const closeWindow = useWindowStore((state) => state.closeWindow);
  const minimizeWindow = useWindowStore((state) => state.minimizeWindow);
  const toggleMaximize = useWindowStore((state) => state.toggleMaximize);
  const updateWindow = useWindowStore((state) => state.updateWindow);
  
  const windowRef = useRef(null);
  const dragControls = useDragControls();

  // If window not found or minimized, don't render (Taskbar handles restoration)
  if (!windowState || windowState.isMinimized) return null;

  const handlePointerDown = () => {
    focusWindow(id);
  };

  const startDrag = (event) => {
    dragControls.start(event);
  };

  // Determine neon border color based on risk (mock implementation for now)
  const riskColor = windowState.risk === 'high' ? '#ff4757' : windowState.risk === 'medium' ? '#ffc107' : '#00ff88';

  // Component to render inside
  // In a real app, use a component registry logic here
  const InnerComponent = windowState.component;

  return (
    <motion.div
      ref={windowRef}
      className={`window-wrapper ${windowState.id === useWindowStore.getState().activeWindowId ? 'active' : ''}`}
      style={{
        zIndex: windowState.zIndex,
        width: windowState.isMaximized ? '100vw' : windowState.width,
        height: windowState.isMaximized ? 'calc(100vh - 48px)' : windowState.height, // Subtract Taskbar height
        x: windowState.isMaximized ? 0 : windowState.x,
        y: windowState.isMaximized ? 0 : windowState.y,
        '--window-neon-color': riskColor,
        position: windowState.isMaximized ? 'fixed' : 'absolute',
        top: 0,
        left: 0,
      }}
      drag={!windowState.isMaximized}
      dragControls={dragControls}
      dragMomentum={false}
      dragListener={false} // Only drag from header
      onDragEnd={(e, info) => {
        if (!windowState.isMaximized) {
            updateWindow(id, { x: windowState.x + info.offset.x, y: windowState.y + info.offset.y });
        }
      }}
      onPointerDown={handlePointerDown}
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      exit={{ scale: 0.9, opacity: 0 }}
      transition={{ duration: 0.15 }}
    >
      {/* Header / Title Bar */}
      <div 
        className="window-header" 
        onPointerDown={startDrag}
        onDoubleClick={() => toggleMaximize(id)}
      >
        <div className="window-controls">
          <button className="control-btn btn-close" onClick={(e) => { e.stopPropagation(); closeWindow(id); }} aria-label="Close" />
          <button className="control-btn btn-minimize" onClick={(e) => { e.stopPropagation(); minimizeWindow(id); }} aria-label="Minimize" />
          <button className="control-btn btn-maximize" onClick={(e) => { e.stopPropagation(); toggleMaximize(id); }} aria-label="Maximize" />
        </div>
        <span className="window-title">{windowState.title}</span>
        {/* Placeholder for toolbar actions */}
        <div style={{ width: 40 }}></div> 
      </div>

      {/* Content */}
      <div className="window-content">
        {InnerComponent ? <InnerComponent {...windowState.props} /> : <div style={{padding: 20}}>Content Placeholder</div>}
      </div>

      {/* Resize Handles (Only if not maximized) */}
      {!windowState.isMaximized && (
        <ResizeHandles />
      )}
    </motion.div>
  );
};

export default WindowWrapper;
