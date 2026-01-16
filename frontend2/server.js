/**
 * Express + Socket.io Server
 * 
 * This is a boilerplate server setup for React + Node.js MVP projects.
 * It includes:
 * - Express server with CORS support
 * - Optional Socket.io for real-time communication
 * - Environment variable configuration
 * - Health check endpoint
 * - API route examples
 * 
 * To enable Socket.io, uncomment the Socket.io sections below.
 * To disable Socket.io, keep those sections commented out.
 * 
 * NOTE: This file uses ES module syntax (import/export) because package.json
 * specifies "type": "module". Use import instead of require.
 */

import dotenv from 'dotenv';
import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import authRouter from './auth.js';
import { authenticateToken } from './authMiddleware.js';
import { db } from './db/index.js';
import { layouts, windowLayouts, roles, userRoles, permissions, rolePermissions, teams, teamMembers, userPreferences } from './db/schema.js';
import { eq, and, or, inArray } from 'drizzle-orm';
import * as dockerService from './dockerService.js';

// Load environment variables
dotenv.config();

// Get __dirname equivalent for ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ============================================================================
// SOCKET.IO SETUP
// ============================================================================

// ============================================================================
// CONFIGURATION
// ============================================================================
const PORT = parseInt(process.env.PORT || '3002', 10); // Default port for this template
const NODE_ENV = process.env.NODE_ENV || 'development';

// ============================================================================
// EXPRESS APP SETUP
// ============================================================================
const app = express();
const httpServer = http.createServer(app);

// ============================================================================
// SOCKET.IO SERVER SETUP
// ============================================================================
const io = new Server(httpServer, {
  cors: {
    origin: "*", // In production, specify your frontend URL
    methods: ["GET", "POST"],
    credentials: true
  }
});

// Socket.io Configuration
const SERVER_MESSAGE_AUTHOR = 'System';

// Secure rooms configuration (room name -> password)
// In production, use environment variables for passwords!
// Example: SECURE_ROOM_PASSWORDS='{"secure":"your-secure-password","top-secret":"another-password"}'
const SECURE_ROOMS = process.env.SECURE_ROOM_PASSWORDS
  ? JSON.parse(process.env.SECURE_ROOM_PASSWORDS)
  : {
    'secure': process.env.SECURE_ROOM_PASSWORD || 'admin123',
    'top-secret': process.env.TOP_SECRET_ROOM_PASSWORD || '007'
  };

// Track validated, active chat participants
let connectedClients = new Set();

// Track user presence
let presenceUsers = new Map(); // socketId -> { userId, username, page, lastActivity }

/**
 * Broadcasts the global client count to everyone.
 */
function broadcastClientCount() {
  io.emit('clientCount', connectedClients.size);
  console.log(`[Socket.io] Active clients: ${connectedClients.size}`);
}

// ============================================================================
// MIDDLEWARE
// ============================================================================

// CORS configuration
app.use(cors({
  origin: "*", // In production, specify your frontend URL
  methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true
}));

// Body parsing middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging middleware (development only)
if (NODE_ENV === 'development') {
  app.use((req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
    next();
  });
}

// ============================================================================
// STATIC FILE SERVING (for production builds)
// ============================================================================
// In production, serve the built React app from the 'dist' directory
if (NODE_ENV === 'production') {
  app.use(express.static(join(__dirname, 'dist')));
}

// ============================================================================
// API ROUTES
// ============================================================================\n
// Auth Routes
app.use('/api/auth', authRouter);

/**
 * Health check endpoint
 * GET /api/health
 * Returns server status and basic information
 */
app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    environment: NODE_ENV,
    port: PORT,
    features: {
      socketio: true,
    }
  });
});

/**
 * Layout Management (Protected)
 */
