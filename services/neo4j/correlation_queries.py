"""
Neo4j Correlation Queries Service.
Provides Cypher queries for finding clusters and contagion risks.
"""
import os
from typing import List, Dict

class CorrelationQueries:
    @staticmethod
    def get_contagion_clusters(threshold: float = 0.8, timeframe: str = '1D') -> str:
        """
        Cypher: Find assets with high correlation hub.
        """
        return f"""
        MATCH (a1:Asset)-[r:CORRELATED_WITH]->(a2:Asset)
        WHERE r.coefficient > {threshold} AND r.timeframe = '{timeframe}'
        WITH a1, collect({{symbol: a2.symbol, correlation: r.coefficient}}) AS correlations
        WHERE size(correlations) >= 3
        RETURN a1.symbol AS hub, correlations
        ORDER BY size(correlations) DESC
        """

    @staticmethod
    def get_systemic_risk_paths(threshold: float = 0.9) -> str:
        """
        Cypher: Detect systemic risk where chains of assets move together.
        """
        return f"""
        MATCH path = (a1:Asset)-[:CORRELATED_WITH*1..3]->(a2:Asset)
        WHERE ALL(r IN relationships(path) WHERE r.coefficient > {threshold})
        RETURN path
        """

    @staticmethod
    def get_correlation_matrix() -> str:
        """
        Cypher: Fetch all correlations for the matrix view.
        """
        return """
        MATCH (a1:Asset)-[r:CORRELATED_WITH]->(a2:Asset)
        RETURN a1.symbol as source, a2.symbol as target, r.coefficient as coefficient, r.direction as direction
        """
