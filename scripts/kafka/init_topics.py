"""
==============================================================================
AI Investor - Kafka Topic Configuration & Initialization
==============================================================================
PURPOSE:
    Initialize Kafka topics for the AI Investor event bus. Creates the
    required topics for market data streaming: VIX, equity, and macro events.

USAGE:
    python scripts/kafka/init_topics.py
    
    Or programmatically:
        from scripts.kafka.init_topics import KafkaTopicManager
        manager = KafkaTopicManager()
        manager.create_all_topics()

TOPICS:
    - market.vix: VIX volatility index updates
    - market.equity: Individual stock/ETF price events
    - market.macro: Macroeconomic indicators (GDP, rates, etc.)
==============================================================================
"""
from typing import Dict, List, Optional
import os
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Topic configuration
TOPIC_CONFIG: Dict[str, Dict] = {
    'market.vix': {
        'description': 'VIX volatility index updates for Protector Agent',
        'partitions': 1,
        'replication_factor': 1,
        'retention_ms': 86400000 * 7,  # 7 days
    },
    'market.equity': {
        'description': 'Individual stock and ETF price updates',
        'partitions': 4,
        'replication_factor': 1,
        'retention_ms': 86400000 * 30,  # 30 days
    },
    'market.macro': {
        'description': 'Macroeconomic indicators (GDP, rates, unemployment)',
        'partitions': 1,
        'replication_factor': 1,
        'retention_ms': 86400000 * 90,  # 90 days
    },
    'agent.signals': {
        'description': 'Inter-agent signal communication',
        'partitions': 2,
        'replication_factor': 1,
        'retention_ms': 86400000 * 1,  # 1 day
    },
    'portfolio.updates': {
        'description': 'Portfolio value and position updates',
        'partitions': 1,
        'replication_factor': 1,
        'retention_ms': 86400000 * 30,  # 30 days
    },
}


@dataclass
class TopicSpec:
    """Specification for a Kafka topic."""
    name: str
    partitions: int
    replication_factor: int
    config: Dict[str, str]


