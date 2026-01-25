
import logging
from flask_socketio import SocketIO
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)

class SocketManager:
    """
    Centralized manager for Socket.IO operations, supporting horizontal scaling via Redis.
    """
    _instance = None
    _socketio = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SocketManager, cls).__new__(cls)
        return cls._instance

    def init_app(self, app, socketio_instance: SocketIO):
        """Initializes the manager with the Socket.IO instance."""
        self._socketio = socketio_instance
        logger.info("SocketManager initialized.")

    def emit_event(self, event: str, data: any, room: str = None, namespace: str = '/'):
        """
        Emits an event to connected clients. 
        If scaled with Redis, this will broadcast to all server nodes.
        """
        if self._socketio:
            self._socketio.emit(event, data, room=room, namespace=namespace)
            logger.debug(f"Emitted event '{event}' to room '{room}'")
        else:
            logger.warning("SocketManager: SocketIO instance not initialized. Cannot emit.")

    def join_room(self, sid, room, namespace='/'):
        """Adds a client to a room."""
        if self._socketio:
            self._socketio.server.enter_room(sid, room, namespace=namespace)

def get_socket_manager() -> SocketManager:
    return SocketManager()
