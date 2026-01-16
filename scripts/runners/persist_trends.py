"""
==============================================================================
FILE: scripts/runners/persist_trends.py
ROLE: Data Persister
PURPOSE: Fetches Google Trends and saves them to Neo4j.
USAGE: python cli.py persist-trends --keywords "margin call,AMZN debt"
INPUT/OUTPUT:
    - Input: List of keywords
    - Output: Persistence status in Neo4j.
==============================================================================
"""

import logging
from typing import List
from services.data.google_trends import GoogleTrendsService
from utils.core.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase

logger = logging.getLogger(__name__)

def run_persist_trends(keywords: str = "margin call,AMZN debt", **kwargs):
    """
    Runner to fetch trends and persist to Neo4j.
    """
    kw_list = [k.strip() for k in keywords.split(",")]
    print(f"--- Persisting Trends for {kw_list} ---")
    
    service = GoogleTrendsService()
    results = service.get_trend_score(kw_list)
    
    if not results:
        print("No results to persist.")
        return False
        
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    try:
        with driver.session() as session:
            for kw, stats in results.items():
                query = """
                MERGE (s:Sentiment {name: $name})
                SET s.score = $score,
                    s.z_score = $z_score,
                    s.is_spike = $is_spike,
                    s.regime = $regime,
                    s.updated_at = timestamp()
                RETURN s
                """
                session.run(query, 
                    name=kw, 
                    score=stats['current_score'],
                    z_score=stats['z_score'],
                    is_spike=stats['is_spike'],
                    regime=stats['regime']
                )
                print(f"Persisted: {kw} (Z-Score: {stats['z_score']})")
                
        print("Successfully persisted all trends to Neo4j.")
        return True
    except Exception as e:
        logger.error(f"Failed to persist to Neo4j: {e}")
        print(f"Error: {e}")
        return False
    finally:
        driver.close()
