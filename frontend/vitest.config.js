import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import { readFileSync, existsSync } from 'fs';

// Color palette plugin for tests
function colorPalettePlugin() {
  const virtualModuleId = 'virtual:color-palette';
  const resolvedVirtualModuleId = '\0' + virtualModuleId;
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
          if (!existsSync(palettePath)) {
            return `export const palette = {}; export default palette;`;
          }
          const paletteData = JSON.parse(readFileSync(palettePath, 'utf-8'));
          const palette = paletteData.palette || {};
          return `export const palette = ${JSON.stringify(palette, null, 2)}; export default palette;`;
        } catch (error) {
          return `export const palette = {}; export default palette;`;
        }
      }
    },
  };
}

export default defineConfig({
  plugins: [react(), colorPalettePlugin()],
  test: {
    globals: true,
    environment: 'jsdom',
    setupFiles: ['./tests/setup.js'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'tests/',
        '*.config.js',
        'dist/',
      ],
    },
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  },
});