app.get('/api/layout', authenticateToken, async (req, res) => {
  try {
    const userLayout = await db.query.layouts.findFirst({
      where: eq(layouts.userId, req.user.userId),
    });
    res.json(userLayout ? JSON.parse(userLayout.layoutData) : null);
  } catch (error) {
    console.error('Fetch layout error:', error);
    res.status(500).json({ error: 'Failed to fetch layout' });
  }
});

app.post('/api/layout', authenticateToken, async (req, res) => {
  const { layoutData } = req.body;
  try {
    const existing = await db.query.layouts.findFirst({
      where: eq(layouts.userId, req.user.userId),
    });

    if (existing) {
      await db.update(layouts)
        .set({ layoutData: JSON.stringify(layoutData), updatedAt: new Date() })
        .where(eq(layouts.userId, req.user.userId));
    } else {
      await db.insert(layouts).values({
        userId: req.user.userId,
        layoutData: JSON.stringify(layoutData),
      });
    }
    res.json({ message: 'Layout saved' });
  } catch (error) {
    console.error('Save layout error:', error);
    res.status(500).json({ error: 'Failed to save layout' });
  }
});

/**
 * Docker Management Routes
 */
app.get('/api/docker/containers', async (req, res) => {
  try {
    const containers = await dockerService.listContainers();
    res.json(containers);
  } catch (error) {
    console.error('Docker list error:', error);
    res.status(500).json({ error: 'Failed to list containers. Is Docker running?' });
  }
});

app.post('/api/docker/containers/:id/start', async (req, res) => {
  try {
    const result = await dockerService.startContainer(req.params.id);
    res.json(result);
  } catch (error) {
    console.error('Docker start error:', error);
    res.status(500).json({ error: `Failed to start container: ${error.message}` });
  }
});

app.post('/api/docker/containers/:id/stop', async (req, res) => {
  try {
    const result = await dockerService.stopContainer(req.params.id);
    res.json(result);
  } catch (error) {
    console.error('Docker stop error:', error);
    res.status(500).json({ error: `Failed to stop container: ${error.message}` });
  }
});

app.post('/api/docker/containers/:id/restart', async (req, res) => {
  try {
    const result = await dockerService.restartContainer(req.params.id);
    res.json(result);
  } catch (error) {
    console.error('Docker restart error:', error);
    res.status(500).json({ error: `Failed to restart container: ${error.message}` });
  }
});

app.delete('/api/docker/containers/:id', async (req, res) => {
  try {
    const force = req.query.force === 'true';
    const result = await dockerService.removeContainer(req.params.id, force);
    res.json(result);
  } catch (error) {
    console.error('Docker remove error:', error);
    res.status(500).json({ error: `Failed to remove container: ${error.message}` });
  }
});

/**
 * Window Layout Management (Protected)
 */
app.get('/api/windows/layouts', authenticateToken, async (req, res) => {
  try {
    const userLayouts = await db.query.windowLayouts.findMany({
      where: eq(windowLayouts.userId, req.user.userId),
      orderBy: (layouts, { desc }) => [desc(layouts.updatedAt)],
    });
    res.json(userLayouts.map(l => ({
      id: l.id,
      name: l.name,
      layoutData: JSON.parse(l.layoutData),
      createdAt: l.createdAt,
      updatedAt: l.updatedAt,
    })));
  } catch (error) {
    console.error('Fetch window layouts error:', error);
    res.status(500).json({ error: 'Failed to fetch window layouts' });
  }
});

app.get('/api/windows/layouts/:name', authenticateToken, async (req, res) => {
  try {
    const layout = await db.query.windowLayouts.findFirst({
      where: (layouts, { and, eq }) => and(
        eq(layouts.userId, req.user.userId),
        eq(layouts.name, req.params.name)
      ),
    });
    if (!layout) {
      return res.status(404).json({ error: 'Layout not found' });
    }
    res.json({
      id: layout.id,
      name: layout.name,
      layoutData: JSON.parse(layout.layoutData),
      createdAt: layout.createdAt,
      updatedAt: layout.updatedAt,
    });
  } catch (error) {
    console.error('Fetch window layout error:', error);
    res.status(500).json({ error: 'Failed to fetch window layout' });
  }
});

