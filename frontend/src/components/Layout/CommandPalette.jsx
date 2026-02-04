/**
 * Command Palette Component
 * 
 * Cmd+K command palette inspired by Vercel/Linear.
 * Uses cmdk library for keyboard navigation.
 */

import React, { useEffect } from 'react';
import { Command } from 'cmdk';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { useColorPalette } from '../../hooks/useColorPalette';

const commands = [
  {
    id: 'dashboard',
    label: 'Go to Dashboard',
    icon: '',
    path: '/dashboard',
    keywords: ['dashboard', 'home', 'overview'],
  },
  {
    id: 'chat',
    label: 'Open Chat',
    icon: '',
    path: '/chat',
    keywords: ['chat', 'messages', 'socket'],
  },
  {
    id: 'telemetry',
    label: 'View Telemetry',
    icon: '',
    path: '/telemetry',
    keywords: ['telemetry', 'metrics', 'stats'],
  },
  {
    id: 'design-system',
    label: 'Design System Playground',
    icon: '',
    path: '/design-system',
    keywords: ['design', 'components', 'playground'],
  },
  {
    id: 'settings',
    label: 'Open Settings',
    icon: '',
    path: '/settings',
    keywords: ['settings', 'config', 'preferences'],
  },
];

function CommandPalette({ open, onOpenChange }) {
  const navigate = useNavigate();
  const { palette } = useColorPalette();
  const [search, setSearch] = React.useState('');

  useEffect(() => {
    if (open) {
      setSearch('');
    }
  }, [open]);

  const handleSelect = (path) => {
    navigate(path);
    onOpenChange(false);
  };

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => onOpenChange(false)}
            style={{
              position: 'fixed',
              inset: 0,
              backgroundColor: 'rgba(0, 0, 0, 0.5)',
              backdropFilter: 'blur(4px)',
              zIndex: 1000,
            }}
          />

          {/* Command Palette */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.2 }}
            style={{
              position: 'fixed',
              top: '20%',
              left: '50%',
              transform: 'translateX(-50%)',
              width: '90%',
              maxWidth: '640px',
              zIndex: 1001,
            }}
          >
            <Command
              style={{
                backgroundColor: palette?.backgrounds?.card || '#fefae8',
                backdropFilter: 'blur(24px)',
                border: `1px solid ${palette?.borders?.primary || '#5a1520'}`,
                borderRadius: 'var(--radius-card)',
                boxShadow: `0 8px 32px 0 ${palette?.shadows?.dark || 'rgba(61, 14, 21, 0.3)'}`,
                overflow: 'hidden',
              }}
            >
              <Command.Input
                placeholder="Type a command or search..."
                value={search}
                onValueChange={setSearch}
                style={{
                  width: '100%',
                  padding: '1rem 1.5rem',
                  border: 'none',
                  borderBottom: `1px solid ${palette?.borders?.secondary || '#ddd4a8'}`,
                  backgroundColor: 'transparent',
                  fontSize: '1rem',
                  color: palette?.text?.primary || '#2a0a0f',
                  outline: 'none',
                }}
              />
              <Command.List
                style={{
                  maxHeight: '400px',
                  overflowY: 'auto',
                  padding: '0.5rem',
                }}
              >
                <Command.Empty
                  style={{
                    padding: '2rem',
                    textAlign: 'center',
                    color: palette?.text?.secondary || '#5a4a3a',
                  }}
                >
                  No results found.
                </Command.Empty>
                {commands.map((cmd) => (
                  <Command.Item
                    key={cmd.id}
                    value={`${cmd.label} ${cmd.keywords.join(' ')}`}
                    onSelect={() => handleSelect(cmd.path)}
                    style={{
                      padding: '0.75rem 1rem',
                      borderRadius: 'var(--radius-chip)',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.75rem',
                      color: palette?.text?.primary || '#2a0a0f',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.backgroundColor =
                        palette?.backgrounds?.hover || '#faf5d8';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.backgroundColor = 'transparent';
                    }}
                  >
                    <span style={{ fontSize: '1.25rem' }}>{cmd.icon}</span>
                    <span style={{ fontWeight: 500 }}>{cmd.label}</span>
                  </Command.Item>
                ))}
              </Command.List>
            </Command>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

export default CommandPalette;

