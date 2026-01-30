
import os
import sys
import socket
import psycopg2
# Remove current directory from path to avoid shadowing 'neo4j' with './neo4j' or 'scripts/neo4j'
if "scripts" in os.getcwd():
    sys.path.remove(os.getcwd())
else:
    # If running from root, ensure scripts/ is not at the front
    for path in list(sys.path):
        if path.endswith("scripts"):
            sys.path.remove(path)

from neo4j import GraphDatabase
import redis
from dotenv import load_dotenv

load_dotenv()

def check_port(ip, port, timeout=3):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def test_postgres():
    print("Testing Postgres connection...")
    db_url = os.getenv("DATABASE_URL")
    try:
        conn = psycopg2.connect(db_url)
        conn.close()
        print("[OK] Postgres reached successfully.")
    except Exception as e:
        print(f"[ERROR] Postgres failure: {e}")

def test_neo4j():
    print("Testing Neo4j connection...")
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))
        driver.verify_connectivity()
        driver.close()
        print("[OK] Neo4j reached successfully.")
    except Exception as e:
        print(f"[ERROR] Neo4j failure: {e}")

def test_redis():
    print("Testing Redis connection...")
    host = os.getenv("REDIS_HOST") or "127.0.0.1"
    password = os.getenv("REDIS_PASSWORD")
    try:
        r = redis.Redis(host=host, port=6379, password=password, socket_timeout=3)
        r.ping()
        print("[OK] Redis reached successfully.")
    except Exception as e:
        print(f"[ERROR] Redis failure: {e}")

if __name__ == "__main__":
    lan_ip = os.getenv("LAN_BOX_IP")
    print(f"LAN_BOX_IP set to: {lan_ip}")
    
    # Quick port check
    services = {
        "Postgres": 5432,
        "Neo4j": 7687,
        "Redis": 6379,
        "Kafka": 9092
    }
    
    for name, port in services.items():
        if check_port(lan_ip, port):
            print(f"[OK] Port {port} ({name}) is open on {lan_ip}")
        else:
            print(f"[FAIL] Port {port} ({name}) is CLOSED on {lan_ip}")
    
    print("-" * 30)
    test_postgres()
    test_neo4j()
    test_redis()
