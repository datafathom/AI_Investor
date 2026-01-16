"""
==============================================================================
AI Investor - Kafka Base Consumer
==============================================================================
PURPOSE:
    Abstract base class for Kafka consumers. Provides common functionality
    for all agents that consume events from the Kafka event bus.

PATTERN:
    Agents inherit from BaseConsumer and implement process_message().
    The consumer handles connection, deserialization, and error recovery.

USAGE:
    class VIXConsumer(BaseConsumer):
        def process_message(self, message):
            self.agent.process_event(message)
==============================================================================
"""
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional
import json
import os
import logging
import threading
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ConsumerConfig:
    """Configuration for a Kafka consumer."""
    topics: List[str]
    group_id: str
    auto_offset_reset: str = 'earliest'
    enable_auto_commit: bool = True
    max_poll_interval_ms: int = 300000
    session_timeout_ms: int = 45000


class BaseConsumer(ABC):
    """
    Abstract base class for Kafka message consumers.
    
    Provides connection management, message deserialization, and
    background consumption loop for all AI Investor agents.
    
    Attributes:
        config (ConsumerConfig): Consumer configuration.
        bootstrap_servers (str): Kafka broker connection string.
        is_running (bool): Whether consumer loop is active.
    """
    
    def __init__(
        self, 
        config: ConsumerConfig,
        bootstrap_servers: Optional[str] = None
    ) -> None:
        """
        Initialize the base consumer.
        
        Args:
            config: Consumer configuration including topics and group ID.
            bootstrap_servers: Kafka broker address. Defaults to env var.
        """
        self.config = config
        self.bootstrap_servers = bootstrap_servers or os.getenv(
            'KAFKA_BOOTSTRAP_SERVERS',
            'localhost:9092'
        )
        self._consumer = None
        self._consume_thread: Optional[threading.Thread] = None
        self.is_running = False
        self._error_count = 0
        self._max_errors = 10  # Circuit breaker threshold
        
        logger.info(f"BaseConsumer initialized for topics: {config.topics}")
    
    @property
    def consumer(self):
        """Lazy-load the Kafka Consumer."""
        if self._consumer is None:
            try:
                from confluent_kafka import Consumer
                self._consumer = Consumer({
                    'bootstrap.servers': self.bootstrap_servers,
                    'group.id': self.config.group_id,
                    'auto.offset.reset': self.config.auto_offset_reset,
                    'enable.auto.commit': self.config.enable_auto_commit,
                    'max.poll.interval.ms': self.config.max_poll_interval_ms,
                    'session.timeout.ms': self.config.session_timeout_ms,
                })
            except ImportError:
                logger.error("confluent-kafka not installed")
                raise
        return self._consumer
    
    @abstractmethod
    def process_message(self, message: Dict[str, Any]) -> None:
        """
        Process a single message from Kafka.
        
        Args:
            message: Deserialized message payload.
            
        Must be implemented by subclasses.
        """
        pass
    
    def deserialize(self, raw_message: bytes) -> Optional[Dict[str, Any]]:
        """
        Deserialize a raw Kafka message.
        
        Args:
            raw_message: Raw bytes from Kafka.
            
        Returns:
            Deserialized dictionary, or None if deserialization fails.
        """
        try:
            return json.loads(raw_message.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.error(f"Failed to deserialize message: {e}")
            return None
    
    def start(self) -> None:
        """Start consuming messages in a background thread."""
        if self.is_running:
            logger.warning("Consumer is already running")
            return
        
        self.consumer.subscribe(self.config.topics)
        self.is_running = True
        self._error_count = 0
        
        self._consume_thread = threading.Thread(
            target=self._consume_loop,
            daemon=True
        )
        self._consume_thread.start()
        
        logger.info(f"Consumer started for topics: {self.config.topics}")
    
    def stop(self) -> None:
        """Stop the consumer gracefully."""
        self.is_running = False
        
        if self._consume_thread and self._consume_thread.is_alive():
            self._consume_thread.join(timeout=5.0)
        
        if self._consumer:
            self._consumer.close()
            self._consumer = None
        
        logger.info("Consumer stopped")
    
    def _consume_loop(self) -> None:
        """Internal consumption loop running in background thread."""
        while self.is_running:
            try:
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    self._handle_error(msg.error())
                    continue
                
                # Deserialize and process
                payload = self.deserialize(msg.value())
                if payload:
                    try:
                        self.process_message(payload)
                        self._error_count = 0  # Reset on success
                    except Exception as e:
                        logger.exception(f"Error processing message: {e}")
                        self._error_count += 1
                        
            except Exception as e:
                logger.exception(f"Consumer loop error: {e}")
                self._error_count += 1
            
            # Circuit breaker
            if self._error_count >= self._max_errors:
                logger.critical(f"Circuit breaker triggered after {self._max_errors} errors")
                self.is_running = False
                break
    
    def _handle_error(self, error) -> None:
        """Handle Kafka consumer errors."""
        from confluent_kafka import KafkaError
        
        if error.code() == KafkaError._PARTITION_EOF:
            # End of partition is not an error
            logger.debug(f"Reached end of partition: {error}")
        else:
            logger.error(f"Kafka error: {error}")
            self._error_count += 1
    
    def health_check(self) -> Dict[str, Any]:
        """
        Return consumer health status.
        
        Returns:
            Dictionary with consumer health information.
        """
        return {
            'is_running': self.is_running,
            'topics': self.config.topics,
            'group_id': self.config.group_id,
            'error_count': self._error_count,
            'circuit_breaker_threshold': self._max_errors,
            'healthy': self.is_running and self._error_count < self._max_errors
        }


class VIXConsumer(BaseConsumer):
    """
    Consumer for VIX market data events.
    
    Forwards VIX updates to the Protector Agent for volatility monitoring.
    """
    
    def __init__(self, agent=None, bootstrap_servers: Optional[str] = None) -> None:
        """
        Initialize VIX consumer.
        
        Args:
            agent: Agent instance to forward events to.
            bootstrap_servers: Kafka broker address.
        """
        config = ConsumerConfig(
            topics=['market.vix'],
            group_id='ai-investor-vix-consumers'
        )
        super().__init__(config, bootstrap_servers)
        self.agent = agent
    
    def process_message(self, message: Dict[str, Any]) -> None:
        """Process VIX update message."""
        logger.debug(f"Received VIX update: {message}")
        
        if self.agent:
            result = self.agent.process_event({
                'type': 'VIX_UPDATE',
                'vix_level': message.get('value', message.get('vix_level')),
                **message
            })
            if result:
                logger.info(f"Agent action: {result}")


class EquityConsumer(BaseConsumer):
    """
    Consumer for equity price events.
    
    Forwards stock/ETF updates to the Searcher Agent for opportunity detection.
    """
    
    def __init__(self, agent=None, bootstrap_servers: Optional[str] = None) -> None:
        """Initialize equity consumer."""
        config = ConsumerConfig(
            topics=['market.equity'],
            group_id='ai-investor-equity-consumers'
        )
        super().__init__(config, bootstrap_servers)
        self.agent = agent
    
    def process_message(self, message: Dict[str, Any]) -> None:
        """Process equity price message."""
        logger.debug(f"Received equity update: {message.get('symbol')}")
        
        if self.agent:
            self.agent.process_event({
                'type': 'EQUITY_UPDATE',
                **message
            })


class SignalConsumer(BaseConsumer):
    """
    Consumer for inter-agent signals.
    
    Enables communication between agents via the event bus.
    """
    
    def __init__(
        self, 
        callback: Optional[Callable[[Dict], None]] = None,
        bootstrap_servers: Optional[str] = None
    ) -> None:
        """
        Initialize signal consumer.
        
        Args:
            callback: Function to call when signal is received.
            bootstrap_servers: Kafka broker address.
        """
        config = ConsumerConfig(
            topics=['agent.signals'],
            group_id='ai-investor-signal-consumers'
        )
        super().__init__(config, bootstrap_servers)
        self.callback = callback
    
    def process_message(self, message: Dict[str, Any]) -> None:
        """Process inter-agent signal."""
        logger.debug(f"Received signal: {message.get('signal_type')}")
        
        if self.callback:
            self.callback(message)
