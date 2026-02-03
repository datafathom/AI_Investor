/**
 * Vite Configuration
 * 
 * This configuration sets up Vite for React development with:
 * - React plugin support
 * - Color palette integration (loads config/color_palette.json at build time)
 * - Development server with proxy for API calls
 * - Production build optimization
 * 
 * The color palette plugin allows the app to use colors from config/color_palette.json
 * without hardcoding any color values. Update the palette file and rebuild to change
 * colors across all apps.
 */

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { readFileSync, existsSync } from 'fs';
import { resolve } from 'path';

// ============================================================================
// COLOR PALETTE PLUGIN
// ============================================================================
/**
 * Vite plugin to inject color palette at build time
 * 
 * This plugin reads config/color_palette.json from the project root
 * and makes it available as a virtual module 'virtual:color-palette'
 * that can be imported in React components.
 * 
 * Usage in React:
 *   import palette from 'virtual:color-palette';
 *   const primaryColor = palette.burgundy.primary;
 */
function colorPalettePlugin() {
  const virtualModuleId = 'virtual:color-palette';
  const resolvedVirtualModuleId = virtualModuleId;

  // Calculate the palette path once
  const palettePath = resolve(__dirname, 'config/color_palette.json');

  return {
    name: 'color-palette-plugin',

    resolveId(id) {
      if (id === virtualModuleId) {
        return resolvedVirtualModuleId;
      }
    },

    load(id) {
      if (id === resolvedVirtualModuleId) {
        try {
          // Check if file exists
          if (!existsSync(palettePath)) {
            console.warn(`[Color Palette] File not found: ${palettePath}`);
            console.warn(`[Color Palette] Using fallback empty palette.`);
            return `export const palette = {};
export default palette;`;
          }

          // Read and parse the palette file
          const paletteData = JSON.parse(readFileSync(palettePath, 'utf-8'));
          const palette = paletteData.palette || {};

          // Export the palette as a module
          return `export const palette = ${JSON.stringify(palette)};
export default palette;`;
        } catch (error) {
          return `export const palette = {};
export default palette;`;
        }
      }
    },

    // Watch the palette file for changes in dev mode
    configureServer(server) {
      server.watcher.add(palettePath);
      server.watcher.on('change', (file) => {
        if (file === palettePath) {
          console.log(`[Color Palette] File changed, reloading...`);
          // Invalidate the virtual module to trigger a reload
          const module = server.moduleGraph.getModuleById(resolvedVirtualModuleId);
          if (module) {
            server.moduleGraph.invalidateModule(module);
          }
        }
      });
    },

    // Handle HMR (Hot Module Replacement) for the palette
    handleHotUpdate({ file, server }) {
      if (file === palettePath) {
        console.log(`[Color Palette] Hot reloading palette...`);
        const module = server.moduleGraph.getModuleById(resolvedVirtualModuleId);
        if (module) {
          server.moduleGraph.invalidateModule(module);
          return [module];
        }
      }
    },
  };
}

// ============================================================================
// VITE CONFIGURATION
// ============================================================================
export default defineConfig({
  plugins: [
    react(),
    colorPalettePlugin(), // Enable color palette integration
  ],

  // Optimize dependencies for better performance
  optimizeDeps: {
    include: ['react-window', 'three', '@react-three/fiber', '@react-three/drei'],
  },

  resolve: {
    alias: {
      'three': resolve(__dirname, 'node_modules/three')
    }
  },

  // Development server configuration
  server: {
    // Port for the Vite dev server (can be overridden via VITE_PORT env var)
    port: parseInt(process.env.VITE_PORT || process.env.PORT || '5173'),

    // Ensure the server is only accessible locally (not on WAN)
    host: '127.0.0.1',

    // Proxy configuration for API calls
    // This forwards requests to /api/* to the Express backend
    proxy: {
      '/api': {
        // Target the Express backend server
        // BACKEND_PORT is set by run_nodeApps.py when starting the server
        target: `http://127.0.0.1:${process.env.BACKEND_PORT || '5050'}`,
        changeOrigin: true,
        secure: false,
      },
      // Socket.io WebSocket proxy
      '/socket.io': {
        target: `http://127.0.0.1:${process.env.BACKEND_PORT || '5050'}`,
        ws: true, // Enable WebSocket proxying
        changeOrigin: true,
      },
    },
  },

  // Production build configuration
  build: {
    outDir: 'dist',
    sourcemap: true, // Generate source maps for debugging
    rollupOptions: {
      output: {
        manualChunks: {
          // Split vendor chunks for better caching
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'chart-vendor': ['recharts', 'chart.js', 'react-chartjs-2'],
          'ui-vendor': ['lucide-react', 'framer-motion'],
        },
      },
    },
  },

  // Base path for assets (use '/' for root)
  base: '/',
});

