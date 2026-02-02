"""
Property Chain Graph Service for 1031 Exchanges
PURPOSE: Track real estate exchange chains in Neo4j to preserve tax basis history.
         When properties are exchanged, the original cost basis carries forward,
         creating a chain of deferred gains that must be tracked for eventual taxation.
"""

import logging
from neo4j import Driver
from typing import Dict, Any, List, Optional
from decimal import Decimal
from datetime import date
from utils.database_manager import db_manager

logger = logging.getLogger(__name__)


class PropertyChainGraph:
    """
    Tracks real estate exchange chains in Neo4j to preserve tax basis history.
    
    In a 1031 exchange chain:
    - Property A (basis $100k) -> Property B (basis $100k, deferred gain $400k)
    - Property B -> Property C (basis still $100k, accumulated deferred $500k)
    
    When Property C is finally sold (not exchanged), ALL deferred gains become taxable.
    """
    
    def __init__(self, driver: Driver = None):
        self.driver = driver or db_manager.neo4j_driver
        
    def link_exchange(
        self, 
        old_property_id: str, 
        new_property_id: str, 
        deferred_gain: float,
        basis_carried: float,
        old_address: str = None,
        new_address: str = None
    ) -> bool:
        """
        Creates an EXCHANGED_INTO relationship between properties.
        """
        query = """
        MERGE (p1:PROPERTY {id: $old_id})
        ON CREATE SET p1.address = $old_addr
        MERGE (p2:PROPERTY {id: $new_id})
        ON CREATE SET p2.address = $new_addr
        CREATE (p1)-[r:EXCHANGED_INTO {
            deferred_gain: $gain,
            basis_at_exchange: $basis,
            exchange_date: date()
        }]->(p2)
        SET p2.original_basis = $basis,
            p2.inherited_deferred_gain = COALESCE(p1.inherited_deferred_gain, 0) + $gain
        """
        try:
            with self.driver.session() as session:
                session.run(
                    query, 
                    old_id=old_property_id, 
                    new_id=new_property_id, 
                    gain=deferred_gain, 
                    basis=basis_carried,
                    old_addr=old_address or old_property_id,
                    new_addr=new_address or new_property_id
                )
            logger.info(f"Neo4j: Linked {old_property_id} -> {new_property_id} via 1031 Exchange")
            return True
        except Exception as e:
            logger.error(f"Failed to link property chain: {e}")
            return False

    def get_exchange_chain(self, property_id: str) -> List[Dict[str, Any]]:
        """
        Traverses the full chain of 1031 exchanges for a property.
        Returns list from original property to current, with all deferred gains.
        """
        query = """
        MATCH path = (origin:PROPERTY)-[:EXCHANGED_INTO*0..]->(current:PROPERTY {id: $prop_id})
        UNWIND nodes(path) as prop
        WITH prop, relationships(path) as rels
        RETURN prop.id as property_id, 
               prop.address as address, 
               prop.original_basis as basis,
               prop.inherited_deferred_gain as total_deferred
        ORDER BY size(rels)
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, prop_id=property_id)
                chain = []
                for record in result:
                    chain.append({
                        "property_id": record["property_id"],
                        "address": record["address"],
                        "basis": record["basis"],
                        "total_deferred_gain": record["total_deferred"] or 0
                    })
                return chain
        except Exception as e:
            logger.error(f"Failed to get exchange chain: {e}")
            return []

    def get_total_deferred_gain(self, property_id: str) -> Decimal:
        """
        Calculate total deferred gain accumulated across all exchanges in chain.
        This is the amount that becomes taxable upon final sale.
        """
        query = """
        MATCH (p:PROPERTY {id: $prop_id})
        RETURN COALESCE(p.inherited_deferred_gain, 0) as total_deferred
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, prop_id=property_id)
                record = result.single()
                if record:
                    return Decimal(str(record["total_deferred"]))
                return Decimal("0")
        except Exception as e:
            logger.error(f"Failed to get deferred gain: {e}")
            return Decimal("0")

    def get_original_basis(self, property_id: str) -> Decimal:
        """
        Get the original cost basis that has carried through all exchanges.
        """
        query = """
        MATCH path = (origin:PROPERTY)-[:EXCHANGED_INTO*0..]->(current:PROPERTY {id: $prop_id})
        WITH origin, size(relationships(path)) as depth
        ORDER BY depth DESC
        LIMIT 1
        RETURN origin.original_basis as basis
        """
        try:
            with self.driver.session() as session:
                result = session.run(query, prop_id=property_id)
                record = result.single()
                if record and record["basis"]:
                    return Decimal(str(record["basis"]))
                return Decimal("0")
        except Exception as e:
            logger.error(f"Failed to get original basis: {e}")
            return Decimal("0")


# Singleton
_instance: Optional[PropertyChainGraph] = None

def get_property_chain_graph() -> PropertyChainGraph:
    global _instance
    if _instance is None:
        _instance = PropertyChainGraph()
    return _instance

