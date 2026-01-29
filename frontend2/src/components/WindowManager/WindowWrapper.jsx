import React, { useRef, useEffect, useMemo } from 'react';
import { useShallow } from 'zustand/react/shallow';
import { motion, useDragControls } from 'framer-motion';
import useWindowStore from '../../stores/windowStore';
import ResizeHandles from './ResizeHandles';
import useWindowSnapshot from '../../hooks/useWindowSnapshot';
import './WindowWrapper.css';

/**
 * Sub-component to handle periodic snapshots for active windows
 */
const SnapshotEffect = React.memo(({ id, elementRef, active }) => {
    const { captureSnapshot } = useWindowSnapshot();
    
    useEffect(() => {
        if (!active) return;
        
        // Take an initial snapshot when window becomes active
        captureSnapshot(id, elementRef.current);
        
        // Setup periodic snapshotting (every 60 seconds)
        const interval = setInterval(() => {
            captureSnapshot(id, elementRef.current);
        }, 60000);
        
        return () => clearInterval(interval);
    }, [id, active, captureSnapshot, elementRef]);
    
    return null;
});

const WindowWrapper = ({ id }) => {
  // Use useShallow and granular selectors to prevent broad re-renders
  const windowState = useWindowStore(useShallow((state) => 
    state.windows.find((w) => w.id === id)
  ));
  
  // Only re-render when THIS window's active status changes
  const isActive = useWindowStore((state) => state.activeWindowId === id);
  
  // Select individual actions to ensure stability and avoid subscribing to the whole store
  const focusWindow = useWindowStore((state) => state.focusWindow);
  const closeWindow = useWindowStore((state) => state.closeWindow);
  const minimizeWindow = useWindowStore((state) => state.minimizeWindow);
  const toggleMaximize = useWindowStore((state) => state.toggleMaximize);
  const updateWindow = useWindowStore((state) => state.updateWindow);
  
  const windowRef = useRef(null);
  const dragControls = useDragControls();
  const { captureSnapshot } = useWindowSnapshot();

  // If window not found or minimized, don't render
  if (!windowState || windowState.isMinimized) return null;

  const handlePointerDown = (e) => {
    focusWindow(id);
  };

  const startDrag = (event) => {
    dragControls.start(event);
  };

  const riskColor = windowState.risk === 'high' ? '#ff4757' : windowState.risk === 'medium' ? '#ffc107' : '#00ff88';

  const InnerComponent = windowState.component;

  return (
    <motion.div
      ref={windowRef}
      className={`window-wrapper ${isActive ? 'active' : ''}`}
      style={{
        zIndex: windowState.zIndex,
        width: windowState.isMaximized ? '100vw' : windowState.width,
        height: windowState.isMaximized ? 'calc(100vh - 48px)' : windowState.height,
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
      dragListener={false}
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
      <SnapshotEffect id={id} elementRef={windowRef} active={isActive} />
      
      <div 
        className="window-header" 
        onPointerDown={startDrag}
        onDoubleClick={() => toggleMaximize(id)}
      >
        <div className="window-controls">
          <button className="control-btn btn-close" onClick={(e) => { e.stopPropagation(); closeWindow(id); }} aria-label="Close" />
          <button className="control-btn btn-minimize" onClick={async (e) => { 
              e.stopPropagation(); 
              await captureSnapshot(id, windowRef.current);
              minimizeWindow(id); 
          }} aria-label="Minimize" />
          <button className="control-btn btn-maximize" onClick={(e) => { e.stopPropagation(); toggleMaximize(id); }} aria-label="Maximize" />
        </div>
        <span className="window-title">{windowState.title}</span>
        <div style={{ width: 40 }}></div> 
      </div>

      <div className="window-content">
        {InnerComponent ? <InnerComponent {...windowState.props} /> : <div style={{padding: 20}}>Content Placeholder</div>}
      </div>

      {!windowState.isMaximized && (
        <ResizeHandles />
      )}
    </motion.div>
  );
};

export default React.memo(WindowWrapper);
