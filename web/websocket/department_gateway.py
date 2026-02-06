"""
==============================================================================
FILE: web/websocket/department_gateway.py
ROLE: Real-time Department WebSocket Gateway
PURPOSE: Provides WebSocket endpoint for department-specific real-time updates.
         Clients subscribe to department channels and receive agent status,
         metrics, and event streams.

ARCHITECTURE:
    - Uses python-socketio for async WebSocket handling
    - JWT authentication on connect
    - Room-based subscriptions per department
    - 30-second heartbeat/ping cycle
    
DEPENDENCIES:
    - python-socketio
    - PyJWT
==============================================================================
"""
import asyncio
import logging
from typing import Dict, Any, Optional, Set
from datetime import datetime, timezone
import jwt

import socketio

from config.environment_manager import get_settings

logger = logging.getLogger("DepartmentGateway")

# Create department-specific Socket.IO server
dept_sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"],
    logger=False,
    engineio_logger=False
)

# ASGI App to be mounted at /ws/departments
dept_socket_app = socketio.ASGIApp(dept_sio, socketio_path='')

# Track connected clients per department for load management
_dept_connections: Dict[int, Set[str]] = {}
MAX_CONNECTIONS_PER_DEPT = 100

# Heartbeat interval (seconds)
HEARTBEAT_INTERVAL = 30


