import logging
import asyncio
from typing import Dict, Any
from datetime import datetime, timezone
from services.infrastructure.event_bus import EventBusService
import web.socket_gateway

logger = logging.getLogger("EventBusWS")

EVENT_BUS_NAMESPACE = "/admin/event-bus"

def register_event_bus_handlers(sio):
    """Register handlers for the Event Bus namespace."""
    
    @sio.event(namespace=EVENT_BUS_NAMESPACE)
    async def connect(sid, environ, auth=None):
        logger.info(f"Client connected to EventBus WS: {sid}")
        await sio.emit('connected', {
            'status': 'connected',
            'message': 'Event Bus Monitor Stream Online',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }, to=sid, namespace=EVENT_BUS_NAMESPACE)

    @sio.event(namespace=EVENT_BUS_NAMESPACE)
    async def disconnect(sid):
        logger.info(f"Client disconnected from EventBus WS: {sid}")

def start_event_bus_broadcast():
    """Subscribe to all event bus topics and broadcast to WS clients."""
    eb = EventBusService()
    sio = web.socket_gateway.get_sio()
    
    # Register handlers on the main SIO instance
    register_event_bus_handlers(sio)

    def handle_event(topic: str, payload: Dict[str, Any]):
        try:
            try:
                loop = asyncio.get_running_loop()
                # We are in the loop, use create_task
                loop.create_task(
                    sio.emit('event', {
                        'topic': topic,
                        'payload': payload,
                        'timestamp': datetime.now(timezone.utc).isoformat()
                    }, namespace=EVENT_BUS_NAMESPACE)
                )

            except RuntimeError:
                # No running event loop in this thread
                pass
        except Exception as e:
            logger.error(f"Error in EventBus WS broadcast: {e}")

    eb.add_global_listener(handle_event)
    logger.info("EventBus WS Broadcaster initialized (Namespace Mode)")
