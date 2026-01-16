/**
 * Toaster Component
 * 
 * Wrapper for Sonner toast notifications with custom styling.
 */

import React from 'react';
import { Toaster as SonnerToaster } from 'sonner';
import { useColorPalette } from '../hooks/useColorPalette';

function Toaster() {
  const { palette } = useColorPalette();

  return (
    <SonnerToaster
      position="bottom-right"
      toastOptions={{
        style: {
          background: palette?.backgrounds?.card || '#fefae8',
          backdropFilter: 'blur(24px)',
          border: `1px solid ${palette?.borders?.primary || '#5a1520'}`,
          borderRadius: 'var(--radius-card)',
          color: palette?.text?.primary || '#2a0a0f',
          boxShadow: `0 8px 32px 0 ${palette?.shadows?.medium || 'rgba(90, 21, 32, 0.2)'}`,
        },
        classNames: {
          toast: 'sonner-toast',
          title: 'sonner-title',
          description: 'sonner-description',
          actionButton: 'sonner-action-button',
          cancelButton: 'sonner-cancel-button',
        },
      }}
      theme="light"
    />
  );
}

export default Toaster;