app.post('/api/windows/layouts', authenticateToken, async (req, res) => {
  const { name, layoutData } = req.body;
  if (!name || !layoutData) {
    return res.status(400).json({ error: 'Name and layoutData are required' });
  }

  try {
    const existing = await db.query.windowLayouts.findFirst({
      where: (layouts, { and, eq }) => and(
        eq(layouts.userId, req.user.userId),
        eq(layouts.name, name)
      ),
    });

    if (existing) {
      await db.update(windowLayouts)
        .set({ 
          layoutData: JSON.stringify(layoutData), 
          updatedAt: new Date() 
        })
        .where(eq(windowLayouts.id, existing.id));
      res.json({ message: 'Layout updated', id: existing.id });
    } else {
      const result = await db.insert(windowLayouts).values({
        userId: req.user.userId,
        name,
        layoutData: JSON.stringify(layoutData),
      });
      res.json({ message: 'Layout saved', id: result.lastInsertRowid });
    }
  } catch (error) {
    console.error('Save window layout error:', error);
    res.status(500).json({ error: 'Failed to save window layout' });
  }
});

app.delete('/api/windows/layouts/:name', authenticateToken, async (req, res) => {
  try {
    const layout = await db.query.windowLayouts.findFirst({
      where: (layouts, { and, eq }) => and(
        eq(layouts.userId, req.user.userId),
        eq(layouts.name, req.params.name)
      ),
    });
    if (!layout) {
      return res.status(404).json({ error: 'Layout not found' });
    }
    await db.delete(windowLayouts).where(eq(windowLayouts.id, layout.id));
    res.json({ message: 'Layout deleted' });
  } catch (error) {
    console.error('Delete window layout error:', error);
    res.status(500).json({ error: 'Failed to delete window layout' });
  }
});

/**
 * Permission Management Routes
 */
app.post('/api/permissions/check', authenticateToken, async (req, res) => {
  const { userId, resource, action } = req.body;
  
  try {
    // Get user roles
    const userRolesList = await db.query.userRoles.findMany({
      where: eq(userRoles.userId, userId || req.user.userId),
    });

    if (userRolesList.length === 0) {
      return res.json({ hasPermission: false });
    }

    const roleIds = userRolesList.map(ur => ur.roleId);

    // Get permissions for these roles
    const rolePerms = await db.query.rolePermissions.findMany({
      where: inArray(rolePermissions.roleId, roleIds),
    });

    const permissionIds = rolePerms.map(rp => rp.permissionId);

    // Check if permission exists
    const perm = await db.query.permissions.findFirst({
      where: and(
        eq(permissions.resource, resource),
        eq(permissions.action, action),
        inArray(permissions.id, permissionIds)
      ),
    });

    res.json({ hasPermission: !!perm });
  } catch (error) {
    console.error('Permission check error:', error);
    res.status(500).json({ error: 'Failed to check permission' });
  }
});

app.get('/api/users/:userId/permissions', authenticateToken, async (req, res) => {
  try {
    const userId = parseInt(req.params.userId);
    
    // Get user roles
    const userRolesList = await db.query.userRoles.findMany({
      where: eq(userRoles.userId, userId),
    });

    if (userRolesList.length === 0) {
      return res.json([]);
    }

    const roleIds = userRolesList.map(ur => ur.roleId);

    // Get permissions
    const rolePerms = await db.query.rolePermissions.findMany({
      where: inArray(rolePermissions.roleId, roleIds),
    });

    const permissionIds = [...new Set(rolePerms.map(rp => rp.permissionId))];

    const perms = await db.query.permissions.findMany({
      where: inArray(permissions.id, permissionIds),
    });

    res.json(perms.map(p => `${p.resource}:${p.action}`));
  } catch (error) {
    console.error('Get user permissions error:', error);
    res.status(500).json({ error: 'Failed to get user permissions' });
  }
});

