"""
Supply and Demand Zone Detection Service.
Identifies areas of significant institutional interest.
"""
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SupplyDemandDetector:
    """
    Identifies 'Supply' and 'Demand' zones based on price imbalances.
    Zones are areas where price left rapidly, indicating unfilled institutional orders.
    """

    @staticmethod
    def identify_zones(candles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Identify S&D zones from OHLC data.
        Look for 'Rally-Base-Drop' (Supply) or 'Drop-Base-Rally' (Demand) patterns.
        """
        zones = []
        if len(candles) < 3:
            return []

        for i in range(1, len(candles) - 1):
            prev = candles[i-1]
            base = candles[i]
            rally_drop = candles[i+1]

            # DEMAND: Drop-Base-Rally or Rally-Base-Rally
            # Criterion: Next candle has a large body move UP.
            min_expansion = 0.0010 # 10 pips for S&D
            if rally_drop['close'] > rally_drop['open']:
                body = rally_drop['close'] - rally_drop['open']
                avg_body = sum(abs(c['close'] - c['open']) for c in candles[max(0, i-5):i]) / 5 if i > 0 else body
                
                if body > min_expansion and body > (avg_body * 2): # Explosive move
                    zones.append({
                        'type': 'DEMAND',
                        'price_high': base['high'],
                        'price_low': base['low'],
                        'timestamp': base['timestamp'],
                        'mitigated': False,
                        'strength': float(body)
                    })

            # SUPPLY: Rally-Base-Drop or Drop-Base-Drop
            # Criterion: Next candle has a large body move DOWN.
            elif rally_drop['close'] < rally_drop['open']:
                body = rally_drop['open'] - rally_drop['close']
                avg_body = sum(abs(c['close'] - c['open']) for c in candles[max(0, i-5):i]) / 5 if i > 0 else body

                if body > min_expansion and body > (avg_body * 2): # Explosive move
                    zones.append({
                        'type': 'SUPPLY',
                        'price_high': base['high'],
                        'price_low': base['low'],
                        'timestamp': base['timestamp'],
                        'mitigated': False,
                        'strength': float(body)
                    })

        return zones
