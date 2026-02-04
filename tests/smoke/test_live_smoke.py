
import pytest
import requests
from services.system.health_check_service import HealthCheckService

# These tests are intended to be run against a LIVE environment.
# They verify that the infrastructure is actually up and running.

@pytest.fixture
def health_check_service():
    # We explicitly do NOT mock here because we want to test live connectivity
    return HealthCheckService()

def test_live_postgres_connectivity(health_check_service):
    """Verify actual connection to Postgres."""
    result = health_check_service.check_postgres()
    print(f"  🎯 Target: {result['target']}")
    assert result['status'] == 'UP', f"Postgres is DOWN: {result.get('error')}"

def test_live_redis_connectivity(health_check_service):
    """Verify actual connection to Redis."""
    result = health_check_service.check_redis()
    print(f"  🎯 Target: {result['target']}")
    assert result['status'] == 'UP', f"Redis is DOWN: {result.get('error')}"

def test_live_neo4j_connectivity(health_check_service):
    """Verify actual connection to Neo4j."""
    result = health_check_service.check_neo4j()
    print(f"  🎯 Target: {result['target']}")
    assert result['status'] == 'UP', f"Neo4j is DOWN: {result.get('error')}"

def test_live_kafka_connectivity(health_check_service):
    """Verify actual connection to Kafka."""
    result = health_check_service.check_kafka()
    print(f"  🎯 Target: {result['target']}")
    assert result['status'] == 'UP', f"Kafka is DOWN: {result.get('error')}"

def test_live_infra_ports(health_check_service):
    """Verify all critical infrastructure ports are open on remote node."""
    result = health_check_service.check_infra_ports()
    print(f"  🎯 Host: {result.get('host')}")
    assert result['status'] == 'UP', f"Infra ports closed on {result.get('host')}: {result.get('closed')}"

def test_live_vendor_apis(health_check_service):
    """Verify connectivity to vendor APIs (if keys present)."""
    result = health_check_service.check_vendor_apis()
    for vendor, status in result.items():
        print(f"  🎯 {vendor} Target: {status['target']}")
        assert status['status'] in ['UP', 'SKIPPED'], f"{vendor} check failed: {status.get('error')}"

def test_backend_http_health():
    """Verify Backend is reachable via HTTP."""
    # Try both known health endpoints
    endpoints = [
        "http://127.0.0.1:5050/health",
        "http://127.0.0.1:5050/api/v1/system/health"
    ]
    
    success = False
    last_error = ""
    
    for url in endpoints:
        print(f"  🎯 Testing: {url}")
        try:
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                success = True
                break
            last_error = f"Status {resp.status_code} for {url}"
        except requests.exceptions.ConnectionError as e:
            last_error = f"ConnectionError for {url}: {e}"
            
    assert success, f"Backend is NOT reachable on standard health endpoints. Last error: {last_error}"

def test_frontend_http_health():
    """Verify Frontend is reachable via HTTP."""
    # Vite often uses 127.0.0.1:5173
    url = "http://127.0.0.1:5173"
    print(f"  🎯 Testing: {url}")
    try:
        resp = requests.get(url, timeout=3)
        assert resp.status_code == 200, f"Frontend returned status: {resp.status_code}"
    except requests.exceptions.ConnectionError:
        # Try localhost as fallback
        print("    ⚠️  127.0.0.1 failed, trying localhost...")
        try:
            resp = requests.get("http://localhost:5173", timeout=3)
            assert resp.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.fail("Frontend (127.0.0.1:5173) is NOT reachable. Is it running?")
