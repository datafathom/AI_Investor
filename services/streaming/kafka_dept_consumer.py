"""
==============================================================================
FILE: services/streaming/kafka_dept_consumer.py
ROLE: Kafka Consumer for Department Topics
PURPOSE: Consumes messages from department-specific Kafka topics and relays
         them to WebSocket clients via the DepartmentBroadcaster.

TOPICS:
    - dept.{id}.events   - Department events (retention: 7d)
    - dept.{id}.metrics  - Performance metrics (retention: 24h)
    - dept.{id}.agents   - Agent status updates (retention: 1h)
    
ARCHITECTURE:
    - Async consumer using aiokafka
    - Falls back to simulation mode if Kafka unavailable
    - Integrates with department_gateway for broadcasting
    
DEPENDENCIES:
    - aiokafka (optional, falls back to simulation)
==============================================================================
"""
import asyncio
import json
import logging
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timezone
import random

from config.environment_manager import get_settings

logger = logging.getLogger("KafkaDeptConsumer")

# Topic patterns
TOPIC_EVENTS = "dept.{dept_id}.events"
TOPIC_METRICS = "dept.{dept_id}.metrics"
TOPIC_AGENTS = "dept.{dept_id}.agents"
TOPIC_TELEMETRY = "telemetry.stream"
TOPIC_ALERTS = "system.alerts"


class KafkaDepartmentConsumer:
    """
    Consumes department-related Kafka topics and broadcasts to WebSocket.
    Falls back to simulation mode if Kafka is unavailable.
    """
    
    def __init__(self, department_ids: Optional[List[int]] = None) -> None:
        """
        Initialize consumer for specified departments.
        
        Args:
            department_ids: List of department IDs to subscribe to. 
                          If None, subscribes to all (1-18).
        """
        settings = get_settings()
        self.bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS or "127.0.0.1:9092"
        self.department_ids = department_ids or list(range(1, 19))
        self.consumer = None
        self.running = False
        self.simulated = False
        self._broadcast_callback: Optional[Callable] = None
    
    def set_broadcast_callback(self, callback: Callable[[int, str, Dict], Any]) -> None:
        """
        Set callback for broadcasting messages.
        
        Callback signature: (dept_id: int, topic_type: str, message: Dict) -> None
        topic_type is one of: 'events', 'metrics', 'agents'
        """
        self._broadcast_callback = callback
    
    async def start(self) -> None:
        """Start consuming from Kafka topics."""
        if self.running:
            return
        
        self.running = True
        
        try:
            # Try to import and connect to Kafka
            from aiokafka import AIOKafkaConsumer
            
            topics = self._build_topic_list()
            
            self.consumer = AIOKafkaConsumer(
                *topics,
                bootstrap_servers=self.bootstrap_servers,
                group_id='dept-websocket-relay',
                auto_offset_reset='latest',
                enable_auto_commit=True,
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            
            await self.consumer.start()
            logger.info(f"Kafka consumer started for {len(topics)} topics")
            
            # Start consumption loop
            asyncio.create_task(self._consume_loop())
            
        except ImportError:
            logger.warning("aiokafka not installed. Running in SIMULATION mode.")
            self.simulated = True
            asyncio.create_task(self._simulation_loop())
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}. Running in SIMULATION mode.")
            self.simulated = True
            asyncio.create_task(self._simulation_loop())
    
    async def stop(self) -> None:
        """Stop the consumer."""
        self.running = False
        if self.consumer:
            await self.consumer.stop()
            logger.info("Kafka consumer stopped")
    
    def _build_topic_list(self) -> List[str]:
        """Build list of topics to subscribe to."""
        topics = [TOPIC_TELEMETRY, TOPIC_ALERTS]
        for dept_id in self.department_ids:
            topics.extend([
                TOPIC_EVENTS.format(dept_id=dept_id),
                TOPIC_METRICS.format(dept_id=dept_id),
                TOPIC_AGENTS.format(dept_id=dept_id)
            ])
        return topics
    
    async def _consume_loop(self) -> None:
        """Main consumption loop for real Kafka messages."""
        try:
            async for msg in self.consumer:
                if not self.running:
                    break
                
                await self._process_message(msg.topic, msg.value)
                
        except Exception as e:
            logger.exception(f"Error in Kafka consumption loop: {e}")
            # Fall back to simulation
            self.simulated = True
            asyncio.create_task(self._simulation_loop())
    
    async def _process_message(self, topic: str, value: Dict[str, Any]) -> None:
        """Process a Kafka message and broadcast to WebSocket clients."""
        # Parse topic to extract dept_id and type
        parts = topic.split('.')
        
        if len(parts) == 3 and parts[0] == 'dept':
            dept_id = int(parts[1])
            topic_type = parts[2]  # events, metrics, or agents
            
            if self._broadcast_callback:
                await self._broadcast_callback(dept_id, topic_type, value)
        
        elif topic == TOPIC_TELEMETRY:
            # Broadcast to all departments
            if self._broadcast_callback:
                for dept_id in self.department_ids:
                    await self._broadcast_callback(dept_id, 'telemetry', value)
        
        elif topic == TOPIC_ALERTS:
            # Broadcast system alerts to all
            if self._broadcast_callback:
                for dept_id in self.department_ids:
                    await self._broadcast_callback(dept_id, 'alert', value)
    
    async def _simulation_loop(self) -> None:
        """
        Simulate Kafka messages for development/demo without Kafka.
        Generates realistic-looking department updates.
        """
        logger.info("Starting Kafka simulation loop")
        
        agent_statuses = ['IDLE', 'BUSY', 'SUCCESS', 'ERROR']
        event_types = ['task_completed', 'alert_triggered', 'config_changed', 'health_check']
        
        while self.running:
            await asyncio.sleep(random.uniform(2.0, 8.0))  # Random interval
            
            if not self._broadcast_callback:
                continue
            
            # Pick a random department
            dept_id = random.choice(self.department_ids)
            
            # Generate random message type
            msg_type = random.choice(['agents', 'metrics', 'events'])
            
            if msg_type == 'agents':
                message = {
                    'agent_id': f"agent_{random.randint(1, 5)}",
                    'status': random.choice(agent_statuses),
                    'cpu_usage': round(random.uniform(5, 80), 1),
                    'memory_mb': random.randint(100, 500),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            elif msg_type == 'metrics':
                message = {
                    'requests_per_sec': random.randint(10, 500),
                    'avg_latency_ms': round(random.uniform(10, 200), 1),
                    'error_rate': round(random.uniform(0, 5), 2),
                    'active_connections': random.randint(1, 50),
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            else:  # events
                message = {
                    'event_type': random.choice(event_types),
                    'severity': random.choice(['INFO', 'WARNING', 'ERROR']),
                    'description': f"Simulated event for department {dept_id}",
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
            
            try:
                await self._broadcast_callback(dept_id, msg_type, message)
            except Exception as e:
                logger.debug(f"Broadcast error (likely no subscribers): {e}")


# Singleton instance
_consumer_instance: Optional[KafkaDepartmentConsumer] = None


def get_dept_consumer() -> KafkaDepartmentConsumer:
    """Get or create the singleton Kafka department consumer."""
    global _consumer_instance
    if _consumer_instance is None:
        _consumer_instance = KafkaDepartmentConsumer()
    return _consumer_instance


async def start_dept_consumer() -> KafkaDepartmentConsumer:
    """Start the department consumer and return it."""
    consumer = get_dept_consumer()
    await consumer.start()
    return consumer
