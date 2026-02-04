# Quick Start Guide

Get up and running with the GUI boilerplate in minutes!

## Prerequisites

- Node.js 18+ and npm
- SQLite (included with Node.js)
- Docker (optional, for Docker widget)

## Installation

```bash
# Clone or navigate to project
cd GUI_boilerplate_react_node_socketio_widgets_os_style

# Install dependencies
npm install

# Initialize database
npm run db:push
```

## Development

### Start Both Servers (Recommended)

```bash
npm run dev:full
```

This starts:
- **Backend**: http://localhost:3002
- **Frontend**: http://localhost:5176

### Start Separately

```bash
# Terminal 1: Backend
npm start

# Terminal 2: Frontend
npm run dev
```

## First Steps

1. **Open the app**: http://localhost:5176
2. **Register a user**: Click "Sign Up" in the login modal
3. **Explore widgets**: Use the "Widgets" menu to open widgets
4. **Customize theme**: Use "View" → "Toggle Dark Mode" or open Theme Editor
5. **Try layouts**: Drag and resize widgets, save your layout

## Testing

```bash
# Run unit tests
npm test

# Run E2E tests (requires dev server running)
npm run test:e2e

# Run with coverage
npm run test:coverage
```

## Building for Production

```bash
# Build frontend
npm run build

# Start production server
npm start
```

## Key Features to Try

### 1. Authentication
- Register/Login via modal
- Protected routes
- JWT token management

### 2. Widgets
- Open widgets from "Widgets" menu
- Drag and resize widgets
- Save/load layouts

### 3. Menu System
- File: Save/load/export layouts
- View: Toggle theme, zoom, fullscreen
- Widgets: Open/close individual widgets
- Tools: Layout manager, dev tools
- Help: Documentation, shortcuts

### 4. Real-time Features
- Socket.io chat (open Socket.io widget)
- Presence indicators
- Live updates

### 5. Window Management
- Minimize/maximize/close windows
- Window registry
- Snap zones
- Window groups

## Common Commands

```bash
# Development
npm run dev          # Frontend only
npm start            # Backend only
npm run dev:full     # Both servers

# Testing
npm test             # Unit tests
npm run test:ui      # Test UI
npm run test:e2e      # E2E tests

# Code Quality
npm run lint         # Lint code
npm run test:coverage # Test coverage

# Database
npm run db:push      # Push schema changes
npm run db:generate  # Generate migrations
```

## Troubleshooting

### Port Already in Use
```bash
# Change ports in .env or package.json
PORT=3003 npm start
VITE_PORT=5177 npm run dev
```

### Database Issues
```bash
# Reset database
rm sqlite.db
npm run db:push
```

### Docker Widget Not Working
- Ensure Docker is running
- Check Docker socket permissions
- Verify dockerode installation

## Next Steps

1. **Read Documentation**: Check `docs/` folder
2. **Explore Components**: See `src/components/`
3. **Customize Theme**: Edit `config/color_palette.json`
4. **Add Widgets**: Use widget registry system
5. **Extend API**: Add endpoints in `server.js`

## Getting Help

- **Documentation**: See `docs/` folder
- **Architecture**: `docs/ARCHITECTURE.md`
- **API Reference**: `docs/API.md`
- **Components**: `docs/COMPONENTS.md`

## Project Structure

```
├── src/
│   ├── components/    # React components
│   ├── hooks/         # Custom hooks
│   ├── services/      # Business logic
│   ├── pages/         # Page components
│   └── utils/         # Utilities
├── tests/             # All tests
├── docs/              # Documentation
├── config/            # Configuration
└── server.js          # Backend server
```

Happy coding! 🚀

