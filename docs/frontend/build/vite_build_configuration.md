# Vite Build Configuration — Reference & Known Issues

> **Last Updated**: 2026-02-14
> **Config File**: `Frontend/vite.config.js`
> **Vite Version**: 5.4.21
> **Node Version**: 23.9.0

## Overview

The frontend build is powered by Vite 5, configured with React plugin support, a custom color palette plugin, development server proxying, and production build optimization. This document covers the configuration decisions, known issues that have been resolved, and guidelines for avoiding future build failures.

## Configuration Breakdown

### Plugins

```javascript
plugins: [
  react(),              // @vitejs/plugin-react for JSX/Fast Refresh
  colorPalettePlugin(), // Custom plugin — see below
],
```

#### Color Palette Plugin

A custom Vite plugin that reads `config/color_palette.json` and exposes it as a virtual module:

```javascript
import palette from 'virtual:color-palette';
const primaryColor = palette.burgundy.primary;
```

This enables centralized color management — update the JSON file once and all components pick it up. The plugin supports HMR, so color changes reflect instantly in dev mode.

### Path Aliases

```javascript
resolve: {
  alias: {
    'three/webgpu': resolve(__dirname, 'node_modules/three/build/three.webgpu.js'),
    'three': resolve(__dirname, 'node_modules/three'),
    '@': resolve(__dirname, './src')
  }
}
```

| Alias | Resolves To | Purpose |
|-------|------------|---------|
| `@` | `./src` | Standard shadcn/ui import convention (`@/components/ui/button`) |
| `three` | `node_modules/three` | Pin Three.js resolution to avoid dependency conflicts |
| `three/webgpu` | `three/build/three.webgpu.js` | WebGPU build variant for 3D visualizations |

### Dependency Optimization

```javascript
optimizeDeps: {
  include: [
    'react-window', 'three', '@react-three/fiber', '@react-three/drei',
    'react-force-graph-3d', '3d-force-graph', 'three-render-objects',
    'react-kapsule', 'three-forcegraph', 'ngraph.forcelayout', 'ngraph.events'
  ],
},
```

The `optimizeDeps.include` list forces Vite to pre-bundle these packages during dev startup. This is necessary because:

- **`react-window`** — CommonJS module that needs CJS→ESM conversion
- **Three.js ecosystem** — Complex dependency tree with nested imports that Vite's auto-detection misses
- **ngraph packages** — CommonJS modules used by the force graph visualizer

### CJS/ESM Interop

```javascript
build: {
  commonjsOptions: {
    transformMixedEsModules: true,
  },
},
```

**Why this exists**: Some npm packages mix CommonJS and ESM syntax in the same file. Without this flag, Rollup's CommonJS plugin may fail to convert them, causing build errors like `"default" is not exported`. The `transformMixedEsModules: true` flag tells the plugin to handle these hybrid files gracefully.

### Manual Chunk Splitting

```javascript
rollupOptions: {
  output: {
    manualChunks: {
      'react-vendor': ['react', 'react-dom', 'react-router-dom'],
      'ui-vendor': ['lucide-react', 'framer-motion'],
    },
  },
},
```

**Critical Rule**: Only list packages that are **actually installed** in `package.json`. If a package is listed in `manualChunks` but not installed, Rollup will fail with `Could not resolve entry module "package-name"`.

### Development Server

```javascript
server: {
  port: parseInt(process.env.VITE_PORT || process.env.PORT || '5173'),
  host: '127.0.0.1',  // SECURITY: Never use 0.0.0.0
  proxy: {
    '/api': {
      target: `http://127.0.0.1:${process.env.BACKEND_PORT || '5050'}`,
      changeOrigin: true,
      secure: false,
    },
    '/ws': { /* WebSocket proxy */ },
    '/socket.io': { /* Socket.io proxy */ },
  },
},
```

The dev server binds to `127.0.0.1` (never `0.0.0.0`) and proxies API calls to the backend on port 5050 by default.

## Important Constraints

These are rules the team must follow to avoid build failures:

| Rule | Why |
|------|-----|
| Only list **installed** packages in `manualChunks` | Rollup treats missing packages as entry modules and fails |
| Add CJS packages to `optimizeDeps.include` | Prevents CJS→ESM conversion failures in dev mode |
| Service files must export both named **and** default | Stores use default imports; direct consumers use named |
| Use `{ List }` from `react-window`, not `FixedSizeList` | v2 renamed the export |
| Escape `>` as `&gt;` in JSX text content | Vite treats unescaped `>` as a warning/error |
| Every `@/components/ui/*` import must have a real file | Shadcn/ui components are source-owned, not from npm (see `docs/frontend/components/`) |
| Verify React peer deps before installing UI packages | React 19 breaks many older libraries (e.g., `react-json-view`) |

## Build Verification Checklist

When making changes that could affect the build:

1. **Run `npx vite build`** — capture output to a file with `*>&1 | Out-File -FilePath build_output.txt -Encoding utf8`
2. **Check module count** — a successful build shows `✓ XXXX modules transformed`
3. **Check for warnings** — JSX warnings, unused exports, circular dependencies
4. **Verify `dist/` output** — ~1100+ files expected in a full production build
5. **If adding npm packages** — verify they're in `package.json`, check for peer dependency conflicts

## Build Performance

| Metric | Current Value |
|--------|--------------|
| Modules transformed | 6,123 |
| Build time | ~60 seconds |
| Output files | ~1,103 |
| Sourcemaps | Enabled |
