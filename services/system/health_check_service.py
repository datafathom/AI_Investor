
import logging
import time
from typing import Dict, Any
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

    def get_full_status(self) -> Dict[str, Any]:
        """Aggregates health status of all systems."""
        status = {
            "infra_ports": self.check_infra_ports(),
            "postgres": self.check_postgres(),
            "redis": self.check_redis(),
            "neo4j": self.check_neo4j(),
            "kafka": self.check_kafka(),
            "vendor_apis": self.check_vendor_apis(),
            "timestamp": time.time()
        }
        
        # Overall status
        critical_components = [
            status["infra_ports"],
            status["postgres"], 
            status["redis"], 
            status["neo4j"], 
            status["kafka"]
        ]
        # Flatten vendor statuses
        vendor_vals = status["vendor_apis"].values()
        
        all_critical_up = all(v["status"] == "UP" for v in critical_components)
        all_vendors_ok = all(v["status"] in ["UP", "SKIPPED"] for v in vendor_vals)
        
        status["overall"] = "UP" if (all_critical_up and all_vendors_ok) else "DEGRADED"
        
        return status

def get_health_check_service() -> HealthCheckService:
    return HealthCheckService()