app.get('/api/users/:userId/roles', authenticateToken, async (req, res) => {
  try {
    const userId = parseInt(req.params.userId);
    
    const userRolesList = await db.query.userRoles.findMany({
      where: eq(userRoles.userId, userId),
    });

    if (userRolesList.length === 0) {
      return res.json([]);
    }

    const roleIds = userRolesList.map(ur => ur.roleId);
    const rolesList = await db.query.roles.findMany({
      where: inArray(roles.id, roleIds),
    });

    res.json(rolesList);
  } catch (error) {
    console.error('Get user roles error:', error);
    res.status(500).json({ error: 'Failed to get user roles' });
  }
});

/**
 * User Preferences Routes
 */
app.get('/api/users/:userId/preferences', authenticateToken, async (req, res) => {
  try {
    const userId = parseInt(req.params.userId);
    
    const prefs = await db.query.userPreferences.findFirst({
      where: eq(userPreferences.userId, userId),
    });

    if (!prefs) {
      return res.json({
        theme: 'light',
        layout: null,
        notifications: {},
      });
    }

    res.json({
      theme: prefs.theme,
      layout: prefs.layout ? JSON.parse(prefs.layout) : null,
      notifications: prefs.notifications ? JSON.parse(prefs.notifications) : {},
    });
  } catch (error) {
    console.error('Get user preferences error:', error);
    res.status(500).json({ error: 'Failed to get user preferences' });
  }
});

app.post('/api/users/:userId/preferences', authenticateToken, async (req, res) => {
  try {
    const userId = parseInt(req.params.userId);
    const { theme, layout, notifications } = req.body;

    const existing = await db.query.userPreferences.findFirst({
      where: eq(userPreferences.userId, userId),
    });

    if (existing) {
      await db.update(userPreferences)
        .set({
          theme: theme || existing.theme,
          layout: layout ? JSON.stringify(layout) : existing.layout,
          notifications: notifications ? JSON.stringify(notifications) : existing.notifications,
          updatedAt: new Date(),
        })
        .where(eq(userPreferences.userId, userId));
    } else {
      await db.insert(userPreferences).values({
        userId,
        theme: theme || 'light',
        layout: layout ? JSON.stringify(layout) : null,
        notifications: notifications ? JSON.stringify(notifications) : null,
      });
    }

    res.json({ message: 'Preferences saved' });
  } catch (error) {
    console.error('Save user preferences error:', error);
    res.status(500).json({ error: 'Failed to save user preferences' });
  }
});

/**
 * Example API endpoint
 * GET /api/example
 * Returns example data
 */
app.get('/api/example', (req, res) => {
  res.json({
    message: 'Hello from the API!',
    data: {
      example: 'This is example data from the backend',
      timestamp: new Date().toISOString(),
    }
  });
});

/**
 * Example POST endpoint
 * POST /api/example
 * Accepts JSON data and returns a response
 */
app.post('/api/example', (req, res) => {
  const { data } = req.body;

  res.json({
    message: 'Data received successfully',
    received: data,
    timestamp: new Date().toISOString(),
  });
});

// ============================================================================
// SOCKET.IO EVENT HANDLERS
// ============================================================================

