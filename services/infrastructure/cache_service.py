import json
import hashlib
import os
import logging
import time
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentResponseCache:
    """
    Persistent cache for agent LLM responses to reduce latency and API costs.
    Uses JSON-based storage for now, easily migratable to Redis or SQLite.
    """
    def __init__(self, cache_dir: str = "data/cache/agents"):
        self.cache_dir = cache_dir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        logger.info(f"AgentResponseCache initialized at {self.cache_dir}")

    def _generate_key(self, agent_id: str, prompt: str, system_message: Optional[str] = None) -> str:
        """Generate a unique MD5 key based on the agent and prompt content."""
        content = f"{agent_id}:{system_message or ''}:{prompt}"
        return hashlib.md5(content.encode('utf-8')).hexdigest()

    def get(self, agent_id: str, prompt: str, system_message: Optional[str] = None) -> Optional[str]:
        """Retrieve a cached response if it exists."""
        key = self._generate_key(agent_id, prompt, system_message)
        file_path = os.path.join(self.cache_dir, f"{key}.json")
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    # Check TTL (default 24 hours) - simplified for now
                    logger.info(f"Cache HIT for agent {agent_id}")
                    return data.get("response")
            except Exception as e:
                logger.error(f"Error reading cache file {file_path}: {e}")
        
        return None

    def set(self, agent_id: str, prompt: str, response: str, system_message: Optional[str] = None) -> None:
        """Store a response in the cache."""
        key = self._generate_key(agent_id, prompt, system_message)
        file_path = os.path.join(self.cache_dir, f"{key}.json")
        
        cache_data = {
            "agent_id": agent_id,
            "prompt": prompt,
            "system_message": system_message,
            "response": response,
            "cached_at": datetime.now().isoformat()
        }
        
        try:
            with open(file_path, 'w') as f:
                json.dump(cache_data, f, indent=2)
            logger.info(f"Cached response for agent {agent_id}")
        except Exception as e:
            logger.error(f"Error writing cache file {file_path}: {e}")

# Singleton helper
_cache_instance = None
def get_agent_cache() -> AgentResponseCache:
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = AgentResponseCache()
    return _cache_instance
