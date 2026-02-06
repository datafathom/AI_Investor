
import logging
import asyncio
from typing import Any, Optional

logger = logging.getLogger(__name__)

class SocketManager:
    """
    Centralized manager for Socket.IO operations (FastAPI/ASGI compatible).
    """
    _instance = None
    _sio = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SocketManager, cls).__new__(cls)
        return cls._instance

    def _get_sio(self):
        """Lazy load the Socket.IO server from the gateway."""
        if self._sio is None:
            try:
                from web.socket_gateway import sio
                self._sio = sio
            except ImportError as e:
                logger.error(f"Failed to import Socket.IO server: {e}")
        return self._sio

    def emit_event(self, event: str, data: Any, room: Optional[str] = None, namespace: str = '/'):
        """
        Emits an event to connected clients. 
        Synchronous wrapper for internal service calls.
        """
        sio = self._get_sio()
        if not sio:
            logger.warning("SocketManager: Socket.IO instance not available.")
            return

        # Handle async emit in sync context
        try:
            # If we are already in an event loop, create a task
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(sio.emit(event, data, room=room, namespace=namespace))
            else:
                loop.run_until_complete(sio.emit(event, data, room=room, namespace=namespace))
        except RuntimeError:
            # No event loop, run new one
            asyncio.run(sio.emit(event, data, room=room, namespace=namespace))
        except Exception as e:
            logger.error(f"Failed to emit Socket.IO event: {e}")

def get_socket_manager() -> SocketManager:
    return SocketManager()