class KafkaTopicManager:
    """
    Manager for Kafka topic creation and administration.
    
    Handles topic lifecycle including creation, verification, and deletion.
    Uses confluent-kafka AdminClient for topic management.
    
    Attributes:
        bootstrap_servers (str): Kafka broker connection string.
        admin_client: Kafka AdminClient instance (lazy loaded).
    """
    
    def __init__(self, bootstrap_servers: Optional[str] = None) -> None:
        """
        Initialize the Kafka Topic Manager.
        
        Args:
            bootstrap_servers: Kafka broker address. Defaults to env var or localhost.
        """
        self.bootstrap_servers = bootstrap_servers or os.getenv(
            'KAFKA_BOOTSTRAP_SERVERS', 
            'localhost:9092'
        )
        self._admin_client = None
        logger.info(f"KafkaTopicManager initialized for {self.bootstrap_servers}")
    
    @property
    def admin_client(self):
        """Lazy-load the Kafka AdminClient."""
        if self._admin_client is None:
            try:
                from confluent_kafka.admin import AdminClient
                self._admin_client = AdminClient({
                    'bootstrap.servers': self.bootstrap_servers
                })
            except ImportError:
                logger.error("confluent-kafka not installed. Run: pip install confluent-kafka")
                raise
        return self._admin_client
    
    def get_topic_specs(self) -> List[TopicSpec]:
        """
        Get topic specifications from configuration.
        
        Returns:
            List of TopicSpec objects for all configured topics.
        """
        specs = []
        for name, config in TOPIC_CONFIG.items():
            specs.append(TopicSpec(
                name=name,
                partitions=config['partitions'],
                replication_factor=config['replication_factor'],
                config={'retention.ms': str(config['retention_ms'])}
            ))
        return specs
    
    def create_topic(self, spec: TopicSpec) -> bool:
        """
        Create a single Kafka topic.
        
        Args:
            spec: Topic specification.
            
        Returns:
            True if topic was created successfully, False otherwise.
        """
        try:
            from confluent_kafka.admin import NewTopic
            
            new_topic = NewTopic(
                spec.name,
                num_partitions=spec.partitions,
                replication_factor=spec.replication_factor,
                config=spec.config
            )
            
            futures = self.admin_client.create_topics([new_topic])
            
            for topic, future in futures.items():
                try:
                    future.result()  # Wait for topic creation
                    logger.info(f"✅ Created topic: {topic}")
                    return True
                except Exception as e:
                    if 'already exists' in str(e).lower():
                        logger.info(f"ℹ️ Topic already exists: {topic}")
                        return True
                    logger.error(f"❌ Failed to create topic {topic}: {e}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error creating topic {spec.name}: {e}")
            return False
    
    def create_all_topics(self) -> Dict[str, bool]:
        """
        Create all configured topics.
        
        Returns:
            Dictionary mapping topic names to creation success status.
        """
        results = {}
        specs = self.get_topic_specs()
        
        logger.info(f"Creating {len(specs)} Kafka topics...")
        
        for spec in specs:
            results[spec.name] = self.create_topic(spec)
        
        success_count = sum(results.values())
        logger.info(f"Topic creation complete: {success_count}/{len(specs)} successful")
        
        return results
    
    def list_topics(self) -> List[str]:
        """
        List all existing topics on the Kafka cluster.
        
        Returns:
            List of topic names.
        """
        try:
            metadata = self.admin_client.list_topics(timeout=10)
            topics = list(metadata.topics.keys())
            return [t for t in topics if not t.startswith('__')]  # Exclude internal topics
        except Exception as e:
            logger.error(f"Error listing topics: {e}")
            return []
    
    def verify_topics(self) -> Dict[str, bool]:
        """
        Verify that all required topics exist.
        
        Returns:
            Dictionary mapping topic names to existence status.
        """
        existing = set(self.list_topics())
        required = set(TOPIC_CONFIG.keys())
        
        return {topic: topic in existing for topic in required}
    
    def delete_topic(self, topic_name: str) -> bool:
        """
        Delete a Kafka topic.
        
        Args:
            topic_name: Name of topic to delete.
            
        Returns:
            True if deletion successful, False otherwise.
        """
        try:
            futures = self.admin_client.delete_topics([topic_name])
            
            for topic, future in futures.items():
                try:
                    future.result()
                    logger.info(f"🗑️ Deleted topic: {topic}")
                    return True
                except Exception as e:
                    logger.error(f"Failed to delete topic {topic}: {e}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting topic {topic_name}: {e}")
            return False


def main():
    """CLI entry point for topic initialization."""
    import argparse
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    parser = argparse.ArgumentParser(description='Kafka Topic Manager')
    parser.add_argument('--bootstrap-servers', default=None, 
                        help='Kafka bootstrap servers')
    parser.add_argument('--list', action='store_true', help='List existing topics')
    parser.add_argument('--verify', action='store_true', help='Verify required topics exist')
    parser.add_argument('--create', action='store_true', help='Create all topics')
    
    args = parser.parse_args()
    
    manager = KafkaTopicManager(args.bootstrap_servers)
    
    if args.list:
        topics = manager.list_topics()
        print(f"\nExisting topics ({len(topics)}):")
        for topic in sorted(topics):
            print(f"  - {topic}")
    
    elif args.verify:
        status = manager.verify_topics()
        print("\nTopic verification:")
        for topic, exists in status.items():
            status_icon = "✅" if exists else "❌"
            print(f"  {status_icon} {topic}")
    
    elif args.create:
        results = manager.create_all_topics()
        print("\nTopic creation results:")
        for topic, success in results.items():
            status_icon = "✅" if success else "❌"
            print(f"  {status_icon} {topic}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
