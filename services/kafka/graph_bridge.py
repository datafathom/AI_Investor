"""
Graph Bridge Service.
Bridges Kafka price events to Neo4j correlation updates.
"""
import logging
from typing import Any, Dict, List
from services.kafka.consumer import BaseConsumer, ConsumerConfig
from services.rolling_window import rolling_window_service
from services.correlation_calculator import CorrelationCalculator
from services.neo4j.edge_weight_updater import edge_weight_updater

logger = logging.getLogger(__name__)

class GraphBridge(BaseConsumer):
    def __init__(self, bootstrap_servers: str = None):
        config = ConsumerConfig(
            topics=['market.fx', 'market.equity'], # Listen to both for correlations
            group_id='ai-investor-graph-bridge'
        )
        super().__init__(config, bootstrap_servers)
        self.calculator = CorrelationCalculator()
        self.symbols_tracked = set()

    def process_message(self, message: Dict[str, Any]) -> None:
        """Process price update and recalculate correlations."""
        symbol = message.get('symbol')
        price = message.get('price', message.get('mid', message.get('value')))
        
        if not symbol or price is None:
            return

        # 1. Update rolling window
        rolling_window_service.add_price(symbol, price)
        self.symbols_tracked.add(symbol)

        # 2. Recalculate correlations with other tracked symbols
        # For efficiency, we only update correlations for the symbol that changed
        # compared to all other symbols currently in memory.
        
        history1 = rolling_window_service.get_history(symbol)
        if len(history1) < 10: # Minimum data points for meaningful correlation
            return

        for other_symbol in self.symbols_tracked:
            if other_symbol == symbol:
                continue
                
            history2 = rolling_window_service.get_history(other_symbol)
            if len(history2) < 10:
                continue

            # Calculate correlation
            coefficient, confidence = self.calculator.calculate_pearson(history1, history2)
            
            # 3. Update Neo4j
            edge_weight_updater.update_correlation(
                symbol, 
                other_symbol, 
                coefficient, 
                confidence
            )

# Global Instance (Note: Start/Stop managed externally)
graph_bridge = GraphBridge()
