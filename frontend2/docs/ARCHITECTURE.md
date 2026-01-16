# Architecture Documentation

## System Overview

This is a full-stack OS-style web application boilerplate built with React, Node.js, and Socket.io.

## Frontend Architecture

### Component Structure
```
src/
├── components/          # React components
│   ├── WindowManager/  # Window management UI
│   ├── WidgetCatalog/ # Widget marketplace
│   ├── ThemeEditor/    # Theme customization
│   └── ...
├── core/               # Core services
│   ├── WidgetRegistry.js
│   ├── WidgetAPI.js
│   └── WidgetLoader.js
├── services/           # Business logic services
│   ├── windowManager.js
│   ├── permissionService.js
│   └── syncService.js
├── hooks/              # React hooks
│   ├── useWindowManager.js
│   ├── useTheme.js
│   └── usePermissions.js
├── store/              # Global state
│   └── store.js
└── themes/             # Theme system
    └── ThemeEngine.js
```

### State Management

- **Global State:** Zustand store for app-wide state
- **Window State:** Window Manager service
- **Widget State:** Widget Registry service
- **Theme State:** Theme Engine service

### Data Flow

1. User interaction → Component
2. Component → Hook/Service
3. Service → API/State Store
4. State Store → Component re-render

## Backend Architecture

### Server Structure
```
server.js              # Main Express server
├── Middleware         # Auth, CORS, logging
├── Routes            # API endpoints
│   ├── /api/auth
│   ├── /api/windows
│   ├── /api/permissions
│   └── /api/docker
└── Socket.io         # Real-time communication
```

### Database Schema

- `users` - User accounts
- `roles` - User roles
- `permissions` - Permission definitions
- `user_roles` - User-role assignments
- `role_permissions` - Role-permission assignments
- `teams` - Team/organization groups
- `team_members` - Team membership
- `layouts` - Widget layouts
- `window_layouts` - Window layouts
- `user_preferences` - User settings

## Key Systems

### Window Management System
- Centralized window registry
- Z-index and stacking management
- Window state operations
- Layout persistence

### Widget Plugin System
- Dynamic widget loading
- Widget registry
- Standard widget API
- Dependency management

### Theme System
- Runtime theme switching
- Design token system
- Theme customization
- CSS variable injection

### Permission System
- Role-based access control
- Granular permissions
- Permission caching
- Resource-based checks

### Sync System
- Offline queue
- Automatic sync
- Conflict resolution
- State synchronization

## Security

- JWT authentication
- Role-based permissions
- Input validation
- CORS configuration
- SQL injection prevention (Drizzle ORM)

## Performance

- Code splitting
- Lazy loading
- State caching
- Virtual scrolling
- Performance monitoring

## Deployment

- Docker support
- Multi-stage builds
- Environment configuration
- Health checks
- CI/CD ready

