/**
 * useColorPalette Hook
 * 
 * React hook to load and apply the color palette from config/color_palette.json.
 * The palette is loaded at build time via Vite's virtual module system.
 * 
 * This hook:
 * 1. Imports the palette data (loaded at build time)
 * 2. Applies colors as CSS variables to the document root
 * 3. Returns the palette object for programmatic access
 * 
 * Usage:
 *   const { palette } = useColorPalette();
 *   const primaryColor = palette.burgundy.primary;
 * 
 * CSS variables are automatically available:
 *   background-color: var(--color-burgundy-primary);
 */

import { useEffect } from 'react';
import { getColorPalette, applyColorPalette } from '../utils/colorPalette';

/**
 * React hook to apply color palette (loaded at build time)
 * @returns {Object} { palette } - The color palette object
 */
export function useColorPalette() {
  useEffect(() => {
    // Palette is loaded at build time, just apply it
    const palette = getColorPalette();
    applyColorPalette(palette);
  }, []);

  return { palette: getColorPalette() };
}

