/**
 * Shell Layout Component
 * 
 * Main application shell with collapsible sidebar, command palette, and routing.
 * Implements the "Shell Architecture" pattern for internal tools.
 */

import React, { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useColorPalette } from '../../hooks/useColorPalette';
import Sidebar from './Sidebar';
import CommandPalette from './CommandPalette';
import PageHeader from './PageHeader';
import Toaster from '../Toaster';
import '../../App.css';

function Shell() {
  const { palette } = useColorPalette();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);
  const location = useLocation();

  // Keyboard shortcuts
  React.useEffect(() => {
    const handleKeyDown = (e) => {
      // Cmd+K or Ctrl+K to open command palette
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen((prev) => !prev);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <div 
      className="shell-container" 
      style={{ 
        display: 'flex', 
        height: '100vh', 
        width: '100vw',
        overflow: 'hidden',
        position: 'relative'
      }}
    >
      {/* Sidebar */}
      <Sidebar 
        collapsed={sidebarCollapsed} 
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Main Content Area */}
      <div 
        className="shell-main"
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          marginLeft: sidebarCollapsed ? '80px' : '280px',
          transition: 'margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          minWidth: 0, // Critical: prevents flex item from overflowing
          width: '100%', // Ensure it takes available space
        }}
      >
        {/* Page Header with Breadcrumbs */}
        <div style={{ flexShrink: 0 }}>
          <PageHeader />
        </div>

        {/* Page Content */}
        <main 
          className="shell-content"
          style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            overflowY: 'auto',
            overflowX: 'hidden',
            padding: '2rem',
            backgroundColor: palette?.backgrounds?.main || '#fffef0',
            minHeight: 0, // Critical: allows flex child to shrink below content size
            width: '100%',
          }}
        >
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ 
                duration: 0.3,
                ease: [0.4, 0, 0.2, 1] // Custom easing for smooth feel
              }}
              style={{
                width: '100%',
                minHeight: '100%', // Ensure it fills parent
                display: 'flex',
                flexDirection: 'column',
              }}
            >
              <Outlet />
            </motion.div>
          </AnimatePresence>
        </main>
      </div>

      {/* Command Palette */}
      <CommandPalette 
        open={commandPaletteOpen}
        onOpenChange={setCommandPaletteOpen}
      />

      {/* Toast Notifications */}
      <Toaster />
    </div>
  );
}

export default Shell;

