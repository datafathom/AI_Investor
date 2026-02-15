# Features Guide

## Overview

This guide covers all major features of the OS-Style Web GUI Boilerplate and how to use them.

## Window Management

### Creating Windows

Windows can be created programmatically or through the UI:

```javascript
import { useWindowManager } from './hooks/useWindowManager';

function MyComponent() {
  const { openWindow } = useWindowManager();
  
  const handleOpen = () => {
    openWindow({
      id: 'my-window',
      title: 'My Window',
      component: 'MyWidget',
      size: { width: 800, height: 600 },
      position: { x: 100, y: 100 }
    });
  };
}
```

### Window Operations

- **Minimize**: Reduces window to dock
- **Maximize**: Fills entire screen
- **Restore**: Returns to previous size
- **Close**: Removes window
- **Lock**: Prevents window operations
- **Bring to Front**: Raises window z-index

### Snap Zones

Enable snap zones to automatically position windows:

1. Open Window Manager widget
2. Toggle "Snap Zones" button
3. Drag window to edge or corner
4. Window snaps to position

Available zones:
- Top, Bottom, Left, Right (edges)
- Top-Left, Top-Right, Bottom-Left, Bottom-Right (corners)

### Window Grouping

Group multiple windows into tabs:

1. Open multiple windows
2. Drag one window onto another
3. Windows group into tabs
4. Click tabs to switch between windows

## Widget System

### Installing Widgets

1. Open Widget Catalog
2. Browse available widgets
3. Click "Install" on desired widget
4. Widget appears in widget list

### Creating Custom Widgets

```javascript
// src/widgets/MyWidget.jsx
import { WidgetAPI } from '../core/WidgetAPI';

export default function MyWidget() {
  const widget = WidgetAPI.getInstance();
  
  widget.onMount(() => {
    console.log('Widget mounted');
  });
  
  return (
    <div className="my-widget">
      <h2>My Custom Widget</h2>
    </div>
  );
}

// Register widget
import widgetRegistry from '../core/WidgetRegistry';
widgetRegistry.register({
  id: 'my-widget',
  name: 'My Widget',
  component: MyWidget,
  description: 'A custom widget',
  version: '1.0.0'
});
```

### Widget Dependencies

Widgets can declare dependencies:

```javascript
widgetRegistry.register({
  id: 'advanced-widget',
  dependencies: ['base-widget', 'chart-library'],
  // ...
});
```

## Theming

### Switching Themes

```javascript
import { useTheme } from './hooks/useTheme';

function MyComponent() {
  const { setTheme, currentTheme } = useTheme();
  
  return (
    <select onChange={(e) => setTheme(e.target.value)}>
      <option value="light">Light</option>
      <option value="dark">Dark</option>
    </select>
  );
}
```

### Customizing Themes

1. Open Theme Editor
2. Select theme to customize
3. Adjust colors, spacing, typography
4. Preview changes in real-time
5. Save or export theme

### Design Tokens

Themes use design tokens:

```css
/* Colors */
--color-primary
--color-secondary
--color-backgrounds-main
--color-backgrounds-card
--color-text-primary
--color-text-secondary
--color-borders-primary
--color-borders-secondary

/* Spacing */
--spacing-xs
--spacing-sm
--spacing-md
--spacing-lg
--spacing-xl

/* Typography */
--font-family-primary
--font-size-base
--font-weight-normal
--font-weight-bold

/* Shadows */
--shadow-sm
--shadow-md
--shadow-lg
```

## Permissions

### Checking Permissions

```javascript
import { usePermissions } from './hooks/usePermissions';

function ProtectedComponent() {
  const { hasPermission } = usePermissions();
  
  if (!hasPermission('widget', 'write')) {
    return <div>Access denied</div>;
  }
  
  return <div>Protected content</div>;
}
```

### Permission Format

Permissions use `resource:action` format:
- `widget:read` - Read widgets
- `widget:write` - Create/edit widgets
- `widget:delete` - Delete widgets
- `window:admin` - Window administration
- `user:manage` - User management

## Layouts

### Using Split Panes

```jsx
import SplitPane from './components/SplitPane/SplitPane';

<SplitPane direction="horizontal" defaultSizes={[30, 70]}>
  <div>Sidebar (30%)</div>
  <div>Main Content (70%)</div>
</SplitPane>
```

### Using Tabbed Layouts

```jsx
import TabbedLayout from './components/TabbedLayout/TabbedLayout';

<TabbedLayout
  tabs={[
    { id: 'tab1', label: 'Tab 1', content: <div>Content 1</div> },
    { id: 'tab2', label: 'Tab 2', content: <div>Content 2</div> },
  ]}
  onTabChange={(tabId) => console.log('Switched to:', tabId)}
/>
```

### Saving Layouts

```javascript
const { saveLayout } = useWindowManager();

saveLayout('my-layout', {
  windows: [...],
  positions: {...}
});
```

## Collaboration

### Presence System

See who's online and what they're viewing:

1. Presence indicator shows online user count
2. Click to see user list
3. View user activity (current page/action)

### Notifications

```javascript
import { useStore } from './store/store';

const addNotification = useStore(state => state.addNotification);

addNotification({
  type: 'success',
  title: 'Operation Complete',
  message: 'Your changes have been saved',
  timestamp: new Date()
});
```

Notification types:
- `success` - Green
- `error` - Red
- `warning` - Yellow
- `info` - Blue

## Performance

### Monitoring Performance

The Performance Monitor widget tracks:
- **LCP** (Largest Contentful Paint) - Loading performance
- **FID** (First Input Delay) - Interactivity
- **CLS** (Cumulative Layout Shift) - Visual stability
- **FCP** (First Contentful Paint) - Initial render
- **TTFB** (Time to First Byte) - Server response

### Performance Scores

- **Good** (Green) - Meets recommended thresholds
- **Needs Improvement** (Yellow) - Below recommended
- **Poor** (Red) - Significantly below recommended

## Offline Support

### Automatic Sync

Actions are queued when offline and synced when connection is restored:

1. Perform action while offline
2. Action is queued
3. Connection restored
4. Actions sync automatically
5. Offline indicator shows sync status

### Manual Sync

```javascript
import syncService from './services/syncService';

// Process queue manually
await syncService.processQueue();

// Check status
const status = syncService.getQueueStatus();
```

## State Management

### Using Global State

```javascript
import { useStore } from './store/store';

function MyComponent() {
  const user = useStore(state => state.user);
  const setUser = useStore(state => state.setUser);
  const notifications = useStore(state => state.notifications);
  
  // Update state
  setUser({ id: 1, username: 'user' });
}
```

### State Persistence

State is automatically persisted to localStorage:
- User preferences
- UI state
- Theme selection

### Cross-Tab Sync

State changes sync across browser tabs automatically.

## Best Practices

1. **Use hooks for service access** - Don't import services directly in components
2. **Handle loading states** - Show loading indicators
3. **Error boundaries** - Wrap components in error boundaries
4. **Optimize renders** - Use React.memo for expensive components
5. **Test features** - Write tests for critical features

