import logging
from typing import Callable, List, Dict, Any

logger = logging.getLogger(__name__)

class EventBusService:
    """
    Global Nervous System.
    Propagates events across the entire architecture.
    Example: 'Geopolitical Shock' (Phase 187) -> 'Margin Call' (Phase 136).
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(EventBusService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self._subscribers: Dict[str, List[Callable]] = {}
        logger.info("EventBusService initialized (Global Nervous System Active)")

    def subscribe(self, topic: str, handler: Callable):
        """Register a callback for a specific topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(handler)
        logger.info(f"EventBus: New subscriber for '{topic}'")

    def publish(self, topic: str, payload: Dict[str, Any]):
        """Broadcast an event to all subscribers."""
        logger.info(f"EventBus: Broadcasting '{topic}' -> {payload}")
        if topic in self._subscribers:
            for handler in self._subscribers[topic]:
                try:
                    handler(payload)
                except Exception as e:
                    logger.error(f"EventBus: Error in handler for '{topic}': {e}")
