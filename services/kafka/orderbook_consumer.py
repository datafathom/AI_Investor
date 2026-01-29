"""
Order Book Kafka Consumer.
Subscribes to depth streams and triggers liquidity analysis.
"""
import logging
from typing import Any, Dict, Optional
from services.kafka.consumer import BaseConsumer, ConsumerConfig
from services.market.level2_parser import Level2Parser
from services.market.depth_aggregator import DepthAggregator

logger = logging.getLogger(__name__)

class OrderBookConsumer(BaseConsumer):
    """
    Consumer for high-fidelity order book updates.
    """
    def __init__(self, bootstrap_servers: Optional[str] = None):
        config = ConsumerConfig(
            topics=['orderbook-depth'],
            group_id='ai-investor-depth-monitoring'
        )
        super().__init__(config, bootstrap_servers)
        self.parser = Level2Parser()
        self.aggregator = DepthAggregator()
        # In memory storage for the latest book per symbol
        self.latest_books: Dict[str, Dict] = {}

    def process_message(self, message: Dict[str, Any]) -> None:
        """Process incoming depth message."""
        book = self.parser.parse_depth_event(message)
        if not book:
            return

        symbol = book['symbol']
        self.latest_books[symbol] = book
        
        # Calculate summary metrics
        metrics = self.aggregator.get_total_volume_at_depth(book)
        
        # Forward to risk or monitoring systems
        # For now, just logging identifying significant imbalances
        if abs(metrics['imbalance']) > 0.5:
            logger.warning(f"Significant Liquidity Imbalance in {symbol}: {metrics['imbalance']:.2f}")

    def get_book(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get the latest cached book for a symbol."""
        return self.latest_books.get(symbol)

# Global Instance
orderbook_consumer = OrderBookConsumer()
