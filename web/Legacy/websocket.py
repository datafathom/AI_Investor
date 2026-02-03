"""
==============================================================================
AI Investor - WebSocket Service
==============================================================================
PURPOSE:
    Flask-SocketIO integration for real-time updates to the Mission Control
    dashboard. Broadcasts agent status, portfolio values, and alerts.

USAGE:
    from web.websocket import socketio, init_socketio
    init_socketio(app)
    
    # Emit portfolio update
    socketio.emit('portfolio_update', {'value': 102500, 'pnl': 2.5})

EVENTS:
    - 'agent_status': Agent health updates
    - 'portfolio_update': Portfolio value changes
    - 'alert': Critical alerts (VIX spike, drawdown, etc.)
    - 'signal': Trading signals from agents
==============================================================================
"""
from typing import Any, Dict, Optional, List
from flask import Flask
import logging
import os

logger = logging.getLogger(__name__)

# Check if flask-socketio is available
try:
    from flask_socketio import SocketIO, emit, join_room, leave_room
    SOCKETIO_AVAILABLE = True
except ImportError:
    SOCKETIO_AVAILABLE = False
    logger.warning("flask-socketio not installed. WebSocket features disabled.")


# Global socketio instance
socketio: Optional['SocketIO'] = None


def init_socketio(app: Flask, **kwargs) -> Optional['SocketIO']:
    """
    Initialize Flask-SocketIO with the Flask app.
    
    Args:
        app: Flask application instance.
        **kwargs: Additional SocketIO configuration.
        
    Returns:
        SocketIO instance if available, None otherwise.
    """
    global socketio
    
    if not SOCKETIO_AVAILABLE:
        logger.error("Cannot initialize SocketIO: flask-socketio not installed")
        return None
    
    cors_origins = kwargs.pop('cors_allowed_origins', '*')
    async_mode = kwargs.pop('async_mode', 'threading')
    
    socketio = SocketIO(
        app,
        cors_allowed_origins=cors_origins,
        async_mode=async_mode,
        **kwargs
    )
    
    # Register event handlers
    _register_handlers(socketio)
    
    logger.info(f"WebSocket initialized with async_mode={async_mode}")
    return socketio


