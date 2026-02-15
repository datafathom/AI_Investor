# Frontend State Management

> **Last Updated**: 2026-02-14
> **Stack**: Zustand stores + React Context API

## Overview

The Sovereign OS frontend uses a hybrid state management approach:

- **Zustand stores** for domain-specific data (portfolios, research, social, market data)
- **React Context API** for cross-cutting concerns (authentication, theme, notifications)

## Zustand Stores

Store files live in `Frontend/src/stores/` and follow a consistent pattern:

```javascript
import { create } from 'zustand';
import serviceModule from '../services/serviceName';

const useServiceStore = create((set, get) => ({
  data: null,
  loading: false,
  error: null,

  fetchData: async () => {
    set({ loading: true, error: null });
    try {
      const result = await serviceModule.getData();
      set({ data: result, loading: false });
    } catch (error) {
      set({ error: error.message, loading: false });
    }
  },
}));

export default useServiceStore;
```

### Active Stores

| Store | Service | Domain |
|-------|---------|--------|
| `researchStore.js` | `researchService.js` | Research data & analysis |
| `socialStore.js` | `socialService.js` | Social sentiment & feeds |

### Import Convention

Stores import services using **default imports**:

```javascript
import researchService from '../services/researchService';
```

All service files must provide both named and default exports to support this pattern:

```javascript
export const researchService = { /* ... */ };
export default researchService;
```

## React Context

Context providers live in `Frontend/src/context/` and wrap the app in `App.jsx`:

- **AuthContext** — Current user, login state, token management
- **ThemeContext** — Dark mode, color palette from `virtual:color-palette`

## Service Layer

API services in `Frontend/src/services/` communicate with the FastAPI backend. All requests go through `apiClient.js` which handles:

- Base URL configuration (proxied via Vite to port 5050)
- JWT token attachment
- Error response normalization

```javascript
import apiClient from './apiClient';

export const researchService = {
  getAnalysis: (symbol) => apiClient.get(`/api/v1/research/${symbol}`),
  runBacktest: (params) => apiClient.post('/api/v1/research/backtest', params),
};

export default researchService;
```

## Data Flow

```
Component (useServiceStore hook)
    │
    ├── Reads: store.data, store.loading, store.error
    │
    └── Calls: store.fetchData()
                 │
                 └── Service function (apiClient.get/post)
                          │
                          └── Vite proxy → FastAPI backend
```
