# Services Documentation

## Overview

Services are core business logic modules that handle state management, API communication, and system operations.

## Window Management

### windowManager

Centralized service for managing window state.

**Location:** `src/services/windowManager.js`

**Methods:**

```javascript
// Register a new window
const window = windowManager.registerWindow({
  id: 'window-id',
  title: 'Window Title',
  component: 'ComponentName',
  size: { width: 800, height: 600 },
  position: { x: 100, y: 100 }
});

// Get all windows
const windows = windowManager.getAllWindows();

// Get specific window
const window = windowManager.getWindow('window-id');

// Window operations
windowManager.minimizeWindow('window-id');
windowManager.maximizeWindow('window-id');
windowManager.restoreWindow('window-id');
windowManager.closeWindow('window-id');
windowManager.bringToFront('window-id');

// Layout management
windowManager.saveLayout('layout-name');
windowManager.loadLayout('layout-name');
windowManager.deleteLayout('layout-name');

// Snap zones
windowManager.toggleSnapZones();
windowManager.snapWindow('window-id', 'top-left');
```

**Events:**
- `window:registered` - Window registered
- `window:closed` - Window closed
- `window:state-changed` - Window state changed
- `layout:saved` - Layout saved

## Widget System

### WidgetRegistry

Manages widget registration and lifecycle.

**Location:** `src/core/WidgetRegistry.js`

**Methods:**

```javascript
// Register a widget
widgetRegistry.register({
  id: 'widget-id',
  name: 'Widget Name',
  component: WidgetComponent,
  description: 'Widget description',
  version: '1.0.0',
  dependencies: ['other-widget']
});

// Get all widgets
const widgets = widgetRegistry.getAll();

// Get specific widget
const widget = widgetRegistry.get('widget-id');

// Search widgets
const results = widgetRegistry.search('search term');

// Install/uninstall
widgetRegistry.install('widget-id');
widgetRegistry.uninstall('widget-id');

// Check dependencies
const check = widgetRegistry.checkDependencies('widget-id');
```

## Permission System

### permissionService

Handles permission checking and caching.

**Location:** `src/services/permissionService.js`

**Methods:**

```javascript
// Check if user has permission
const hasPermission = await permissionService.checkPermission(
  userId,
  'widget',
  'read'
);

// Get all user permissions
const permissions = await permissionService.getUserPermissions(userId);

// Get user roles
const roles = await permissionService.getUserRoles(userId);

// Clear cache
permissionService.clearCache();
```

**Caching:**
- Permissions are cached for 5 minutes
- Cache key: `permission:${userId}:${resource}:${action}`

## Theme System

### ThemeEngine

Manages themes and design tokens.

**Location:** `src/themes/ThemeEngine.js`

**Methods:**

```javascript
// Get theme engine instance
const themeEngine = ThemeEngine.getInstance();

// Get current theme
const theme = themeEngine.getCurrentTheme();

// Set theme
themeEngine.setTheme('dark');

// Update theme
themeEngine.updateTheme({
  colors: {
    primary: '#ff0000'
  }
});

// Get all themes
const themes = themeEngine.getThemes();

// Export theme
const themeJson = themeEngine.exportTheme('theme-name');

// Import theme
themeEngine.importTheme(themeJson);
```

**Events:**
- `theme:changed` - Theme changed
- `theme:updated` - Theme updated

## Sync Service

### syncService

Handles data synchronization and offline support.

**Location:** `src/services/syncService.js`

**Methods:**

```javascript
// Queue an action for sync
const actionId = syncService.queueAction({
  type: 'save',
  endpoint: '/api/data',
  method: 'POST',
  data: { key: 'value' }
});

// Process queue
await syncService.processQueue();

// Get queue status
const status = syncService.getQueueStatus();
// Returns: { length, isOnline, isSyncing }

// Clear queue
syncService.clearQueue();
```

**Events:**
- `online` - Connection restored
- `offline` - Connection lost
- `action:queued` - Action queued
- `sync:started` - Sync started
- `sync:completed` - Sync completed
- `queue:cleared` - Queue cleared

## Presence Service

### presenceService

Tracks user presence and activity.

**Location:** `src/services/presenceService.js`

**Methods:**

```javascript
// Initialize presence
presenceService.initialize(userId, username);

// Update activity
presenceService.updateActivity('dashboard', 'viewing');

// Get online users
const users = presenceService.getOnlineUsers();

// Get specific user
const user = presenceService.getUser(userId);

// Disconnect
presenceService.disconnect();
```

**Events:**
- `presence:updated` - User presence updated
- `presence:user-joined` - User joined
- `presence:user-left` - User left
- `presence:list-updated` - User list updated

## State Store

### useStore (Zustand)

Global state management.

**Location:** `src/store/store.js`

**Usage:**

```javascript
import { useStore } from '../store/store';

function MyComponent() {
  const user = useStore(state => state.user);
  const setUser = useStore(state => state.setUser);
  const notifications = useStore(state => state.notifications);
  const addNotification = useStore(state => state.addNotification);
  
  // Use state
}
```

**State Structure:**
```javascript
{
  user: null,
  uiState: {
    sidebarOpen: true,
    theme: 'light',
    notifications: []
  },
  userPreferences: {
    theme: 'light',
    layout: null,
    notifications: {}
  },
  windows: [],
  widgets: [],
  notifications: [],
  history: [],
  historyIndex: -1
}
```

## Widget API

### WidgetAPI

Standard interface for widgets.

**Location:** `src/core/WidgetAPI.js`

**Methods:**

```javascript
// Widget lifecycle
widget.onMount(() => {
  // Widget mounted
});

widget.onUnmount(() => {
  // Widget unmounted
});

// Window operations
widget.openWindow({ id: 'win1', title: 'Window' });
widget.closeWindow('win1');

// Notifications
widget.showNotification({
  type: 'success',
  message: 'Operation completed'
});

// Permissions
const canEdit = await widget.checkPermission('widget', 'write');
```

## Best Practices

1. **Use services for business logic** - Keep components focused on UI
2. **Cache expensive operations** - Use service-level caching
3. **Handle errors gracefully** - Services should catch and handle errors
4. **Emit events for state changes** - Allow components to react
5. **Document service methods** - Keep JSDoc comments updated

