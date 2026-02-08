import logging
import asyncio
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from utils.database_manager import get_database_manager
from services.system.cache_service import get_cache_service

logger = logging.getLogger(__name__)

class HealthCheckService:
    """
    Service for monitoring the health of all backing services.
    Used for staging smoke tests and production monitoring.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HealthCheckService, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.db = get_database_manager()
        self.cache = get_cache_service()

    def check_postgres(self) -> Dict[str, Any]:
        """Checks connectivity to PostgreSQL."""
        from utils.core.config import POSTGRES_HOST
        try:
            start = time.time()
            with self.db.pg_cursor() as cur:
                cur.execute("SELECT 1")
            return {
                "status": "UP", 
                "latency_ms": round((time.time() - start) * 1000, 2),
                "target": POSTGRES_HOST
            }
        except Exception as e:
            logger.error(f"HealthCheck: Postgres DOWN on {POSTGRES_HOST}: {e}")
            return {"status": "DOWN", "error": str(e), "target": POSTGRES_HOST}

    def check_redis(self) -> Dict[str, Any]:
        """Checks connectivity to Redis."""
        from utils.core.config import REDIS_HOST
        try:
            start = time.time()
            self.cache.get("healthcheck_ping")
            return {
                "status": "UP", 
                "latency_ms": round((time.time() - start) * 1000, 2),
                "target": REDIS_HOST
            }
        except Exception as e:
            logger.error(f"HealthCheck: Redis DOWN on {REDIS_HOST}: {e}")
            return {"status": "DOWN", "error": str(e), "target": REDIS_HOST}

    def check_neo4j(self) -> Dict[str, Any]:
        """Checks connectivity to Neo4j."""
        from utils.core.config import NEO4J_URI
        try:
            from services.neo4j.neo4j_service import neo4j_service
            start = time.time()
            # Simple query to verify connection
            neo4j_service.execute_query("RETURN 1")
            return {
                "status": "UP", 
                "latency_ms": round((time.time() - start) * 1000, 2),
                "target": NEO4J_URI
            }
        except Exception as e:
            logger.error(f"HealthCheck: Neo4j DOWN: {e}")
            return {"status": "DOWN", "error": str(e), "target": NEO4J_URI}

    def check_kafka(self) -> Dict[str, Any]:
        """Checks connectivity to Kafka."""
        try:
            from kafka import KafkaConsumer
            from utils.core.config import KAFKA_BOOTSTRAP_SERVERS
            start = time.time()
            # Create a simple consumer to check connection
            consumer = KafkaConsumer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS, request_timeout_ms=2000)
            topics = consumer.topics() # fetches metadata
            consumer.close()
            return {
                "status": "UP", 
                "latency_ms": round((time.time() - start) * 1000, 2), 
                "topics_count": len(topics),
                "target": KAFKA_BOOTSTRAP_SERVERS
            }
        except Exception as e:
            logger.error(f"HealthCheck: Kafka DOWN: {e}")
            return {"status": "DOWN", "error": str(e), "target": os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')}

    def check_vendor_apis(self) -> Dict[str, Any]:
        """Checks reachability of critical vendor APIs (AlphaVantage, Polygon)."""
        import requests
        from utils.core.config import ALPHA_VANTAGE_API_KEY, POLYGON_API_KEY
        
        status = {}
        
        # AlphaVantage
        if ALPHA_VANTAGE_API_KEY:
            try:
                start = time.time()
                # Use a lightweight quote or just check connectivity to base URL
                requests.get("https://www.alphavantage.co", timeout=2) 
                status["alpha_vantage"] = {"status": "UP", "latency_ms": round((time.time() - start) * 1000, 2), "target": "https://www.alphavantage.co"}
            except Exception as e:
                status["alpha_vantage"] = {"status": "DOWN", "error": str(e), "target": "https://www.alphavantage.co"}
        else:
             status["alpha_vantage"] = {"status": "SKIPPED", "error": "No API Key", "target": "https://www.alphavantage.co"}

        # Polygon
        if POLYGON_API_KEY:
             try:
                start = time.time()
                requests.get("https://api.polygon.io", timeout=2)
                status["polygon"] = {"status": "UP", "latency_ms": round((time.time() - start) * 1000, 2), "target": "https://api.polygon.io"}
             except Exception as e:
                status["polygon"] = {"status": "DOWN", "error": str(e), "target": "https://api.polygon.io"}
        else:
             status["polygon"] = {"status": "SKIPPED", "error": "No API Key", "target": "https://api.polygon.io"}
             
        return status

    def check_infra_ports(self) -> Dict[str, Any]:
        """Verify that infrastructure ports are open on the LAN node."""
        import socket
        from utils.core.config import get_env
        host = get_env("LAN_BOX_IP", "localhost")
        
        # Maps port to name
        # Removed Zookeeper (2181) as it's not exposed externally
        ports = {
            5432: "Postgres",
            6379: "Redis",
            7687: "Neo4j Bolt",
            9092: "Kafka"
        }
        
        status = {"total": len(ports), "open": 0, "closed": [], "host": host}
        
        for port, name in ports.items():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    if s.connect_ex((host, port)) == 0:
                        status["open"] += 1
                    else:
                        status["closed"].append(f"{name} ({port})")
            except Exception:
                status["closed"].append(f"{name} ({port})")
        
        status["status"] = "UP" if status["open"] == status["total"] else "DEGRADED"
        return status

    def get_uptime_history(self, service_id: str) -> List[Dict[str, Any]]:
        """Return 30-day uptime history (mocked)."""
        import random
        from datetime import datetime, timedelta
        
        history = []
        for i in range(30):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            history.append({
                "date": date,
                "uptime": random.uniform(98.0, 100.0) if random.random() > 0.05 else random.uniform(80.0, 95.0)
            })
        return sorted(history, key=lambda x: x['date'])

    def get_dependency_map(self) -> List[Dict[str, Any]]:
        """Return a graph of service dependencies."""
        return [
            {"source": "API Gateway", "target": "Auth Service", "type": "REST"},
            {"source": "API Gateway", "target": "Market Data Service", "type": "REST"},
            {"source": "Auth Service", "target": "PostgreSQL", "type": "SQL"},
            {"source": "Market Data Service", "target": "Kafka", "type": "PubSub"},
            {"source": "Searcher Agent", "target": "Kafka", "type": "PubSub"},
            {"source": "Searcher Agent", "target": "Neo4j", "type": "Graph"},
            {"source": "Protector Agent", "target": "Event Bus", "type": "Internal"}
        ]

    def trigger_health_check(self, service_id: str) -> Dict[str, Any]:
        """Manually trigger a health check for a specific service."""
        logger.info(f"Manual health check triggered for {service_id}")
        # Routing to specific check based on ID
        if service_id == "postgres": return self.check_postgres()
        if service_id == "redis": return self.check_redis()
        if service_id == "neo4j": return self.check_neo4j()
        if service_id == "kafka": return self.check_kafka()
        return {"status": "UNKNOWN", "id": service_id}

    def get_full_status(self) -> Dict[str, Any]:
        """Aggregates health status of all systems with added metadata."""
        status = {
            "services": [
                {"id": "postgres", "name": "PostgreSQL", **self.check_postgres()},
                {"id": "redis", "name": "Redis", **self.check_redis()},
                {"id": "neo4j", "name": "Neo4j Graph", **self.check_neo4j()},
                {"id": "kafka", "name": "Kafka Broker", **self.check_kafka()},
                {"id": "infra", "name": "Infrastructure Ports", **self.check_infra_ports()}
            ],
            "vendor_apis": self.check_vendor_apis(),
            "timestamp": time.time()
        }
        
        # Overall status logic
        all_up = all(s["status"] == "UP" for s in status["services"])
        status["overall"] = "UP" if all_up else "DEGRADED"
        
        return status

def get_health_check_service() -> HealthCheckService:
    return HealthCheckService()
