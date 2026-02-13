"""
FastAPI Socket.io Gateway - Real-time Dashboard Updates
Migrated from python-socketio (web/websocket.py)
"""

import socketio
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

_sio = None
_socket_app = None

def get_sio():
    global _sio
    if _sio is None:
        import socketio
        _sio = socketio.AsyncServer(
            async_mode='asgi',
            cors_allowed_origins=[]  # Disable - FastAPI middleware handles CORS
        )
        _register_handlers(_sio)
    return _sio

def get_socket_app():
    global _socket_app
    if _socket_app is None:
        import socketio
        _socket_app = socketio.ASGIApp(get_sio())
    return _socket_app

def _register_handlers(sio):
    @sio.event
    async def connect(sid, environ):
        logger.info(f"Client connected: {sid}")
        await sio.emit('connected', {'status': 'connected', 'message': 'Mission Control online (FastAPI)'}, to=sid)

    @sio.event
    async def disconnect(sid):
        logger.info(f"Client disconnected: {sid}")

    @sio.event
    async def subscribe(sid, data: Dict[str, Any]):
        channel = data.get('channel', 'general')
        await sio.enter_room(sid, channel)
        logger.debug(f"Client {sid} subscribed to: {channel}")
        await sio.emit('subscribed', {'channel': channel}, to=sid)

    @sio.event
    async def unsubscribe(sid, data: Dict[str, Any]):
        channel = data.get('channel', 'general')
        await sio.leave_room(sid, channel)
        logger.debug(f"Client {sid} unsubscribed from: {channel}")

    @sio.event
    async def ping(sid):
        from datetime import timezone, datetime
        await sio.emit('pong', {'timestamp': datetime.now(timezone.utc).isoformat() + 'Z'}, to=sid)

    @sio.event
    async def update_mutation_rate(sid, data: Dict[str, Any]):
        rate = data.get('rate', 0.1)
        logger.info(f"Mutation rate update: {rate}")
        await sio.emit('mutation_rate_changed', {'rate': rate}, room='evolution')

    @sio.event
    async def evolution_control(sid, data: Dict[str, Any]):
        cmd = data.get('command')
        val = data.get('value')
        logger.info(f"Evolution control: {cmd} (val: {val})")
        await sio.emit('evolution_status_update', {'command': cmd, 'value': val}, room='evolution')


# --- Broadcaster Class ---

class FastAPIWebSocketBroadcaster:
    """
    Utility for broadcasting events via the FastAPI-Socket.IO server.
    """
    
    async def broadcast_agent_status(self, agent_name: str, status: str, is_active: bool, details: Dict = None):
        data = {
            'agent': agent_name,
            'status': status,
            'active': is_active,
            'details': details or {},
            'timestamp': self._get_timestamp()
        }
        sio = get_sio()
        await sio.emit('agent_status', data, room='agents')


    async def broadcast_portfolio_update(self, current_value: float, set_point: float, pnl_percent: float):
        data = {
            'value': current_value,
            'set_point': set_point,
            'gap': current_value - set_point,
            'gap_percent': ((current_value - set_point) / set_point) * 100,
            'pnl_percent': pnl_percent,
            'timestamp': self._get_timestamp()
        }
        sio = get_sio()
        await sio.emit('portfolio_update', data, room='portfolio')


    def _get_timestamp(self) -> str:
        from datetime import timezone, datetime
        return datetime.now(timezone.utc).isoformat() + 'Z'

# Singleton instance
broadcaster = FastAPIWebSocketBroadcaster()
