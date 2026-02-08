import logging
import asyncio
from typing import Dict, Any
from datetime import datetime, timezone
import socketio
from services.infrastructure.event_bus import EventBusService

logger = logging.getLogger("EventBusWS")

# Create Socket.IO server for event bus monitoring
eb_sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"]
)
eb_socket_app = socketio.ASGIApp(eb_sio, socketio_path='')

@eb_sio.event
async def connect(sid: str, environ: Dict, auth: Any = None):
    logger.info(f"Client connected to EventBus WS: {sid}")
    await eb_sio.emit('connected', {
        'status': 'connected',
        'message': 'Event Bus Monitor Stream Online',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }, to=sid)

@eb_sio.event
async def disconnect(sid: str):
    logger.info(f"Client disconnected from EventBus WS: {sid}")

def start_event_bus_broadcast():
    """Subscribe to all event bus topics and broadcast to WS clients."""
    eb = EventBusService()
    
    def handle_event(topic: str, payload: Dict[str, Any]):
        try:
            # We use eb_sio.emit which is async. 
            # EventBusService calls handlers synchronously. 
            # We need a safe way to run this.
            try:
                loop = asyncio.get_running_loop()
                asyncio.run_coroutine_threadsafe(
                    eb_sio.emit('event', {
                        'topic': topic,
                        'payload': payload,
                        'timestamp': datetime.now(timezone.utc).isoformat()
                    }),
                    loop
                )
            except RuntimeError:
                # No running event loop in this thread
                pass
        except Exception as e:
            logger.error(f"Error in EventBus WS broadcast: {e}")

    eb.add_global_listener(handle_event)
    logger.info("EventBus WS Broadcaster initialized")