io.on('connection', (socket) => {
  const userAgent = socket.handshake.headers['user-agent'] || 'Unknown';
  console.log(`[Socket.io] Client connected: ${socket.id} | Agent: ${userAgent}`);

  // --- PRESENCE SYSTEM ---
  socket.on('presence:register', (data) => {
    const { userId, username } = data;
    presenceUsers.set(socket.id, {
      userId,
      username: username || `User ${userId}`,
      page: null,
      lastActivity: new Date(),
    });

    // Send current user list to new user
    socket.emit('presence:list', Array.from(presenceUsers.values()));

    // Notify others
    socket.broadcast.emit('presence:user-joined', {
      userId,
      username: username || `User ${userId}`,
      timestamp: new Date().toISOString(),
    });

    console.log(`[Presence] User ${username} (${userId}) registered`);
  });

  socket.on('presence:activity', (data) => {
    const presence = presenceUsers.get(socket.id);
    if (presence) {
      presence.page = data.page;
      presence.action = data.action;
      presence.lastActivity = new Date();
      presenceUsers.set(socket.id, presence);

      // Broadcast update
      socket.broadcast.emit('presence:update', {
        userId: presence.userId,
        username: presence.username,
        page: data.page,
        action: data.action,
        timestamp: data.timestamp,
      });
    }
  });

  // --- 1. SECURE ROOMS FEATURE: Handle Joining with Validation ---
  socket.on('joinRoom', ({ room, password }, callback) => {
    // Security check for secure rooms
    if (SECURE_ROOMS.hasOwnProperty(room)) {
      const requiredPassword = SECURE_ROOMS[room];
      if (password !== requiredPassword) {
        console.log(`[Security] Access denied for ${socket.id} to room '${room}'`);
        if (callback) {
          return callback({
            status: 'error',
            message: 'Access Denied: Invalid Password.'
          });
        }
        return;
      }
    }

    // Leave notification (switching rooms)
    Array.from(socket.rooms).forEach((r) => {
      if (r !== socket.id) {
        const leaveMessage = {
          author: SERVER_MESSAGE_AUTHOR,
          text: `User ${socket.id.substring(0, 4)} left ${r}.`,
          timestamp: new Date().toLocaleTimeString()
        };
        io.to(r).emit('chatThread', leaveMessage);
        socket.leave(r);
      }
    });

    // Join the new room
    socket.join(room);
    console.log(`[Socket.io] ${socket.id} joined room: ${room}`);

    // Only count the client if they haven't been counted yet
    if (!connectedClients.has(socket.id)) {
      connectedClients.add(socket.id);
      broadcastClientCount();
    }

    // Notify users in the NEW room
    const joinMessage = {
      author: SERVER_MESSAGE_AUTHOR,
      text: `User ${socket.id.substring(0, 4)} joined ${room}.`,
      timestamp: new Date().toLocaleTimeString()
    };
    io.to(room).emit('chatThread', joinMessage);

    // Send success acknowledgement
    if (callback) {
      callback({
        status: 'ok',
        room: room
      });
    }
  });

  // --- 2. TYPING INDICATORS ---
  socket.on('typing', (roomName) => {
    socket.to(roomName).emit('userTyping', `User ${socket.id.substring(0, 4)} is typing...`);
  });

  socket.on('stopTyping', (roomName) => {
    socket.to(roomName).emit('userTyping', '');
  });

  // --- 3. MESSAGE HANDLING ---
  socket.on('chatMessage', ({ room, message }, callback) => {
    if (!socket.rooms.has(room)) {
      if (callback) callback({ status: 'error', message: 'You are not in this room.' });
      return;
    }

    const structuredMessage = {
      author: `Client (${socket.id.substring(0, 4)})`,
      text: message,
      timestamp: new Date().toLocaleTimeString()
    };

    // Broadcast to all clients in the room (including sender)
    // io.to(room) includes all sockets in the room, so the sender will also receive the message
    io.to(room).emit('chatThread', structuredMessage);
    console.log(`[Chat - ${room}] ${structuredMessage.author}: ${structuredMessage.text}`);
    console.log(`[Chat - ${room}] Broadcasting to ${io.sockets.adapter.rooms.get(room)?.size || 0} client(s) in room`);

    if (callback) {
      callback({
        status: 'ok',
        timestamp: new Date().toISOString()
      });
    }
  });

  // --- 4. LEAVE NOTIFICATION (Disconnection) ---
  socket.on('disconnecting', () => {
    const rooms = Array.from(socket.rooms);
    rooms.forEach((room) => {
      if (room !== socket.id) {
        const leaveMessage = {
          author: SERVER_MESSAGE_AUTHOR,
          text: `User ${socket.id.substring(0, 4)} has disconnected.`,
          timestamp: new Date().toLocaleTimeString()
        };
        io.to(room).emit('chatThread', leaveMessage);
        console.log(`[System] Notified ${room} of disconnect.`);
      }
    });
  });

  // --- Disconnect Handler ---
  socket.on('disconnect', () => {
    console.log(`[Socket.io] Client disconnected: ${socket.id}`);

    // Handle presence cleanup
    const presence = presenceUsers.get(socket.id);
    if (presence) {
      socket.broadcast.emit('presence:user-left', {
        userId: presence.userId,
        username: presence.username,
        timestamp: new Date().toISOString(),
      });
      presenceUsers.delete(socket.id);
    }

    // Only update count if they were a "real" participant
    if (connectedClients.has(socket.id)) {
      connectedClients.delete(socket.id);
      broadcastClientCount();
    }
  });
});

