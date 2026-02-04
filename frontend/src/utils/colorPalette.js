/**
 * Color Palette Utility
 * 
 * Loads color palette from config/color_palette.json at build time
 * and provides utilities to apply it to the application via CSS variables.
 * 
 * This allows all apps to share the same color scheme by updating
 * a single config/color_palette.json file.
 */

// Import palette at build time via Vite virtual module
// This is provided by the colorPalettePlugin in vite.config.js
import paletteData from 'virtual:color-palette';

/**
 * Get the color palette (loaded at build time)
 * @returns {Object} Color palette object
 */
export function getColorPalette() {
  return paletteData;
}

/**
 * Apply color palette to CSS variables on the document root
 * This makes all colors available as CSS variables throughout the app
 * 
 * @param {Object} palette - Color palette object
 */
export function applyColorPalette(palette) {
  const root = document.documentElement;
  
  // Apply burgundy colors
  if (palette.burgundy) {
    Object.entries(palette.burgundy).forEach(([key, value]) => {
      root.style.setProperty(`--color-burgundy-${key}`, value);
    });
  }
  
  // Apply cream colors
  if (palette.cream) {
    Object.entries(palette.cream).forEach(([key, value]) => {
      root.style.setProperty(`--color-cream-${key}`, value);
    });
  }
  
  // Apply text colors
  if (palette.text) {
    Object.entries(palette.text).forEach(([key, value]) => {
      root.style.setProperty(`--color-text-${key}`, value);
    });
  }
  
  // Apply background colors
  if (palette.backgrounds) {
    Object.entries(palette.backgrounds).forEach(([key, value]) => {
      root.style.setProperty(`--color-bg-${key}`, value);
    });
  }
  
  // Apply border colors
  if (palette.borders) {
    Object.entries(palette.borders).forEach(([key, value]) => {
      root.style.setProperty(`--color-border-${key}`, value);
    });
  }
  
  // Apply shadow colors
  if (palette.shadows) {
    Object.entries(palette.shadows).forEach(([key, value]) => {
      root.style.setProperty(`--color-shadow-${key}`, value);
    });
  }
}

/**
 * Get a color value from the palette
 * @param {Object} palette - Color palette object (optional, uses default if not provided)
 * @param {string} category - Color category (e.g., 'burgundy', 'cream')
 * @param {string} key - Color key within category (e.g., 'primary', 'dark')
 * @returns {string} Color value
 * @throws {Error} If color not found
 */
export function getColor(category, key, palette = null) {
  const paletteToUse = palette || getColorPalette();
  const value = paletteToUse[category]?.[key];
  if (!value) {
    throw new Error(
      `Color '${category}.${key}' not found in palette. ` +
      `Available categories: ${Object.keys(paletteToUse).join(', ')}`
    );
  }
  return value;
}

