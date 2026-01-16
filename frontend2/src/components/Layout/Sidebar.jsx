/**
 * Collapsible Sidebar Component
 * 
 * Glassmorphic sidebar with smooth expand/collapse animations.
 * Uses framer-motion for fluid transitions.
 */

import React from 'react';
import { NavLink } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useColorPalette } from '../../hooks/useColorPalette';

const navigationItems = [
  { path: '/dashboard', icon: '📊', label: 'Dashboard', description: 'Overview & status' },
  { path: '/chat', icon: '💬', label: 'Chat', description: 'Socket.io realtime' },
  { path: '/telemetry', icon: '📈', label: 'Telemetry', description: 'Server metrics' },
  { path: '/design-system', icon: '🎨', label: 'Design System', description: 'Component playground' },
  { path: '/settings', icon: '⚙️', label: 'Settings', description: 'Configuration' },
];

function Sidebar({ collapsed, onToggle }) {
  const { palette } = useColorPalette();

  return (
    <motion.aside
      className="sidebar"
      initial={false}
      animate={{
        width: collapsed ? 80 : 280,
      }}
      transition={{
        duration: 0.3,
        ease: [0.4, 0, 0.2, 1],
      }}
      style={{
        position: 'fixed',
        left: 0,
        top: 0,
        height: '100vh',
        width: collapsed ? '80px' : '280px', // Explicit width
        flexShrink: 0, // Prevent sidebar from shrinking
        backgroundColor: collapsed 
          ? `${palette?.backgrounds?.card || '#fefae8'}cc` // More transparent when collapsed
          : `${palette?.backgrounds?.card || '#fefae8'}f5`, // More opaque when expanded
        backdropFilter: 'blur(24px) saturate(180%)',
        WebkitBackdropFilter: 'blur(24px) saturate(180%)', // Safari support
        borderRight: `1px solid ${palette?.borders?.primary || '#5a1520'}40`, // Semi-transparent border
        boxShadow: `0 8px 32px 0 ${palette?.shadows?.light || 'rgba(90, 21, 32, 0.15)'}`,
        zIndex: 100,
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
      }}
    >
      {/* Sidebar Header */}
      <div
        style={{
          padding: '1.5rem',
          borderBottom: `1px solid ${palette?.borders?.secondary || '#ddd4a8'}`,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
        }}
      >
        <AnimatePresence mode="wait">
          {!collapsed && (
            <motion.h2
              key="title"
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -10 }}
              transition={{ duration: 0.2 }}
              style={{
                margin: 0,
                fontSize: '1.25rem',
                fontWeight: 700,
                color: palette?.burgundy?.primary || '#5a1520',
              }}
            >
              Burgundy App
            </motion.h2>
          )}
        </AnimatePresence>
        <button
          onClick={onToggle}
          style={{
            background: 'transparent',
            border: 'none',
            cursor: 'pointer',
            padding: '0.5rem',
            borderRadius: '6px',
            color: palette?.burgundy?.primary || '#5a1520',
            fontSize: '1.25rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'background 0.2s',
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = palette?.backgrounds?.hover || '#faf5d8';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'transparent';
          }}
          aria-label={collapsed ? 'Expand sidebar' : 'Collapse sidebar'}
        >
          {collapsed ? '→' : '←'}
        </button>
      </div>

      {/* Navigation Items */}
      <nav
        style={{
          flex: 1,
          padding: '1rem 0',
          overflowY: 'auto',
        }}
      >
        {navigationItems.map((item) => (
          <SidebarNavItem
            key={item.path}
            item={item}
            collapsed={collapsed}
            palette={palette}
          />
        ))}
      </nav>

      {/* Sidebar Footer */}
      <div
        style={{
          padding: '1rem 1.5rem',
          borderTop: `1px solid ${palette?.borders?.secondary || '#ddd4a8'}`,
          fontSize: '0.75rem',
          color: palette?.text?.secondary || '#5a4a3a',
          textAlign: collapsed ? 'center' : 'left',
        }}
      >
        <AnimatePresence mode="wait">
          {!collapsed ? (
            <motion.div
              key="footer-text"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              v1.0.0
            </motion.div>
          ) : (
            <motion.div
              key="footer-icon"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              v1
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.aside>
  );
}

function SidebarNavItem({ item, collapsed, palette }) {
  return (
    <NavLink
      to={item.path}
      style={({ isActive }) => ({
        display: 'flex',
        alignItems: 'center',
        padding: '0.75rem 1.5rem',
        color: isActive
          ? palette?.burgundy?.primary || '#5a1520'
          : palette?.text?.primary || '#2a0a0f',
        textDecoration: 'none',
        position: 'relative',
        transition: 'background 0.2s',
        backgroundColor: isActive
          ? palette?.backgrounds?.hover || '#faf5d8'
          : 'transparent',
      })}
      title={collapsed ? item.label : undefined}
    >
      {({ isActive }) => (
        <>
          {/* Active Indicator */}
          {isActive && (
            <motion.div
              layoutId="activeIndicator"
              style={{
                position: 'absolute',
                left: 0,
                top: 0,
                bottom: 0,
                width: '4px',
                backgroundColor: palette?.burgundy?.primary || '#5a1520',
                borderRadius: '0 4px 4px 0',
              }}
              transition={{
                type: 'spring',
                stiffness: 500,
                damping: 30,
              }}
            />
          )}

          {/* Icon */}
          <span style={{ fontSize: '1.25rem', marginRight: collapsed ? 0 : '0.75rem' }}>
            {item.icon}
          </span>

          {/* Label & Description */}
          <AnimatePresence mode="wait">
            {!collapsed && (
              <motion.div
                key="label"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                transition={{ duration: 0.2 }}
                style={{ flex: 1 }}
              >
                <div style={{ fontWeight: 600, fontSize: '0.875rem' }}>
                  {item.label}
                </div>
                <div
                  style={{
                    fontSize: '0.75rem',
                    opacity: 0.7,
                    marginTop: '0.125rem',
                  }}
                >
                  {item.description}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </>
      )}
    </NavLink>
  );
}

export default Sidebar;

