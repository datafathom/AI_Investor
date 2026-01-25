"""
Database Query Optimizer
Optimizes database queries for better performance
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class QueryOptimizer:
    """Optimizes database queries."""
    
    def __init__(self):
        self.query_cache = {}
        self.slow_query_threshold = 1.0  # seconds
    
    def optimize_select(self, query: str, params: Optional[Dict] = None) -> str:
        """Optimize SELECT query."""
        query_lower = query.lower().strip()
        
        # Add LIMIT if missing and not aggregating
        if 'select' in query_lower and 'limit' not in query_lower:
            if 'group by' not in query_lower and 'count(' not in query_lower:
                query += ' LIMIT 1000'
        
        # Ensure indexes are used
        # This is a simplified version - in production, use EXPLAIN ANALYZE
        return query
    
    def should_use_cache(self, query: str, params: Optional[Dict] = None) -> bool:
        """Determine if query result should be cached."""
        query_lower = query.lower()
        
        # Cache SELECT queries
        if query_lower.startswith('select'):
            # Don't cache queries with NOW() or random functions
            if 'now()' in query_lower or 'random()' in query_lower:
                return False
            return True
        
        return False
    
    def get_cache_key(self, query: str, params: Optional[Dict] = None) -> str:
        """Generate cache key for query."""
        import hashlib
        key_data = f"{query}:{params or {}}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def log_slow_query(self, query: str, duration: float, params: Optional[Dict] = None):
        """Log slow queries for optimization."""
        if duration > self.slow_query_threshold:
            logger.warning(
                f"Slow query detected ({duration:.2f}s): {query[:100]}... "
                f"Params: {params}"
            )


class ConnectionPool:
    """Database connection pool manager."""
    
    def __init__(self, max_connections: int = 20):
        self.max_connections = max_connections
        self.active_connections = 0
        self.pool = []
    
    def get_connection(self):
        """Get connection from pool."""
        if self.pool:
            return self.pool.pop()
        elif self.active_connections < self.max_connections:
            self.active_connections += 1
            # Create new connection (implementation depends on DB driver)
            return None  # Placeholder
        else:
            # Wait for available connection
            return None
    
    def return_connection(self, conn):
        """Return connection to pool."""
        if conn:
            self.pool.append(conn)


def get_query_optimizer() -> QueryOptimizer:
    """Get query optimizer instance."""
    return QueryOptimizer()
