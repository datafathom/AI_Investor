import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MiddlewareManager:
    """
    Manages the request/response interceptor chain.
    Allows for runtime inspection and (simulated) toggling of middleware steps.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MiddlewareManager, cls).__new__(cls)
            cls._instance._init_pipeline()
        return cls._instance

    def _init_pipeline(self):
        # Initial pipeline state
        self.pipeline = [
            {"id": "logging", "name": "Structured Logging", "order": 0, "enabled": True, "avg_ms": 1.2},
            {"id": "auth", "name": "JWT Authentication", "order": 1, "enabled": True, "avg_ms": 4.5},
            {"id": "signature", "name": "Sovereign Signature", "order": 2, "enabled": True, "avg_ms": 8.1},
            {"id": "rate_limit", "name": "DDoS Rate Limiter", "order": 3, "enabled": True, "avg_ms": 0.8},
            {"id": "cache", "name": "Performance Cache", "order": 4, "enabled": True, "avg_ms": 2.2},
            {"id": "failover", "name": "Circuit Breaker", "order": 5, "enabled": True, "avg_ms": 0.5}
        ]

    def get_pipeline(self) -> List[Dict[str, Any]]:
        return sorted(self.pipeline, key=lambda x: x['order'])

    def update_order(self, new_order: List[str]):
        """Update middleware execution order."""
        for i, mid in enumerate(new_order):
            for step in self.pipeline:
                if step['id'] == mid:
                    step['order'] = i
        logger.info(f"Middleware pipeline order updated: {new_order}")

    def toggle_middleware(self, middleware_id: str, enabled: bool):
        """Enable or disable a specific middleware."""
        for step in self.pipeline:
            if step['id'] == middleware_id:
                step['enabled'] = enabled
                logger.warning(f"Middleware {middleware_id} {'enabled' if enabled else 'disabled'}")
                return True
        return False

    def get_stats(self) -> Dict[str, Any]:
        """Get performance stats for the pipeline."""
        return {
            "total_avg_ms": sum(s['avg_ms'] for s in self.pipeline if s['enabled']),
            "step_stats": {s['id']: s['avg_ms'] for s in self.pipeline}
        }

def get_middleware_manager() -> MiddlewareManager:
    return MiddlewareManager()
