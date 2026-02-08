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
        self._global_listeners: List[Callable] = []
        self._history: Dict[str, List[Dict[str, Any]]] = {}
        self._max_history = 1000
        self._stats: Dict[str, Dict[str, Any]] = {}
        logger.info("EventBusService initialized (Global Nervous System Active)")

    def add_global_listener(self, listener: Callable):
        """Register a callback for ALL topics."""
        self._global_listeners.append(listener)
        logger.info("EventBus: New global listener added")

    def subscribe(self, topic: str, handler: Callable):
        """Register a callback for a specific topic."""
        if topic not in self._subscribers:
            self._subscribers[topic] = []
            self._stats[topic] = {"publish_count": 0, "last_published": None}
            self._history[topic] = []
        self._subscribers[topic].append(handler)
        logger.info(f"EventBus: New subscriber for '{topic}'")

    def publish(self, topic: str, payload: Dict[str, Any]):
        """Broadcast an event to all subscribers."""
        logger.info(f"EventBus: Broadcasting '{topic}' -> {payload}")
        
        # Update metrics
        if topic not in self._stats:
            self._stats[topic] = {"publish_count": 0, "last_published": None}
            self._history[topic] = []
        
        self._stats[topic]["publish_count"] += 1
        self._stats[topic]["last_published"] = datetime.now().isoformat()
        
        # Store in history
        self._history[topic].append({
            "timestamp": datetime.now().isoformat(),
            "payload": payload
        })
        if len(self._history[topic]) > self._max_history:
            self._history[topic].pop(0)

        # Notify global listeners
        for listener in self._global_listeners:
            try:
                listener(topic, payload)
            except Exception as e:
                logger.error(f"EventBus: Error in global listener: {e}")

        if topic in self._subscribers:
            for handler in self._subscribers[topic]:
                try:
                    handler(payload)
                except Exception as e:
                    logger.error(f"EventBus: Error in handler for '{topic}': {e}")

    def get_stats(self) -> Dict[str, Any]:
        """Get throughput metrics per topic."""
        return {
            "total_topics": len(self._stats),
            "topics": self._stats
        }

    def get_recent_messages(self, topic: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Recent messages for a topic (paginated)."""
        if topic not in self._history:
            return []
        
        # Simple slicing for pagination on the list
        messages = list(reversed(self._history[topic])) # Show newest first
        start = offset
        end = offset + limit
        return messages[start:end]

    def get_all_topics_metadata(self) -> List[Dict[str, Any]]:
        """List all topics with metadata."""
        topics = []
        for topic in self._stats:
            topics.append({
                "topic": topic,
                "subscriber_count": len(self._subscribers.get(topic, [])),
                "publish_count": self._stats[topic]["publish_count"],
                "last_published": self._stats[topic]["last_published"]
            })
        return topics

from datetime import datetime