// ============================================================================
// CATCH-ALL ROUTE (for React Router in production)
// ============================================================================
// In production, serve the React app for all non-API routes
if (NODE_ENV === 'production') {
  app.get('*', (req, res) => {
    // Don't serve React app for API routes
    if (req.path.startsWith('/api')) {
      return res.status(404).json({ error: 'API endpoint not found' });
    }
    res.sendFile(join(__dirname, 'dist', 'index.html'));
  });
}

// ============================================================================
// SERVER STARTUP
// ============================================================================
function startServer(attemptPort = PORT, maxAttempts = 10) {
  const numericPort = Number(attemptPort);
  if (!Number.isFinite(numericPort) || numericPort <= 0 || numericPort >= 65536) {
    console.error(`\n❌ Invalid port value: ${attemptPort}. Please check PORT environment variable.`);
    process.exit(1);
  }

  httpServer.listen(numericPort, () => {
    const actualPort = numericPort;
    console.log('\n' + '='.repeat(60));
    console.log('✅ React + Node.js Template Server Started');
    console.log('='.repeat(60));
    console.log(`Environment: ${NODE_ENV}`);
    console.log(`Server URL: http://localhost:${actualPort}`);
    console.log(`API Base: http://localhost:${actualPort}/api`);
    console.log(`Health Check: http://localhost:${actualPort}/api/health`);
    if (actualPort !== PORT) {
      console.log(`Note: Using port ${actualPort} (requested ${PORT} was busy)`);
    }
    console.log(`Socket.io: Enabled`);
    console.log('='.repeat(60) + '\n');
  });

  // Handle server errors
  httpServer.on('error', (error) => {
    if (error.code === 'EADDRINUSE') {
      const nextPort = numericPort + 1;
      const attemptsLeft = maxAttempts - 1;

      if (attemptsLeft > 0) {
        console.warn(`\n⚠️  Port ${attemptPort} is already in use, trying port ${nextPort}...`);
        // Close the current server attempt and wait for it to fully close
        httpServer.close(() => {
          // Server is fully closed, now try next port
          startServer(nextPort, attemptsLeft);
        });
      } else {
        console.error(`\n❌ ERROR: Could not find an available port starting from ${PORT}!`);
        console.error(`   Tried ${maxAttempts} consecutive ports, all are in use.`);
        console.error(`   Please either:`);
        console.error(`   1. Stop processes using ports ${PORT}-${attemptPort}`);
        console.error(`   2. Set a different PORT in your .env file`);
        console.error(`   3. Use: PORT=3003 node server.js\n`);
        process.exit(1);
      }
    } else {
      console.error('\n❌ Server error:', error);
      process.exit(1);
    }
  });
}

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('\n[INFO] SIGTERM received, shutting down gracefully...');
  httpServer.close(() => {
    console.log('[OK] Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('\n[INFO] SIGINT received, shutting down gracefully...');
  httpServer.close(() => {
    console.log('[OK] Server closed');
    process.exit(0);
  });
});

// Start the server
startServer();
