# Component Documentation

## Overview

This document describes all React components in the boilerplate, their props, usage, and examples.

## Window Management Components

### WindowManagerWidget

Main widget for managing windows in the application.

**Location:** `src/components/WindowManager/WindowManagerWidget.jsx`

**Props:**
- None (uses context and hooks internally)

**Usage:**
```jsx
import WindowManagerWidget from './components/WindowManager/WindowManagerWidget';

<WindowManagerWidget />
```

**Features:**
- List all open windows
- Close, minimize, maximize windows
- Toggle snap zones
- Window state management

### WindowRegistry

Displays registered windows and their metadata.

**Location:** `src/components/WindowManager/WindowRegistry.jsx`

**Props:**
- `windows` (array) - Array of window objects
- `onWindowSelect` (function) - Callback when window is selected

### SnapZones

Visual overlay showing snap zones for window docking.

**Location:** `src/components/WindowManager/SnapZones.jsx`

**Props:**
- `visible` (boolean) - Show/hide snap zones
- `onSnap` (function) - Callback when window is snapped

### WindowGroup

Tabbed interface for grouping multiple windows.

**Location:** `src/components/WindowManager/WindowGroup.jsx`

**Props:**
- `windows` (array) - Windows to group
- `activeWindow` (string) - Currently active window ID
- `onWindowChange` (function) - Callback when active window changes

## Widget System Components

### WidgetCatalog

Marketplace for browsing and installing widgets.

**Location:** `src/components/WidgetCatalog/WidgetCatalog.jsx`

**Props:**
- None

**Usage:**
```jsx
import WidgetCatalog from './components/WidgetCatalog/WidgetCatalog';

<WidgetCatalog />
```

**Features:**
- Search widgets
- Filter by category
- Install/uninstall widgets
- View widget details

## Theming Components

### ThemeEditor

Visual editor for customizing themes.

**Location:** `src/components/ThemeEditor/ThemeEditor.jsx`

**Props:**
- None

**Usage:**
```jsx
import ThemeEditor from './components/ThemeEditor/ThemeEditor';

<ThemeEditor />
```

**Features:**
- Switch between themes
- Customize colors
- Adjust spacing and typography
- Export/import themes
- Live preview

## Layout Components

### LayoutBuilder

Visual drag-and-drop layout editor.

**Location:** `src/components/LayoutBuilder/LayoutBuilder.jsx`

**Props:**
- `onSave` (function) - Callback when layout is saved
- `onClose` (function) - Callback when editor is closed

**Usage:**
```jsx
<LayoutBuilder
  onSave={(layout) => console.log('Saved:', layout)}
  onClose={() => setShowBuilder(false)}
/>
```

### SplitPane

Resizable split-pane layout component.

**Location:** `src/components/SplitPane/SplitPane.jsx`

**Props:**
- `direction` (string) - 'horizontal' | 'vertical'
- `children` (ReactNode) - Child components
- `defaultSizes` (array) - Default sizes in percentage
- `minSize` (number) - Minimum size in percentage
- `onResize` (function) - Callback when pane is resized

**Usage:**
```jsx
<SplitPane direction="horizontal" defaultSizes={[50, 50]}>
  <div>Left Pane</div>
  <div>Right Pane</div>
</SplitPane>
```

### TabbedLayout

Tab-based layout for organizing content.

**Location:** `src/components/TabbedLayout/TabbedLayout.jsx`

**Props:**
- `tabs` (array) - Array of tab objects
- `defaultTab` (string) - Default active tab ID
- `onTabChange` (function) - Callback when tab changes
- `onTabClose` (function) - Callback when tab is closed
- `closable` (boolean) - Allow closing tabs

**Usage:**
```jsx
<TabbedLayout
  tabs={[
    { id: 'tab1', label: 'Tab 1', content: <div>Content 1</div> },
    { id: 'tab2', label: 'Tab 2', content: <div>Content 2</div> },
  ]}
  onTabChange={(tabId) => console.log('Active:', tabId)}
/>
```

## Collaboration Components

### PresenceIndicator

Shows online users and their activity.

**Location:** `src/components/PresenceIndicator/PresenceIndicator.jsx`

**Props:**
- None

**Features:**
- Display online user count
- Show user list
- Display user activity

### NotificationCenter

Centralized notification system.

**Location:** `src/components/NotificationCenter/NotificationCenter.jsx`

**Props:**
- `onClose` (function) - Callback when center is closed

**Features:**
- View all notifications
- Filter by read/unread
- Mark as read
- Dismiss notifications

## Performance Components

### PerformanceMonitor

Displays Core Web Vitals and performance metrics.

**Location:** `src/components/PerformanceMonitor/PerformanceMonitor.jsx`

**Props:**
- None

**Features:**
- Track LCP, FID, CLS, FCP, TTFB
- Performance scores
- Real-time updates

## Utility Components

### OfflineIndicator

Shows online/offline status and sync queue.

**Location:** `src/components/OfflineIndicator/OfflineIndicator.jsx`

**Props:**
- None

**Features:**
- Display connection status
- Show sync queue length
- Auto-hide when online

## Common Patterns

### Using Hooks

Most components use custom hooks:

```jsx
import { useWindowManager } from '../hooks/useWindowManager';
import { useTheme } from '../hooks/useTheme';
import { usePermissions } from '../hooks/usePermissions';

function MyComponent() {
  const { windows, openWindow } = useWindowManager();
  const { currentTheme, setTheme } = useTheme();
  const { hasPermission } = usePermissions();
  
  // Component logic
}
```

### Styling

All components use CSS modules or CSS files:

```jsx
import './Component.css';

<div className="component">
  {/* Content */}
</div>
```

Components respect theme variables:

```css
.component {
  background: var(--color-backgrounds-card);
  color: var(--color-text-primary);
  border: 1px solid var(--color-borders-secondary);
}
```

