# API Documentation

## Authentication

### POST /api/auth/register
Register a new user.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "message": "User registered successfully"
}
```

### POST /api/auth/login
Login and get JWT token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "token": "jwt-token",
  "user": {
    "id": 1,
    "username": "string"
  }
}
```

## Window Management

### GET /api/windows/layouts
Get all saved window layouts for the current user.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
[
  {
    "id": 1,
    "name": "layout-name",
    "layoutData": {...},
    "createdAt": "2026-01-08T...",
    "updatedAt": "2026-01-08T..."
  }
]
```

### POST /api/windows/layouts
Save a window layout.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "name": "layout-name",
  "layoutData": {...}
}
```

### DELETE /api/windows/layouts/:name
Delete a saved layout.

**Headers:** `Authorization: Bearer <token>`

## Permissions

### POST /api/permissions/check
Check if user has a specific permission.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "userId": 1,
  "resource": "widget",
  "action": "read"
}
```

**Response:**
```json
{
  "hasPermission": true
}
```

### GET /api/users/:userId/permissions
Get all permissions for a user.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
["widget:read", "widget:write", "window:admin"]
```

## User Preferences

### GET /api/users/:userId/preferences
Get user preferences.

**Headers:** `Authorization: Bearer <token>`

**Response:**
```json
{
  "theme": "light",
  "layout": {...},
  "notifications": {...}
}
```

### POST /api/users/:userId/preferences
Save user preferences.

**Headers:** `Authorization: Bearer <token>`

**Request Body:**
```json
{
  "theme": "dark",
  "layout": {...},
  "notifications": {...}
}
```

## Docker Management

### GET /api/docker/containers
List all Docker containers.

**Response:**
```json
[
  {
    "id": "container-id",
    "name": "container-name",
    "image": "image-name",
    "state": "running",
    "status": "Up 2 hours",
    "ports": "3002:3002"
  }
]
```

### POST /api/docker/containers/:id/start
Start a container.

### POST /api/docker/containers/:id/stop
Stop a container.

### POST /api/docker/containers/:id/restart
Restart a container.

### DELETE /api/docker/containers/:id
Remove a container.

## Socket.io Events

### Client → Server

- `joinRoom` - Join a chat room
- `chatMessage` - Send a chat message
- `presence:register` - Register for presence tracking
- `presence:activity` - Update user activity

### Server → Client

- `clientCount` - Total connected clients
- `chatThread` - Chat message received
- `presence:list` - List of online users
- `presence:user-joined` - User joined
- `presence:user-left` - User left
- `presence:update` - User activity update

