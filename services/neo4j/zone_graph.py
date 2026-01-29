"""
Zone Graph Service.
Maps institutional liquidity zones and order blocks to the Neo4j knowledge graph.
"""
import logging
from typing import Dict, Any, List
from services.neo4j.edge_weight_updater import edge_weight_updater

logger = logging.getLogger(__name__)

class ZoneGraphService:
    """
    Service to persist and manage LIQUIDITY_ZONE nodes in Neo4j.
    """

    @staticmethod
    def create_zone(symbol: str, zone_data: Dict[str, Any]):
        """
        Create a LIQUIDITY_ZONE node in the graph.
        """
        query = """
        MERGE (z:LiquidityZone {
            symbol: $symbol,
            price_high: $price_high,
            price_low: $price_low,
            type: $type
        })
        SET z.strength = $strength,
            z.timestamp = $timestamp,
            z.mitigated = $mitigated,
            z.updated_at = datetime()
        WITH z
        MATCH (a:Asset {symbol: $symbol})
        MERGE (a)-[:HAS_ZONE]->(z)
        RETURN z
        """
        
        params = {
            'symbol': symbol,
            'price_high': float(zone_data['price_high']),
            'price_low': float(zone_data['price_low']),
            'type': zone_data['type'],
            'strength': float(zone_data.get('strength', 1.0)),
            'timestamp': str(zone_data['timestamp']),
            'mitigated': zone_data.get('mitigated', False)
        }

        try:
            with edge_weight_updater.driver.session() as session:
                session.run(query, params)
                logger.info(f"Mapped Zone to Neo4j: {symbol} {zone_data['type']} at {zone_data['price_low']}")
        except Exception as e:
            logger.error(f"Failed to map zone to Neo4j: {e}")

    @staticmethod
    def mitigate_zone(symbol: str, price: float):
        """
        Mark zones as mitigated (hit) if price penetrates them.
        """
        query = """
        MATCH (z:LiquidityZone {symbol: $symbol, mitigated: false})
        WHERE (z.type = 'SUPPLY' AND $price >= z.price_low)
           OR (z.type = 'DEMAND' AND $price <= z.price_high)
        SET z.mitigated = true,
            z.mitigated_at = datetime()
        RETURN count(z) as count
        """
        
        params = {'symbol': symbol, 'price': price}
        
        try:
            with edge_weight_updater.driver.session() as session:
                res = session.run(query, params)
                count = res.single()['count']
                if count > 0:
                    logger.info(f"Mitigated {count} zones for {symbol} at {price}")
        except Exception as e:
            logger.error(f"Failed to mitigate zones: {e}")