def _register_handlers(sio: 'SocketIO') -> None:
    """Register WebSocket event handlers."""
    
    @sio.on('connect')
    def handle_connect():
        """Handle client connection."""
        logger.info("Client connected to WebSocket")
        emit('connected', {'status': 'connected', 'message': 'Mission Control online'})
    
    @sio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection."""
        logger.info("Client disconnected from WebSocket")
    
    @sio.on('subscribe')
    def handle_subscribe(data: Dict[str, Any]):
        """
        Handle channel subscription requests.
        
        Args:
            data: {'channel': 'portfolio' | 'agents' | 'alerts'}
        """
        channel = data.get('channel', 'general')
        join_room(channel)
        logger.debug(f"Client subscribed to channel: {channel}")
        emit('subscribed', {'channel': channel})
    
    @sio.on('unsubscribe')
    def handle_unsubscribe(data: Dict[str, Any]):
        """Handle channel unsubscription."""
        channel = data.get('channel', 'general')
        leave_room(channel)
        logger.debug(f"Client unsubscribed from channel: {channel}")
    
    @sio.on('ping')
    def handle_ping():
        """Handle ping for latency measurement."""
        emit('pong', {'timestamp': _get_timestamp()})

    @sio.on('update_mutation_rate')
    def handle_mutation_rate(data: Dict[str, Any]):
        """
        Handle live mutation rate update from user.
        Args: data: {'rate': 0.15}
        """
        rate = data.get('rate', 0.1)
        logger.info(f"Mutation rate update requested: {rate}")
        # In a real scenario, this would update the GeneticDistillery instance
        # For now, we broadcast it back to confirm
        emit('mutation_rate_changed', {'rate': rate}, room='evolution')

    @sio.on('evolution_control')
    def handle_evolution_control(data: Dict[str, Any]):
        """
        Handle evolution speed and pause/resume.
        Args: data: {'command': 'pause' | 'resume' | 'speed', 'value': 2.0}
        """
        cmd = data.get('command')
        val = data.get('value')
        logger.info(f"Evolution control command: {cmd} (val: {val})")
        emit('evolution_status_update', {'command': cmd, 'value': val}, room='evolution')


def _get_timestamp() -> str:
    """Get current ISO timestamp."""
    from datetime import datetime
    return datetime.utcnow().isoformat() + 'Z'


class WebSocketBroadcaster:
    """
    Utility class for broadcasting events to connected clients.
    
    Provides typed methods for common event types used in the
    AI Investor dashboard.
    """
    
    def __init__(self, sio: Optional['SocketIO'] = None) -> None:
        """
        Initialize the broadcaster.
        
        Args:
            sio: SocketIO instance. Uses global if not provided.
        """
        self._sio = sio
    
    @property
    def sio(self) -> Optional['SocketIO']:
        """Get the SocketIO instance."""
        return self._sio or socketio
    
    def _emit(self, event: str, data: Dict, room: Optional[str] = None) -> bool:
        """
        Internal emit with availability check.
        
        Returns:
            True if emit succeeded, False if SocketIO unavailable.
        """
        if self.sio is None:
            logger.warning(f"Cannot emit '{event}': SocketIO not initialized")
            return False
        
        if room:
            self.sio.emit(event, data, room=room)
        else:
            self.sio.emit(event, data)
        
        return True
    
    def broadcast_agent_status(
        self,
        agent_name: str,
        status: str,
        is_active: bool,
        details: Optional[Dict] = None
    ) -> bool:
        """
        Broadcast agent status update.
        
        Args:
            agent_name: Name of the agent.
            status: Status message (e.g., 'healthy', 'warning', 'error').
            is_active: Whether agent is currently active.
            details: Additional status details.
            
        Returns:
            True if broadcast succeeded.
        """
        data = {
            'agent': agent_name,
            'status': status,
            'active': is_active,
            'details': details or {},
            'timestamp': _get_timestamp()
        }
        return self._emit('agent_status', data, room='agents')
    
    def broadcast_portfolio_update(
        self,
        current_value: float,
        set_point: float,
        pnl_percent: float,
        positions: Optional[Dict] = None
    ) -> bool:
        """
        Broadcast portfolio value update.
        
        Args:
            current_value: Current portfolio value.
            set_point: Target/initial portfolio value.
            pnl_percent: Profit/Loss percentage.
            positions: Optional position details.
            
        Returns:
            True if broadcast succeeded.
        """
        data = {
            'value': current_value,
            'set_point': set_point,
            'gap': current_value - set_point,
            'gap_percent': ((current_value - set_point) / set_point) * 100,
            'pnl_percent': pnl_percent,
            'positions': positions or {},
            'timestamp': _get_timestamp()
        }
        return self._emit('portfolio_update', data, room='portfolio')
    
    def broadcast_alert(
        self,
        alert_type: str,
        severity: str,
        message: str,
        data: Optional[Dict] = None
    ) -> bool:
        """
        Broadcast critical alert.
        
        Args:
            alert_type: Type of alert (e.g., 'VIX_SPIKE', 'DRAWDOWN', 'KILL_SWITCH').
            severity: Severity level ('info', 'warning', 'critical').
            message: Human-readable alert message.
            data: Additional alert data.
            
        Returns:
            True if broadcast succeeded.
        """
        alert_data = {
            'type': alert_type,
            'severity': severity,
            'message': message,
            'data': data or {},
            'timestamp': _get_timestamp()
        }
        return self._emit('alert', alert_data, room='alerts')
    
        data = {
            'signal': signal_type,
            'symbol': symbol,
            'confidence': confidence,
            'source': source_agent,
            'timestamp': _get_timestamp()
        }
        return self._emit('signal', data, room='signals')

    def broadcast_gene_frequency(self, frequency_data: Dict[str, Any]) -> bool:
        """
        Broadcast gene prevalence trends for the current generation.
        """
        data = {
            'frequencies': frequency_data,
            'timestamp': _get_timestamp()
        }
        return self._emit('gene_frequency_update', data, room='evolution')

    def broadcast_fitness_surface(self, surface_data: List[Dict[str, Any]]) -> bool:
        """
        Broadcast 3D surface plot data for the training terrain.
        """
        data = {
            'surface': surface_data,
            'timestamp': _get_timestamp()
        }
        return self._emit('fitness_surface_update', data, room='evolution')


# Global broadcaster instance
broadcaster = WebSocketBroadcaster()
