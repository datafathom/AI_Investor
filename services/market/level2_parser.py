"""
Level 2 Market Data Parser.
Normalizes heterogeneous level 2 order book data into a consistent internal format.
"""
from typing import Any, Dict, List, Optional
from datetime import timezone, datetime
import logging

logger = logging.getLogger(__name__)

class Level2Parser:
    """
    Parser for normalized depth data from various liquidity providers.
    """

    @staticmethod
    def parse_depth_event(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parses a raw Kafka message into a structured order book snapshot.
        
        Args:
            payload: Deserialized Kafka message.
            
        Returns:
            Dict: Normalized snapshot or None if corrupted.
        """
        try:
            symbol = payload.get('symbol')
            timestamp_raw = payload.get('timestamp')
            
            if not symbol or not timestamp_raw:
                return None
                
            # Normalize timestamp
            if isinstance(timestamp_raw, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp_raw.replace('Z', '+00:00'))
                except ValueError:
                    timestamp = datetime.now(timezone.utc)
            else:
                timestamp = datetime.now(timezone.utc)

            # Extract Bids and Asks
            bids = payload.get('bids', [])
            asks = payload.get('asks', [])

            # Ensure they are sorted: Bids descending, asks ascending
            sorted_bids = sorted(
                [{'price': float(b['price']), 'size': float(b['size'])} for b in bids],
                key=lambda x: x['price'],
                reverse=True
            )
            sorted_asks = sorted(
                [{'price': float(a['price']), 'size': float(a['size'])} for a in asks],
                key=lambda x: x['price']
            )

            # Basic stats logic
            best_bid = sorted_bids[0]['price'] if sorted_bids else None
            best_ask = sorted_asks[0]['price'] if sorted_asks else None
            spread = (best_ask - best_bid) if (best_bid and best_ask) else None
            mid = (best_ask + best_bid) / 2 if (best_bid and best_ask) else None

            return {
                'symbol': symbol,
                'timestamp': timestamp,
                'bids': sorted_bids,
                'asks': sorted_asks,
                'spread': spread,
                'mid': mid,
                'depth_levels': len(sorted_bids) + len(sorted_asks)
            }
            
        except (ValueError, KeyError, TypeError) as e:
            logger.error("Failed to parse L2 depth event: %s", str(e))
            return None