def _verify_jwt(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token and return payload if valid."""
    settings = get_settings()
    try:
        # Use JWT_SECRET as per AppSettings
        secret = getattr(settings, 'JWT_SECRET', 'dev_secret_key')
        algorithm = getattr(settings, 'JWT_ALGORITHM', 'HS256')
        
        payload = jwt.decode(
            token,
            secret,
            algorithms=[algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        logger.warning("JWT token expired")
        return None
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {e}")
        return None


@dept_sio.event
async def connect(sid: str, environ: Dict, auth: Optional[Dict] = None) -> bool:
    """
    Handle client connection with optional JWT authentication.
    """
    # Extract token from auth data or query string
    token = None
    if auth and 'token' in auth:
        token = auth['token']
    else:
        # Try query string
        query_string = environ.get('QUERY_STRING', '')
        if 'token=' in query_string:
            for param in query_string.split('&'):
                if param.startswith('token='):
                    token = param.split('=', 1)[1]
                    break
    
    # Verify token if provided (optional for development)
    user_id = "anonymous"
    if token:
        payload = _verify_jwt(token)
        if payload:
            user_id = payload.get('sub', 'authenticated')
            await dept_sio.save_session(sid, {'user_id': user_id, 'authenticated': True})
        else:
            # In production, reject invalid tokens
            # For development, allow connection but mark as unauthenticated
            await dept_sio.save_session(sid, {'user_id': 'anonymous', 'authenticated': False})
    else:
        await dept_sio.save_session(sid, {'user_id': 'anonymous', 'authenticated': False})
    
    logger.info(f"Client connected: {sid} (user: {user_id})")
    
    # Send welcome message
    await dept_sio.emit('connected', {
        'status': 'connected',
        'message': 'Department Gateway online',
        'heartbeat_interval': HEARTBEAT_INTERVAL,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }, to=sid)
    
    # Start heartbeat task for this client unless in testing mode
    settings = get_settings()
    if getattr(settings, 'APP_ENV', '') != 'testing':
        asyncio.create_task(_heartbeat_loop(sid))
    
    return True


@dept_sio.event
async def disconnect(sid: str) -> None:
    """Handle client disconnection."""
    # Remove from all department rooms
    for dept_id, connections in _dept_connections.items():
        connections.discard(sid)
    
    logger.info(f"Client disconnected: {sid}")


@dept_sio.event
async def subscribe_department(sid: str, data: Dict[str, Any]) -> None:
    """
    Subscribe to a specific department's updates.
    
    Expected data: {"dept_id": 1}
    """
    dept_id = data.get('dept_id')
    if not dept_id or not isinstance(dept_id, int):
        await dept_sio.emit('error', {'message': 'Invalid dept_id'}, to=sid)
        return
    
    # Check connection limit
    if dept_id not in _dept_connections:
        _dept_connections[dept_id] = set()
    
    if len(_dept_connections[dept_id]) >= MAX_CONNECTIONS_PER_DEPT:
        await dept_sio.emit('error', {
            'message': f'Department {dept_id} at max capacity ({MAX_CONNECTIONS_PER_DEPT})'
        }, to=sid)
        return
    
    # Join room and track connection
    room_name = f"dept_{dept_id}"
    await dept_sio.enter_room(sid, room_name)
    _dept_connections[dept_id].add(sid)
    
    logger.debug(f"Client {sid} subscribed to department {dept_id}")
    await dept_sio.emit('subscribed', {
        'dept_id': dept_id,
        'room': room_name,
        'active_connections': len(_dept_connections[dept_id])
    }, to=sid)


@dept_sio.event
async def unsubscribe_department(sid: str, data: Dict[str, Any]) -> None:
    """Unsubscribe from a department."""
    dept_id = data.get('dept_id')
    if dept_id and dept_id in _dept_connections:
        room_name = f"dept_{dept_id}"
        await dept_sio.leave_room(sid, room_name)
        _dept_connections[dept_id].discard(sid)
        
        await dept_sio.emit('unsubscribed', {'dept_id': dept_id}, to=sid)


@dept_sio.event
async def ping(sid: str) -> None:
    """Respond to client ping with pong."""
    await dept_sio.emit('pong', {
        'timestamp': datetime.now(timezone.utc).isoformat()
    }, to=sid)


async def _heartbeat_loop(sid: str) -> None:
    """Send periodic heartbeat pings to client."""
    try:
        while True:
            await asyncio.sleep(HEARTBEAT_INTERVAL)
            # Check if client still connected
            try:
                await dept_sio.emit('heartbeat', {
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }, to=sid)
            except Exception:
                # Client disconnected
                break
    except asyncio.CancelledError:
        pass


# --- Broadcaster Functions ---

async def broadcast_agent_status(dept_id: int, agent_id: str, status: str, details: Optional[Dict] = None) -> None:
    """Broadcast agent status update to department subscribers."""
    room_name = f"dept_{dept_id}"
    await dept_sio.emit('agent_status', {
        'dept_id': dept_id,
        'agent_id': agent_id,
        'status': status,
        'details': details or {},
        'timestamp': datetime.now(timezone.utc).isoformat()
    }, room=room_name)


async def broadcast_metrics(dept_id: int, metrics: Dict[str, Any]) -> None:
    """Broadcast metrics update to department subscribers."""
    room_name = f"dept_{dept_id}"
    await dept_sio.emit('metrics', {
        'dept_id': dept_id,
        'metrics': metrics,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }, room=room_name)


async def broadcast_event(dept_id: int, event_type: str, payload: Dict[str, Any]) -> None:
    """Broadcast generic event to department subscribers."""
    room_name = f"dept_{dept_id}"
    await dept_sio.emit('dept_event', {
        'dept_id': dept_id,
        'event_type': event_type,
        'payload': payload,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }, room=room_name)


def get_department_connection_count(dept_id: int) -> int:
    """Get current connection count for a department."""
    return len(_dept_connections.get(dept_id, set()))


# Create singleton broadcaster instance
class DepartmentBroadcaster:
    """Facade for broadcasting department events."""
    
    async def agent_status(self, dept_id: int, agent_id: str, status: str, details: Optional[Dict] = None) -> None:
        await broadcast_agent_status(dept_id, agent_id, status, details)
    
    async def metrics(self, dept_id: int, metrics: Dict[str, Any]) -> None:
        await broadcast_metrics(dept_id, metrics)
    
    async def event(self, dept_id: int, event_type: str, payload: Dict[str, Any]) -> None:
        await broadcast_event(dept_id, event_type, payload)


dept_broadcaster = DepartmentBroadcaster()
