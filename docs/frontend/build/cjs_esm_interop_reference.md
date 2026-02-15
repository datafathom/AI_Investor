# CJS/ESM Interop — Lessons Learned & Best Practices

> **Last Updated**: 2026-02-14
> **Applies To**: All frontend npm dependencies, Vite build pipeline
> **Key Config**: `vite.config.js` → `optimizeDeps.include`, `build.commonjsOptions`

## The Problem

The JavaScript ecosystem is in a multi-year transition from CommonJS (CJS) to ES Modules (ESM). Many popular npm packages still ship as CJS, while our Vite-powered frontend uses ESM. This causes interoperability issues during both development (where Vite pre-bundles) and production builds (where Rollup bundles).

### How CJS Differs from ESM

| Feature | CommonJS (CJS) | ES Modules (ESM) |
|---------|---------------|-------------------|
| Export | `module.exports = { ... }` | `export const x = ...` |
| Import | `const x = require('...')` | `import { x } from '...'` |
| Default | `module.exports = fn` | `export default fn` |
| Evaluation | Synchronous, at runtime | Static, analyzed at build time |
| Named exports | Dynamic, can't be statically analyzed | Static, Rollup can tree-shake |

## Real-World Issues We've Encountered

### Issue 1: `react-window` — Named Export from CJS

**Package**: `react-window` (ships as CJS via `dist/react-window.js`)

**Symptom**:
```
"FixedSizeList" is not exported by "node_modules/react-window/dist/react-window.js"
```

**Root Cause**: `react-window` v2 renamed `FixedSizeList` to `List`. But even with the correct name, Rollup's static analysis cannot determine named exports from a CJS module.

**Solution**: Use a direct named import and ensure the package is in `optimizeDeps.include`:

```javascript
// ✅ CORRECT — Vite pre-bundles and wraps in ESM
import { List } from 'react-window';

// ❌ WRONG — Rollup can't statically resolve named exports from CJS
import { FixedSizeList } from 'react-window';

// ⚠️ WORKAROUND — Works but bypasses tree-shaking
import * as ReactWindow from 'react-window';
const List = ReactWindow.List || ReactWindow.default?.List;
```

**Config Required**:
```javascript
// vite.config.js
optimizeDeps: {
  include: ['react-window'], // Pre-bundle CJS→ESM during dev
},
build: {
  commonjsOptions: {
    transformMixedEsModules: true, // Handle mixed CJS/ESM in production
  },
},
```

### Issue 2: Service Files — Missing Default Export

**Files**: `researchService.js`, `socialService.js`

**Symptom**:
```
"default" is not exported by "src/services/researchService.js"
```

**Root Cause**: The service file used only a named export (`export const researchService = { ... }`), but the consuming store file used a default import (`import researchService from '../services/researchService'`).

**Solution**: Provide both export styles:

```javascript
// ✅ CORRECT — supports both import styles
export const researchService = { /* ... */ };
export default researchService;

// Consumers can now use either:
import researchService from '../services/researchService';        // default import
import { researchService } from '../services/researchService';   // named import
```

### Issue 3: `react-json-view` — Incompatible Peer Dependencies

**Package**: `react-json-view`

**Symptom**: Installation fails with React 19 peer dependency conflict.

**Root Cause**: `react-json-view` requires React ^17 or ^18.

**Solution**: Don't use it. Replace with inline rendering or a compatible alternative:

```jsx
// ❌ BROKEN with React 19
import ReactJson from 'react-json-view';
<ReactJson src={data} theme="monokai" />

// ✅ REPLACEMENT — inline JSON rendering
<pre className="bg-slate-900 p-4 rounded overflow-auto text-xs text-green-400">
  {JSON.stringify(data, null, 2)}
</pre>
```

**Compatible Alternatives**:
- `react-json-view-lite` — lightweight, supports React 19
- `@microlink/react-json-view` — maintained fork with React 19 support

## Vite Config — CJS/ESM Settings Explained

### `optimizeDeps.include`

Forces Vite to pre-bundle specified packages during dev server startup. This is where CJS→ESM conversion happens for **development mode**.

```javascript
optimizeDeps: {
  include: ['react-window', 'three', /* ... */],
},
```

**When to add a package here**:
- Package ships as CJS (check `node_modules/<pkg>/package.json` for `"type": "module"` — if absent, it's CJS)
- Package has complex nested imports that Vite's auto-detection misses
- You see `Optimized dependencies changed. Reloading...` loops in dev mode

### `build.commonjsOptions.transformMixedEsModules`

Controls how Rollup handles files that mix CJS and ESM syntax during **production builds**.

```javascript
build: {
  commonjsOptions: {
    transformMixedEsModules: true,
  },
},
```

**When to enable**: If any dependency does something like:

```javascript
// Mixed CJS + ESM in the same file
const React = require('react');
export const MyComponent = () => <div />;
```

Without this flag, Rollup's CommonJS plugin will refuse to transform such files.

## Diagnostic Checklist

When you encounter a CJS/ESM interop error, follow this checklist:

### Step 1: Identify the Package Format

```bash
# Check if the package declares ESM
cat node_modules/<package>/package.json | grep '"type"'
# If output is "type": "module" → ESM
# If no output → CJS
```

### Step 2: Check Export Structure

```bash
# View the actual exports
node -e "console.log(Object.keys(require('<package>')))"
```

### Step 3: Add to `optimizeDeps.include` (Dev)

```javascript
// vite.config.js
optimizeDeps: {
  include: ['<package>'],
},
```

### Step 4: Enable `transformMixedEsModules` (Production)

```javascript
// vite.config.js
build: {
  commonjsOptions: {
    transformMixedEsModules: true,
  },
},
```

### Step 5: Use Compatible Import Style

```javascript
// For CJS packages with a single main export:
import pkg from 'package';         // ✅ Default import

// For CJS packages with multiple exports (after pre-bundling):
import { feature } from 'package'; // ✅ Named import (Vite wraps it)

// Avoid namespace imports for CJS in production:
import * as pkg from 'package';    // ⚠️ May fail in Rollup
```

## Golden Rules

1. **Always check `package.json` `"type"` field** before importing a new dependency
2. **Add CJS packages to `optimizeDeps.include`** — it prevents dev mode issues
3. **Enable `transformMixedEsModules`** — it's a safe default with no downside
4. **Prefer named imports** over namespace (`*`) imports for CJS packages
5. **Provide both named and default exports** in your own service/utility files
6. **Never add uninstalled packages to `manualChunks`** — Rollup treats them as entry modules
7. **Check peer dependencies** before installing UI packages — React 19 breaks many older libraries
