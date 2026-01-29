"""
==============================================================================
FILE: services/system/kafka_monitor_service.py
ROLE: Infrastructure Monitoring Service
PURPOSE: Monitors the health, throughput, and consumer lag of the Kafka 
         event streaming platform ("The Nervous System").
         
ARCHITECTURE:
    - Interfaces with Kafka via AdminClient.
    - Provides real-time cluster statistics.
    - Simulates throughput metrics for MVP demo logic where JMX isn't exposed.
    
DEPENDENCIES:
    - kafka-python (KafkaAdminClient)
    - asyncio
==============================================================================
"""
import asyncio
from typing import Dict, List, Any
from kafka.admin import KafkaAdminClient
import logging
import random
from config.environment_manager import get_settings

class KafkaMonitorService:
    """
    Service for monitoring Kafka Cluster health and statistics.
    """
    
    def __init__(self, bootstrap_servers=None):
        """Initialize with bootstrap servers."""
        settings = get_settings()
        self.bootstrap_servers = bootstrap_servers or settings.KAFKA_BOOTSTRAP_SERVERS or "127.0.0.1:9092"
        self.logger = logging.getLogger("KafkaMonitor")
        self._admin_client = None

    def _get_admin_client(self):
        """Lazy load Admin Client connection."""
        if not self._admin_client:
            try:
                self._admin_client = KafkaAdminClient(
                    bootstrap_servers=self.bootstrap_servers,
                    client_id='backend-monitor',
                    request_timeout_ms=1000,
                    reconnect_backoff_ms=500,
                    reconnect_backoff_max_ms=1000
                )
            except Exception as e:
                self.logger.error(f"Failed to connect to Kafka: {e}")
                return None
        return self._admin_client

    async def get_cluster_status(self) -> Dict[str, Any]:
        """
        Retrieves high-level cluster status (healthy/down/topics).
        Run blocking Kafka calls in executor to avoid blocking Main Loop.
        """
        client = self._get_admin_client()
        if not client:
            return {"status": "down", "topics": []}
            
        try:
            # Run blocking call in executor
            topics = await asyncio.to_thread(client.list_topics)
            
            return {
                "status": "healthy",
                "topic_count": len(topics),
                "topics": sorted(list(topics)),
                "broker": self.bootstrap_servers
            }
        except Exception as e:
            self.logger.error(f"Error fetching cluster status: {e}")
            return {"status": "error", "message": str(e)}

    async def get_throughput_stats(self) -> List[Dict]:
        """
        Get throughput statistics per topic.
        
        Currently SIMULATED for MVP demo purposes.
        Production would interface with Prometheus/JMX Exporter.
        
        Returns:
            List[Dict]: List of topic metrics (msg/sec, lag).
        """
        topics = ["market-data", "risk-alerts", "options-flow", "social-sentiment"]
        return [
            {
                "topic": t,
                "msg_per_sec": random.randint(10, 500) if t == "market-data" else random.randint(0, 50),
                "lag": random.randint(0, 5)
            }
            for t in topics
        ]

# Singleton Instance
kafka_monitor_service = KafkaMonitorService()
