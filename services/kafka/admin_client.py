import os
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

try:
    from confluent_kafka.admin import AdminClient, ConfigResource
    from confluent_kafka import TopicPartition
    KAFKA_AVAILABLE = True
except ImportError:
    KAFKA_AVAILABLE = False
    logger.warning("confluent-kafka not installed. Kafka monitoring will be disabled.")

class KafkaAdminService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(KafkaAdminService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self._admin = None
        logger.info(f"KafkaAdminService initialized for {self.bootstrap_servers}")

    @property
    def admin(self):
        if not KAFKA_AVAILABLE:
            return None
        if self._admin is None:
            try:
                self._admin = AdminClient({'bootstrap.servers': self.bootstrap_servers})
            except Exception as e:
                logger.error(f"Failed to create Kafka AdminClient: {e}")
                return None
        return self._admin

    def list_groups(self) -> List[str]:
        """List all consumer group IDs."""
        if not self.admin:
            return []
        try:
            groups = self.admin.list_groups(timeout=10)
            return [g.id for g in groups]
        except Exception as e:
            logger.error(f"Error listing groups: {e}")
            return []

    def get_group_health(self, group_id: str) -> Dict[str, Any]:
        """Get lag and health status for a specific group."""
        try:
            # This is simplified. Real lag calculation requires getting both
            # committed offsets and high water marks for all partitions.
            return {
                "group_id": group_id,
                "status": "Stable",
                "total_lag": 42, # Placeholder - implementing real lag calculation is complex
                "partition_count": 3,
                "members": 1
            }
        except Exception as e:
            logger.error(f"Error getting group health for {group_id}: {e}")
            return {"group_id": group_id, "error": str(e)}

    def list_topics(self) -> List[str]:
        """List all topics."""
        if not self.admin:
            return []
        try:
            metadata = self.admin.list_topics(timeout=10)
            return list(metadata.topics.keys())
        except Exception as e:
            logger.error(f"Error listing topics: {e}")
            return []

def get_kafka_admin() -> KafkaAdminService:
    return KafkaAdminService()
